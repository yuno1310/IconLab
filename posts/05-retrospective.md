# What this build revealed about proving trustworthiness

Draft retrospective for the intern to review and personalize. This describes the recorded build, not a claim about personal beliefs or meetings that never happened.

The first mistaken implementation assumption was that asking a small model to return JSON would make its output reliably parseable. The initial live run produced malformed or incorrectly shaped responses. An explicit JSON schema corrected the transport contract in a smoke test, and both baseline and improved runs were repeated with that same schema. The failed run remains in the evidence folder.

The second mistaken assumption was that source-ID recovery meant the useful evidence had reached generation. The naive agent sometimes recovered the correct ID while splitting its sentence at a 95-character boundary. That is a retrieval-content defect even when the source-ID metric passes. A future suite should score evidence spans as well as document IDs.

Actual local Qwen2.5 0.5B: baseline retrieval 30/50, generation 15/50; improved retrieval 50/50, generation 38/50. Errors: 2 baseline, 10 improved.

The fixture check also revealed another limit: the improved retriever can include unrelated service plans. Keyword grading detects some contaminated answers but does not comprehensively identify irrelevant or false extra claims. A fluent contradiction containing all required words may pass. The suite does not cover multilingual questions, semantic prompt injection, multi-turn state, or real user distributions.

Next I would commission independently authored questions, calibrate a blinded human review sample, add evidence-span recall and claim-level precision, and measure the cost of unnecessary refusals. Repeated runs with a model digest would quantify variance instead of treating temperature zero as a guarantee.

The security work found and fixed object-ownership and request-quota defects. It also demonstrated why a local process principal is not a production authentication system. The setup gate still requires an actual second person and a clean machine; an automated rerun cannot replace that evidence.

The project delivers a reusable golden set, adapter-based harness, local model integration, MCP tests, versioned policy reading and trace aggregation. Portfolio publication and the team's combined deck need human follow-through. No review, sign-off or submission is claimed here.
