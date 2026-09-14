# OWASP API Security Top 10 assessment

Scope: our own local MCP stdio process and two synthetic case records. Version: MCP 2025-06-18. Assessment date: 2026-09-14. Evidence: `evidence/security.json`; regression suite: `tests/test_lab.py`. No remote systems were tested.

| OWASP 2023 item | Applicability, test, result and remaining limit |
|---|---|
| API1 Object authorization | Applicable. Archived fixture returns case-b to analyst-a. Served implementation checks owner and returns `Case unavailable`. Actual stdio response id 2 confirms denial. |
| API2 Authentication | The OS process owner configures LAB_PRINCIPAL. Missing/unknown principals fail startup; request parameters cannot change identity. This is local process isolation, not network authentication. A process owner can launch another identity; remote/multi-user hosting requires real identity verification. |
| API3 Property authorization | Archived fixture leaks private_note. The fix projects only case_id and summary. Response id 1 contains only those fields. Extra principal parameter rejected in id 5. |
| API4 Resource consumption | Archived fixture accepts 1,000/1,000 calls. Fixed service accepts 20 and rejects 980 in one simulated minute. Transport caps a line at 16,384 bytes. Rate-window expiry is tested. Restarting the process resets the quota; no claim of distributed protection. |
| API5 Function authorization | Only read_case is exposed. delete_case fails with `Unknown tool` in response id 3. No write/admin function exists. |
| API6 Sensitive workflows | No purchases, reservations or business state mutations exist. Reads still allow scraping, bounded per process by the API4 control. Business workflow abuse assessment is limited by this deliberately small surface. |
| API7 SSRF | No URL-fetching tool exists. URL-looking case ID returns `Case unavailable` (response id 4). Model endpoint is fixed to loopback in source. No DNS or remote network request is made by read_case. |
| API8 Misconfiguration | Stdio has no listening network port. Invalid JSON and oversized lines return bounded errors; no stack trace is sent to clients. Container services bind to loopback. Dependency and host OS security remain outside these tests. |
| API9 Inventory | tools/list advertises the sole read_case tool and schema; unknown methods fail. initialize reports server 1.0.0 and protocol 2025-06-18. No HTTP legacy/debug routes exist. |
| API10 API consumption | read_case uses owned in-memory data, so no third-party dependency exists in this tool. The separate Ollama adapter limits response bytes, checks JSON types, and validates improved-mode citations. Live adversarial model-output testing remains required; schema checks alone do not establish grounding. |

Injection: SQL-like and traversal-like identifiers are dictionary lookups and fail. No SQL, shell, eval or path interpolation is used. This does not test semantic prompt injection into the model; that needs an additional adversarial corpus and grader.

Two primary weaknesses reproduced and fixed: missing object ownership and unbounded request frequency. Excessive property exposure was also fixed. The before-fix object exists only in `scripts/security_evidence.py`; it cannot be selected by the actual server CLI.

Source: [OWASP API Security Top 10, 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/), read 2026-09-14. This is a small lab assessment, not certification or a complete penetration test.
