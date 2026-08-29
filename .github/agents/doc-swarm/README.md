# Documentation Swarm

> **STATUS: Historical.** This proposed swarm was never adopted as the current documentation workflow. The relevant generator workflows were removed on 2026-08-23. Use `AGENTS.md`, `docs/current-state/README.md`, and the active PR validation workflow instead.

Specialized agent team for autonomous documentation generation and maintenance.

## Overview

The Documentation Swarm consists of 6 specialized agents that work together to create, maintain, and improve all project documentation.

**Purpose:** Keep documentation fresh, accurate, comprehensive, and aligned with code changes.

## Agents

1. **Content Analyzer** (`content-analyzer.agent.md`) - Analyzes code for documentation needs
2. **README Writer** (`readme-writer.agent.md`) - Generates and updates README files
3. **API Documenter** (`api-documenter.agent.md`) - Creates API documentation
4. **Tutorial Creator** (`tutorial-creator.agent.md`) - Writes user guides
5. **Style Enforcer** (`style-enforcer.agent.md`) - Ensures consistent style
6. **Link Validator** (`link-validator.agent.md`) - Validates all links

## Pipeline

```
Code Change → Content Analyzer → [README Writer, API Documenter, Tutorial Creator] → Style Enforcer → Link Validator → PR
```

## Use Cases

- Auto-update README when features added
- Generate API docs from code comments
- Create tutorials from specifications
- Maintain documentation freshness
- Ensure consistent style across all docs
- Validate all links work

## Status

**Retired proposal** — retained only as design history.
