#!/usr/bin/env python3
"""Register a supplied, visually approved v2 atlas as a new immutable version."""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile

from gallery import ROOT, ID, VERSION, STATES, COUNTS, GalleryError, require, image_rgba, sha256, validate_release, catalog_entries, deterministic_zip


def write_json(path, value):
    temporary = path.with_name(path.name + ".tmp")
    try:
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def import_atlas(root, pid, name, version, atlas_path, description="", set_latest=False):
    root = Path(root).resolve()
    require(ID.fullmatch(pid) is not None, "Use lowercase letters, numbers and hyphens for id")
    require(VERSION.fullmatch(version) is not None, "Use a three-part version such as 1.0.0")
    require(bool(name.strip()), "Display name must not be empty")
    catalog_entries(root)
    catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    existing = next((x for x in catalog["pets"] if x["id"] == pid), None)
    dest = root / "pets" / pid / "versions" / version
    require(not dest.exists(), f"Refusing to overwrite existing version: {dest}")
    require(existing is None or version not in existing["versions"], "Version already registered")
    atlas_path = Path(atlas_path)
    image = image_rgba(atlas_path, (1536, 2288))
    require(0 < atlas_path.stat().st_size <= 20 * 1024 * 1024, "Atlas exceeds 20 MiB")
    for row, count in enumerate(COUNTS):
        for col in range(8):
            bounds = image.crop((col*192, row*208, (col+1)*192, (row+1)*208)).getchannel("A").getbbox()
            require((bounds is not None) == (col < count), f"Wrong cell occupancy at {row},{col}")
            if bounds:
                require(bounds[0] > 0 and bounds[1] > 0 and bounds[2] < 192 and bounds[3] < 208,
                        f"Artwork touches cell edge at {row},{col}")
    with tempfile.TemporaryDirectory(prefix="gallery-import-") as temp:
        staged = Path(temp)
        shutil.copyfile(atlas_path, staged / "spritesheet.png")
        rows = []
        directions = []
        for row, (state, count) in enumerate(zip(STATES, COUNTS, strict=True)):
            folder = staged / "frames" / state
            folder.mkdir(parents=True)
            frames = []
            for col in range(count):
                frame = folder / f"{col:02d}.png"
                image.crop((col*192, row*208, (col+1)*192, (row+1)*208)).save(frame)
                frames.append({"path": frame.relative_to(staged).as_posix(), "sha256": sha256(frame)})
            entry = {"row": row, "state": state, "frame_count": count, "visual": "待补充", "frames": frames}
            if row >= 9:
                entry["directions_degrees"] = [(row-9)*180 + col*22.5 for col in range(8)]
                directions.extend({"degrees": d, "rowIndex": row, "columnIndex": col}
                                  for col, d in enumerate(entry["directions_degrees"]))
            rows.append(entry)
        archive = staged / "frames.zip"
        deterministic_zip(archive, {p.relative_to(staged).as_posix(): p.read_bytes()
                                   for p in (staged / "frames").rglob("*.png")})
        pet = {"id": pid, "displayName": name, "description": description,
               "spriteVersionNumber": 2, "spritesheetPath": "spritesheet.png"}
        write_json(staged / "pet.json", pet)
        write_json(staged / "layout.json", {
            "spritesheetPath": "spritesheet.png",
            "spritesheetLayout": {"columns": 8, "rows": 11, "cellWidth": 192, "cellHeight": 208,
                                  "lookDirectionCount": 16, "neutralLookFrame": {"rowIndex": 0, "columnIndex": 0}},
            "lookDirections": directions})
        manifest = {
            "schema_version": 1, "id": pid, "display_name": name, "version": version,
            "release_date": date.today().isoformat(), "description": description, "sprite_version": 2,
            "atlas": {"file": "spritesheet.png", "sha256": sha256(staged / "spritesheet.png"),
                      "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest(),
                      "width": 1536, "height": 2288, "cell_width": 192, "cell_height": 208,
                      "columns": 8, "rows": 11, "required_frames": 73, "unused_cells": 15},
            "rows": rows, "sources": [], "overrides": [],
            "frames_archive": {"path": "frames.zip", "sha256": sha256(archive), "file_count": 73},
            "generation": {"method": "Supplied atlas imported; provenance must be completed by maintainer."},
            "qa_status": "needs-visual-review", "asset_license_status": "to-be-recorded",
            "visual_warnings": ["Imported layout is structurally valid; complete visual review and provenance before release."]
        }
        write_json(staged / "manifest.json", manifest)
        validate_release(staged / "manifest.json", pid, version)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(staged, dest)
    relative = (dest / "manifest.json").relative_to(root).as_posix()
    if existing is None:
        catalog["pets"].append({"id": pid, "display_name": name, "latest": version, "versions": {version: relative}})
    else:
        existing["versions"][version] = relative
        if set_latest:
            existing["latest"] = version
    try:
        write_json(root / "catalog.json", catalog)
    except Exception:
        shutil.rmtree(dest)
        raise
    return dest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--atlas", type=Path, required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--set-latest", action="store_true")
    args = parser.parse_args(argv)
    try:
        dest = import_atlas(ROOT, args.id, args.name, args.version, args.atlas, args.description, args.set_latest)
    except (GalleryError, OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Imported: {dest}\nNext: complete provenance, visual review, previews and checksums.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
