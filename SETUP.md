# Reproduce the lab

Run commands from the repository root. Use Python **3.12.14** (`python --version`), Docker Engine with Compose, and enough disk for container images and the 398 MB model. Everything runs locally; there is no paid API requirement. The core runtime has no pip dependencies. On Windows, replace `python` with your Python executable if needed.

## 1. Confirm files and test the harness

```powershell
python -m unittest discover -s tests -v
python -m src.evaluate --mode naive --out tmp/reviewer-fixture-baseline
python -m src.evaluate --mode improved --out tmp/reviewer-fixture-improved
```

Fixture expectations: retrieval 30/50 and generation 10/50 for naive; retrieval 50/50 and generation 48/50 for improved. This is an extractive test double. It verifies the mechanics without a model. Exact scores should match; latency need not match.

The corpus is 50 Markdown files with metadata mirrored in `corpus/index.json`. The runtime reads the index; regenerate both with `python scripts/build_corpus.py` if intentionally changing the source dataset. That script also regenerates the golden set, so keep independent evaluation datasets elsewhere.

## 2. Start isolated free services

```powershell
python scripts/init_local.py
docker compose up -d
docker compose exec -T ollama ollama pull qwen2.5:0.5b
```

`init_local.py` refuses to overwrite an existing `.env`. Reuse it on this machine. The file contains random local credentials and is excluded from Git. Services use a dedicated Compose project and named volumes. Ports 11434 and 3000 bind only to loopback. PostgreSQL has no host port.

Pinned images: Ollama 0.34.0, Langfuse 2.95.11, PostgreSQL 17.6-alpine. Langfuse v2 is deliberately used for this small local lab and its tested legacy ingestion API. It is not the current production recommendation. Registry digest locks are recorded in `evidence/container-lock.json` when available. The model tag resolves to the digest in `evidence/model-lock.json`; verify it before comparison. If the upstream tag changes, restore the original model artifact or declare a new experiment.

## 3. Run the actual model evaluations

```powershell
python -m src.evaluate --backend ollama --mode naive --out tmp/reviewer-model-baseline
python -m src.evaluate --backend ollama --mode improved --out tmp/reviewer-model-improved
```

Each run processes all 50 questions and writes `results.json` and `traces.jsonl`. Exit code 1 means at least one model/adapter error; results still contain every question. Error rows are evidence to review, not successful refusals. Compare to `evidence/final-baseline` and `evidence/final-improved`. The original malformed-output run and intermediate schema run are retained separately.

Settings: temperature 0, seed 42, max generated tokens 256, explicit JSON schema, Qwen2.5 0.5B Q4_K_M. Record your runtime and hardware. Model-run tolerance: up to 2/50 difference in each score is an investigation threshold, not permission to silently replace results. Compare every differing row. Latency is hardware-sensitive and has no equality tolerance.

## 4. Verify Langfuse and measure from its exported traces

Open http://localhost:3000. Sign in as `reviewer@harbor.invalid` using LANGFUSE_USER_PASSWORD from the local `.env`; never put it in a screenshot. The project is Evidence Lab.

```powershell
python scripts/with_env.py src.langfuse_sync tmp/reviewer-model-improved/traces.jsonl --export tmp/reviewer-model-improved/langfuse-export.jsonl
python -m src.trace_report tmp/reviewer-model-improved/langfuse-export.jsonl --out tmp/reviewer-latency.json
```

Sync uses stable IDs, checks per-event errors and verifies observations exist on export. If ingestion is still asynchronous, rerun sync. Filter traces by `track-d`, `ollama` and `improved`. The report reads persisted start/end timestamps and tokens; it never times the agent itself. Fixture generation is sometimes below the wall-clock resolution and has no model token count.

Cost is optional until a price source is supplied. For a hosted-price scenario pass `--input-usd-per-million`, `--output-usd-per-million`, and `--price-source`. Comparing another hosted model's prices with local Qwen token counts is only a budgeting scenario, not an exact bill or equal-quality comparison. Local API spend is $0, excluding electricity/hardware.

## 5. Test the MCP surface

```powershell
python scripts/security_evidence.py
$env:LAB_PRINCIPAL = 'analyst-a'
python -m src.mcp_server
```

Send newline-delimited JSON-RPC initialize, notifications/initialized, then tools/list or tools/call. The transport regression test is a reproducible working client. Trust resides in the OS-owned stdio process. LAB_PRINCIPAL is not remote authentication. Only `read_case` exists; case-a belongs to analyst-a, case-b to analyst-b. Inputs cannot override the principal. No real customer or external system is involved.

## 6. Reuse the harness

Provide `your_adapter.py` with `def answer(question)` returning a dictionary containing `answer`, `citations`, `refused`, `retrieved_sources`, and optionally `error`. The adapter receives only the question, not expected answers. Run:

```powershell
python -m src.evaluate --adapter your_adapter:answer --golden golden-set.yaml --out tmp/other-system
```

For another corpus, author expected sources and answer criteria independently. Preserve the schema. This grader matches terms and source IDs; it is not a semantic judge. Measure false accepts and false rejects against human review.

## 7. Second-person gate and shutdown

Give a fresh copy to a person who has not seen the lab. They follow this file without verbal help, record errors verbatim, and fill `docs/reproduction-log.md`. A local self-test does not satisfy that requirement.

`docker compose stop` stops this project's services while preserving model/database volumes. `docker compose start` resumes them. Do not delete volumes unless intentionally discarding evidence.
