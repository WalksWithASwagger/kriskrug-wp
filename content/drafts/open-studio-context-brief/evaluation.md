# Context-brief observation protocol

Status: proposed protocol, not executed. No participants recruited, contacted or tested. KK editorial acceptance and approval of any recruitment or external messages remain required. Issue #981; application evaluation belongs to #983.

## Question and hypotheses

Does the guided exercise help someone produce a more usable brief than the article and a blank worksheet alone?

Proposed targets, currently unmeasured:

- At least 4 of 5 visitors produce a usable brief in the guided condition within ten minutes, without facilitator help.
- At least 3 of 5 subsequently use their own brief on a real task within seven days.

Five observations provide directional evidence, not a population estimate or proof of conversion impact. Report raw counts and order effects, not statistical significance.

## Participants and consent

Seek five adults resembling the intended audience: creative professionals, founders or community organizers with a concrete work task. Include phone and desktop users, and record accessibility/input needs without collecting medical details. They need not be AI experts. Exclude authors of the exercise from the five.

A human owner obtains consent for observation and separately for follow-up. No recordings by default. Explain that participation is optional, they can stop, and fictional or non-sensitive tasks are welcome. Never ask for passwords, private client documents or sensitive participant information. Use participant codes P1 to P5. Store any approved notes in a restricted location, not this repository or a public PR. Retain only aggregate outcomes in public evidence; agree the private retention/deletion date before recruitment.

## Materials and counterbalancing

Freeze the article URL/readback date, packet commit, method version and application commit before testing. Condition A supplies the article plus worksheet.md. Condition B supplies the same article plus the guided exercise using copy.md, including its teaching example. Neither condition uses a model. This compares the whole guided experience, not an isolated prompt.

Give everyone the same short article-reading period before timed work; do not count it as brief completion time. Each participant performs two distinct, comparable brief tasks, ten minutes each. Use the four sequences below for P1 to P4; assign P5's sequence before observing outcomes. Record it. Task learning cannot be eliminated in this small crossover; analyze the first condition separately as a check.

| Participant | First condition/task | Second condition/task |
|---|---|---|
| P1 | A / X | B / Y |
| P2 | B / X | A / Y |
| P3 | A / Y | B / X |
| P4 | B / Y | A / X |
| P5 | A / X | B / Y |

Synthetic task X: prepare a brief for a one-page introduction to a fictional community repair session. Available: approved list of repair activities and venue description. Missing: event date and access confirmation. Audience: first-time adult attendees. Organizer must verify details and approve publication. Do not include participant contacts or unapproved pictures.

Synthetic task Y: prepare a brief for a one-page introduction to a fictional community seed exchange. Available: approved list of seed categories and venue description. Missing: event date and access confirmation. Audience: first-time adult attendees. Organizer must verify details and approve publication. Do not include participant contacts or unapproved pictures.

Both tasks require plain language, a maximum 250-word final invitation and visible unresolved facts. Supply these facts identically in A and B. Ask for a brief to commission the invitation, not the invitation itself. Pilot timing and clarity with an internal reviewer outside the five; freeze any changes before the cohort begins. Do not show the fictional photo-walk example in A.

## Session procedure

1. Explain consent, task and controls without teaching the six-field answers.
2. Read the article, then begin the assigned condition. Start the timer when the task and materials are visible.
3. Say: “Prepare a brief someone could use to draft this invitation. Save a copy you could use later. You have ten minutes. Say when you think it is ready.”
4. Observe silently. Log navigation obstacles, requests for help, export outcome and elapsed time. Do not rescue an answer. If assistance is essential for safety or access, provide it and mark the run assisted; do not count it as unassisted completion.
5. Stop at ten minutes; preserve unfinished status honestly. Collect only a consented, sanitized artifact for rubric review.
6. Run the other task/condition without explaining rubric gaps from the first.
7. Ask what was unclear, what they would change before using the brief, and whether they understood its limits. Do not ask a leading satisfaction question.
8. Offer an optional own-task attempt after timed comparison. It does not replace a failed timed run. With separate consent, ask at seven days whether they actually used that own-task brief, what for, and what they changed. No reply counts as unknown, not success. The real-use target cannot be met by exporting a synthetic task alone.

## Usable-brief rubric

Two reviewers independently assess artifacts without seeing the condition label where practical. Score each dimension 0 (absent, invented or unusable), 1 (present but vague/incomplete), or 2 (specific enough to act on). Resolve disagreements with an evidence note; retain both original scores. No model scoring.

| Dimension | Score 2 requires |
|---|---|
| Objective | Concrete deliverable and scope; commissioning the invitation rather than pretending it is published |
| Audience | Identified intended readers and what the result helps them do |
| Source availability | Available sources distinguished from missing facts; no invented date/access claim |
| Done conditions | Observable format/content checks, including the word limit and unresolved facts |
| Boundaries | Explicit sharing/action exclusions; no private contacts or unauthorized publication |
| Human review | Named role and specific checks/approval before sharing |

