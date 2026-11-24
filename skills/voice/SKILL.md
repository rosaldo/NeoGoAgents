---
name: voice
description: Build on-device speech and transcription with Moonshine, or drive a local VoiceStudio backend for dubbing.
metadata: { agent: voice-ai-integration-engineer }
---

# Voice

One voice entry point, two paths. Pick by what the user has, not by habit.

## Path A — on-device Moonshine

No API keys, no cloud, no substituting Whisper, OpenAI Realtime or a hosted STT/TTS API when on-device was requested. Verify the installed SDK against live docs before writing code; model memory is not enough. Code samples run through `uvx --with moonshine-voice python -c "..."` (or the project's pinned wrapper) — never a bare interpreter or a package-manager install command.

- Construct → setters → `load()` → `start()`. Constructors are cheap; `load()` is the slow, fallible call that may populate a local model cache. Set options before loading.
- `MicTranscriber` for a live microphone, `Transcriber` when feeding PCM/WAV, `AgentFlow` for spoken conversational flows (do not assemble its internal pieces unless asked), `TextToSpeech` for playback and voice design.
- `on_text` is a partial hypothesis and will change; only `on_line` is a finished segment. Never report partial text as a transcript.
- Language, keyterms and domain customization matter; fetch the current docs for the installed version before promising a capability. Model downloads need explicit user consent; some legacy non-English non-streaming models carry a non-commercial community licence, so check the exact model licence before any commercial use.

## Path B — local VoiceStudio backend

Honor the user's configured address (default `http://localhost:3900`). Check `/health`, discover the running version's contracts with `/openapi.json`, and list voices/engines before using any profile ID. Electron renderer and dev proxy are not the public API.

- Generate speech from a discovered voice profile; check HTTP status and probe the output file before calling it audio — an error body can be saved as `.wav`. Report real path, format and duration.
- Transcribe with the format the running schema supports (`json`, `text`, `verbose_json`, `srt`/`vtt`). Check model readiness first; a missing model needs the user's authorization, never a silent download.
- Cloning only with voices the user is authorized to use. Dubbing preserves the source media, speaker assignments, segment timing and background audio; translation completion is not rendered-dub completion. Use returned job IDs and status endpoints instead of blind retries.
- `401`/`403` are authentication failures, not permission to disable auth. Never print tokens or put placeholders in config. Container `localhost` is not the host.

## Boundaries

No credentials in the repo, no remote provider swap, no model download or second backend without explicit approval. No duplicate trigger with the motion or video-analysis skills: this one is speech and audio only.

## Provenance

- `moonshine` — `moonshine-ai/moonshine` · Licence: MIT — upstream LICENSE (Moonshine code and models) · ADOTAR — base on-device voice path.
  - Third-party gate: CAUTION — model cache download needs consent; legacy non-English non-streaming models use a non-commercial community licence.
- `VoiceStudio` — `debpalash/VoiceStudio` · Licence: AGPL-3.0-only — Copyright 2024-present Palash Debnath and contributors · FUNDIR — cloning/dubbing/transcription path distilled from documentation only; no AGPL source copied.
  - Third-party gate: CAUTION — AGPL source, owner-policy docs, analytics/cloud/telemetry paths excluded; documentation-level technique only.

Technique distilled from documentation and skill instructions; no upstream scripts, binaries, model files or verbatim SKILL.md bodies are vendored here. Attribution above is the record of origin.
