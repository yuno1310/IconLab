# Why one evaluation score tells you too little

Actual local Qwen2.5 0.5B: baseline retrieval 30/50, generation 15/50; improved retrieval 50/50, generation 38/50. Errors: 2 baseline, 10 improved.

The customer in this synthetic project is a support team that cannot tell whether an answer is safe to use. I separated source recovery from answer correctness because those failures need different repairs.

**Q21: What is the Anchor returns window when East and West bulletins disagree?**

Expected sources: anchor-east, anchor-west. Retrieved: anchor-east, anchor-west. Retrieval pass: True. Generation pass: False.

Actual answer:
```text
The Anchor returns window is 30 days in the East bulletin and 45 days in the West bulletin.
```

Error: `None`.

This case has the needed source IDs but still fails the answer rubric. Inspect the actual chunks: recovering a document ID is weaker than recovering its complete evidence. Then inspect the prompt and model output. Adding another embedding model would not by itself establish that the answer is grounded.

**Q11: What is the current Anchor response deadline and required escalation evidence?**

Expected sources: anchor-current, anchor-routing. Retrieved: anchor-old, anchor-current. Retrieval pass: False. Generation pass: False.

Actual answer:
```text
Anchor current response deadline is 24 hours. This policy supersedes the 2025 response policy. Coverage
```

Error: `None`.

Here the required source set is missing. The first intervention is retrieval: preserve paragraphs, rerank candidates, keep both conflicting bulletins, and retire old versions only within the same policy family.

A blended score compresses these causes. Even a high retrieval score can hide poor generation. Keep the two per-question columns and quote the transcript that supports the diagnosis.

The reusable golden set has ten questions in each of five categories: easy, synthesis, conflict, stale, and must-refuse. Each record contains an expected answer, expected source IDs, required terms, forbidden terms and refusal intent. `golden-set.yaml` uses JSON syntax, a YAML 1.2 subset. The harness accepts a `module:function` adapter so the next intern can supply another system without rewriting the grader.

Limits: these are rule-based checks on a jointly authored synthetic development set. Matching required phrases can accept irrelevant or contradictory text; paraphrases can fail. Source-ID recall misses partial-chunk defects. A second human should calibrate a sample before using these scores for a release decision. All numbers above come from saved results, not a prediction of production performance.

Evidence: `evidence/final-baseline/results.json`, `evidence/final-improved/results.json`. Draft for author review; not published.
