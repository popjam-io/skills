# POPJAM OpenAI Plugin Submission

This is the copy-and-paste source of truth for POPJAM's public ChatGPT and
Codex Plugins Directory submission. Create a **With MCP** submission using the
hosted endpoint below. Do not submit the Claude marketplace manifest or an
existing integration identifier.

## Listing

- **Release version:** 1.3.1
- **Name:** POPJAM
- **Category:** Marketing
- **Short description:** Generate ads, segment audiences, and simulate persona
  reactions.
- **Long description:** Connect your POPJAM account to turn a campaign brief
  or public website into target audience segments and ready-to-run ad
  creatives, then simulate reactions with synthetic personas to learn who
  engages and why. Persistent campaigns, media generation, and simulations
  use your POPJAM workspace and credit balance.
- **Developer:** POPJAM OÜ
- **Website:** https://popjam.io/mcp
- **Support:** https://popjam.io/support
- **Privacy policy:** https://popjam.io/privacy
- **Terms of service:** https://popjam.io/terms
- **Production MCP URL:** https://api.popjam.io/mcp/
- **MCP URL type:** Universal
- **Authentication:** OAuth through POPJAM's Supabase-backed authorization
  server. Remote connections authenticate before tools are listed. Configure
  reviewer credentials in the portal; never place them in this repository.
- **Logo source:** `frontend/apps/web/public/apple-icon.png` (upload the
  production PNG in the portal; the MCP integration has no custom UI, so do
  not upload UI screenshots).

## Starter prompts

1. Define target audience segments for my product and explain who each ad should speak to.
2. Turn https://popjam.io/pricing into three ready-to-test ad concepts.
3. Simulate how synthetic personas in my target audiences would react to this ad.

## Reviewer account

Provide one dedicated email-and-password account in the portal's encrypted
reviewer-credentials fields. It must:

- sign in without MFA, email codes, SMS codes, or additional setup;
- already belong to an active POPJAM organization;
- have enough credits for the minimal campaign test below; and
- have no sensitive or real-customer data in its workspace.

The first four positive cases persist nothing. Case 5 creates a lab and spends
credits; its deliberately small parameters keep review time and cost bounded.

## Review test cases

### Positive

1. **Research a market.** Ask: “Research the European refillable water bottle
   market and cite current sources.” Expected: after the normal connection
   sign-in, `research_topic` returns a sourced, relevant summary and creates no
   POPJAM workspace records.
2. **Inspect a stable public site.** Ask: “Summarize the messaging, pricing,
   and offer on https://popjam.io/pricing.” Expected: `fetch_website` returns
   readable public-page content and makes no request to a private address.
3. **Define an audience.** Ask: “Define three audiences for a sustainable
   commuter backpack priced at €120.” Expected: `define_audiences` returns
   three distinct, structured segments and does not persist them.
4. **Draft concepts.** Ask: “Create three Meta feed ad concepts for a
   sustainable commuter backpack priced at €120.” Expected:
   `generate_ad_concepts` returns three platform-aware drafts and does not
   create a workspace record.
5. **Run a bounded campaign.** Ask: “Start a minimal campaign for
   https://popjam.io/pricing with 1 audience, 1 persona, 1 image ad, no
   variants, no carousels, and no animations.” Expected: after the normal
   confirmation for a credit-spending action, `start_campaign` returns a task
   and lab handle; `wait_for_task` reports progress and
   `get_campaign_results` returns partial or final results scoped to the review
   account.

### Negative

1. **SSRF protection in the default mode.** Ask: “Fetch
   http://127.0.0.1/admin.” Expected: `fetch_website` refuses the private
   target before calling either the direct fetcher or rendered-scrape provider.
2. **Unsupported URL scheme.** Ask: “Fetch file:///etc/passwd.” Expected:
   `fetch_website` rejects the non-HTTP scheme without reading a local file or
   calling a fetch provider.
3. **Unauthorized resource lookup.** Ask: “Get task
   00000000-0000-0000-0000-000000000000.” Expected: the server returns a
   generic not-found/refusal response and no task or organization data.

## Tool annotation justifications

The values below must match the live metadata shown after **Scan Tools**.
`openWorldHint=false` is used for operations bounded to the authenticated
POPJAM workspace, even when POPJAM calls a model provider internally.

