# Source register

Read on 2026-09-14, Asia/Bangkok.

- Program rules: intern-program.pdf, user supplied, 2 pages.
- Track D: intern-program (1).pdf, user supplied, 4 pages. These are requirements, not authority to publish or claim human review.
- SAP API Policy v.4.2026a: https://help.sap.com/doc/sap-api-policy/latest/en-US/API_Policy_latest.pdf. Both pages read.
- SAP API Policy FAQ v1.3, June 2026, 21 pages, 56 questions: https://d.dam.sap.com/x/UL9AiqH?doi=SAP1307757. SHA-256: 080ec09161bdbf832404b174e661c787e8cca247338604ee5a058ad83e2d9f34. Relevant Q23, Q27, Q31, Q35, Q39, Q56 read. Do not infer a stable version from a stable URL. The primary landing page failed before the official redirect succeeded.
- OWASP API Security Top 10, 2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/.
- MCP transport specification 2025-06-18: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports.
- Ollama chat API: https://docs.ollama.com/api/chat. Exact runtime and model fingerprint recorded in evidence/.
- Langfuse local deployment: https://langfuse.com/self-hosting/deployment/docker-compose. Current docs describe v4. This resource-constrained local lab intentionally pins legacy v2.95.11 and verifies its ingestion/export API directly. Do not reuse this legacy deployment in production.

## Starting-point credit

The task design comes from the two supplied PDFs. Their references credit Hector Enriquez (policy), Mohan Sharma (evaluation), Onibex (hallucinations), Florian Okos (OWASP), Felix Sasaki (grounding), and Naveen Panakkal (reliability patterns). Their blog content has not been independently verified here. The code and synthetic corpus were newly authored with AI assistance, not copied from those posts.

The slide design is the selected OpenAI Operating Review template. The original template is unchanged.
