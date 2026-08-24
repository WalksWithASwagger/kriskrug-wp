# AI Policy Source Matrix

This matrix supports the draft in `policy.md`. It separates sourced principles and observed local practice from proposed commitments that still require Kris Krüg's review. It is editorial evidence, not a claim that every external policy applies to KrisKrug.co.

## Status legend

| Status | Meaning |
| --- | --- |
| External principle | A transferable idea from a public policy. Language was adapted, not copied. |
| Local practice evidence | A repo or KrisKrug.co source showing current practice or an existing refusal line. |
| Proposed policy | A rule drafted for this page that requires Kris's approval before it becomes a public commitment. |
| Unresolved human decision | A threshold, wording choice, or operational promise Kris must confirm. |

## External research

| ID | Source | Principle used | Adaptation and limits | Draft sections |
| --- | --- | --- | --- | --- |
| E01 | [Lara Kroeker Interactive, “My AI policy, the real version”](https://larakroekerinteractive.com/ai-guidelines/) | Name actual uses, explain workflow in plain language, distinguish scoped structured access from blanket access, publish an update date, and invite questions. | Used as the launching tone and specificity model. Rejected Lara's claims that the idea begins with her before AI and that she does not scrape sites because neither accurately describes Kris's broader workflow. No sentence was copied. | “I use AI a lot”; “Agents get lanes”; update line; closing invitation |
| E02 | [Associated Press, updated newsroom AI standards, July 23, 2026](https://www.ap.org/the-definitive-source/announcements/ap-updates-newsroom-standards-for-artificial-intelligence/) | AI can assist research, summaries, transcription, translation, headlines, search support, and code while editorial judgment, verification, and accountability stay human. Material AI use should be disclosed, and synthetic news photography is prohibited. | Adapted the verification, materiality, and documentary distinctions. Kris is not adopting a newsroom ban on generated imagery or AI-written copy. | “Facts need receipts”; “What I will not fake”; “Synthetic media and disclosure”; “I own what ships” |
| E03 | [The Guardian's approach to generative AI](https://www.theguardian.com/help/insideguardian/2023/jun/16/the-guardians-approach-to-generative-ai) | Require human oversight, a specific benefit for significant use, transparency with audiences, attention to bias, and respect for creator permission and fair reward. | Adapted as a benefit-and-harm test and creator-respect principle. The Guardian's editorial approval structure is not represented as Kris's workflow. | “Creators are not a moodboard vending machine”; “Cost is part of the prompt”; “I own what ships” |
| E04 | [WIRED, “How WIRED Will Use Generative AI Tools”](https://www.wired.com/about/generative-ai-policy/) | Treat AI research as pointers that must be checked against original sources; distinguish brainstorming from publishing; disclose generated imagery and reject obvious imitation or infringement. | Adapted the original-source and visual-disclosure tests. Rejected WIRED's ban on AI-written and AI-edited editorial copy because full drafts are part of Kris's practice. | “Facts need receipts”; “Creators are not a moodboard vending machine”; “Synthetic media and disclosure” |
| E05 | [Government of Canada guide on generative AI](https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/responsible-use-ai/guide-use-generative-ai.html) | Risk depends on use and controls. The FASTER framework covers fairness, accountability, security, transparency, education, and relevance. Public tools and secured systems have different privacy boundaries. Bias, hallucinations, energy, water, labour, and hardware costs need consideration. | Adapted into a personal risk-tiering and data-minimization practice, not government compliance language. The federal prohibition on personal information in public tools informed the boundary but is not presented as legal advice to Kris. | “Private means private”; “Facts need receipts”; “Agents get lanes”; “Cost is part of the prompt” |
| E06 | [Mangrove Web AI Policy](https://mangrove-web.com/ai-policy/) | Disclose AI's role in drafting the policy, protect client material in approved secured systems, avoid identifiable creator imitation, weigh cultural, social, labour, and environmental costs, and admit the policy will need correction. | Adapted the meta-disclosure and humility. Avoided its absolute “human-led” framing because Kris may use agents for complete first passes and bounded execution. | Proposed disclosure; “Creators are not a moodboard vending machine”; “Cost is part of the prompt”; “I own what ships” |
| E07 | [A Great Idea, Ethical AI Policy for Mission-Driven Communications](https://www.agreatidea.com/ai-policy) | Protect lived experience and relationship-based collaboration, fair labour, original craft, and higher-care contexts such as identity, health, and safety. Acknowledge embedded AI features in ordinary software. | Adapted the relationship, labour, sensitivity, and embedded-feature principles. Did not copy the agency's narrower “light production support” use case. | “What has to be real first”; “Private means private”; “Cost is part of the prompt” |
| E08 | [Buffer, creator AI-policy examples](https://buffer.com/resources/ai-content-policy/) | A short, specific explanation of actual uses and refusals can build audience understanding. Different creators draw different lines. | Used as a readability contrast. Rejected the example restriction against AI drafting because it would misstate Kris's practice. | Whole-page structure; “I use AI a lot” |

## Local practice and voice evidence

| ID | Source | Evidence | Adaptation and limits | Draft sections |
| --- | --- | --- | --- | --- |
| L01 | `content/drafts/2026-05-21-i-wont-fake-the-people-who-showed-up/post.md` | Kris's documentary line permits AI around the frame but refuses synthetic people, attendance, community, ceremony, evidence, and witness. It develops “Presence Is Provenance” and the art-adjacent-work principle. | This is Kris's draft writing, not an external policy. The public policy condenses its refusal lines and keeps illustration separate from documentary evidence. Publication status remains draft, so the matrix treats it as local practice evidence rather than a public promise already in force. | “What has to be real first”; “Send the machines”; “What I will not fake” |
| L02 | `content/drafts/2026-05-21-speak-it-into-existence-ai-voice-first-workflows/post.md` | Names agents researching, comparing, drafting, refactoring, sorting, testing, building, checking, and updating. States that agents do bounded work while the human decides what ships and owns the consequences. | Supports the actual-use list and agent model. It does not prove every workflow meets every proposed privacy or disclosure rule. | “I use AI a lot”; “Agents get lanes”; “I own what ships” |
| L03 | `content/drafts/2026-06-04-ai-keynote-slides-visual-workflow/post.md` | Shows generated visual experimentation, provenance from note to prompt to artifact, explicit selector review, rejection of generic output, and the continued value of real photographs as evidence that an idea lived in a room. | Supports honest acknowledgement of generated imagery and the candidate-versus-evidence distinction. It does not establish a site-wide disclosure convention, which remains a human decision below. | “Send the machines”; “What has to be real first”; “Synthetic media and disclosure” |
| L04 | `content/drafts/pillars/ai-ethics-philosophy.html` | Frames Kris's approach as holding capability and critique together while working through power, bias, consent, sovereignty, and obligations to each other. | Supports the Both Hands Full framing. The draft adds operational commitments that the hub itself does not contain. | “The short version”; “Cost is part of the prompt” |
| L05 | [`https://kriskrug.co/robots.txt`](https://kriskrug.co/robots.txt); `fixes/robots.txt` | Public AI and search crawlers are intentionally allowed for discovery and citation while admin and search routes remain disallowed. | Public readback on 2026-08-23 confirmed the same directive stance. Its `Last reviewed` comment says 2026-06-07 while the repo source says 2026-07-01, so the comments drift even though the allow/disallow rules support the policy claim. Crawler access does not settle copyright, attribution, imitation, or context questions. | “Creators are not a moodboard vending machine” |
| L06 | `AGENTS.md`; `docs/current-state/INCIDENT-2026-05-15-overwritten-post.md`; `docs/current-state/ACCESS_CHANNELS.md` | Repo rules require dry-runs, exact slug and ID checks, reversible steps, and human approval for risky live changes after a real overwrite incident. | Supports specific agent gates for this site. These operational rules do not prove the same controls exist in every external tool Kris uses. | “Agents get lanes, not the keys to everything” |
| L07 | `content/drafts/2026-05-21-speak-it-into-existence-ai-voice-first-workflows/post.md`; `content/drafts/2026-06-04-ai-keynote-slides-visual-workflow/post.md`; this repo's agent workflow | Current materials explicitly include complete drafting, source work, code, tests, archive operations, visual generation, and bounded agent execution. | Supports the non-cute actual-use list. “Accessibility work” is phrased as support and candidates, not a claim that AI independently validates accessibility. | “I use AI a lot” |

## Proposed policy and unresolved decisions

| ID | Status | Proposed claim or question | Evidence or reason | Human gate |
| --- | --- | --- | --- | --- |
| P01 | Proposed policy | Treat this as a public transparency statement rather than legal terms, a privacy promise, or a client contract. | Issue #883 architecture decision. | Confirm page scope before payload work. |
| P02 | Proposed policy | Use materiality as the disclosure test and label generated or materially altered photorealistic media near the artifact. | E02, E03, E04, E06 plus L01 and L03. | Kris must approve the threshold and examples. |
| P03 | Proposed policy | Permit sensitive material in a deliberately selected secured workflow after checking access, retention, training use, sharing, data location where relevant, authority, and purpose. | E05, E06, E07. This avoids the false claim that private material never enters AI. | Kris must confirm this matches current provider settings and client/student agreements. |
| P04 | Proposed policy | Reject prompts for a living creator's identifiable style and prefer owned, licensed, commissioned, or public-domain sources where practical. | E03, E04, E06, E07. | Kris must approve this as a durable refusal line. |
| P05 | Proposed policy | Keep public AI/search crawling enabled for discovery and citation while rejecting plagiarism, cloning, impersonation, unattributed reuse, and context removal. | L05 and issue #883. | Confirm this remains the intended crawler stance at publication time. |
| P06 | Proposed policy | Gate live, destructive, external-send, spending, sensitive-data, and high-human-stakes agent actions according to risk. | L02, L06, E05. | Confirm the list catches Kris's actual high-impact workflows. |
| P07 | Proposed policy | Consider labour, cultural, bias, energy, water, hardware, and community costs when choosing whether and how to use AI. | E03, E05, E06, E07, L04. | Approve as a decision practice, not a measurable carbon claim. |
| H01 | Unresolved human decision | Does substantial AI drafting of a public artifact require a disclosure every time, or only when authorship/context would materially change audience judgment? | Existing practice includes full drafts, but the repo does not show a consistent historical disclosure rule. | Decide before #885. Do not imply retroactive compliance. |
| H02 | Unresolved human decision | Should older generated or materially altered media be labelled retroactively, and if so which routes are in scope? | This draft defines a forward-looking rule but no inventory has been audited. | Out of scope for #884; file a bounded follow-up if desired. |
| H03 | Unresolved human decision | Which AI workspaces are verified for sensitive client, student, interview, or community material, under which settings? | No provider-by-provider security register was reviewed for this issue. | Required before naming any platform as approved. |
| H04 | Unresolved human decision | Is the “living creator's identifiable style” line the intended boundary, or should it cover deceased creators and named studios too? | Public comparison policies vary, and model provenance remains opaque. | Kris chooses the durable wording. |
| H05 | Unresolved human decision | Is the contact page the preferred route for corrections and policy challenges? | It is the current public owned contact route. | Confirm before publication. |

## Claim-level crosswalk

| Draft claim | Type | Support | Notes |
| --- | --- | --- | --- |
| Kris uses AI for research, transcription, synthesis, drafting, code, tests, archives, image work, and bounded agents. | Local practice evidence | L02, L03, L07 | Full first drafts are stated honestly; no “light assistance” fiction. |
| Real witness, collaborators, source material, and lived experience precede documentary claims. | Local practice evidence + proposed policy | L01, L02, P02 | Kris must approve the public commitment. |
| AI candidates do not become quotes, facts, citations, or code without source/test checks. | External principle + proposed policy | E02, E04, E05, L02 | “Every” is avoided because universal enforcement cannot be proven. |
| Public/unmanaged tools and secured workspaces have different data boundaries. | External principle + proposed policy | E05, E06, E07, P03 | No provider is named approved. |
| Public crawling is intentionally allowed for discovery and citation. | Local practice evidence | L05 | Must be rechecked at publication time. |
| Creator imitation, competitor cloning, unattributed reuse, and plagiarism are refusal lines. | External principle + proposed policy | E01, E03, E04, E06, P04, P05 | Public research itself remains permitted. |
| Synthetic illustration is permitted but documentary fabrication is refused. | Local practice evidence + proposed policy | L01, L03, E02, E04, P02 | Disclosure convention awaits approval. |
| Agents receive bounded scopes, tests, source trails, rollback paths, and human gates for high-impact actions. | Local practice evidence + proposed policy | L02, L06, P06 | Applies directly to this repo; broader workflow coverage should be confirmed. |
| Labour, cultural, environmental, bias, and power costs belong in tool choice. | External principle + local philosophy + proposed policy | E03, E05, E06, E07, L04, P07 | No quantitative footprint claim is made. |
| Lara Kroeker's policy launched this drafting process, and the comparison set includes AP, the Guardian, WIRED, Government of Canada, Mangrove Web, A Great Idea, and Buffer. | External research record | E01-E08 | Public links in the draft preserve credit and make the research trail inspectable. |
| Kris owns the decision, correction, and consequences of published work. | External principle + local practice evidence | E02, E03, E06, L02 | The proposed page makes the principle explicit. |

## Absolute-language audit

The required scan targets `always`, `never`, `only`, `all`, and `none` in `policy.md`.

| Term / passage | Location | Verdict | Evidence or revision |
| --- | --- | --- | --- |
| “Here is the non-cute version of the list” | “I use AI a lot” | Not an absolute term. | Included here to show the list is illustrative, not exhaustive. |
| `always` | No occurrence in draft body. | Pass | Avoided because universal enforcement is not evidenced. |
| `never` | “a documentary photograph, recording, or transcript that never touched a life” | Keep as a definitional refusal line. | L01 supports the documentary boundary. This does not claim perfect detection. |
| `only` | No occurrence in draft body. | Pass | Replaced with scoped conditions where needed. |
| `all` | “not the keys to everything” is used instead of an all-access claim. | Pass | Avoids overstating technical enforcement across tools. |
| `none` | No occurrence in draft body. | Pass | No universal absence claim is made. |

## Red-team scenarios

| Scenario | Draft outcome | Source / gate |
| --- | --- | --- |
| Client transcript | Keep it out of public tools. Use a secured workflow after verifying settings, authority, purpose, and minimum necessary data. | E05, E06, P03, H03 |
| Student data | Treat as identifiable sensitive material. Do not use a public tool; a secured workflow still requires authority and data minimization. | E05, E07, P03, H03 |
| Unpublished interview | Preserve the recording/transcript as source truth. Use AI in a secured, permitted workflow; check quotes against the source before publication. | L01, L02, E04, P03 |
| AI headshot | Treat as synthetic illustration, not documentary proof or a real portrait. Label material photorealistic generation and do not imply a real sitting occurred. | L01, L03, P02 |
| Documentary crowd image | Reject as evidence of attendance, community, diversity, ceremony, or consensus. Use real documentation or clearly separate speculative illustration. | L01, E02, P02 |
| Hallucinated citation | Do not ship it. Resolve and inspect the original/authoritative source or remove the claim. | E02, E04, E05 |
| Prompt to copy an artist's style | Reject the identifiable-style instruction and build an original reference set from permitted sources and role-based qualities. | E03, E04, E06, P04, H04 |
| Agent attempts a live deploy | Stop at the human gate. Require exact target checks, dry-run or preview, rollback path, and explicit approval appropriate to the action. | L06, P06 |
| AI-generated full first draft | Permitted. Check sources, edit for meaning and voice, own the result, and apply the approved material-disclosure threshold. | L02, E02, P02, H01 |

## Drafting disclosure status

AI assisted with research, comparison, drafting, and the first voice-check pass for these two files. The disclosure in `policy.md` remains explicitly **pending** because Kris Krüg has not yet reviewed or approved the final wording.
