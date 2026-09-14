# What SAP's API policy on AI agents actually prohibits

**Technical reading of public documents, not legal advice. Read on 2026-09-14.**

SAP API Policy **v.4.2026a**, section 2.2.2, restricts AI systems that plan, select or execute API call sequences unless they operate through the relevant endorsed architectures and within their limits. Section 3 prevents evasion through proxies, gateways or custom code. A wrapper changes the route, not the obligation.

The distinction matters for customer code. FAQ **v1.3, June 2026**, Q23, Q27 and Q31 describes conditional permission for customer-namespace interfaces, including custom ABAP, OData and RFC services. Their underlying calls must still comply. Calling an interface custom does not establish that its use is permitted.

FAQ **v1.3**, Q35 identifies MCP Gateway on SAP Integration Suite, SAP-provided MCP servers through Joule Studio, and A2A as agentic pathways. These are the named examples, not a promise that the lab has access to them. Our lab uses generated documents and no SAP endpoint.

There is an important nuance in **v1.3**: Q39 favors the Integration Suite MCP Gateway over customer-operated MCP for enterprise access, while Q56 explicitly permits third-party/custom MCP when the agreement, documentation and API controls are satisfied. I would preserve both passages in an architecture review and ask SAP for guidance on a concrete design, rather than assert either a blanket ban or blanket permission.

The FAQ at the program's download URL resolved to **v1.3, June 2026**, on **2026-09-14**. The file contains 56 questions. A URL without a version and reading date would hide this distinction. Record the hash as well, because content can change at the same address.

For this internship, the decision is straightforward: generated data, an owned local server, and no client systems. The program's own rule remains the boundary even if a broader product policy permits another arrangement.

Sources: [SAP policy v.4.2026a](https://help.sap.com/doc/sap-api-policy/latest/en-US/API_Policy_latest.pdf), [SAP FAQ landing page](https://www.sap.com/documents/2026/04/e2a0665e-4c7f-0010-bca6-c68f7e60039b.html), [official FAQ download](https://d.dam.sap.com/x/UL9AiqH?doi=SAP1307757). All read 2026-09-14. See `docs/sources.md` for the content fingerprint. Draft for author review; not published.
