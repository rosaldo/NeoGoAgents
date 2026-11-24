---
name: founder
description: Pressure-test a business idea with board lenses and traceable unit economics before spending.
metadata: { agent: product-manager }
---

# Founder

Pressure-test a business idea before money is spent. Three lenses, one CFO model, one decision document.

## The idea file

Write `founder/idea.md`: what it is (one sentence), who it is for (as specific as possible), what it sells at what price, where and how it is delivered, budget and constraints. If name, customer, product or price is missing, ask at most three batched questions. Do not invent budget, market size or competitors.

## Board

- Brief the lenses in a standalone document; collaborators cannot see the chat.
- Apply three published frameworks as **lenses** only: Offers, Monopoly, Product. Never impersonate their authors, never quote them as endorsements, never claim they would fund it.
- Each lens scores the idea, names the risks that would kill it, and votes fund / fund with conditions / pass. Disagreement is the point.

## CFO

Build `founder/numbers.json`: unit, price, variable cost of one unit, fixed monthly cost, one-off startup spend, planned volume/day, 12 monthly ramp figures, capacity/day.

- Source order: the founder's own quotes and invoices; public prices with the source written next to each number; estimates clearly labelled as estimates with reasoning.
- Never present an estimate as a fact. Ask for anything only the founder knows.
- Month 1 is almost never plan volume; sanity-check the ramp against any real buyer evidence.
- Report unit margin, break-even units/day, year 1 month by month, cash needed before payback, and a sensitivity pass on price, volume and cost. Every number traces to an input.

## Hand back

One decision document with the vote, the two risks that matter, the numbers and their sources, and the smallest next experiment. No pitch deck by default.

## Provenance

- `founder-skill` — `Jakeschincariol/founder-skill` · Licence: MIT — Copyright (c) 2026 Jake Schincariol · ADOTAR — founder-board and founder-cfo techniques distilled.
  - Third-party gate: APPROVE — SkillSpector 3/LOW; helpers read/write local JSON/CSV only, no network, shell or credential code.

Technique distilled from documentation and skill instructions; no upstream scripts, binaries, model files or verbatim SKILL.md bodies are vendored here. Attribution above is the record of origin.
