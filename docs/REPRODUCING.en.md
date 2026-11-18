# Reproduction and source artwork

[简体中文](REPRODUCING.md) · **English**

## Three ways to reproduce a version

| Goal | Inputs | Result |
| --- | --- | --- |
| Use the published version | `spritesheet.png` and `pet.json` | The exact bytes of the frozen sprite sheet |
| Reassemble the published version | 73 approved PNGs in `frames.zip` | Identical decoded RGBA pixels |
| Redraw or extend animations | Artwork, high-resolution strips, and prompts in `sources/` | Design and process references. Regenerated artwork can vary. |

The hashes and source history below refer to DeepSeek-chan 1.0.1. Scholar Disguise 1.0.0 uses the same offline reconstruction process and has its own [version notes](versions/deepseek-gpt-scholar-1.0.0.en.md) and [file and pixel hashes](../pets/deepseek-gpt-scholar/versions/1.0.0/manifest.json).

SHA-256 of the final DeepSeek-chan 1.0.1 PNG:

~~~text
be535f9abd7aeca27c0c33bd04b4cfe3267dd907de6d29eaca4341aa552b0af1
~~~

SHA-256 of decoded RGBA bytes from the 1536 × 2288 image in row-major order:

~~~text
64674e1ed187ba8c49a921bb37e8f8e0c725fc82845dc6a49d0697c60d7d0be4
~~~

The sheet downloaded from the installed pet matches the RGBA hash. The server may re-encode the PNG, so the downloaded file can have a different file hash.

## Reassemble offline

Use Python 3.11 or later. Pick a version in the [version gallery](../VERSIONS.en.md). This example uses Foodie Edition 1.0.1. For Scholar Disguise, use ID `deepseek-gpt-scholar` and version `1.0.0`.

~~~bash
python -m pip install -r requirements.txt
python tools/gallery.py verify-files
python tools/gallery.py validate --pet deepseek-chan --version 1.0.1
python tools/gallery.py build --pet deepseek-chan --version 1.0.1
~~~

The tool verifies the SHA-256 hashes of the atlas, frames, and sources. It reads the 73 cleaned frames from `frames.zip`, places them on a transparent canvas, and checks all pixels after re-encoding. Direct RGBA pasting preserves semitransparent edges.

After installing dependencies, reconstruction uses only local files. It requires no account, upload links, original machine paths, or Pets plugin. Pinning Python and Pillow helps reduce encoding differences. The preserved original is the reference when you need byte-for-byte PNGs across platforms.

## Redrawing and high-resolution sources

`sources/references/` contains the base illustration, eating-prop art, the user-provided reference, and approved direction anchors. `sources/strips/` contains 11 selected strips. The left drag is a native-size frame-by-frame mirror, and the other newly drawn strips have high-resolution sources. `sources/prompts/` records the prompts.

The original workflow used Codex imagegen and the Pets plugin 0.1.6 assembly tools:

1. Generate a separate strip for each state from a common character design. Include bowl and chopstick references for eating.
2. Extract complete characters using connected components, remove the green background, and scale each row consistently.
3. Align the standing feet using integer translation. Align the drag poses at the cowlick grab point and keep the kicking and sway.
4. Approve the four cardinal poses, then generate and verify all 16 directions clockwise.
5. Assemble the v2 atlas and remove local green spill while preserving alpha.
6. Check structure, state meaning, direction, transparent edges, and the full animation.

For 1.0.1, see the source generation record and `qa/idle/`, `qa/drag/`, `qa/drag-pair/`, `qa/tail-wag/`, and `qa/running/`. QA for inherited states is in the 1.0.0 directory. Historical run paths document earlier work and are outside the tool's dependencies.

The offline tool starts from approved frames. Reprocessing a new high-resolution strip can yield different pixels. The historical plugin implementation is outside the repository. The tools returned no model ID or seed at the time. Prompt references to earlier strips and attachment order describe the editing context. Use the approved references and final artwork to interpret them, since discarded attempts were not archived.

## Verification scope

- `tools/gallery.py` checks project inventory, layout, used and transparent cells, frame consistency, and pixel-exact reconstruction.
- `qa/` contains sanitized records of actual server validation, Pets plugin checks, and approved historical direction reviews.
- New characters and revised poses require visual review for meaning and movement in addition to hash and geometry checks.

The complete frame set is in `frames.zip`. Paths match `manifest.json`, and each frame retains its original PNG bytes and hash. The tool can rebuild without extracting it. `frames/` is an optional preview cache. If present, the validator compares it with the frozen version.

## Export previews again

~~~bash
python tools/render_previews.py --atlas pets/deepseek-chan/versions/1.0.1/spritesheet.png --output dist/previews
python tools/preview_transitions.py --atlas pets/deepseek-chan/versions/1.0.1/spritesheet.png --compare pets/deepseek-chan/versions/1.0.0/spritesheet.png --output dist/transitions
~~~

Pillow is sufficient for PNG and GIF. Add `--ffmpeg ffmpeg` to the first command for MP4 if FFmpeg is installed. Each state preview repeats one cycle at the inspected frame timings. Separate transition previews show the three-loop fallback and interruptions.
