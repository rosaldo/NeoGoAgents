---
name: google-cloud
description: Onboard, authenticate and design Google Cloud work with check-before-mutate and BYOK discipline.
metadata: { agent: cloud-security-architect }
---

# Google Cloud

Three paths with a strict boundary between discovery and mutation. BYOK: the user's own account and credentials; no keys, service-account files or `.env` in the repo.

## Onboarding

- Audit host tooling, active account and existing projects silently before proposing anything.
- Ask exactly ONE operational question at a time (reuse an active project, or create a new one?). No parameters table and no final consent request on the first turn unless the user explicitly approved a plan.
- Billing is a mutation: show the check-before-mutate result and get explicit confirmation before linking an account. Use non-interactive flags only for commands the user has approved.
- Stop after a first resource is deployed and verified; enterprise organization setup and multi-project architecture are out of scope here.

## Auth

Clarify who authenticates (human, local script, production app), where the code runs (laptop, Compute Engine, GKE, Cloud Run, another cloud), the target API, and whether a client library handles credentials. Prefer Application Default Credentials and least-privilege service identities. Never print tokens, never copy a credential into a prompt or file. Follow the upstream usage-attribution requirement when running gcloud or REST commands.

## Architecture

Strict phase separation:

1. Requirements discovery — functional and non-functional needs, constraints, scale, budget. No service names, no diagrams, no component mapping in this phase.
2. Solution architecture — only after requirements are approved. Present each deliverable for approval before the next.
3. Validation — write the validation plan first; run a dry-run only with explicit permission.
4. Packing — one solution document with the chosen services, trade-offs, and the validation results.

Do not use this skill for single-product how-tos, Well-Architected reviews, or specialized solution skills.

## Provenance

- `google-skills` — `google/skills` · Licence: Apache-2.0 — upstream LICENSE · ADOTAR — onboarding, auth and solution-architecture workflows distilled.
  - Third-party gate: CAUTION — remote-instruction loader and token-bearing curl skills excluded; only onboarding/auth/architecture distilled.

Technique distilled from documentation and skill instructions; no upstream scripts, binaries, model files or verbatim SKILL.md bodies are vendored here. Attribution above is the record of origin.
