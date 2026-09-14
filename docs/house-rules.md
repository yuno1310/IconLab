# House rules

Technical reading of public documents, not legal advice. Prepared 2026-09-14 (Asia/Bangkok). Circulation to the team is pending.

1. Use our local code and generated documents. Never connect this lab to a client, colleague, or production system, including for read-only work. The program restriction is stricter than any general product permission.
2. Use no customer information, including anonymized customer data. Trace payloads and demos must remain synthetic. Keep secrets out of Git, screenshots, posts, and videos.
3. Before any future SAP project, identify each API, its documented purpose, permissions, quotas, and the applicable architecture. Owning an account alone does not establish permission for a particular access pattern.
4. SAP API Policy **v.4.2026a**, read **2026-09-14**, section 2.2.2 restricts agent-driven call sequences outside the applicable endorsed pathways. Section 3 also prohibits bypasses through wrappers or intermediaries.
5. SAP API Policy FAQ **v1.3, June 2026**, read **2026-09-14**, Q23/Q27/Q31 preserves conditional use of customer-developed interfaces. This does not authorize circumvention or remove requirements on downstream SAP API calls.
6. FAQ **v1.3**, Q35 names MCP Gateway on Integration Suite, SAP-provided MCP through Joule Studio, and A2A. Q56 permits third-party/custom MCP subject to the agreement, documentation and controls. Q39 has narrower wording: obtain case-specific clarification before treating a custom MCP architecture as approved.
7. Only test the lab's own isolated tool process. Keep the vulnerable fixture outside the served implementation. Review all business actions manually; this lab exposes only synthetic case reads.
8. Save source version, publication date, reading date, URL and file hash. A stable FAQ URL does not prove unchanged contents. Recheck before external use.

Sources and checksums: [source register](sources.md). Supervisor review and distribution are still required.
