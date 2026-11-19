# Repository instructions

These rules apply to every Copilot chat and agent in this repository. They are the
single source of truth for validation rules. Do not copy them into prompts or agent
files. Refer to this file.

## Where each kind of information lives

| Information | Source of truth |
|---|---|
| Requirements and acceptance criteria | The task or issue |
| Plans and decisions | `docs/handoff.md` and the pull request description |
| Validation rules | This file |
| Results | CI workflow runs and their artifacts |

If two places disagree, stop and ask which one is current. Do not pick silently.

## Validation rules

- Run `python -m pytest -q` before saying a change is done. All tests must pass.
- New endpoints return JSON with an explicit status code.
- Outbound HTTP requests must set a timeout.
- Do not edit anything under `.github/` unless the task says so.
- Do not turn on debug mode or add secrets to the code.

## Risk tiers (risk-based autonomy)

Autonomy depends on risk. Classify every task before planning. When unsure, use the
higher tier.

| Tier | Examples | What the agents may do |
|---|---|---|
| Low | Tests, docs, comments | Plan, then implement after the human approves the plan |
| Medium | Application code such as `app.py` | Plan, human approves, implement, reviewer checks |
| High | `.github/`, `requirements.txt`, secrets, permissions, deploy settings | Agents stop. They only describe the change. A named human makes it. |

Guidance only. The hard stop for high-tier paths is `CODEOWNERS` plus a repository
ruleset that requires code-owner review (`DEMO-STEPS.md`, Stage 5e).

## Audit trail

Every pull request from this team states: the task, the risk tier, the approved plan,
which agent did what, who approved, the test result, and a rollback step. Use the pull
request template.

## Saved state

For multi-step work, keep `docs/handoff.md` up to date. A new session must be able to
resume from that file without repeating finished steps. If the task changes, rewrite
the file and note why.
