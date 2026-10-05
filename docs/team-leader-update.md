# Progress update — 2026-10-05

Ready-to-use summary based on the recorded work:

I prepared a solo RAG evaluation project with free local tooling and synthetic data. The project includes a 50-question golden set, separate retrieval and answer scoring, local Ollama integration, exported Langfuse traces, an MCP security assessment, and a reusable harness. The code, five posts, six decks and six narrated evidence replays are published on GitHub.

In the recorded local-model comparison, retrieval improved from 30/50 to 50/50 and answer passes improved from 15/50 to 38/50. All ten must-refuse cases passed in the improved run. The remaining answer failures are preserved in the evidence.

The main challenges were malformed model responses, invalid citations, stale or conflicting source material, and misleadingly good source-ID scores when chunked evidence was incomplete. I addressed these with schema constraints, citation checks, paragraph-preserving chunks, reranking, newest-version filtering and a refusal path. The suite also exposed limits: keyword grading can miss false extra claims, and a small local model remains unreliable on some cases.

The delivery pack is ready for personal review and submission. Automated checks support reproducibility; independent human reproduction and formal acceptance have not been claimed.