Usable means all six dimensions score 2, with no unsafe sharing or invented missing facts. Report partial scores as well; do not weaken this definition after seeing results. An honest missing fact with a next check can satisfy source availability; an empty field cannot. This research rubric is not a product quality score shown to visitors.

## Report and decision

Report per condition: n attempted, usable within ten minutes, assisted runs, export failures, median observed time with unfinished runs identified, per-dimension scores, and first-condition/order effects. Record accessibility blockers separately. For follow-up report actual use / no use / unknown out of all five, plus consent coverage.

Proceed toward a second practice only after editorial review and evidence that guided artifacts resolve meaningful gaps beyond A. If 4/5 completion is missed, fix the observed problem and run a fresh cohort without combining results to disguise failures. If both conditions perform equally well, prefer the simpler worksheet unless another observed benefit justifies the interface. Do not claim the 3/5 real-use target until follow-up actually occurs. Publication, privacy verification and live rollback remain separate gates.

## Blank observation and scoring sheets

Use these sheets only after the consent/storage checkpoint. Copy blank templates into the approved private location; do not fill this repository with real observations. The preflight freezes versions; confirm the same method/copy/application for every run.

Before recruitment, the human owner fills: protocol/version ___; facilitator ___; second reviewer ___; restricted storage location ___; access list ___; identity-key location (separate) ___; retention/deletion date ___; consent wording/version ___. Suggested operational retention is 30 days after the final follow-up, subject to the owner's recorded decision before consent. Do not collect data without a fixed retention decision.

| Code | Observation consent/date | Optional follow-up consent | Adult/audience fit confirmed | Device/input needs (no medical detail) | Withdrawal/deletion handled |
|---|---|---|---|---|---|
| P1 | | | | | |
| P2 | | | | | |
| P3 | | | | | |
| P4 | | | | | |
| P5 | | | | | |

Consent script for owner review: “This compares two ways to prepare a work brief. Taking part is optional; you can stop or skip a question. Use the fictional task and leave out personal or client information. We will record coded observations and, only with your permission, a sanitized brief. We will not record audio or video. Agreeing to this session does not agree to a later follow-up. The owner will explain where notes are kept and when they are deleted before you decide.” This is a proposed script, not evidence that consent occurred.

P5 is preassigned **A / X then B / Y**, before any outcomes. Preserve P1–P4's existing sequence. The small sample has three A-first and two B-first participants; report that imbalance rather than describing perfect counterbalancing.

| Code/run | Condition/task | Start / finish or timeout | Elapsed seconds | Assisted? Why? | Export outcome | Sanitized artifact code | Observed obstacle |
|---|---|---|---|---|---|---|---|
| P1/1 | A / X | | | | | | |
| P1/2 | B / Y | | | | | | |
| P2/1 | B / X | | | | | | |
| P2/2 | A / Y | | | | | | |
| P3/1 | A / Y | | | | | | |
| P3/2 | B / X | | | | | | |
| P4/1 | B / Y | | | | | | |
| P4/2 | A / X | | | | | | |
| P5/1 | A / X | | | | | | |
| P5/2 | B / Y | | | | | | |

For each coded artifact, make two independent copies of this score row. Hide the condition label from reviewers where practical; join it only for analysis. Record original scores and any reconciliation note.

| Artifact code | Reviewer code | Objective 0–2 | Audience 0–2 | Sources 0–2 | Done 0–2 | Boundaries 0–2 | Human review 0–2 | Unsafe sharing/invented facts? | Evidence/reconciliation |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

A run counts toward the ten-minute target only when it is unassisted, within ten minutes, all six final dimensions score 2, and no unsafe sharing or invented missing facts are present. Missing or unscored observations are unknown; they are never passes.

| Code | Own-task attempt offered/accepted | Separate follow-up consent | Due date | Follow-up status/date | Actual use / no use / unknown | What changed (sanitized) | Deleted on |
|---|---|---|---|---|---|---|---|
| P1 | | | | | | | |
| P2 | | | | | | | |
| P3 | | | | | | | |
| P4 | | | | | | | |
| P5 | | | | | | | |

Follow-up is handled only by an authorized human contact process. Do not create reminders that send participants messages. Ask about actual use of an own-task brief, not whether they liked the exercise. No response remains unknown out of the original five.

Public aggregate report template: frozen versions ___; dates ___; attempted A __/5 and B __/5; usable within ten minutes A __/5 and B __/5; assisted A __ and B __; unfinished A __ and B __; export failures A __ and B __; median observed time with timeout handling ___; dimension totals ___; A-first/B-first and first-condition findings ___; accessibility blockers ___; follow-up consent __/5; actual use __/5, no use __/5, unknown __/5; limitations ___; owner decision ___. Publish no contact key, raw answers, identifying quotes or participant-level combination that could identify someone. A blank template is not a result.
