# Cost and latency from persisted traces

Source: `evidence/final-improved/langfuse-export.jsonl`, exported back from local Langfuse. Aggregator: `src/trace_report.py`. 50 requests, including refusals and rejected outputs. Nearest-rank percentiles. UTC timestamps correspond to 14 September 2026 in Asia/Bangkok.

| Node | p50 ms | p95 ms | Guessed p50 / p95 ms | Actual minus guess ms | Input / output tokens | Modeled USD |
|---|---:|---:|---:|---:|---:|---:|
| Retrieval | 2 | 4 | 5 / 20 | -3 / -16 | 0 / 0 | 0 |
| Generation | 744 | 1,977 | 3,000 / 10,000 | -2,256 / -8,023 | 15,363 / 2,816 | 0.0176658 |

Guesses were saved in `evidence/latency-guesses.json` before the first benchmark. These are engineering assumptions supplied during the build, not claims about the intern's own prior estimates. The generation series includes ten pre-model refusals; token totals include model outputs rejected by validation. This is a warm local run, not a concurrency or cold-start benchmark.

The cost column applies Groq's listed Qwen3.6-27B rates of $0.60 per million input tokens and $3.00 per million output tokens to the observed Qwen2.5 token counts: `(15363 * 0.60 + 2816 * 3.00) / 1000000`. Source: https://console.groq.com/docs/models, read 2026-09-14. **This is a price scenario for a different model, not a quote for Qwen2.5 0.5B, an exact hosted bill, or an equal-quality comparison.** Different tokenizers would change the counts. Local API spend is $0; electricity and hardware are excluded.

The short fixture generation spans occasionally round to zero at wall-clock resolution. That is a measurement limitation, not proof of zero compute. Model latency and percentiles are read from exported trace timestamps so they use the same observations as the dashboard.
