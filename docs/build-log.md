# Build and failure log

- Initial PDF extraction stopped on a Windows encoding error: `UnicodeEncodeError: 'charmap' codec can't encode character '\u2192'`. Re-read with escaped Unicode and visually inspected all six source pages.
- Initial Docker check in the sandbox failed: `permission denied while trying to connect to the docker API at npipe:////./pipe/docker_engine`. An approved read outside the sandbox found Engine 29.7.2. The project's separate Compose stack then started successfully.
- SAP's landing-page PDF request returned Access Denied. The official redirected `d.dam.sap.com` URL succeeded and delivered FAQ v1.3, June 2026. No unverified older FAQ version was substituted.
- The first model baseline asked for generic JSON and produced 45 errors across 50 cases. See `evidence/baseline-ollama/results.json` for each verbatim error.
- Added a concrete JSON schema to both model variants. The paired schema run recorded 15/50 baseline and 37/50 improved answer passes.
- Added token accounting and raw output retention for validation failures. The final paired run recorded 15/50 baseline and 38/50 improved answer passes, with 2 and 10 errors respectively. Preserve the variation: temperature zero and a seed did not imply identical answer scoring across local runs.
- Final trace ingestion and API re-export succeeded for 100 actual model traces. API-exported observations supplied the latency/cost report.
- Deterministic fixture tests recorded 30/50 retrieval and 10/50 generation before changes, 50/50 and 48/50 after. These are not model results.
- The fixture's two remaining answer failures include unrelated plan policies. This is a known retriever contamination limit; it is documented rather than hidden by altering the golden answers.

The detailed machine-readable evidence is authoritative where a summary is rounded. No second-person reproduction, supervisor sign-off, public repository or external submission is claimed.
