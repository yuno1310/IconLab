# Reproduction gate

Solo verification status: **automated extracted-copy and isolated Linux runtime checks passed on 2026-10-05**. Original-program second-person and full clean-machine deployment gates remain unperformed. No human reproduction or sign-off is claimed.

- Fresh Windows virtual environment with no pip packages: ten tests, both 50-case fixture evaluations and CLI refusal check passed. See `evidence/extracted-pack-check.json`.
- Disposable pinned Python 3.12.14 Linux container, network disabled: the same ten tests and fixture scores matched, and CLI refusal passed. See `evidence/clean-container-check.json`. This checks runtime portability, not a fresh complete model/database deployment.
- Existing local Ollama and Langfuse: policy lookup, naive failure and improved refusal exercised; all three traces re-exported from Langfuse. See `evidence/solo-demo-2026-10-05`.

| Reviewer | Date | OS / Python / Docker | Model digest | Baseline R/G | Improved R/G | Stopping point verbatim | Fix and rerun |
|---|---|---|---|---|---|---|---|
| Pending | Pending | Pending | Pending | Pending | Pending | Pending | Pending |

Required acceptance: run from SETUP.md alone without verbal assistance, compare row-level results, explain any difference, and meet the documented tolerance. Record whether this is a fresh machine, a fresh checkout on the same machine, or only a rerun. These are different claims.
