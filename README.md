# Harbor Support Evidence Lab

## Who is the customer?

Harbor Devices is a fictional distributor whose support analysts need current, cited policy answers. The assumed workflow and success metric are in [the discovery brief](docs/discovery-brief.md). All data is generated.

## What was broken?

An answer could look convincing while using an obsolete deadline, omitting half a conflict, or inventing information absent from the corpus. The baseline intentionally uses 95-character chunks, simple overlap ranking, two chunks, and no refusal guard. Source recovery and answer correctness must be measured separately.

## What did you build?

A local RAG lab, 50-question golden set, independent retrieval/generation grading, an Ollama adapter, persisted traces with local Langfuse replay/export, a minimal read-only MCP stdio server, an OWASP assessment, and submission posts/decks. See [START-HERE.md](START-HERE.md) for the delivered files and remaining human steps.

## How does it work?

Python 3.12.14 with no third-party runtime packages. The improved retriever preserves paragraphs, reranks lexical candidates using IDF, suppresses obsolete family versions, and applies a query coverage refusal guard. It is intentionally ordinary application code: a fixed workflow does not require an orchestration framework. Ollama generates schema-constrained answers locally. Citations are checked against retrieved IDs. No SAP system is connected.

Run the deterministic smoke path from the repository root:

```powershell
python -m unittest discover -s tests -v
python -m src.evaluate --mode naive --out tmp/my-baseline
python -m src.evaluate --mode improved --out tmp/my-improved
```

Ask a question against the local model with `python -m src.chat --question "What is the current Anchor response deadline?"`. Add `--backend fixture` for a labelled test double without Docker. See [the live demo guide](docs/live-demo-guide.md) and [current solo status](docs/solo-status.md).

The three smoke commands use a deterministic extractive fixture, not a language model. The complete model, Docker, tracing and reviewer procedure is in [SETUP.md](SETUP.md). Output directories must be new to avoid overwriting evidence.

## How did you evaluate it?

Ten cases each cover easy lookup, synthesis, conflicting sources, stale facts and must-refuse questions. Each records expected answers and sources. The harness emits retrieval pass, source recall and answer pass separately. Errors count as failed answers. [Measured results](evidence/results-summary.md) link to the live-model evidence. The MCP suite tests process transport, ownership, projection, malicious parameters, bounded requests and quota expiry. A 1,000-call test and before/fix comparison are in [the assessment](docs/owasp-assessment.md).

## What would you change before production?

Add independently authored test cases, human grading calibration, evidence-span and claim-level scoring, semantic prompt-injection tests, stronger retrieval isolation, authenticated multi-user access, persistent quotas and deployment hardening. Replace the legacy local Langfuse release with a supported production deployment. Validate a larger model and repeat runs to measure variance. The current corpus and golden set were jointly authored with AI assistance; results are development evidence, not production assurance. The project is published at https://github.com/yuno1310/IconLab/tree/main. Human sign-off, second-person reproduction and program submission are pending.
