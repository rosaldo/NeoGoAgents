---
name: instagram
description: Write and audit Instagram Reels and carousels, and read account insights without guessing.
metadata: { agent: instagram-curator }
---

# Instagram

Reels, carousels and honest reads of the account's own insights. Not for posting — the human approves every asset.

## Voice first

Read the creator's voice profile in project docs if present; otherwise ask for three of their own Reels and infer it. A thin idea gets one batched question: what happened, to whom, and what did it cost or return? No padding, no invented metrics.

## Reel

- Write three hooks, score them, keep the best. Spoken line and on-screen line are written separately; the first frame has motion, not a static face.
- Beat sheet: `0:00–0:02` hook, `0:02–0:07` stake, then one idea per beat with a changing frame, last 3s the payoff and ONE ask, final word echoing the hook so the loop lands clean.
- Working length 15–45s. Under 7s inflates loop counts; 3-minute Reels almost nobody should use.

## Carousel

Use for sequence that needs re-reading (steps, framework, before/after). Use a Reel for motion or a payoff that must be seen happening. One claim is neither.

- 6–10 slides (cap 20, below 5 the swipe never starts).
- Cover ≤6 words, large, legible as a grid thumbnail; slide 2 stands alone as a second cover.
- One idea per slide: 3–7 word headline, ≤25 words below. If it needs a paragraph, split it.
- Recap slide is the screenshot-and-send asset: standalone, readable with no context. Last slide: one CTA. Number slides (3/8).
- Build 1080×1350, keep text inside the middle with ~120px safe margin; small handle on every slide; alt text on the cover at minimum.

## Audit

Rank by **outlier multiple** (views / account median) and **sends per reach**, not raw views. Also read non-follower reach, hold at 3s (the hook's grade), average watch time and follows per reach, showing the arithmetic.

Compare the top five with the bottom five: hold at 3s first, then hook formula, format, length, theme, first-hour comment replies. Day and time last — almost never the cause.

## Scope guard

Public or user-supplied data only. No logged-in scraping, no credential storage, no publishing.

## Provenance

- `instagram-agent-skill` — `Jakeschincariol/instagram-agent-skill` · Licence: MIT — Copyright (c) 2026 Jake Schincariol · ADOTAR — ig-reel, ig-carousel and ig-audit techniques distilled.
  - Third-party gate: APPROVE — SkillSpector 18/LOW; posting and login are forbidden in the upstream rules, helpers are stdin/file-only.

Technique distilled from documentation and skill instructions; no upstream scripts, binaries, model files or verbatim SKILL.md bodies are vendored here. Attribution above is the record of origin.
