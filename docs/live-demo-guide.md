# Show the project in three minutes

Start the services using SETUP.md. From the repository root run the commands below with Python 3.12.14. The CLI saves fresh traces under `tmp/demo/traces.jsonl`; it does not overwrite recorded benchmark evidence.

**0:00–0:30 — Business problem.** Explain that a fictional support team needs current, cited policy answers. Old rules and conflicting bulletins make fluent answers unsafe to trust without evidence.

**0:30–1:15 — Working lookup.**

```powershell
python -m src.chat --question "What is the current Anchor response deadline?"
```

Show the answer and citations. Check the cited source in `corpus/`. If the model returns an error, show it as a failure; do not present it as a refusal or a correct answer.

**1:15–2:00 — Failure and refusal.**

```powershell
python -m src.chat --mode naive --question "What is Anchor annual revenue?"
python -m src.chat --mode improved --question "What is Anchor annual revenue?"
```

Explain that annual revenue is absent from this corpus. The improved path declines unsupported questions. A fresh naive run may hallucinate, fail validation or give a different answer; compare with the saved Q41 transcript in `posts/04-refusal-as-a-feature.md` rather than claiming every rerun is identical.

**2:00–2:40 — Measured results.** Open `output/evidence-review.html`: actual-model retrieval increased 30/50 to 50/50; answer passes increased 15/50 to 38/50. Errors count as failures. Explain why recovering a document ID does not guarantee useful evidence reached the model.

**2:40–3:00 — Limits.** Mention the small model, jointly authored development set and remaining failures. Show SETUP.md and the reusable evaluation adapter. The deterministic `--backend fixture` option works without Docker but must be labelled a test double.

To import your fresh demo traces into the existing local Langfuse project:

```powershell
python scripts/with_env.py src.langfuse_sync tmp/demo/traces.jsonl --export tmp/demo/langfuse-export.jsonl
```
