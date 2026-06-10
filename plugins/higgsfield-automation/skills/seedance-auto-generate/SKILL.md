---
name: seedance-auto-generate
description: Generate a Seedance video from an image on Higgsfield via the official Higgsfield API (higgsfield-mcp server). Use when the user provides an image and wants to create an AI video from it on Higgsfield. Triggers on requests like "generate a video", "create a seedance video", "make a video on higgsfield", "auto-generate video", or any request to submit a video generation job to Higgsfield. Requires HF_API_KEY/HF_SECRET and consumes credits.
---

# Seedance Auto-Generate via the Higgsfield API

This skill animates an image into a video using ByteDance **Seedance v1 Pro**, exposed through the bundled `higgsfield-mcp` server (MCP server name: `higgsfield`). It submits an asynchronous job, polls until it completes, and returns the finished video URL — no browser automation involved.

> Seedance is image-to-video: it needs a **public HTTPS image URL** plus a **movement/action prompt** describing how the still should come alive.

---

## Prerequisites

- The **higgsfield-automation** plugin is installed (it bundles the `higgsfield-mcp` server).
- `HF_API_KEY` and `HF_SECRET` are set in the environment. Get them at https://cloud.higgsfield.ai/api-keys.
- Run `debug_credentials` once to verify the credentials are loaded. If generation fails with an auth error, check this first.
- Generation **consumes credits**. Results are retained for 7 days.
- MCP tools may be **deferred** in this harness. Before first use, load them with `ToolSearch` — e.g. `ToolSearch(query: "select:generate_video_seedance,get_request_status,upload_image")` or a keyword search for `higgsfield`.

---

## Input Requirements

