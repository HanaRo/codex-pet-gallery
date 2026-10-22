import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import gallery
from add_pet import import_atlas

RELEASE = ROOT / "pets/deepseek-chan/versions/1.0.0"


class GalleryTests(unittest.TestCase):
    def test_rebuild_reproduces_entire_decoded_atlas(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "rebuilt.png"
            result = gallery.build_release(RELEASE / "manifest.json", output)
            self.assertTrue(result["exact_rgba_match"])
            self.assertEqual(Image.open(output).tobytes(), Image.open(RELEASE / "spritesheet.png").tobytes())

    def test_relative_path_cannot_escape_release(self):
        with self.assertRaises(gallery.GalleryError):
            gallery.safe_path(RELEASE, "../../../../outside.png")
        with self.assertRaises(gallery.GalleryError):
            gallery.safe_path(RELEASE, "/tmp/outside.png")

    def test_changed_frame_is_rejected_even_with_updated_file_hash(self):
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "release"
            shutil.copytree(RELEASE, copy)
            path = copy / "frames/idle/00.png"
            m = gallery.read_json(copy / "manifest.json")
            changed = gallery.frame_image(copy, m, m["rows"][0]["frames"][0])
            path.parent.mkdir(parents=True, exist_ok=True)
            changed.putpixel((96, 104), (255, 0, 0, 255))
            changed.save(path)
            m = gallery.read_json(copy / "manifest.json")
            m["rows"][0]["frames"][0]["sha256"] = gallery.sha256(path)
            (copy / "manifest.json").write_text(json.dumps(m))
            with self.assertRaisesRegex(gallery.GalleryError, "checksum mismatch|differs from frozen atlas"):
                gallery.validate_release(copy / "manifest.json")

    def test_archive_only_checkout_rebuilds_without_expanded_frames(self):
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "release"
            shutil.copytree(RELEASE, copy, ignore=shutil.ignore_patterns("frames"))
            result = gallery.build_release(copy / "manifest.json", Path(temp) / "out.png")
            self.assertTrue(result["exact_rgba_match"])

    def test_package_is_reproducible_and_contains_client_files(self):
        with tempfile.TemporaryDirectory() as temp:
            a, b = Path(temp) / "a.zip", Path(temp) / "b.zip"
            gallery.package_release(RELEASE / "manifest.json", a)
            gallery.package_release(RELEASE / "manifest.json", b)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            with gallery.zipfile.ZipFile(a) as z:
                self.assertTrue({"pet.json", "spritesheet.png", "SHA256SUMS.txt"} <= set(z.namelist()))
                pet = json.loads(z.read("pet.json"))
                self.assertEqual(pet["spritesheetPath"], "spritesheet.png")
                self.assertEqual(hashlib.sha256(z.read("spritesheet.png")).hexdigest(),
                                 gallery.sha256(RELEASE / "spritesheet.png"))

    def test_new_pet_and_new_version_are_registered_without_overwriting(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            # Keep this import fixture independent of how many real versions are published.
            catalog = {"schema_version": 1, "project": "test-gallery", "pets": [{
                "id": "deepseek-chan", "display_name": "DeepSeek 娘", "latest": "1.0.0",
                "versions": {"1.0.0": "pets/deepseek-chan/versions/1.0.0/manifest.json"}}]}
            (root / "catalog.json").write_text(json.dumps(catalog))
            dest = root / "pets/deepseek-chan/versions/1.0.0"
            shutil.copytree(RELEASE, dest)
            first = import_atlas(root, "new-pet", "Test", "1.0.0", RELEASE / "spritesheet.png")
            gallery.validate_release(first / "manifest.json", "new-pet", "1.0.0")
            with self.assertRaisesRegex(gallery.GalleryError, "visual review"):
                gallery.package_release(first / "manifest.json", root / "unreviewed.zip")
            with self.assertRaisesRegex(gallery.GalleryError, "overwrite"):
                import_atlas(root, "new-pet", "Test", "1.0.0", RELEASE / "spritesheet.png")
            import_atlas(root, "new-pet", "Test", "1.1.0", RELEASE / "spritesheet.png", set_latest=True)
            pet = next(x for x in gallery.read_json(root / "catalog.json")["pets"] if x["id"] == "new-pet")
            self.assertEqual(pet["latest"], "1.1.0")
            self.assertEqual(len(pet["versions"]), 2)
            self.assertEqual(len(gallery.catalog_entries(root)), 3)

    def test_preview_export_preserves_audited_clock_and_source(self):
        atlas = RELEASE / "spritesheet.png"
        original = gallery.sha256(atlas)
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run([sys.executable, str(ROOT / "tools/render_previews.py"),
                            "--atlas", str(atlas), "--output", temp],
                           check=True, capture_output=True, text=True)
            for state, expected in [("idle", [1680, 660, 660, 840, 840, 1920]),
                                    ("running", [120]*5 + [220])]:
                with Image.open(Path(temp) / "states" / f"{state}.gif") as gif:
                    actual = []
                    for index in range(gif.n_frames):
                        gif.seek(index)
                        actual.append(gif.info["duration"])
                self.assertEqual(actual, expected)
        self.assertEqual(gallery.sha256(atlas), original)


if __name__ == "__main__":
    unittest.main()
