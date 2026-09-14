# Track D submission pack

The project is built and evaluated locally using free tooling and published at [yuno1310/IconLab](https://github.com/yuno1310/IconLab/tree/main). **The program is not fully signed off or submitted:** human review, independent reproduction and submission remain pending.

## Open first

- `docs/final-handoff.md`: publishing commands and the specific human acceptance gates.
- `output/evidence-review.html`: interactive comparison of all 50 recorded model answers, scores and security evidence. Open directly in a browser; no server is required.
- `output/decks/final-deck-ready.pptx`: final editable eight-slide deck.
- `output/videos/final-deck.mp4`: three-minute synthetic-voice evidence replay, with a companion transcript/subtitle file. It demonstrates saved actual runs, not a live screen recording or a human presentation.
- `README.md` and `SETUP.md`: project explanation and reproducibility instructions.

## What was measured

| System | Retrieval passes | Answer passes | Execution / validation errors |
|---|---:|---:|---:|
| Actual local model, naive | 30/50 | 15/50 | 2 |
| Actual local model, improved | 50/50 | 38/50 | 10 |

Errors count as failed answers. Ten must-refuse cases pass in the improved system. All ten security/regression tests passed. One hundred final model traces were re-exported from local Langfuse. These are synthetic development results, not a production-readiness claim.

## Assignment coverage

| Assignment | Prepared evidence | Remaining acceptance step |
|---|---|---|
| 1 | `docs/discovery-brief.md`, `docs/house-rules.md`, versioned sources | Supervisor sign-off and team circulation |
| 2 | `src/agent.py`, corpus, local Ollama, Langfuse traces | Reviewer demonstration acceptance |
| 3 | `golden-set.yaml`: 50 balanced questions | Published on GitHub |
| 4 | Policy post, assignment-04 deck and video | Author review and submission |
| 5 | Reusable harness and recorded baseline | Published on GitHub |
| 6 | Separate-scores post, assignment-06 deck and video | Author review and submission |
| 7 | SETUP.md and reproduction log | Actual second person on a clean setup |
| 8 | OWASP assessment, before/fix evidence and tests | Reviewer acceptance of documented scope |
| 9 | Improved run, security post, assignment-09 deck and video | Submission |
| 10 | All ten refusal transcripts, assignment-10 deck and video | Submission |
| 11 | Langfuse-exported latency, token totals, prior guesses and cost scenario | Review different-model price assumption |
| 12 | README, setup, reusable harness, final deck/video, archive | Clean-machine verification |
| 13 | Retrospective draft, assignment-13 deck/video, final team section | Personalize, contribute to team and submit |

## Files for the five submissions

For assignment numbers 04, 06, 09, 10 and 13, each `output/decks/assignment-NN-ready.pptx` has eight slides and each `output/videos/assignment-NN.mp4` has a three-minute narrated replay. Posts are numbered 01 through 05 in `posts/`. The consolidated final deck is `final-deck-ready.pptx`.

Use `docs/submission-message.md` for the published repository and snapshot tag. No message has been sent; personal review, meetings, sign-off and second-person reproduction remain pending.

## Running services

The dedicated `harbor-evidence-lab` Compose project has local Ollama and Langfuse, with PostgreSQL internal to Docker. `docker compose stop` pauses it; data volumes remain. The ignored `.env` holds local credentials. It is deliberately absent from the archive and Git. Generate new credentials when reproducing elsewhere.

The source PDFs are unchanged. The corpus is synthetic. See `docs/sources.md` for source versions and attribution, and `docs/build-log.md` for observed failures.
