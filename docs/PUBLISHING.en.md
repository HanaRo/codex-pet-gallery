# Publishing to GitHub

[简体中文](PUBLISHING.md) · **English**

Gallery Releases in [HanaRo/codex-pet-gallery](https://github.com/HanaRo/codex-pet-gallery) use the tag `v<gallery version>`. Each character has its own `latest` in `catalog.json` and a tag such as `deepseek-gpt-scholar-v1.0.0`. [Release notes index](../RELEASE_NOTES.en.md)

## Prepare a new version

1. Import an approved atlas into a new version directory. Keep published directories frozen.
2. Archive the final frames, high-resolution sources, prompts, previews, actual QA, and known limitations. Remove local paths, account IDs, temporary URLs, and credentials.
3. Complete the source inventory, hashes, state descriptions, reconstruction records, and `qa_status` in `manifest.json`. Update `catalog.json` and both language editions of the README, version gallery, changelog, and release index. Write the release notes in `docs/releases/v<version>.md` (Chinese) and `docs/releases/v<version>.en.md` (English), with reciprocal language links.
4. Record credit and license status. The MIT license applies to the tools. Character and reference artwork rights are recorded separately. [Asset rights](../ASSET_LICENSE.en.md)

~~~bash
python tools/gallery.py checksums
python tools/gallery.py verify-files
python tools/gallery.py validate --all
python tools/gallery.py build --all
python -m unittest discover -s tests -v
python tools/gallery.py package --pet deepseek-chan --version 1.0.1
~~~

Confirm published versions are intact before committing. Check that the installer repackages consistently and its sprite sheet matches the version's file byte for byte.

## Release body and attachments

Put links to both languages at the top of the GitHub Release. Under `## 中文` and `## English`, include the same information in each language. Start with a short character and version description, then the desktop ZIP, Work PNG, animation changes, and installation. Put the source archive, SHA-256, verification, and limitations under a collapsible developer section. Pin version-specific assets and QA links to the matching tags. Use absolute links in the Release body so documentation links work from the Release page.

Export full sources from the committed Git snapshot to exclude working caches, private configuration, and uncommitted files. The commands use historical v1.0.1 as an example.

~~~bash
git archive --format=zip --prefix=codex-pet-gallery-v1.0.1/ -o dist/codex-pet-gallery-v1.0.1-source.zip HEAD
git tag -a v1.0.1 -m "Codex Pet Gallery v1.0.1"
git tag -a deepseek-chan-v1.0.1 -m "DeepSeek-chan 1.0.1"
git push origin main v1.0.1 deepseek-chan-v1.0.1
~~~

Attach the installer, source archive, separate sprite sheet, and a `SHA256SUMS.txt` for the three downloads. The repository's root `SHA256SUMS.txt` covers project files.

Save the combined bilingual Release body as `dist/v1.0.1-notes.md`. Create a draft, upload assets, and check GitHub's attachment digests before publishing.

~~~bash
gh release create v1.0.1 --verify-tag --draft --title "v1.0.1 · DeepSeek 娘" --notes-file dist/v1.0.1-notes.md
gh release upload v1.0.1 dist/deepseek-chan-1.0.1-pet.zip dist/codex-pet-gallery-v1.0.1-source.zip dist/deepseek-chan-1.0.1-spritesheet.png dist/SHA256SUMS.txt
gh release edit v1.0.1 --draft=false --latest
~~~

Extract the full source archive into a clean directory, then run file verification, validation, reconstruction, and tests. The tools read directly from `frames.zip` and use no original machine paths or Pets plugin. Published tags, old version directories, and old attachments are frozen. Use a new release for asset or config fixes.
