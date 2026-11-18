# Updating and adding characters

[简体中文](CONTRIBUTING.md) · **English**

## Stable IDs and independent versions

- Give each character a stable ID such as `deepseek-chan`. Keep account-specific Pet IDs out of the repository.
- Create a new version directory for artwork, frame, or config changes, and record the changes. Published directories are frozen.
- Place a new character in `pets/<id>/versions/<version>/` and add it to `catalog.json`.
- The `latest` field is per character. Character tags use `<id>-v<version>`. Gallery Releases use `v<version>`. For example, `v1.0.1` and `deepseek-chan-v1.0.1` point to the same commit.
- Use lowercase English letters, digits, and hyphens in IDs. Use three-part versions such as `1.1.0`.
- Keep the Chinese and English docs in sync when editing them. Use a patch for small artwork fixes, a minor version for new animations or a substantial revision, and a major version for incompatible format changes. [Publishing guide](docs/PUBLISHING.en.md)

## Import an approved atlas

The tool seeds a version from a completed v2 RGBA PNG with all required frames.

~~~bash
python tools/add_pet.py --id your-character --name "Character name" --version 1.0.0 --atlas /path/to/approved-spritesheet.png --description "Character description"
~~~

To add a version under the same ID, run the command with a higher version. The tool rejects an existing version. Use `--set-latest` to update an existing character's `latest` field. A new character's first version becomes its latest automatically.

The tool creates `frames.zip` with all 73 final frames, `pet.json`, `layout.json`, and `manifest.json`, then updates the catalog and flags visual review as pending. Add sources, previews, credits, and semantic checks. After visual review, set `qa_status` to `approved` or `approved-with-documented-warnings` in `manifest.json`. Packaging requires completed visual review.

## Checks before submitting

~~~bash
python tools/gallery.py checksums
python tools/gallery.py verify-files
python tools/gallery.py validate --all
python tools/gallery.py build --all
python -m unittest discover -s tests -v
~~~

Visually inspect all states and 16 directions for proportions, foot baseline, direction, occlusion, transparent edges, props, and hand consistency. Record the sources, references, and generation tools for new art. Keep access tokens, signed download URLs, account-specific IDs, private Page references, and raw chat logs out of the repository.

## Animation transitions

Read the transition guide before editing poses. Check each loop, the automatic return to idle after three loops, mid-animation interruptions, hover, drag reversal and release, and gaze overrides. Frame 0 serves both as the entry frame and as the reduced-motion still, so inspect it independently. [State transitions](docs/TRANSITIONS.en.md)

~~~bash
python tools/preview_transitions.py --atlas pets/deepseek-chan/versions/1.0.1/spritesheet.png --output dist/transitions
~~~

For a before-and-after comparison, add `--compare /path/to/before.png`. Both versions use the same state events and inspected frame timings. Silhouette metrics can locate jumps. Review the visuals yourself and preserve the hard cuts the client actually displays.
