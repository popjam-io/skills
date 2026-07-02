# POPJAM Skills

**Free, open-source agent skills for marketing, ads & creatives** — shared by the [POPJAM.IO](https://popjam.io) team.

These are distilled versions of the pipelines we run in production at POPJAM: brand research, audience discovery, synthetic persona panels, ad creative generation, engagement simulation, landing pages that convert, and brand-guideline extraction. They work in Claude Code and any agent that supports the [Agent Skills](https://agentskills.io) standard (Cursor, Codex, Amp, opencode, …).

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Skills

| Skill | What it does |
|---|---|
| [**popjam-growth-engine**](skills/popjam-growth-engine) | Turn one website URL into tested ad creatives: brand research → audience segments → synthetic persona panel → ad angles → real creatives (image/video/animation) → deterministic engagement simulation → iteration. Ends with a leaderboard of who converts and why. |
| [**award-landing-page**](skills/award-landing-page) | Design and build pages that sell — landing, pricing, waitlist, launch pages. Full deliverable: funnel research, art direction, conversion copywriting, distinctive design & motion, technical SEO, CTA wiring. |
| [**brand-guideline-extraction**](skills/brand-guideline-extraction) | Reverse-engineer a complete brand style guide from a folder of design assets (posts, ads, banners, decks, videos) — including a reusable "style prompt block" for on-brand AI image generation. |
| [**remotion-render-pitfalls**](skills/remotion-render-pitfalls) | Render-breaking [Remotion](https://remotion.dev) mistakes that pass `tsc` + `eslint` but crash at render time. Battle-tested against POPJAM's production render pipeline; useful for any strict Remotion setup. |

## Install

### With the skills CLI (recommended)

Works with Claude Code, Cursor, Codex, and [every other supported agent](https://skills.sh):

```bash
# Install all skills (interactive picker)
npx skills add popjam-io/skills

# Or install a specific skill
npx skills add popjam-io/skills --skill popjam-growth-engine
```

### Claude Code — plugin marketplace

```
/plugin marketplace add popjam-io/skills
/plugin install popjam-skills@popjam
```

### Manual (any agent)

Copy a skill directory into your agent's skills folder, e.g. for Claude Code:

```bash
git clone https://github.com/popjam-io/skills.git
cp -r skills/skills/popjam-growth-engine ~/.claude/skills/   # personal, all projects
# or into <your-project>/.claude/skills/ for a single project
```

## Try it

Once installed, just describe the outcome — the skills trigger themselves:

- *"Make ads for https://yourbrand.com"* → **popjam-growth-engine** runs the full pipeline
- *"Who is my target audience?"* → audience segments + persona panel with evidence
- *"Test this ad concept against our audience"* → persona simulation + scored leaderboard
- *"Build a landing page for our launch on Thursday"* → **award-landing-page**
- *"Extract brand guidelines from ./assets"* → **brand-guideline-extraction**

Some phases of the growth engine generate real media. Image/video generation uses the [Higgsfield MCP](https://higgsfield.ai) and animations use [Remotion](https://remotion.dev) — if neither is available, the skill still delivers strategy and simulation on text concepts, honestly.

## Repo structure

```
skills/
├── popjam-growth-engine/
│   ├── SKILL.md              # entry point — frontmatter + instructions
│   ├── references/           # per-phase playbooks, loaded on demand
│   ├── scripts/              # deterministic scoring (never let the LLM do math)
│   ├── workflows/            # multi-agent fan-out templates
│   └── evals/                # eval suite the skill was validated against
├── award-landing-page/
├── brand-guideline-extraction/
└── remotion-render-pitfalls/
```

Each skill follows the [Agent Skills specification](https://agentskills.io/specification): a `SKILL.md` with `name` + `description` frontmatter, and progressive disclosure — references are read only when their phase begins, keeping context lean.

## Why free?

We build [POPJAM](https://popjam.io) — an AI marketing platform that runs these same pipelines as a product: brand onboarding from a URL, reusable audiences & persona panels, ad/content generation, persona simulation with scored leaderboards, and campaign iteration — with a team UI, asset storage, and integrations on top.

These skills are the "run it yourself in your agent" edition. If you'd rather have the whole loop managed for you (or your marketing team doesn't live in a terminal), [try POPJAM](https://popjam.io).

## Contributing

Issues and PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Good contributions: failure cases the skills should handle, new reference playbooks, eval cases, and new marketing/creative skills.

## License

[MIT](LICENSE) © POPJAM
