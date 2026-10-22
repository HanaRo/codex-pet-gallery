#!/usr/bin/env python3
"""Verify, rebuild and package frozen Pet releases without network access."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]
STATES = ["idle", "running-right", "running-left", "waving", "jumping",
          "failed", "waiting", "running", "review", "look-row-9", "look-row-10"]
ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION = re.compile(r"^\d+\.\d+\.\d+(?:-[a-z0-9.-]+)?$")
SHA = re.compile(r"^[0-9a-f]{64}$")


class GalleryError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise GalleryError(message)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def safe_path(base, relative):
    require(isinstance(relative, str) and relative, "Missing relative path")
    rel = Path(relative)
    require(not rel.is_absolute(), f"Absolute path forbidden: {relative}")
    target = (Path(base) / rel).resolve()
    require(target.is_relative_to(Path(base).resolve()), f"Path escapes release: {relative}")
    return target


def catalog_entries(root=ROOT):
    catalog = read_json(Path(root) / "catalog.json")
    require(catalog.get("schema_version") == 1, "Unsupported catalog schema")
    ids = set()
    result = []
    for pet in catalog["pets"]:
        pid = pet["id"]
        require(ID.fullmatch(pid) is not None and pid not in ids, f"Invalid or duplicate id: {pid}")
        ids.add(pid)
        require(pet["latest"] in pet["versions"], f"Missing latest version: {pid}")
        for version, relative in pet["versions"].items():
            require(VERSION.fullmatch(version) is not None, f"Invalid version: {version}")
            path = safe_path(root, relative)
            require(path == Path(root).resolve() / "pets" / pid / "versions" / version / "manifest.json",
                    f"Unexpected version path: {relative}")
            result.append((pid, version, path))
    require(result, "Empty catalog")
    return result


def selected(args):
    entries = catalog_entries()
    if args.all:
        require(args.pet is None and args.version is None, "--all cannot be combined with --pet/--version")
        return entries
    require(args.pet is not None, "Choose --pet ID or --all")
    catalog = read_json(ROOT / "catalog.json")
    pet = next((p for p in catalog["pets"] if p["id"] == args.pet), None)
    require(pet is not None, f"Unknown pet: {args.pet}")
    version = args.version or pet["latest"]
    chosen = [x for x in entries if x[:2] == (args.pet, version)]
    require(chosen, f"Unknown version: {args.pet} {version}")
    return chosen


def image_rgba(path, size=None):
    with Image.open(path) as im:
        require(im.format == "PNG" and im.mode == "RGBA", f"Expected RGBA PNG: {path}")
        require(size is None or im.size == size, f"Wrong dimensions: {path}: {im.size}")
        return im.copy()


def check_digest(base, entry):
    expected = entry.get("sha256", "")
    require(SHA.fullmatch(expected) is not None, f"Invalid SHA-256: {entry.get('path')}")
    path = safe_path(base, entry["path"])
    require(path.is_file(), f"Missing file: {path}")
    require(sha256(path) == expected, f"File checksum mismatch: {path}")
    return path


def frame_image(base, manifest, entry):
    path = safe_path(base, entry["path"])
    if path.is_file():
        data = path.read_bytes()
    else:
        archive = manifest.get("frames_archive")
        require(archive is not None, f"Missing frame: {entry['path']}")
        archive_path = safe_path(base, archive["path"])
        with zipfile.ZipFile(archive_path) as z:
            data = z.read(entry["path"])
    require(hashlib.sha256(data).hexdigest() == entry["sha256"],
            f"Frame checksum mismatch: {entry['path']}")
    return image_rgba(io.BytesIO(data), (192, 208))


def validate_release(manifest_path, expected_id=None, expected_version=None):
    path = Path(manifest_path)
    base = path.parent
    m = read_json(path)
    require(m.get("schema_version") == 1, "Unsupported manifest schema")
    require(ID.fullmatch(m["id"]) is not None, "Invalid pet id")
    require(VERSION.fullmatch(m["version"]) is not None, "Invalid release version")
    require(expected_id is None or m["id"] == expected_id, "Catalog/manifest id mismatch")
    require(expected_version is None or m["version"] == expected_version, "Catalog/manifest version mismatch")
    require(m["sprite_version"] == 2, "Only v2 is supported")
    atlas_meta = m["atlas"]
    expected_geometry = dict(width=1536, height=2288, cell_width=192, cell_height=208,
                             columns=8, rows=11, required_frames=73, unused_cells=15)
    require(all(atlas_meta.get(k) == v for k, v in expected_geometry.items()), "Atlas metadata mismatch")
    atlas_path = check_digest(base, {"path": atlas_meta["file"], "sha256": atlas_meta["sha256"]})
    require(0 < atlas_path.stat().st_size <= 20 * 1024 * 1024, "Atlas exceeds 20 MiB")
    atlas = image_rgba(atlas_path, (1536, 2288))
    require(hashlib.sha256(atlas.tobytes()).hexdigest() == atlas_meta["rgba_sha256"],
            "Atlas decoded RGBA checksum mismatch")
    require(len(m["rows"]) == 11, "Expected eleven rows")
    if m.get("frames_archive"):
        archive_path = check_digest(base, m["frames_archive"])
        expected_members = {f["path"] for row in m["rows"] for f in row["frames"]}
        with zipfile.ZipFile(archive_path) as z:
            require(set(z.namelist()) == expected_members and len(z.namelist()) == 73,
                    "Frame archive must contain exactly the 73 declared frames")
            for row in m["rows"]:
                for entry in row["frames"]:
                    require(hashlib.sha256(z.read(entry["path"])).hexdigest() == entry["sha256"],
                            f"Archived frame checksum mismatch: {entry['path']}")
    frame_paths = set()
    for row, count, state, item in zip(range(11), COUNTS, STATES, m["rows"], strict=True):
        require((item["row"], item["state"], item["frame_count"]) == (row, state, count),
                f"Wrong layout for row {row}")
        require(len(item["frames"]) == count, f"Wrong frame count for {state}")
        if row >= 9:
            require(item.get("directions_degrees") == [(row-9)*180 + c*22.5 for c in range(8)],
                    f"Wrong look-direction order for row {row}")
        for col in range(8):
            cell = atlas.crop((col*192, row*208, (col+1)*192, (row+1)*208))
            bounds = cell.getchannel("A").getbbox()
            if col >= count:
                require(bounds is None, f"Unused cell is not transparent: row {row}, col {col}")
                continue
            require(bounds is not None, f"Empty required cell: row {row}, col {col}")
            require(bounds[0] > 0 and bounds[1] > 0 and bounds[2] < 192 and bounds[3] < 208,
                    f"Artwork touches cell boundary: row {row}, col {col}")
            entry = item["frames"][col]
            fpath = safe_path(base, entry["path"])
            require(fpath not in frame_paths, f"Duplicate frame path: {fpath}")
            frame_paths.add(fpath)
            frame = frame_image(base, m, entry)
            require(frame.tobytes() == cell.tobytes(), f"Frame differs from frozen atlas: {fpath}")
    for entry in m["sources"]:
        check_digest(base, entry)
    pet = read_json(base / "pet.json")
    require(pet["id"] == m["id"] and pet["spriteVersionNumber"] == 2 and
            pet["spritesheetPath"] == atlas_meta["file"], "Client pet.json mismatch")
    layout = read_json(base / "layout.json")
    require(layout["spritesheetPath"] == atlas_meta["file"], "layout.json points to wrong atlas")
    require(len(layout["lookDirections"]) == 16, "layout.json has wrong direction count")
    return m, atlas


def build_release(manifest_path, destination):
    m, original = validate_release(manifest_path)
    base = Path(manifest_path).parent
    atlas = Image.new("RGBA", (1536, 2288))
    for row in m["rows"]:
        for col, entry in enumerate(row["frames"]):
            frame = frame_image(base, m, entry)
            # Paste exact RGBA values; compositing could alter semitransparent edge pixels.
            atlas.paste(frame, (col*192, row["row"]*208))
    require(atlas.tobytes() == original.tobytes(), "Rebuild does not match frozen atlas")
    output = Path(destination)
    output.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(output, format="PNG", compress_level=9, optimize=True)
    require(image_rgba(output).tobytes() == original.tobytes(), "PNG encoding changed RGBA pixels")
    return {"output": str(output), "rgba_sha256": m["atlas"]["rgba_sha256"],
            "encoded_sha256": sha256(output), "exact_rgba_match": True,
            "exact_encoded_match": sha256(output) == m["atlas"]["sha256"]}


def deterministic_zip(destination, files):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    return sha256(destination)


def package_release(manifest_path, destination):
    m, _ = validate_release(manifest_path)
    require(m.get("qa_status") in {"approved", "approved-with-documented-warnings"},
            "Complete and record visual review before packaging a release")
    base = Path(manifest_path).parent
    files = {name: (base / name).read_bytes() for name in ["pet.json", "spritesheet.png", "layout.json"]}
    metadata = {k: m[k] for k in ["id", "version", "display_name", "description", "sprite_version", "atlas", "overrides"]}
    metadata["metadata_note"] = "Release metadata only; not a client installation config."
    files["release.json"] = (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n").encode()
    files["INSTALL.md"] = (ROOT / "docs/INSTALL.md").read_bytes()
    files["ASSET_LICENSE.md"] = (ROOT / "ASSET_LICENSE.md").read_bytes()
    files["CREDITS.md"] = (ROOT / "CREDITS.md").read_bytes()
    files["SHA256SUMS.txt"] = "".join(
        f"{hashlib.sha256(data).hexdigest()}  {name}\n" for name, data in sorted(files.items())
    ).encode()
    value = deterministic_zip(destination, files)
    return {"output": str(destination), "sha256": value, "version": m["version"]}


def project_files():
    for p in sorted(ROOT.rglob("*")):
        relative = p.relative_to(ROOT)
        # Expanded frames are an optional working cache; the checked archive is authoritative.
        if "pets" in relative.parts and "frames" in relative.parts:
            continue
        if (not p.is_file() or relative.name == ".DS_Store" or relative == Path("SHA256SUMS.txt")
                or any(x in relative.parts for x in [".git", ".venv", "__pycache__", "dist", "build", ".pytest_cache"])):
            continue
        yield relative.as_posix(), p


def checksums(write=False):
    path = ROOT / "SHA256SUMS.txt"
    actual = {name: sha256(p) for name, p in project_files()}
    if write:
        path.write_text("".join(f"{value}  {name}\n" for name, value in actual.items()), encoding="utf-8")
        return {"files": len(actual), "written": str(path)}
    expected = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        require(SHA.fullmatch(digest) is not None, "Malformed SHA256SUMS.txt")
        safe_path(ROOT, name)
        require(name not in expected, f"Duplicate checksum entry: {name}")
        expected[name] = digest
    require(expected == actual, "Project file inventory/checksums changed; inspect changes, then run checksums")
    return {"files": len(actual), "ok": True}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    sub.add_parser("checksums", help="Refresh root checksum inventory after an intentional edit")
    sub.add_parser("verify-files", help="Check every tracked project file against SHA256SUMS.txt")
    for command in ["validate", "build", "package"]:
        child = sub.add_parser(command)
        child.add_argument("--pet")
        child.add_argument("--version")
        child.add_argument("--all", action="store_true")
        if command != "validate":
            child.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            for pid, version, path in catalog_entries():
                print(f"{pid}\t{version}\t{path.relative_to(ROOT)}")
            return 0
        if args.command in ["checksums", "verify-files"]:
            print(json.dumps(checksums(write=args.command == "checksums"), ensure_ascii=False, indent=2))
            return 0
        results = []
        for pid, version, path in selected(args):
            if args.command == "validate":
                m, _ = validate_release(path, pid, version)
                result = {"id": pid, "version": version, "ok": True,
                          "rgba_sha256": m["atlas"]["rgba_sha256"], "required_frames": 73}
            elif args.command == "build":
                validate_release(path, pid, version)
                result = build_release(path, args.output / pid / version / "spritesheet.png")
            else:
                validate_release(path, pid, version)
                result = package_release(path, args.output / f"{pid}-{version}-pet.zip")
            results.append(result)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0
    except (GalleryError, KeyError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
