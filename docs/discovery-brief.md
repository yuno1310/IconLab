# Discovery brief: Harbor Support Evidence Lab

Prepared 2026-09-14. Fictional customer and workflow assumptions; no interviews or sign-off claimed.

**Customer:** Harbor Devices, a fictional equipment distributor with 20 support analysts handling an assumed 800 policy questions each week across ten service plans.

**Users:** support analysts need cited answers; a support lead reviews uncertain cases; an evaluator maintains the evidence suite.

**Current workflow:** an analyst searches separate policy, escalation, and bulletin files, selects a rule, and copies it into a ticket. Old policies remain searchable. Two regional bulletins occasionally disagree. Analysts cannot readily tell whether a fluent answer reflects current evidence.

**Pain:** a confident unsupported answer can promise a refund or response time that the company cannot meet. Searching faster alone does not solve the trust problem.

**Systems:** generated Markdown knowledge base, local Python retrieval application, local Ollama model endpoint, local Langfuse tracing, a read-only MCP tool surface, and a reusable evaluation CLI. No SAP connection is needed.

**Constraints:** free tools, synthetic documents only, local processing, no autonomous ticket changes, no external security targets, and no real credentials in version control. The vulnerable implementation is test-only. Every model experiment must record its exact model digest and configuration.

**One success metric:** unsupported-answer rate on the ten held-out-in-name-only must-refuse questions: target 0/10 after changes. The set is authored with the corpus and is a development benchmark, not independent validation. A separate unseen set is needed before claiming generalization. Report useful-answer coverage alongside this metric to expose trivial always-refuse behavior.

**Scope:** retain an intentionally weak baseline, build a balanced 50-question suite, separate retrieval and answer scores, repair the system, and package reproducible evidence. Human analysts remain responsible for business decisions.

**Approval:** pending program supervisor review. Circulation and personal discovery interviews have not occurred.
