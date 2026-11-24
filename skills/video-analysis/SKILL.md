---
name: video-analysis
description: Reverse engineer a reference video shot by shot and produce an evidence-based remake plan.
metadata: { agent: short-video-editing-coach }
---

# Video analysis

Reverse engineer a **reference** video shot by shot: how each image was produced, what was overlaid, where the sound came from, and how to remake it. Reply in the user's language.

## Per-shot classification

Pick one source per shot from: live action, stock footage, AI-generated video, digital human, 3D render, 2D animation, stop-motion, code/template render, screen capture, photo push, still image. Some classes are not machine-detectable — judge from frames. For live action also note AI edits (face swap, lip sync, restyle, background swap).

## Layers to report

- **Overlays:** per-line subtitles with timing and style, kinetic text, titles/chapter cards, tracked labels, stickers/GIFs, picture-in-picture. Tie each to the spoken line or frame event.
- **Sound:** voice origin (human or synthetic), music style/BPM/key and source, sound effects with timestamp and triggering event, cuts on beat. Mark "to confirm" with a verification method when the source is uncertain.
- **Assets:** embedded real pixels (the original photo, screenshot or clip is required to remake) versus reference images of products/logos/people appearing inside generated frames (only reference material).
- **Live-action craft:** framing, camera position, lighting setup, grade, and editing rhythm — for real footage only. For synthetic shots label the same description as generation guidance, not a shooting plan.

## Method

Use an installed analysis tool if one is configured; discover its actual command surface instead of memorizing flags. Inspect the storyboard and audio overview first, then only the low-confidence or near-tie shots at full frame resolution. Cross-check tool output against frames you actually looked at; your review wins when they disagree, with the reason written down. Never paste a giant internal breakdown into the chat, never pass the user's `.env` to a tool, and require explicit consent before sending media or prompts to an external model provider.

## Deliverable

One-line conclusion, narrative line, per-shot table with confidence, remake route per shot and per generation unit, asset list, uncertainties, and the path to the user-facing report. Evidence over confidence: "AI, ~70%, to confirm" beats a made-up certainty.

## Provenance

- `rea-video` — `JuneYaooo/rea-video` · Licence: Apache-2.0 — upstream LICENSE · COMPLEMENTAR — shot taxonomy and review discipline distilled; CLI not installed.
  - Third-party gate: CAUTION — CLI upload path, `--env-file` and Gemini API key flow excluded; external model/API calls need explicit consent.

Technique distilled from documentation and skill instructions; no upstream scripts, binaries, model files or verbatim SKILL.md bodies are vendored here. Attribution above is the record of origin.
