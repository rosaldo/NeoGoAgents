# Technique packs folded into Motion Studio

Seven upstream skill packs were reduced to **reference technique**, not seven competing skills. Motion Studio's own rules stay authoritative: deterministic frames, the spring/idle-motion contract, the two-layer review and the approval gate. Where an upstream doctrine disagrees (for example "no idle wobble"), the existing skill's validated behaviour wins. Do not copy upstream code, templates, fonts, model files, scripts or installers into this skill.

## What each pack contributed

| Pack | Distilled technique | Boundary |
| --- | --- | --- |
| `bang-motion` | Anti-PPT continuity: one persistent subject, a camera that actually moves, and text that lives inside the scene. Decide the concept before reaching for a starter; the frame must still read at thumbnail size. Reject the same opener skeleton on a second project. | CDN fonts, Node/ffmpeg install prompts, MCP bridges and starter HTML stay upstream. |
| `hyperframes` | Plan seams as vectors: an exit's axis, direction, speed and phase determine the entry; cut mid-motion on both sides. Pick one dominant travel direction for the film and spend a different one only with a visible cause. Carry a concrete object across the cut when one exists. | No second renderer, no block registry, no ledger format from upstream. |
| `motionmaxxing` | A measured timing law: land decelerates and leave accelerates, so most travel happens early in the move and then eases into a long tail. Keep springs rare in a film, build the hardest hero beat first, and show proof before describing it. Fails get fixed, not explained. | Its scripts, numeric gates, credential probing and provider calls are not imported; use this skill's `check-video` and contact sheet. |
| `lemo-opuscar` | One timeline is the source of truth: place a page sampled frame by frame alongside voice, music, foley and subtitles, then mix once at the end. Direct a short film with one visual thesis and watch the result before shipping. | Docs are CC BY-NC 4.0; only an independent idea-level restatement is kept here. No prose, style packs, demos or downloads reused. |
| `manim` | Programmatic, frame-exact construction is the point: scenes are declared, not drawn by hand, and mathematical/abstract motion benefits from explicit intermediate states. | No engine install, no LaTeX/OpenGL toolchain, no sample scenes vendored. |
| `raea` | A single editable source of truth can be reviewed scene by scene, with hand edits written back to that source and the render checked against it. | Engine and installer excluded (FSL-1.1-ALv2); no code or app copied. |
| `claude-animation-skills` | Narration-first timing: derive on-screen word timing from measured speech instead of fixed durations. Start from one reproducible graphic idea on a fixed canvas — a line drawing itself, a map route, an exploded view — and vary timing, not element count. | No TTS key or API path, installer, model download, SKILL.md body or font copied. |

## Choosing a pack

Pick **one** dominant grammar per video and write it into the plan: a shot grammar (bang-motion), a seam grammar (hyperframes), a proof grammar (motionmaxxing and manim), a direction grammar (lemo-opuscar, raea) or a single-graphic grammar (claude-animation-skills). Mixing two grammars as equals produces incoherent motion. The choice is a plan line the user approves, not a new skill trigger.

## Media ingestion with `yt-dlp`

`yt-dlp` is an **external binary**, not a prompt, skill or Python dependency. Use it only when the user supplies a URL they are allowed to download.

1. Check the binary is available; if not, say so and ask the user to provide the already-downloaded file. Never install it silently.
2. Fetch into the video's `assets/` directory with the user's URL, keeping the source URL and retrieval date in `style.md`. Public or user-owned media only: no login, no cookies, no credential file, no bypass of paywalls or DRM, no private-session scraping.
3. Confirm the result is a real media file (type and size) and that its licence permits the intended use. Inspect frames only with the review tooling; never feed untrusted media metadata into a shell command.
4. `FFmpeg`/`ffprobe` stay a codec-and-pipeline **reference** for diagnosing format problems. This skill installs neither; it uses the existing `encode` script and its pinned toolchain.

No upload, scheduling, account login or credential storage belongs in this flow.

## Provenance

- `bang-motion` — `bangtutorial/bang-motion` · Licence: MIT — Copyright (c) 2026 Bang Tutorial · Third-party gate: APPROVE — SkillSpector 2.12.0 static; ~40 AE1 hits are explicit static_parse_limit coverage artifacts and 9 P2 hits are MIT attribution comments. CDN fonts, Node/ffmpeg install prompts and starter HTML excluded.
- `hyperframes` — `heygen-com/hyperframes` · Licence: Apache-2.0 — upstream LICENSE · Third-party gate: CAUTION — semantic-only gate (bounded discovery, no JSON): remote MCP endpoint, signed-in-account telemetry and sandbox fingerprinting excluded; seam-vector technique only.
- `motionmaxxing` — `motionmaxxing/motionmaxxing` · Licence: Apache-2.0 — upstream LICENSE · Third-party gate: CAUTION — ~20 AE1 hits are coverage artifacts and NOTE/HTML hits are scene markers; home-dir credential probing, provider APIs and install scripts excluded; measured timing law only.
- `lemo-opuscar` — `lemomo-ai/lemo-opuscar` · Licence: Code MIT; docs CC BY-NC 4.0 with a film-making permission — upstream LICENSE/REUSE.toml · Third-party gate: CAUTION — docs are CC BY-NC 4.0 per REUSE.toml; idea-level restatement only, no verbatim prose, styles, demos, music or tiered downloads.
- `manim` — `3b1b/manim (ManimGL)` · Licence: MIT — Copyright (c) 2020-2026 3Blue1Brown LLC · Third-party gate: CAUTION — MIT library, but README install commands, unpinned requirements and exec() of scene code excluded; geometry/easing idea only.
- `raea` — `shinyobjectz/raea` · Licence: FSL-1.1-ALv2 — Copyright 2026 Shane Murphy · Third-party gate: CAUTION — FSL-1.1-ALv2 engine, installer, chroot curl|sh and toolchain excluded; hand-editable frame-accurate timeline idea only.
- `claude-animation-skills` — `ArtemNovitckii/claude-animation-skills` · Licence: MIT — Copyright (c) 2026 Artem Novitckii · Third-party gate: CAUTION — ElevenLabs key/API path, symlink installer and unpinned model downloads excluded; narration-first timing idea only.
- `yt-dlp` — `yt-dlp/yt-dlp (ingestion binary)` · Licence: Unlicense — public domain · Third-party gate: CAUTION — Unlicense binary: no embedding, no network fetching, no cookies, extractors or hooks; user-consented ingestion boundary only.

Technique distilled from documentation and skill instructions. No upstream script, template, binary, font, model, installer or verbatim `SKILL.md` body is vendored here. Attribution above is the record of origin.
