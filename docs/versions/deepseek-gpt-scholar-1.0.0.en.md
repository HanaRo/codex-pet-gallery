# DeepSeek-chan · Scholar Disguise 1.0.0

[简体中文](../../pets/deepseek-gpt-scholar/versions/1.0.0/README.md) · **English**

Added to the gallery on 2026-11-17 using the palette-corrected build applied on 2026-10-30. The transparent v2 atlas is 1536 × 2288 with 192 × 208 cells. Its 73 frames cover nine animation states and 16 gaze directions. The installed pet downloaded afterward matches the atlas's RGBA pixels. [Sprite sheet](../../pets/deepseek-gpt-scholar/versions/1.0.0/spritesheet.png) · [Manifest and hashes](../../pets/deepseek-gpt-scholar/versions/1.0.0/manifest.json) · [Pixel verification](../../pets/deepseek-gpt-scholar/versions/1.0.0/qa/update-verification.json)

| State | Animation |
| --- | --- |
| idle | Holds the book, looks around, and looks down at the rice |
| running | Raises the book with both hands to hide her mouth, then lowers it to reveal the rice |
| running-left / running-right | Kicks and wags her tail when lifted, then straightens her slipping wig |
| jumping | Plants both feet and wags the whale tail behind her body |
| waving | Holds the book with one hand and waves with the other |
| failed | Looks disappointed, lowers her head, and hugs the book and bowl |
| waiting | Offers the book and bowl slightly forward and looks up for a response |
| review | Scans both pages, then opens her eyes and nods |
| look | Turns her head and gaze through 16 directions while the body, book, and bowl face forward |

## Idle and tail-wag palette

The original tail-wag frames had deeper purple shadows on the clothing and a blue cast. The correction matches the idle palette by lightening the shadows and adjusting hair and skin colors. Five frames were recolored. The previous atlas is archived for comparison or rollback. [Palette comparison](../../pets/deepseek-gpt-scholar/versions/1.0.0/previews/palette-comparison.png) · [Transition on the same timeline](../../pets/deepseek-gpt-scholar/versions/1.0.0/previews/transitions/hover-enter-exit.gif) · [Atlas before correction](../../pets/deepseek-gpt-scholar/versions/1.0.0/sources/history/atlas-before-tail-palette-fix.png)

## Installation and offline reproduction

Place the version's `pet.json` and `spritesheet.png` in `<CODEX_HOME>/pets/deepseek-gpt-scholar/`. ChatGPT Work can import the atlas through a v2-compatible entry point. [Installation and import](../INSTALL.en.md)

Run these commands from the repository root. The 73 final frames in `frames.zip` reconstruct the published RGBA pixels. The source folder contains design concepts, high-resolution strips, prompts, and generation records.

~~~bash
python -m pip install -r requirements.txt
python tools/gallery.py verify-files
python tools/gallery.py validate --pet deepseek-gpt-scholar --version 1.0.0
python tools/gallery.py build --pet deepseek-gpt-scholar --version 1.0.0
python tools/gallery.py package --pet deepseek-gpt-scholar --version 1.0.0
~~~

The installer is written to `dist/deepseek-gpt-scholar-1.0.0-pet.zip`. [Frames](../../pets/deepseek-gpt-scholar/versions/1.0.0/frames.zip) · [Generation record](../../pets/deepseek-gpt-scholar/versions/1.0.0/sources/generation-plan.json) · [QA reports](../../pets/deepseek-gpt-scholar/versions/1.0.0/qa/)

The client's direct frame switch can make the raised book or tail jump when interrupted. The 112.5° pose tilts down only slightly. All four cardinal poses passed an independent blind review. [Transition records](../../pets/deepseek-gpt-scholar/versions/1.0.0/previews/transitions/) · [Direction comparison](../../pets/deepseek-gpt-scholar/versions/1.0.0/previews/direction-qa.png) · [Asset rights](../../ASSET_LICENSE.en.md)
