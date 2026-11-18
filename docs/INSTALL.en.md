# Installation and import

[简体中文](INSTALL.md) · **English**

The installer includes `pet.json`, `spritesheet.png`, and `layout.json`. Desktop clients read `pet.json`. The gallery uses `release.json` and `manifest.json` to record version metadata.

## Local Codex and compatible desktop clients

For a client that reads the `pets` folder under `CODEX_HOME`:

1. Extract the entire installer ZIP.
2. Create a folder under `CODEX_HOME/pets` that matches the `id` in `pet.json`. Use `deepseek-gpt-scholar` for Scholar Disguise or `deepseek-chan` for the blue-haired maid. If `CODEX_HOME` is unset, the location is usually `~/.codex/pets`.
3. Place `pet.json` and `spritesheet.png` in the same folder. Keep the existing `spritesheetPath` in `pet.json`. You can keep `layout.json` alongside them.
4. In Settings → Pets, refresh and select the pet.

~~~text
<CODEX_HOME>/pets/deepseek-gpt-scholar/
├── pet.json
├── spritesheet.png
└── layout.json
~~~

When upgrading an existing pet, back up its folder before replacing the files. A desktop installation can appear as a separate entry from a cloud pet created through the Pets plugin. The client assigns cloud Pet IDs separately.

The installer ZIP is a set of assets for a compatible client. It contains no standalone Windows desktop pet or background process.

## ChatGPT Work and the Pets plugin

Where custom pet creation is available, attach the version's `spritesheet.png` and use its preferred display name and description from `pet.json`. For Scholar Disguise, you can use this prompt.

> Validate the attached v2 sprite sheet and use it to create a pet called “DeepSeek-chan · Scholar Disguise.” Description: “DeepSeek-chan in a white-dragon scholar disguise, wearing glasses and holding a book with a rice bowl hidden behind it.” The jumping state shows her standing and wagging her tail.

Create a fresh pet under your own account so the client can assign its ID.

## Web upload

If Settings → Personalization → Pet offers **Upload pet**, follow the requirements shown there. This gallery ships v2 PNGs at 1536 × 2288. If the entry point only accepts v1 sheets at 1536 × 1872, keep the v2 file at its original size and use the v2-capable Pets plugin or a compatible desktop client.

Availability depends on the client and account. [Pets documentation](https://learn.chatgpt.com/docs/pets)

## The eating animation stops before the task does

The desktop client described in the playback guide returns to idle after three working loops. The source art, resolution, and preview GIF loop settings cannot alter that behavior. [Client playback](https://github.com/HanaRo/codex-pet-gallery/blob/main/docs/PLAYBACK.en.md)
