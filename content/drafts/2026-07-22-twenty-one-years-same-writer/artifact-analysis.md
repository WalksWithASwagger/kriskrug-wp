# Artifact analysis

## Verdict

The supplied Claude artifact is an unusually strong piece of editorial design. It treats analysis as a forensic report rather than a dashboard, keeps its corrections visible, and ends with a method section that tells the reader where not to trust it.

Its core thesis is publishable:

> A voice checker can detect a machine that nobody edited. It cannot prove a human wrote the result.

The current artifact is not ready to republish verbatim because its visible numbers come from several iterations of the study. The best blog version keeps the argument, the retractions, and the exhibit structure while freezing the evidence to one reconciled ledger.

## What works

### The opening lands fast

The title and first score comparison establish the whole problem without throat-clearing. The AI-assisted newsletter scoring better than Kris is the right reversal.

### Retractions are part of the design

The red correction panel is not a production note. It gives the analysis credibility and creates narrative tension. Both corrections should remain public.

### The exhibit structure earns the length

The page moves from a controlled head-to-head, to the scorecard, to generated pastiche, to genuine archive writing, then to actions. Each section answers the objection raised by the one before it.

### The genuine 2005 excerpts do more than the charts

The missing commas, run-ons, slang, and named obsessions show a person more effectively than a detector score. The post should let those excerpts breathe.

### The visual language matches the argument

- Charcoal field instead of glossy gradient.
- Warm ivory serif for the human, monospaced gold labels for the instrument.
- Muted brick red reserved for corrections.
- Wide breathing room, compact score cards, and evidence tables.
- No stock robot, neon brain, or generic AI imagery.

## What needs correction

### Freeze one numeric iteration

The artifact currently shows conflicting word totals for the classic, typed, AI-assisted, and Machine-Kris corpora. The public draft uses only the stable archive counts and rounded comparison rates, with the rate table blocked on a regenerated score export.

### There are four corpora now, not three

The visible scorecard contains Classic Blogger, Kris typing, Sent as Kris, and Machine-Kris. The blog draft corrects the legacy `Three corpora` heading to four.

### One action item is already fixed

The artifact says Dark Crystal still grades against a 54-rule vendored anti-glossary. Current fetched source has matching source and vendored files, both loading 97 rules. The blog reframes this as a bug found and fixed, not a current defect.

### The private artifact is not a public citation

The artifact was marked `Share, private` at inspection. The blog should not link it unless Kris intentionally changes that state. The article can stand on the archived sources and a published method note.

### The voice should be first-person on KrisKrug.co

The artifact speaks about Kris as a subject. The blog version keeps the forensic distance in its labels but lets Kris own the experiment, the errors, and the conclusion in first person.

## WordPress translation

The styled payload uses one scoped wrapper, `kk-vf-shell`, so the report look does not leak into other posts. It preserves the artifact's palette, score cards, bar comparisons, table, red retraction panel, and exhibit labels without changing Aurora theme files.

The tradeoff is editability: one Custom HTML block is harder to revise in the visual editor. If that is too expensive, the fallback is native Gutenberg groups, columns, table, and quote blocks with a smaller scoped CSS snippet. The prose and source ledger do not depend on either visual implementation.

## Recommended publication shape

1. Approve the first-person article and quotations.
2. Regenerate the raw score export and freeze the numbers.
3. Create a private WordPress draft from `post.html`.
4. Test desktop, narrow mobile, table overflow, and style-tag retention.
5. Generate one typographic featured image from `image-brief.md`.
6. Publish only after the normal slug, snapshot, and dry-run gates.
