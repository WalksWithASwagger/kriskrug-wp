import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import docs_truth_check  # noqa: E402


def scan_text(relative_path: str, text: str):
    with tempfile.TemporaryDirectory() as tmp:
        repo_root = Path(tmp)
        path = repo_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

        return docs_truth_check.scan_file(repo_root, path)


class EphemeralMorningTruthGuidanceTests(unittest.TestCase):
    def test_active_guidance_rejects_routine_report_commit_flow(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            work_plan = repo_root / "docs/current-state/WORK-PLAN-2026-08-25.md"
            work_plan.parent.mkdir(parents=True)
            work_plan.write_text(
                "1. `make morning-truth` while online.\n"
                "2. Commit the fresh report.\n",
                encoding="utf-8",
            )

            findings = docs_truth_check.scan_file(repo_root, work_plan)

        self.assertTrue(
            any("morning-truth-checkpoint" in finding.message for finding in findings)
        )

    def test_active_guidance_rejects_commit_first_routine_report_flow(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            master_plan = repo_root / "docs/current-state/MASTER-PLAN-2026-07-30.md"
            master_plan.parent.mkdir(parents=True)
            master_plan.write_text(
                "- Commit fresh `make morning-truth` report\n",
                encoding="utf-8",
            )

            findings = docs_truth_check.scan_file(repo_root, master_plan)

        self.assertTrue(
            any("morning-truth-checkpoint" in finding.message for finding in findings)
        )

    def test_active_guidance_allows_ephemeral_and_checkpoint_modes(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            readme = repo_root / "docs/current-state/README.md"
            readme.parent.mkdir(parents=True)
            readme.write_text(
                "Run `make status-readonly` for routine startup.\n"
                "Use `make morning-truth` only for an ignored local copy.\n"
                "Use `make morning-truth-checkpoint` and commit it for a durable handoff.\n",
                encoding="utf-8",
            )

            findings = docs_truth_check.scan_file(repo_root, readme)

        self.assertFalse(
            any("morning-truth-checkpoint" in finding.message for finding in findings)
        )

    def test_active_guidance_allows_negated_commit_safety_language(self):
        samples = [
            "Use `make morning-truth` for an ignored local copy; do not commit it.\n",
            "Do not commit output from `make morning-truth`; it is ephemeral.\n",
        ]

        for sample in samples:
            with self.subTest(sample=sample), tempfile.TemporaryDirectory() as tmp:
                repo_root = Path(tmp)
                readme = repo_root / "docs/current-state/README.md"
                readme.parent.mkdir(parents=True)
                readme.write_text(sample, encoding="utf-8")

                findings = docs_truth_check.scan_file(repo_root, readme)

            self.assertFalse(
                any("morning-truth-checkpoint" in finding.message for finding in findings)
            )


class ActiveFrontDoorRegressionTests(unittest.TestCase):
    def test_current_work_plan_is_in_active_guidance_set(self):
        self.assertIn(
            Path("docs/current-state/WORK-PLAN-2026-08-25.md"),
            docs_truth_check.ACTIVE_GUIDANCE_PATHS,
        )

    def test_rejects_superseded_active_runbook_links(self):
        samples = {
            "docs/INDEX.md": (
                "| `WORK-PLAN-2026-08-24.md` | Active two-session runbook |\n"
            ),
            "docs/current-state/CURRENT-STATE-2026-07-30.md": (
                "Latest dated runbook: WORK-PLAN-2026-08-24.md.\n"
            ),
            "docs/current-state/MASTER-PLAN-2026-07-30.md": (
                "Day runbook: WORK-PLAN-2026-08-24.md.\n"
            ),
        }

        for path, text in samples.items():
            with self.subTest(path=path):
                findings = scan_text(path, text)
                self.assertTrue(
                    any("WORK-PLAN-2026-08-25.md" in finding.message for finding in findings)
                )

    def test_rejects_nonexistent_top_level_skill_links(self):
        samples = {
            "README.md": "skills/  # Claude Code skills used in this repo\n",
            "docs/INDEX.md": "| [`../skills/`](../skills/) | Skills |\n",
        }

        for path, text in samples.items():
            with self.subTest(path=path):
                findings = scan_text(path, text)
                self.assertTrue(
                    any("retired" in finding.message for finding in findings)
                )

    def test_rejects_archived_files_as_the_active_backlog(self):
        findings = scan_text(
            "README.md",
            "- Active backlog: `FIX_QUEUE.md`, `SITE-AUDIT-2026-05-16.md`\n",
        )

        self.assertTrue(
            any("open GitHub issue list" in finding.message for finding in findings)
        )

    def test_rejects_pinned_local_php_minor(self):
        findings = scan_text(
            "AGENTS.md",
            "- PHP is **8.3** here (CI pins 8.2).\n",
        )

        self.assertTrue(
            any("local PHP minor" in finding.message for finding in findings)
        )

    def test_rejects_pre_partial_issue_4_front_door_status(self):
        samples = {
            "AGENTS.md": (
                "repair two wrong duplicate-media writes and five corrected targets\n"
            ),
            "docs/current-state/README.md": (
                "two wrong duplicate-media writes and five corrected targets await repair\n"
            ),
        }

        for path, text in samples.items():
            with self.subTest(path=path):
                findings = scan_text(path, text)
                self.assertTrue(
                    any("three-target state" in finding.message for finding in findings)
                )

    def test_rejects_pre_cleanup_worktree_status(self):
        findings = scan_text(
            "docs/current-state/CURRENT-STATE-2026-07-30.md",
            "Three `/private/tmp` worktree registrations were prunable.\n",
        )

        self.assertTrue(findings)

    def test_delegates_issue_count_truth_to_live_drift_contract(self):
        samples = {
            "docs/current-state/README.md": "0 open PRs, 43 open issues.\n",
            "docs/current-state/CURRENT-STATE-2026-07-30.md": "Open issues: `40`.\n",
        }

        for path, text in samples.items():
            with self.subTest(path=path):
                findings = scan_text(path, text)
                self.assertFalse(findings)


class PersonalSiteIdentityRegressionTests(unittest.TestCase):
    def test_rejects_bc_ai_personification_in_agent_context(self):
        samples = {
            ".claude/context/project-context.md": (
                "Kris Krug is a grassroots ecosystem initiative dedicated to BC.\n"
            ),
            ".claude/agents-vibe.md": (
                "This is community infrastructure for building BC's inclusive AI future.\n"
            ),
        }

        for path, text in samples.items():
            with self.subTest(path=path):
                findings = scan_text(path, text)
                self.assertTrue(
                    any("personal-site identity" in finding.message for finding in findings)
                )

    def test_rejects_legacy_domain_and_bc_ai_mission_in_issue_templates(self):
        samples = {
            ".github/ISSUE_TEMPLATE/bug_report.yml": (
                "description: Report a bug with the BC+AI website at kk.ca\n"
            ),
            ".github/ISSUE_TEMPLATE/feature_request.yml": (
                "- label: This feature aligns with BC+AI's mission\n"
            ),
        }

        for path, text in samples.items():
            with self.subTest(path=path):
                findings = scan_text(path, text)
                self.assertTrue(
                    any("kriskrug.co" in finding.message for finding in findings)
                )

    def test_default_scan_includes_agent_context_and_issue_templates(self):
        expected = {
            Path(".claude/context/project-context.md"),
            Path(".claude/agents-vibe.md"),
            Path(".github/ISSUE_TEMPLATE/accessibility.yml"),
            Path(".github/ISSUE_TEMPLATE/bug_report.yml"),
            Path(".github/ISSUE_TEMPLATE/content.yml"),
            Path(".github/ISSUE_TEMPLATE/feature_request.yml"),
            Path(".github/ISSUE_TEMPLATE/performance.yml"),
            Path(".github/agent-state/README.md"),
            Path(".github/agents/doc-swarm/README.md"),
        }

        self.assertTrue(expected.issubset(set(docs_truth_check.DEFAULT_BASES)))

    def test_dormant_agent_guides_require_historical_banner(self):
        samples = {
            ".github/agent-state/README.md": "# Agent State Directory\n\nUsage instructions.\n",
            ".github/agents/doc-swarm/README.md": "# Documentation Swarm\n\nComing soon.\n",
        }

        for path, text in samples.items():
            with self.subTest(path=path):
                findings = scan_text(path, text)
                self.assertTrue(
                    any("STATUS: Historical" in finding.message for finding in findings)
                )

    def test_rejects_audited_access_and_work_plan_drift(self):
        samples = {
            "docs/current-state/ACCESS_CHANNELS.md": (
                "The agent swarm in `.github/` can be triggered via issues + labels.\n"
            ),
            "docs/INDEX.md": (
                "Active runbook: correct the remaining issue #4 media identity.\n"
            ),
        }

        for path, text in samples.items():
            with self.subTest(path=path):
                findings = scan_text(path, text)
                self.assertTrue(
                    any("audited current-state" in finding.message for finding in findings)
                )


class MergePolicyGuidanceTests(unittest.TestCase):
    def test_active_guidance_rejects_routine_admin_override(self):
        findings = scan_text(
            "docs/current-state/MASTER-PLAN-2026-07-30.md",
            "| Phase 0–1 docs PRs | Agent draft; KK merge (admin override) |\n",
        )

        self.assertTrue(any("Merge policy" in finding.message for finding in findings))

    def test_active_guidance_rejects_one_review_requirement(self):
        findings = scan_text(
            "AGENTS.md",
            "`main` requires 1 approving review before a content PR can merge.\n",
        )

        self.assertTrue(any("one-review" in finding.message for finding in findings))

    def test_active_guidance_rejects_second_account_requirement(self):
        findings = scan_text(
            ".env.schema",
            "Without a valid second-account token, `gh pr merge` fails.\n",
        )

        self.assertTrue(any("second-account" in finding.message for finding in findings))

    def test_active_guidance_rejects_universal_human_approval(self):
        findings = scan_text(
            "CONTRIBUTING.md",
            "Human maintainer reviews and approves every pull request.\n",
        )

        self.assertTrue(any("human approval" in finding.message for finding in findings))

    def test_agents_requires_the_current_merge_contract(self):
        findings = scan_text(
            "AGENTS.md",
            "Content and docs use the normal protected merge path.\n",
        )

        self.assertTrue(any("0 approving reviews" in finding.message for finding in findings))

    def test_agents_accepts_the_current_merge_contract(self):
        findings = scan_text(
            "AGENTS.md",
            "\n".join(
                [
                    "Theme / plugins / `inc/` / live deploy PRs: ask KK before merging.",
                    "Content/docs-only PRs: `main` requires 0 approving reviews.",
                    "Require `Test PR / summary` green and the branch up to date with `main`.",
                    "Merge with `gh pr merge <n> --squash --delete-branch`; no `--admin`.",
                ]
            ),
        )

        self.assertFalse(any("Merge policy" in finding.message for finding in findings))

    def test_default_scan_can_include_the_environment_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            schema = repo_root / ".env.schema"
            schema.write_text("GH_TOKEN=\n", encoding="utf-8")

            files = docs_truth_check.iter_markdown_files(
                repo_root,
                [Path(".env.schema")],
                [],
            )

        self.assertEqual(files, [schema.resolve()])


class DiagnosticMessageTests(unittest.TestCase):
    def test_stale_count_diagnostics_do_not_claim_current_counts(self):
        messages = [message for _, message in docs_truth_check.KNOWN_STALE_PATTERNS]

        self.assertFalse(any("current normalized count" in message for message in messages))


if __name__ == "__main__":
    unittest.main()
