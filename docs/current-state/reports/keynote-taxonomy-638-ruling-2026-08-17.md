# Keynote taxonomy ruling, issue #638

**Date:** 2026-08-17
**Lane:** Track A, docs only. No live WordPress write. This file records a KK decision; it does not close #638.
**Decision authority:** Kris Krüg, 2026-08-17.
**Source of the set:** [`content/source-packs/keynotes-2026/talk-topic-bank.md`](../../../content/source-packs/keynotes-2026/talk-topic-bank.md)

---

## Headline

The canonical keynote set is the **6-talk topic bank**. Workshops stay add-ons. Live `/speaking/` must not invent a seventh taxonomy.

That ends the Set A / B / B2 / C / D / E conflict prepared in `content/drafts/2026-07-26-speaking-page/keynote-taxonomy.md` and in the #638 comments. The research recommendation (3 + 1) is on the record and is **overruled**. The page, schema, and internal links follow the six headings in the topic bank, in that order.

---

## The six signature keynotes

| # | Talk | Topic-bank heading | Status in the bank |
|---|---|---|---|
| 1 | Both Hands Full | Both Hands Full | Public proof: World AI Film Festival Brasil 2026 / bothhandsfull.com |
| 2 | Punk Rock AI / Creative Rebellion | Punk Rock AI / Creative Rebellion | Public proof: CreativeMornings Vancouver / punkrockai.com |
| 3 | Developing an AI Mindset | Developing an AI Mindset | Public proof: developinganaimindset.com |
| 4 | Compost AI | Compost AI | Available topic. In development until a public delivered-event source is verified. |
| 5 | Leadership After the AI Point of No Return | Leadership After the AI Point of No Return | Available topic. Program option, not past-stage proof. |
| 6 | Power, Taste, and Trust | Power, Taste, and Trust | Available topic. Program option, not past-stage proof. |

Aliases that stay inside these six, and do not become extra cards:

- **Creative Rebellion** is the Punk Rock AI heading, not a seventh talk.
- **Taste as Moat / Authored Judgment / Your Moat Isn't Your Code Anymore** do not join the signature set.
- **BC's Real AI Advantage** and **Who Sets the Direction Now?** do not join the signature set.
- **Dear AI: We Need to Talk About Your Soul** is a delivered Bass Coast **workshop**, not a signature keynote.
- **Responsible AI** is the Responsible AI Professional **certification**, not a keynote. It must not occupy a signature-topic card on `/speaking/`.

---

## Workshops stay add-ons

The topic bank lists these as workshop add-ons, not as a seventh keynote lane:

- AI mindset mapping for teams
- Build your creative corpus
- Prompting for taste, not just output
- Personal knowledge-base and memory workflows
- Community-first AI adoption
- AI risk, consent, and cultural responsibility
- Prototype day: from idea to public artifact

A workshop menu, a formats row, or a link to `/services/` is fine. A seventh signature-topic card is not.

---

## What this unblocks

- **#419** Speaking multimedia rebuild: the six talks are the page architecture. The live Set C four (Both Hands Full, Punk Rock AI, Developing an AI Mindset, Responsible AI) is retired as the taxonomy, even though it is still what page 1887 ships today.
- Schema and internal links that name "signature keynotes" use these six titles only.
- `content/source-packs/keynotes-2026/wp-payloads/speaking.html` and `content/drafts/2026-07-26-speaking-page/payload-body.html` must not grow a seventh talk or put Responsible AI back in the keynote grid.

---

## What this does not do

- It does not PATCH page 1887.
- It does not close #638. Close that issue after live `/speaking/` matches this set.
- It does not invent delivery history. Compost AI, Leadership After the AI Point of No Return, and Power, Taste, and Trust stay labeled as available / in-development program options until a public delivered-event source exists.
- It does not clear stage photography. #419 still uses recorded assets and the photographer-cleared stills only.

---

## Blast radius (unchanged, now decided)

| Surface | Required alignment |
|---|---|
| Live `/speaking/` (page 1887) | Six talks. No Responsible AI keynote card. No seventh title. Apply is a later, approved write. |
| Speaking draft payload | Rebuild around this set (#419). |
| Source-pack `speaking.html` | Same six headings. Do not re-apply the pre-ruling file as-is. |
| About / Services / Work cross-links | Point at the six talks or at `/speaking/`, not at a four-card or 3+1 set. |
| Schema / JSON-LD | If a talk list is emitted, it is these six. |

---

## Decision log

| Item | Ruling |
|---|---|
| Canonical set | Topic bank, six talks, order above |
| Workshops | Add-ons only |
| Responsible AI on `/speaking/` | Out of the keynote grid |
| 3+1 research recommendation | Overruled |
| Seventh taxonomy on live `/speaking/` | Forbidden |
| Close #638 from this file | No |