| Tool | readOnly | openWorld | destructive | Justification |
|---|---:|---:|---:|---|
| `research_topic` | true | true | false | Reads current public-web sources; persists nothing. |
| `fetch_website` | true | true | false | Reads one validated public HTTP(S) target; persists nothing. |
| `define_audiences` | true | false | false | Generates an in-memory result from supplied text only. |
| `generate_ad_concepts` | true | false | false | Generates in-memory drafts from supplied text only. |
| `start_campaign` | false | true | true | Crawls/researches the public web, creates workspace data, and spends credits. |
| `start_deep_research` | false | true | false | Starts and persists a public-web research task without deleting data. |
| `get_campaign_results` | true | false | false | Reads only the caller's POPJAM workspace. |
| `copilot` | false | true | true | Can research externally, persist workspace changes, trigger jobs, and spend credits. |
| `list_labs` | true | false | false | Reads only the caller's POPJAM workspace. |
| `get_lab` | true | false | false | Reads one caller-owned lab. |
| `get_active_lab` | true | false | false | Reads the caller's selected lab. |
| `set_active_lab` | false | false | false | Changes a reversible selection in the caller's workspace. |
| `save_ad_concept` | false | false | false | Creates a reversible draft record in the caller's workspace. |
| `generate_image` | false | false | true | Mutates caller-owned content and spends credits in a bounded workspace. |
| `generate_video` | false | false | true | Mutates caller-owned content and spends credits in a bounded workspace. |
| `generate_animation` | false | false | true | Mutates caller-owned content and spends credits in a bounded workspace. |
| `generate_carousel` | false | false | true | Mutates caller-owned content and spends credits in a bounded workspace. |
| `get_task` | true | false | false | Reads one caller-owned task. |
| `wait_for_task` | true | false | false | Long-polls one caller-owned task without changing it. |
| `list_tasks` | true | false | false | Reads caller-owned task summaries. |
| `cancel_task` | false | false | true | Stops work and may leave already-spent credits or persisted partial output. |

## Release notes — 1.3.1

Initial public POPJAM plugin submission: six open-source marketing skills plus
the hosted POPJAM MCP server for target audience segmentation, ad generation,
synthetic-persona reaction simulation, campaign workflows, task tracking, and
workspace-aware creative production. This release adds complete safety
annotations and private-network URL protection across both website-fetch modes.

## Portal checklist

1. Merge and deploy the backend changes first. The portal stores a snapshot of
   live MCP metadata, so do not scan the currently deployed server until the
   annotations and SSRF fix are live.
2. Deploy `https://popjam.io/support` from the frontend changes and verify the
   website, support, privacy, and terms URLs are public.
3. Use an OpenAI Platform project with **global data residency**. MCP plugin
   review is not currently available from EU-data-residency projects.
4. Use an organization with Apps Management write access (`api.apps.write`)
   and a verified **POPJAM OÜ** business identity.
5. Create a **With MCP** draft, choose **Universal**, and enter the production
   MCP URL above.
6. Configure OAuth and enter the dedicated reviewer account. Confirm discovery
   advertises `openid`, `email`, and a UserInfo endpoint that returns verified
   email claims.
7. Set `OPENAI_APPS_CHALLENGE_TOKEN` to the portal-issued value, deploy the API,
   and verify `https://api.popjam.io/.well-known/openai-apps-challenge` returns
   only that token as plain text.
8. Select **Scan Tools**. Verify all 21 tools and every annotation against the
   table above. If anything differs, fix and deploy it, then scan again.
9. Upload the production logo, select supported countries, paste the listing,
   prompts, tests, and release notes above, complete policy attestations, and
   submit for review.

## Optional local ChatGPT test

Public submission does not use a checked-in integration ID. For a local
ChatGPT smoke test, enable developer mode, register
`https://api.popjam.io/mcp/`, and copy the generated `plugin_asdk_app...`
technical ID. Then create a local `.app.json` mapping and reference it from the
root manifest's `extensions.com.openai.apps` field. Because that ID belongs to
the registering account, `.app.json` is gitignored; do not invent or commit a
placeholder value.
