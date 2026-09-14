"""Generate evidence-based posts and submission documents after the model runs."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path): return json.loads((ROOT/path).read_text())
def main():
    b=read('evidence/final-baseline/results.json'); f=read('evidence/final-improved/results.json')
    summary=f"Actual local Qwen2.5 0.5B: baseline retrieval {b['summary']['retrieval_passes']}/50, generation {b['summary']['generation_passes']}/50; improved retrieval {f['summary']['retrieval_passes']}/50, generation {f['summary']['generation_passes']}/50. Errors: {b['summary']['errors']} baseline, {f['summary']['errors']} improved."
    def example(row):
        return f"**{row['id']}: {row['question']}**\n\nExpected sources: {', '.join(row['expected_sources']) or 'none'}. Retrieved: {', '.join(row['actual']['retrieved_sources']) or 'none'}. Retrieval pass: {row['retrieval_pass']}. Generation pass: {row['generation_pass']}.\n\nActual answer:\n```text\n{row['actual']['answer']}\n```\n\nError: `{row['actual'].get('error')}`.\n"
    gen=next((r for r in b['rows'] if r['retrieval_pass'] and not r['generation_pass']),b['rows'][20])
    ret=next(r for r in b['rows'] if not r['retrieval_pass'])
    (ROOT/'posts/02-one-number-hides-the-bug.md').write_text(f'''# Why one evaluation score tells you too little

{summary}

The customer in this synthetic project is a support team that cannot tell whether an answer is safe to use. I separated source recovery from answer correctness because those failures need different repairs.

{example(gen)}
This case has the needed source IDs but still fails the answer rubric. Inspect the actual chunks: recovering a document ID is weaker than recovering its complete evidence. Then inspect the prompt and model output. Adding another embedding model would not by itself establish that the answer is grounded.

{example(ret)}
Here the required source set is missing. The first intervention is retrieval: preserve paragraphs, rerank candidates, keep both conflicting bulletins, and retire old versions only within the same policy family.

A blended score compresses these causes. Even a high retrieval score can hide poor generation. Keep the two per-question columns and quote the transcript that supports the diagnosis.

The reusable golden set has ten questions in each of five categories: easy, synthesis, conflict, stale, and must-refuse. Each record contains an expected answer, expected source IDs, required terms, forbidden terms and refusal intent. `golden-set.yaml` uses JSON syntax, a YAML 1.2 subset. The harness accepts a `module:function` adapter so the next intern can supply another system without rewriting the grader.

Limits: these are rule-based checks on a jointly authored synthetic development set. Matching required phrases can accept irrelevant or contradictory text; paraphrases can fail. Source-ID recall misses partial-chunk defects. A second human should calibrate a sample before using these scores for a release decision. All numbers above come from saved results, not a prediction of production performance.

Evidence: `evidence/final-baseline/results.json`, `evidence/final-improved/results.json`. Draft for author review; not published.
''',encoding='utf-8')
    (ROOT/'posts/03-owasp-mcp.md').write_text(f'''# The OWASP API Security Top 10, aimed at an MCP server

A grounded answer is insufficient if its tool can read another user's case. I tested an owned local MCP stdio server over two synthetic support records.

The archived before-fix implementation looked up a case ID and returned its entire record. Analyst A could read analyst B's case, including its internal note. The fixed service derives identity from the local process, checks record ownership on each call, and projects only the public summary. The same attempted access now returns `Case unavailable`.

The second weakness was resource consumption. In a bounded 1,000-call test, the old implementation accepted every request. The fixed service accepted 20 and rejected 980 within the same simulated minute. The transport separately caps each request at 16,384 bytes. A new process resets the limit, so this is not a distributed quota or complete denial-of-service defense.

I also tried a caller-supplied principal, a SQL-like identifier, a URL-shaped identifier and an unknown write tool. None caused a business action or external request. The server exposes only `read_case`; it is a small MCP protocol implementation, not a claim of full ecosystem conformance.

The full assessment covers every OWASP 2023 category in `docs/owasp-assessment.md`, distinguishing tested controls from non-applicable surfaces and residual risks. Actual stdio responses are saved in `evidence/security.json`.

The RAG changes were evaluated separately. {summary} Security results do not contribute to these answer scores. Both types of evidence matter, but neither substitutes for the other.

Before production I would add authenticated multi-user sessions, persistent quotas, deployment hardening, dependency scanning, and adversarial prompt-injection evaluation. The vulnerable code stays confined to the test script.

Source: [OWASP API Security Top 10, 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/), read 2026-09-14. Evidence is limited to our own local system. Draft for author review; not published.
''',encoding='utf-8')
    refusals=[r for r in f['rows'] if r['must_refuse']]
    refusal_pass=sum(r['generation_pass'] for r in refusals)
    naive_pass=sum(r['generation_pass'] for r in b['rows'] if r['must_refuse'])
    transcripts='\n'.join(f"## {new['id']}\n\n{new['question']}\n\nBaseline:\n```text\n{old['actual']['answer']}\n```\nBaseline error: `{old['actual'].get('error')}`\n\nImproved:\n```text\n{new['actual']['answer']}\n```\nImproved error: `{new['actual'].get('error')}`\n" for old,new in zip(b['rows'][40:],f['rows'][40:]))
    (ROOT/'posts/04-refusal-as-a-feature.md').write_text(f'''# Refusal as a feature: the test case everyone skips

The fictional support team should not invent a bank account, live stock count or future price merely because a customer asks. Its knowledge base contains policies, not those facts.

On the ten must-refuse cases, the baseline passed {naive_pass}/10 and the improved system passed {refusal_pass}/10. These are actual local model-pipeline results. A refusal in the improved retrieval guard can happen before model generation, so it uses zero model tokens. An execution error is always a failed answer, never a successful refusal.

The improved path rejects unsupported queries and requires source citations for answers. This makes uncertainty visible, but citations alone do not establish truth. The lexical coverage guard can over-refuse a legitimate paraphrase or accept a misleading query made entirely from known words. It needs separate adversarial and paraphrase tests.

The transcripts below preserve all ten cases. Where the baseline refuses or fails instead of confidently hallucinating, that is what happened; the evidence should not be rewritten to fit the assignment's expected story.

{transcripts}

{summary}

Grounding requires matching each claim to evidence, not attaching a plausible filename. A release gate should measure unsupported answers and useful-answer coverage together. Zero unsupported answers achieved by refusing everything would not satisfy the customer.

Evidence: saved per-question results in `evidence/final-baseline` and `evidence/final-improved`. Draft for author review; not published.
''',encoding='utf-8')
    (ROOT/'posts/05-retrospective.md').write_text(f'''# What this build revealed about proving trustworthiness

Draft retrospective for the intern to review and personalize. This describes the recorded build, not a claim about personal beliefs or meetings that never happened.

The first mistaken implementation assumption was that asking a small model to return JSON would make its output reliably parseable. The initial live run produced malformed or incorrectly shaped responses. An explicit JSON schema corrected the transport contract in a smoke test, and both baseline and improved runs were repeated with that same schema. The failed run remains in the evidence folder.

The second mistaken assumption was that source-ID recovery meant the useful evidence had reached generation. The naive agent sometimes recovered the correct ID while splitting its sentence at a 95-character boundary. That is a retrieval-content defect even when the source-ID metric passes. A future suite should score evidence spans as well as document IDs.

{summary}

The fixture check also revealed another limit: the improved retriever can include unrelated service plans. Keyword grading detects some contaminated answers but does not comprehensively identify irrelevant or false extra claims. A fluent contradiction containing all required words may pass. The suite does not cover multilingual questions, semantic prompt injection, multi-turn state, or real user distributions.

Next I would commission independently authored questions, calibrate a blinded human review sample, add evidence-span recall and claim-level precision, and measure the cost of unnecessary refusals. Repeated runs with a model digest would quantify variance instead of treating temperature zero as a guarantee.

The security work found and fixed object-ownership and request-quota defects. It also demonstrated why a local process principal is not a production authentication system. The setup gate still requires an actual second person and a clean machine; an automated rerun cannot replace that evidence.

The project delivers a reusable golden set, adapter-based harness, local model integration, MCP tests, versioned policy reading and trace aggregation. Portfolio publication and the team's combined deck need human follow-through. No review, sign-off or submission is claimed here.
''',encoding='utf-8')
    (ROOT/'evidence/results-summary.md').write_text('# Measured results\n\n'+summary+'\n\n'+ '\n'.join(f"- {c}: baseline R {sum(r['retrieval_pass'] for r in b['rows'] if r['category']==c)}/10, G {sum(r['generation_pass'] for r in b['rows'] if r['category']==c)}/10; improved R {sum(r['retrieval_pass'] for r in f['rows'] if r['category']==c)}/10, G {sum(r['generation_pass'] for r in f['rows'] if r['category']==c)}/10." for c in ['easy','synthesis','conflict','stale','must_refuse'])+'\n',encoding='utf-8')
    print(summary)
if __name__=='__main__': main()

