# Final acceptance and publishing

The deliverables are prepared. Completion of the program still requires real human approvals and publication. A percentage is an estimate, not a verified acceptance result.

## Publish the prepared repository

`output/harbor-track-d.bundle` is a portable Git repository containing the reviewed submission files and the `submission-ready-v1` tag. The commit identifies the preparation tool as Codex; it does not impersonate the intern. This tag marks the completed preparation snapshot, not past assignment submissions.

Create an empty public repository in your own GitHub account, then run:

```powershell
git clone -b codex/track-d output/harbor-track-d.bundle harbor-track-d-publish
cd harbor-track-d-publish
git remote remove origin
git remote add origin https://github.com/YOUR-ACCOUNT/YOUR-REPOSITORY.git
git push -u origin codex/track-d
git push origin submission-ready-v1
```

Replace the example URL with the actual repository URL. Authenticate through GitHub's normal sign-in flow; do not paste tokens into chat. The bundle is delivered beside the ZIP to avoid embedding a repository inside itself. If using the ZIP alone, initialize Git in its extracted folder instead.

## Required human actions

| Gate | Evidence to supply | Current state |
|---|---|---|
| Supervisor approval | Name, date and actual approval of discovery brief and house rules | Pending |
| Team circulation/contribution | Actual team discussion or shared work reference | Pending |
| Independent reproduction | Reviewer completes `docs/reproduction-log.md` using `SETUP.md` | Pending |
| Authorship review | Intern checks and personalizes the retrospective | Pending |
| Presentation acceptance | Reviewer accepts synthetic narration/replay, or intern records required personal/live demos | Pending |
| Public repository | Published URL and accessible submission tag | Pending |
| Submission | Actual destination and confirmation of receipt | Pending |

Use `docs/submission-message.md` after filling these real details. Automated tests and an isolated extracted-copy check support readiness but cannot substitute for a second person's review.
