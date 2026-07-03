# Contributing

Thanks for helping improve POPJAM's agent skills!

## Adding or changing a skill

- Each skill lives in `skills/<skill-name>/` with a `SKILL.md` entry point. The `name` in frontmatter must match the directory name (lowercase, hyphens only).
- Frontmatter needs `name` and `description`. The description is the trigger: write *what it does + when to use it*, including the phrasings users actually type. This single field decides whether an agent ever loads your skill.
- Keep `SKILL.md` under ~500 lines. Push depth into `references/*.md` and tell the reader *when* to load each one (progressive disclosure). Don't inline everything.
- Scripts in `scripts/` should be dependency-light Python or shell, runnable as-is. Anything deterministic (scoring, math, aggregation) belongs in a script, not in agent instructions.
- Validate before opening a PR:

  ```bash
  npx skills-ref validate skills/<skill-name>
  ```

- If you add a new skill, register it in two places: the `skills` array in `.claude-plugin/marketplace.json`, and the table in `README.md`.

## What makes a good PR

- **Failure cases**: a real prompt where a skill misfired or produced a bad result, plus the rule/example that fixes it. Prefer adding a worked example over adding a rule.
- **Eval cases**: new entries in a skill's `evals/evals.json` that pin behavior.
- **Reference playbooks**: distilled, opinionated guidance, not generic best-practice lists.
- **New skills**: marketing/ads/creative scope, validated on at least a few real runs.

## Testing a skill locally

```bash
# symlink into your Claude Code skills dir and try real prompts
npx skills add . --skill <skill-name>
```

Then run the prompts from the skill's description and check it triggers and completes.
