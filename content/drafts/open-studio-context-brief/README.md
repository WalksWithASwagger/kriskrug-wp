# Open Studio context-brief teaching packet

Draft for KK editorial acceptance. Issue [#981](https://github.com/WalksWithASwagger/kriskrug-wp/issues/981), transformation [#977](https://github.com/WalksWithASwagger/kriskrug-wp/issues/977). Method version: **0.1-draft**. No application code or WordPress payload is included. Drafting approval does not approve this wording or publication.

- [copy.md](copy.md): invitation, six questions/help, fictional teaching example and interface wording.
- [worksheet.md](worksheet.md): blank, printable Markdown artifact without an email gate.
- [evaluation.md](evaluation.md): five-person comparison and follow-up protocol; not executed.

## Source ledger

Public readback verified on 2026-09-06 through unauthenticated WordPress REST GETs. No private notes or participant material were used.

| Source | Verified evidence | Use and limit |
|---|---|---|
| [North House article, post 12744](https://kriskrug.co/2026/09/03/what-i-showed-founders-about-ai-workflows/) | Slug `what-i-showed-founders-about-ai-workflows`; modified GMT `2026-09-03T21:13:56`; featured media 12742. Sections “The whole workflow is one habit” and “One challenge to take home” describe a project home, gathering context and using an assistant. | Grounds the opening paragraph. The six-question method and example are new teaching material. No speed, productivity, participant-success or economic claims are adopted. |
| [Tracked article source](../2026-09-02-north-house-show-and-tell/post.md) | Corresponding workflow sections agree in substance with the public readback. Folder date differs from public publication date. | Traceability only; current public URL uses September 3. This packet does not replace the article. |
| [Public photograph, media 12742](https://kriskrug.co/wp-content/uploads/2026/09/kris-krug-north-house-show-and-tell-2026.jpg) | Public media metadata identifies the workshop photograph used by post 12744. Alt text: “Kris Krüg speaking to founders at North House in Vancouver, with the Futureproof Festival speaker page on the screen behind him”. | Approved source reference for the later proof. No photo is copied into this packet. Never use it as evidence that the fictional photo walk occurred or identify additional people from it. |
| [Design brief #403](https://github.com/WalksWithASwagger/kriskrug-wp/issues/403) | Existing identity and practical interaction constraints carried in the approved blueprint. | Short task language, no invented spatial labels or decorative interaction requirement. |

## Handoff boundaries

The proposed application uses six fixed questions and explicit exports. It must preserve missing answers, render visitor input literally and pass the complete privacy/fallback checks in #982/#983. Do not promise tested browser-only privacy from this draft alone. Method version belongs in the artifact footer; graduate from draft only when KK accepts the exact copy commit.

The example is wholly fictional, including its assumed sources. It is not a quotation or reconstructed North House exercise. Review its disclosure alongside the example wherever displayed. The blank worksheet intentionally excludes the guided help/example so the comparison condition remains distinct.

## Validation and pending review

Baseline before this packet: `make voice-check PYTHON=python3` passed (166 files, zero new violations, 214 existing waivers); `make docs-truth-check` passed. The Python override uses the system interpreter because the isolated worktree has no copied venv; these checkers use the standard library.

Post-draft validation: both checks passed (default voice scan: 167 files, zero new violations, 214 existing waivers). Explicit scanning of all four packet files passed with zero violations and zero waivers. Relative links resolve and manual source assertions were checked against public readback. `git diff --check` passed; repeat on the staged diff before commit. `copy.md` is covered by the default scanner's `PAYLOAD_NAMES`; explicitly verify membership so a quiet check is not mistaken for coverage. No waiver is requested.

Manual plain-Markdown review checked heading order, six matching fields, the visible example disclosure, blank responses, and footer links. Actual desktop/mobile rendered review is pending a preview; plain-text review does not establish responsive application behavior. No visitor tests have run and no outreach is authorized by this packet.

KK must accept the exact wording before it becomes approved public copy. #982 may consume it only in accordance with that issue's editorial gate. #983 owns later application/user evidence. No production rollback applies; revert or supersede the four draft files if the packet is rejected.
