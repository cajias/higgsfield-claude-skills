# Higgsfield AI — Claude Code Plugin Marketplace

A Claude Code plugin marketplace for [Higgsfield AI](https://higgsfield.ai). It ships two plugins:
**15 Seedance 2.0 prompt-engineering skills** that turn Claude into a specialist video prompt engineer (free, no setup),
and an **API automation pack** that generates images and videos end-to-end through the official Higgsfield API.
Install one or both straight from Claude Code.

---

## Install

In Claude Code, add this marketplace and install the plugins you want:

```text
/plugin marketplace add cajias/higgsfield-claude-skills
/plugin install higgsfield-prompts@higgsfield
/plugin install higgsfield-automation@higgsfield
```

**`higgsfield-prompts`** is free, needs no API key, and requires no setup — for most people it's all you need.
It makes Claude an expert at writing production-grade Seedance 2.0 prompts that you paste into Higgsfield yourself.
You can stop after installing it.

**`higgsfield-automation`** is optional. It actually drives the Higgsfield API to generate images and videos for you,
so it needs API credentials (see the next section) and **consumes Higgsfield credits**.

> **Prerequisites**: [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
> (`npm i -g @anthropic-ai/claude-code`) and a free [Higgsfield](https://higgsfield.ai) account.
> The automation plugin additionally needs API keys.

---

## Setup for `higgsfield-automation` (API keys)

The automation plugin bundles the **higgsfield-mcp** server, which talks to the official Higgsfield API.
It reads two credentials from your environment.

1. Get your **API key** and **secret** from the Higgsfield API console: <https://cloud.higgsfield.ai/api-keys>
2. Export them in your shell (the bundled `higgsfield-mcp` server reads them automatically):

```bash
export HF_API_KEY=your_api_key
export HF_SECRET=your_secret
```

1. Restart Claude Code so the MCP server picks up the variables, then run the **`debug_credentials`** tool to confirm
   your keys load correctly.

### Credits

Generation consumes Higgsfield credits. Rough costs:

| Operation            | Approx. cost |
| -------------------- | ------------ |
| Image — 720p         | ~$0.09       |
| Image — 1080p        | ~$0.19       |
| Video — Lite         | ~$0.13       |
| Video — Turbo        | ~$0.41       |
| Video — Standard     | ~$0.56       |
| Character (one-time) | ~$2.50       |

Top up at <https://cloud.higgsfield.ai/credits>. Prices are indicative — check the console for current rates.

---

## What you get

### `higgsfield-prompts` — 15 skills (no API key)

Each skill turns Claude into a specialist prompt engineer for one video style, producing **15–25 line, paste-ready
Seedance 2.0 prompts** with a 2-second hook, beat-by-beat timeline, camera moves, lighting, and sound design.
Claude usually auto-invokes the right one from your request; you can also call it explicitly by name.

| Command                      | Style               | When to use                                      |
| ---------------------------- | ------------------- | ------------------------------------------------ |
| `/seedance-cinematic`        | Cinematic Film      | Dramatic lighting, anamorphic, noir, epic        |
| `/seedance-3d-cgi`           | 3D CGI              | Pixar, Unreal Engine, ray tracing                |
| `/seedance-cartoon`          | Cartoon & Animation | Cel-shaded, hand-drawn, vector, watercolor       |
| `/seedance-comic-to-video`   | Comic to Video      | Manga, webtoons, graphic novels                  |
| `/seedance-fight-scenes`     | Fight & Action      | Martial arts, chase scenes, superhero battles    |
| `/seedance-motion-design-ad` | Motion Design Ad    | SaaS launches, feature showcases, app promos     |
| `/seedance-ecommerce-ad`     | E-Commerce Ad       | Product ads, fashion, beauty, TikTok Shop        |
| `/seedance-anime-action`     | Anime               | Shonen, mecha, magical girl, anime openings      |
| `/seedance-product-360`      | Product 360°        | Turntable, multi-angle, product reveal           |
| `/seedance-music-video`      | Music Video         | Beat-synced, performance, concert visuals        |
| `/seedance-social-hook`      | Social Hook         | TikTok, Reels, Shorts, scroll-stopping hooks     |
| `/seedance-brand-story`      | Brand Story         | Origin stories, company culture, founder stories |
| `/seedance-fashion-lookbook` | Fashion Lookbook    | Model walks, outfit showcases, runway clips      |
| `/seedance-food-beverage`    | Food & Beverage     | Restaurant promos, recipe content, food ASMR     |
| `/seedance-real-estate`      | Real Estate         | Property tours, architecture, interior design    |

### `higgsfield-automation` — 4 skills (API)

These skills call the Higgsfield API through the bundled **higgsfield-mcp** server to actually render assets.
They require `HF_API_KEY` / `HF_SECRET` and consume credits.

| Command                   | Description                                                                  |
| ------------------------- | ---------------------------------------------------------------------------- |
| `/higgsfield-image-auto`  | Generate an AI image on Higgsfield (Soul / Seedream) from a prompt           |
| `/seedance-auto-generate` | Turn an existing image into a Seedance 2.0 video                             |
| `/ugc-hot-girl`           | Craft a detailed image prompt for an attractive female UGC ad character      |
| `/ugc-video-auto`         | Full UGC pipeline — generate a character image, then animate it into a video |

---

## How it works

**Prompt skills** turn Claude into a specialist prompt engineer. Each one writes Seedance 2.0 prompts built around a
2-second scroll-stopping hook, a beat-by-beat timeline (up to ~15s), camera-movement choices, lighting and atmosphere,
and sound design. You paste the result into Higgsfield yourself — no API key, no cost.

**Automation skills** drive the official Higgsfield API via the bundled higgsfield-mcp server. Generation runs as
**async jobs**: the skill submits a job, polls its status, and returns the output URL when it's ready. Generated images
and videos are retained for **7 days**.

The natural flow:

> Pick a style skill (e.g. `/seedance-ecommerce-ad`) to craft the prompt → hand it to `/seedance-auto-generate`
> (or run the whole thing with `/ugc-video-auto`) to render it.

So you can use just the prompt skills as a free creative co-pilot, or wire them into the automation pack for hands-off
generation.

---

## Updating / Uninstalling

```text
/plugin marketplace update higgsfield
/plugin uninstall higgsfield-prompts@higgsfield
/plugin uninstall higgsfield-automation@higgsfield
```

---

## Credits & links

- **Higgsfield AI** — <https://higgsfield.ai>
- **API console** (keys & credits) — <https://cloud.higgsfield.ai>
- **higgsfield-automation** bundles the third-party **higgsfield-mcp** server —
  <https://github.com/Storyvord/higgsfield-mcp>

Prompt skills adapted from
[beshuaxian/higgsfield-seedance2-jineng](https://github.com/beshuaxian/higgsfield-seedance2-jineng).
UGC automation skill concepts originated with [@AKCodez](https://github.com/AKCodez).
