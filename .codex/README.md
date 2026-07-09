# `.codex/`

This folder contains Codex-specific operating material for Scrape-n-Email. Repo-wide instructions belong in `AGENTS.md`; task-specific playbooks, prompts, skills, and checklists live here. Runnable Codex slash commands live in the repo-root `commands/` directory, and Claude mirrors live in `.claude/`.

## Purpose

Use `.codex/` to help future Codex agents work safely in this small Python scraper/email automation repo without rediscovering the setup, test commands, and secret-handling rules each time.

## Available Routines

- `routines/first-pass-repo-review.md` - orient in the repo before edits.
- `routines/bugfix.md` - diagnose and fix parser, CSV, mailer, or orchestration bugs.
- `routines/feature.md` - add focused functionality without turning the project into a framework.
- `routines/refactor.md` - improve structure while preserving behavior.
- `routines/test-and-verify.md` - choose the right unittest/import checks.
- `routines/pr-review.md` - review diffs with parser, email, and generated-file risks in mind.
- `routines/security-review.md` - check secrets, CSV injection, SMTP, and untrusted scrape content.

## Available Skills

- `skills/ponytail/SKILL.md` - smallest safe diff, stdlib-first, no scope creep.
- `skills/optimize/SKILL.md` - bounded hotspot cleanup with measurable improvement.
- `skills/site-selector-refresh/SKILL.md` - update parser selectors and offline tests when source HTML drifts.
- `skills/daily-run-check/SKILL.md` - verify scrape -> file -> email behavior with the narrowest offline checks.

## Prompt Templates

- `prompts/issue-triage.md`
- `prompts/implementation-plan.md`
- `prompts/review-diff.md`
- `prompts/release-notes.md`

Each prompt references `AGENTS.md`; copy one into a Codex prompt and fill in the placeholders.

## Commands

- `commands/ponytail.toml` - switch into minimal-diff, dependency-light repo mode.
- `commands/optimize.toml` - focus a task on tight, measurable cleanup or improvement.
- `commands/selector-refresh.toml` - focus a task on repairing selector drift from source HTML changes.
- `commands/daily-run-check.toml` - focus a task on offline pipeline verification.

These command files are the Codex-facing mirrors of the lighter command prompts under `.claude/commands/`. Keep the pairs aligned.

## Checklists

- `checklists/pre-commit.md`
- `checklists/pre-pr.md`
- `checklists/regression-risk.md`

Use these as quick reminders. They do not replace reading the code or running the relevant tests.

## Adding New Routines

1. Put repo-wide agent rules in `AGENTS.md`.
2. Put task-specific playbooks in `.codex/routines/`.
3. Put reusable repo-specific workflows in `.codex/skills/`.
4. Register runnable Codex commands in the repo-root `commands/`.
5. Link to `README.md`, `CONTRIBUTING.md`, and `.github/workflows/ci.yml` rather than copying large sections.
6. Keep routines and skills concise and grounded in actual commands.

## Scratch Work

Do not commit generated scrape outputs, logs, local notes, credentials, or temporary artifacts unless the maintainer explicitly requests them.
