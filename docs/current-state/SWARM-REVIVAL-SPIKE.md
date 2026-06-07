# Agent Swarm Revival — Spike & Pilot Proposal

**Date:** 2026-06-07 · **Status:** decision spike (no code wired yet) · **Refs:** `.github/agents/`, `.github/workflows/agent-pr-generator.yml`

## Context

`.github/agents/` defines a 7-stage issue→PR pipeline (Orchestrator → Analyzer → Test-Writer → Implementer → QA → Reviewer → PR-Creator, plus a doc-swarm). It produced PRs #71/#72 in May 2026, then was parked. `agent-pr-generator.yml` is now a read-only `workflow_dispatch` stub.

**The blocker (spec ↔ runner gap):** the orchestrator invokes each stage via `gh agent-task create --custom-agent <name>` — a bespoke CLI surface that no longer exists/drives anything. The markdown role prompts are fine; the **runner is gone**. A revival = re-bind these specs to a real runner. Today there are two real runners.

## The two real runners (verified 2026-06-07)

| | `anthropics/claude-code-action@v1` | Claude Agent SDK (Python/TS) |
|---|---|---|
| Shape | **Single Claude invocation** per run (built on the SDK) | Programmatic, **multi-stage / multi-subagent** orchestration |
| Fits our 7-stage pipeline? | No — it's one agent, not a staged swarm | Yes — analyzer→implementer→reviewer as resumed sessions/subagents |
| Trigger | `@claude` mention, **`label_trigger`** (non-interactive w/ prompt), `workflow_dispatch`/cron | Whatever wrapper you build (custom Action/CI) |
| Role prompts | No `.agent.md` support → use `CLAUDE.md` + `claude_args: --append-system-prompt` | Pass `.agent.md` content as `AgentDefinition`/system prompts |
| PR output | Commits to a `claude/`-prefixed branch, opens a **draft PR** via the GitHub App (CI runs on its commits) | You implement PR creation |
| Safety knobs | `--max-turns`, `--allowedTools`/`--disallowedTools`, scoped `permissions:` | Full control, more code |
| Effort to trial | **Low** (one workflow file + a secret) | High (write + maintain an orchestrator) |

## Recommendation: phased

**Phase 1 (MVP — recommended now):** off-the-shelf `claude-code-action@v1`, gated by label. The literal 7 stages collapse onto infrastructure we already have:

```
Issue (label: auto-implement, already swarm-ready)
  → claude-code-action  (Analyzer + Implementer, one run, --max-turns capped)
  → test-pr.yml         (QA: PHPCS + JS + docs-truth — already our PR gate)
  → human review        (Reviewer + PR-Creator: draft PR, human merges)
```
The `analyzer/implementer.agent.md` prompts become `--append-system-prompt`; `qa.agent.md` is replaced by `test-pr.yml`; `reviewer/pr-creator` become the human-reviewed draft PR. We lose the *literal* autonomous swarm but keep its value with ~1 file of config.

**Phase 2 (graduate only if MVP proves out):** Agent SDK custom Action for a true staged swarm (separate analyzer → implementer → reviewer subagents), reusing the `.agent.md` specs as `AgentDefinition`s. Only worth the maintenance cost if Phase 1 shows real throughput and the single-agent run is the bottleneck.

### Phase-1 workflow sketch (illustrative — not yet committed)
```yaml
name: Agent Implement
on:
  issues:
    types: [labeled]
permissions:
  contents: write          # push a claude/ branch
  pull-requests: write     # open a draft PR
  issues: write            # comment status
concurrency: { group: agent-implement-${{ github.event.issue.number }}, cancel-in-progress: false }
jobs:
  implement:
    if: github.event.label.name == 'auto-implement'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Implement GitHub issue #${{ github.event.issue.number }} as a DRAFT PR. Follow AGENTS.md and CLAUDE.md. Make the smallest change that satisfies the acceptance criteria. Do not touch scripts/notion-to-wp/** or fixes/** (publisher/prod-snippet code)."
          claude_args: "--max-turns 15 --append-system-prompt \"$(cat .github/agents/implementer.agent.md)\""
```

## Safety rails (non-negotiable — informed by the #75 overwrite incident)
1. **Gated trigger:** only fires on `auto-implement`, added by a human, on issues already triaged `swarm-ready`. Not on every issue.
2. **Draft PR only + human merge.** No auto-merge. `test-pr.yml` must pass.
3. **No prod / publisher reach.** It can only open repo PRs — it cannot touch the live Pagely site or the Notion→WP publisher. Prompt explicitly excludes `scripts/notion-to-wp/**` and `fixes/**`.
4. **Scoped `permissions:`** as above; **`--max-turns`** cap for cost/runaway; **`concurrency`** one-run-per-issue.
5. **Secret:** `ANTHROPIC_API_KEY` in repo secrets (the only new surface). Bills to the Anthropic account.

## Pilot proposal — one issue, end to end
**Pick #48 — `[A11Y] Create Accessibility Statement`** (swarm-ready, swarm-wave-1, priority:high). Why: self-contained static-page creation, easy to verify, zero publisher/prod risk, clear acceptance criteria.

**Run:** add `auto-implement` to #48 → action opens a draft PR creating the accessibility-statement page/pattern → `test-pr.yml` runs → human reviews the draft, requests changes via `@claude` if needed, merges. Success = a correct draft PR with green CI and no out-of-scope changes. If it misbehaves (scope creep, wrong files, runaway turns), that's the signal to keep it parked or move to a tighter SDK harness.

## Decision needed
- Approve **Phase-1 MVP** (commit the workflow + add `ANTHROPIC_API_KEY`)? — needs a maintainer to add the secret.
- Approve the **#48 pilot** before widening to other `swarm-ready` issues?
- Or keep parked and revisit. (Phase 2 / SDK is explicitly deferred until the MVP earns it.)
