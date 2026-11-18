# Changelog

[简体中文](CHANGELOG.md) · **English**

## Gallery v1.1.0 · 2026-11-18

- Published Scholar Disguise 1.0.0 with a desktop installer, Work import PNG, full source archive, and download checksums. [GitHub Release](https://github.com/HanaRo/codex-pet-gallery/releases/tag/v1.1.0)
- Added previews and downloads for Classic 1.0.0, Foodie Edition 1.0.1, and Scholar Disguise 1.0.0 on the home page and in the gallery. [Version gallery](VERSIONS.en.md)

## DeepSeek-chan · Scholar Disguise 1.0.0 · 2026-11-17

- Added Scholar Disguise to the gallery using the palette-corrected build applied on 2026-10-30.
- Archived nine animation states and 16 gaze directions, including looking at the rice, eating behind the book, straightening the wig when picked up, and wagging her tail while standing.
- Matched the five tail-wag frames to the idle palette by lightening the purple clothing shadows and adjusting the blue cast in the hair.
- Included a transparent v2 atlas, desktop config, 73 lossless frames, high-resolution artwork, prompts, animation previews, QA reports, and the atlas from before the palette correction.

## DeepSeek-chan 1.0.1 · 2026-10-22

- Updated idle to wait with an empty bowl while breathing and blinking.
- Updated horizontal drags to look like she's picked up by her cowlick, kicking her feet, wagging her tail, and gently swaying. The left drag mirrors the right drag frame by frame.
- Kept the bowl in the standing tail wag for closer alignment with idle and working.
- Reduced the chopstick lift, narrowed the hair and ear fins, and aligned body scale and foot baseline.
- Updated 33 frames and retained the pixels in the other 40, including all 16 gaze directions.
- Archived high-resolution sources, prompts, key drag poses, a rollback image, all 73 final frames, and post-installation pixel checks.
- Added exact-timing preview tools and regression tests, and documented transition behavior.
- Preserved the 1.0.0 archive and recorded the remaining gaze-prop, drag-anchor, and hard-cut limitations.

## Development tooling · 2026-10-22

- Added transition guidance and `AGENTS.md` for task changes, hover, drag, gaze overrides, and reduced motion.
- Added offline previews for 18 common transitions, a 9 × 9 frame-boundary stress matrix, and before-and-after comparisons on a shared timeline.
- Recorded slow idle frame timings and automatic fallback boundaries, with seven playback-model tests.
- Established separate versions for artwork changes while preserving the published 1.0.0 directory and attachments.

## DeepSeek-chan 1.0.0 · 2026-10-22

First public archive, based on artwork created on 2026-10-21.

- Archived a full v2 sprite sheet with 73 used cells, 15 transparent empty cells, and 16 gaze directions.
- Used the `jumping` state for a standing tail wag that passes behind the body.
- Enlarged the character by about 25% relative to early previews and aligned the standing foot baseline.
- Kept the bowl-holding wait and rice-eating working animations.
- Included high-resolution artwork, final strips, prompts, the 73 lossless frames in `frames.zip`, and historical QA.
- Added offline verification, pixel-exact reconstruction, and installer tooling.
- Documented the client's automatic return to idle after three loops.
