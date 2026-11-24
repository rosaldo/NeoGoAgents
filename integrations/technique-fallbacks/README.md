# Techniques and fallbacks — documentation only

These entries were evaluated but are **not installed** and get no adapter, no binary and no credential in `agency-agents`. They are recorded as techniques or fallbacks so a future decision has a starting point. The canonical runtime stack is [`../canonical-stack/README.md`](../canonical-stack/README.md).

| Entry | Kind | What it contributes | Why it stays documentation | Revisit when |
| --- | --- | --- | --- | --- |
| `Graft` | technique | Graph-shaped context grafting for code questions | `codebase-memory-mcp` is the single installed graph provider; a second one would compete and duplicate context | The canonical graph server cannot answer a measured question and an A/B eval shows a real gain |
| `graphify` | technique | Turning a repository into navigable entities/edges | Same graph boundary as above | Same as Graft |
| `Understand-Anything` | technique | Broad repo comprehension workflow | Overlaps the installed graph path and the catalog's Level 1 → Level 2 reading order | A repo class fails with graph + catalog alone |
| `milvus` | fallback | Vector store for large-scale retrieval | `zvec` covers local vector experiments; hosting another store adds operations without evidence | Retrieval quality is bounded by the local index and a load test justifies a server |
| `OmniRoute` | fallback | Model-routing gateway | BYOK gateways are owner-configured; installing a second gateway would duplicate `litellm` | Measured routing savings exceed the extra hop and the owner opts in |
| `freellmapi` | fallback | Free-model discovery | Discovery aid, not a runtime dependency | A concrete workflow needs it and licence/terms are rechecked |
| `clodfarm` | protocol reference | Fleet/agent coordination ideas | Reference for the Maestro protocol only; no persona or installed service | A Maestro gate change is being designed |
| `ruflo` | protocol reference | Multi-agent orchestration patterns | Same boundary: study the protocol, never import a competing orchestrator persona | Same as clodfarm |
| `everything-claude-code` | protocol reference | Broad agent/tool conventions | Reference material; importing it wholesale would duplicate existing personas and skills | A specific convention is adopted deliberately, one line at a time |

## OmniRoute: memory OFF contract

If the owner ever evaluates OmniRoute, **memory must be OFF for every request** — the default injects roughly 2K tokens of recalled context per request and would quietly compete with the Maestro ledger:

```
x-omniroute-no-memory: 1
```

Never send a real key in a doc example. BYOK stays in the owner's environment; the header above is the only value shown here.

## Boundaries

- No gateway with memory enabled. No second graph server. No redundant installation of a fallback.
- No `.env`, token, credential file or plaintext key in this repository or in a commit message.
- No persona is added because of a protocol reference. Maestro remains the single orchestration protocol and the ledger remains the single memory of record.
