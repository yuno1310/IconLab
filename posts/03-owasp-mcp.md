# The OWASP API Security Top 10, aimed at an MCP server

A grounded answer is insufficient if its tool can read another user's case. I tested an owned local MCP stdio server over two synthetic support records.

The archived before-fix implementation looked up a case ID and returned its entire record. Analyst A could read analyst B's case, including its internal note. The fixed service derives identity from the local process, checks record ownership on each call, and projects only the public summary. The same attempted access now returns `Case unavailable`.

The second weakness was resource consumption. In a bounded 1,000-call test, the old implementation accepted every request. The fixed service accepted 20 and rejected 980 within the same simulated minute. The transport separately caps each request at 16,384 bytes. A new process resets the limit, so this is not a distributed quota or complete denial-of-service defense.

I also tried a caller-supplied principal, a SQL-like identifier, a URL-shaped identifier and an unknown write tool. None caused a business action or external request. The server exposes only `read_case`; it is a small MCP protocol implementation, not a claim of full ecosystem conformance.

The full assessment covers every OWASP 2023 category in `docs/owasp-assessment.md`, distinguishing tested controls from non-applicable surfaces and residual risks. Actual stdio responses are saved in `evidence/security.json`.

The RAG changes were evaluated separately. Actual local Qwen2.5 0.5B: baseline retrieval 30/50, generation 15/50; improved retrieval 50/50, generation 38/50. Errors: 2 baseline, 10 improved. Security results do not contribute to these answer scores. Both types of evidence matter, but neither substitutes for the other.

Before production I would add authenticated multi-user sessions, persistent quotas, deployment hardening, dependency scanning, and adversarial prompt-injection evaluation. The vulnerable code stays confined to the test script.

Source: [OWASP API Security Top 10, 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/), read 2026-09-14. Evidence is limited to our own local system. Draft for author review; not published.