The user provides:
1. **An image** — either a public HTTPS URL, or a local file (we'll upload it first).
2. **A movement/action prompt** describing what should happen in the video.

The Seedance `prompt` is a **motion/action description**, not a static-scene description. To craft a strong one, first invoke the matching prompt-style skill from the **higgsfield-prompts** plugin (see the table below), then pass its output here.

---

## Crafting the Prompt — Sub-Skills (higgsfield-prompts plugin)

Each sub-skill turns Claude into a specialized prompt engineer for that video style — generating large, detailed, paste-ready prompts with powerful **2-second hooks** that stop the scroll. Pick the one that matches your video, invoke it, then feed the result into `generate_video_seedance`.

### Creative Styles

| Slash Command | Skill Name | When to Use |
|---|---|---|
| `/seedance-cinematic` | Cinematic Film | Film quality — dramatic lighting, camera language, depth of field, anamorphic, noir, epic |
| `/seedance-3d-cgi` | 3D CGI | 3D rendered — Pixar, Unreal Engine, photorealistic, isometric, ray tracing, volumetric |
| `/seedance-cartoon` | Cartoon & Animation | 2D animation — cel-shaded, hand-drawn, flat vector, watercolor, rubber hose, motion graphics |
| `/seedance-comic-to-video` | Comic to Video | Animate comics — manga pages, webtoons, storyboards, sequential art, graphic novels |
| `/seedance-fight-scenes` | Fight Scenes & Action | Combat — martial arts, sword fights, chase scenes, superhero battles, action choreography |
| `/seedance-anime-action` | Anime | Japanese animation — shonen, seinen, mecha, magical girl, isekai, anime openings |

### Commercial & Marketing

| Slash Command | Skill Name | When to Use |
|---|---|---|
| `/seedance-motion-design-ad` | Motion Design Ad | Software/SaaS — product launches, feature showcases, app promos, tech demos, UI animation |
| `/seedance-ecommerce-ad` | E-Commerce Ad | Product ads — fashion, beauty, electronics, food, Amazon/Shopify/TikTok Shop, unboxing |
| `/seedance-product-360` | Product 360 | Turntable — multi-angle showcase, product reveal, hero shots, beauty shots, product spin |
| `/seedance-social-hook` | Social Hook | Viral content — TikTok, Instagram Reels, YouTube Shorts, scroll-stopping hooks |
| `/seedance-brand-story` | Brand Story | Brand narrative — origin stories, mission videos, company culture, founder stories |

### Industry-Specific

| Slash Command | Skill Name | When to Use |
|---|---|---|
| `/seedance-music-video` | Music Video | Beat-synced — performance, lyric video, music visualization, concert visuals, album art |
| `/seedance-fashion-lookbook` | Fashion Lookbook | Fashion — lookbooks, model walks, outfit showcases, runway clips, streetwear, campaigns |
| `/seedance-food-beverage` | Food & Beverage | Food — restaurant promos, recipe content, food ASMR, menu showcases, appetite appeal |
| `/seedance-real-estate` | Real Estate | Property — house tours, architecture, interior design, listings, virtual tours, renovation |

### What Each Sub-Skill Generates

Every sub-skill provides:
- **2-Second Hook Framework** — attention-grabbing opener patterns
- **Timeline Segmentation** — beat-by-beat breakdown
- **Camera Movement Encyclopedia** — techniques with exact phrasing
- **Lighting & Atmosphere** — setups that communicate mood and quality
- **Sound Design** — ambient, foley, music, silence guidance
- **Platform Optimization** — TikTok, Instagram, YouTube, etc.
- **Large Example Prompts** — production-quality, paste-ready

---

## Seedance Notes

| Aspect | Detail |
|---|---|
| Model | ByteDance Seedance v1 Pro (`generate_video_seedance`) |
| Input image | Must be a **public HTTPS URL** (use `upload_image` for local files) |
| Prompt | Movement / action / camera description |
| Output | **One finished video URL per request** |

The API returns a single rendered video per `request_id` — there is no multi-file batch or in-browser asset grid.

---

## Automation Flow

### Step 0 (only if the image is local): host it as a public URL

Video tools require a **public HTTPS** `image_url`. If the user gives a local file, upload it first to get a URL:

```
upload_image(
  image_base64: "<RAW base64, NO data: prefix>",
  content_type: "image/png"   // "image/jpeg" | "image/png" | "image/webp"
)
→ returns { public_url }
```

If the image already comes from a Higgsfield image generation (e.g. `full_quality_url` from `/higgsfield-image-auto`), it's **already a public URL** — skip this step and use it directly.

### Step 1: Submit the Seedance video job

```
generate_video_seedance(
  image_url: "<public HTTPS image URL>",
  prompt: "<movement/action prompt from a sub-skill>"
)
→ returns { request_id }
```

**Confirm with the user before submitting** — video generation consumes more credits than images.

### Step 2: Poll for completion

```
get_request_status(request_id: "<request_id>")
→ returns { status, output_url? }
```

Poll every few seconds. The `status` moves through:
- `queued` — accepted, waiting for a worker
- `in_progress` — rendering
- `completed` — done; the output video URL is populated
- `failed` — generation error (suggest retry / simpler prompt)
- `nsfw` — blocked by the safety filter
- `cancelled` — the request was cancelled

Video jobs take longer than images (typically a minute or more), so allow several poll cycles.

### Step 3: Return the result

When `status == "completed"`, give the user the finished **video URL**.

> Alternative video model: `generate_video_kling(image_url, prompt)` (Kling v2.1 Pro, prompt = camera movement) also returns a `request_id` polled with `get_request_status`, if the user prefers Kling over Seedance.

---

## Error Handling

- **Auth error / 401**: Run `debug_credentials`. Ensure `HF_API_KEY` and `HF_SECRET` are exported.
- **`image_url` rejected**: It must be a reachable **public HTTPS** URL. Local paths and `data:` URIs won't work — run `upload_image` first.
- **`status: failed`**: Suggest retrying or simplifying the motion prompt.
- **`status: nsfw`**: The safety filter blocked it — suggest revising the prompt.
- **Need to cancel**: `cancel_request(request_id)` cancels a job **only while it is still `queued`**.
- **Tool not found**: Load it with `ToolSearch` and retry.

---

## Example Workflows

### Example 1: Real Estate Video (end-to-end)

```
User: "Create a video for this house photo" + [local file]

Step 1 → Invoke /seedance-real-estate to craft a cinematic property motion prompt
Step 2 → upload_image(...) → public_url
Step 3 → generate_video_seedance(image_url: public_url, prompt: <generated prompt>) → request_id
Step 4 → Confirm with user before submitting
Step 5 → Poll get_request_status until completed → return video URL
```

### Example 2: Product Ad (image already on Higgsfield)

```
User: "Make a TikTok ad for my sneakers" + [Higgsfield image URL]

Step 1 → Invoke /seedance-ecommerce-ad to craft a product showcase motion prompt
Step 2 → generate_video_seedance(image_url: <higgsfield url>, prompt: <generated prompt>) → request_id
Step 3 → Confirm, then poll get_request_status until completed
```

### Example 3: Quick Generate (no sub-skill)

```
User: "Just animate this image, cinematic style" + [image URL]

Step 1 → Write a concise cinematic motion prompt directly (or auto-invoke /seedance-cinematic)
Step 2 → generate_video_seedance(image_url, prompt) → request_id
Step 3 → Confirm, poll, return video URL
```
