# Pet gallery development

- Before changing animation artwork, read `docs/TRANSITIONS.md` and the target version's manifest. Treat state boundaries and interruptions as part of the animation design.
- Keep published version directories immutable. New artwork belongs in a new version or an explicitly marked working preview; retain source art, exact encoded frames, QA evidence and a rollback copy.
- Keep a common body scale, registration and prop geometry across related states. Review natural exits, arbitrary-frame interruptions, hover, drag reversal/release and look overrides. Do not add a fake crossfade to a preview unless it is explicitly labeled as a proposed player feature.
- For artwork changes, validate the actual encoded atlas and generate relevant transition previews with `tools/preview_transitions.py`. Its desktop timing model is a documented snapshot, not a client setting or a promise about future versions.
- After changing the QA tools, run `python -m unittest discover -s tests -v`. After changing repository contents, refresh `SHA256SUMS.txt` and run `tools/gallery.py verify-files`. Keep private account IDs, signed URLs and copied client bundles out of the repository.
