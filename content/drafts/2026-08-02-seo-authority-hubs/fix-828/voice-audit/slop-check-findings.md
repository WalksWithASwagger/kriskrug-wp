# Mechanical slop-check findings

Target: `../post-body.html`

Initial result: two warnings, zero hard-rule violations.

## Fix

1. Line 11: `hair and makeup team`
   - Reason: the canonical corpus prefers `crew` for collaborators.
   - Revision: `hair and makeup crew`.
2. Line 45: `anyone else the team agreed to name`
   - Reason: same preferred-vocabulary warning.
   - Revision: `anyone else the crew agreed to name`.

The repository checker independently returned zero violations. No em dash, banned LLM phrase, canonical-spelling error, or chatbot leakage was present.
