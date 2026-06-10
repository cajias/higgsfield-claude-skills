---
name: ugc-video-auto
description: Full UGC ad video pipeline via the official Higgsfield API (higgsfield-mcp server) — generates a character image, then animates it into a Seedance video. Orchestrates the complete flow from image prompt to finished UGC video. Use when the user wants to create a UGC ad video end-to-end, or wants to turn a Higgsfield-generated image into a video. Triggers on "create a UGC video", "make a UGC ad", "UGC pipeline", "turn this into a UGC video", or any request combining image generation with video creation for ads/UGC content. Requires HF_API_KEY/HF_SECRET and consumes credits.
---

# UGC Video Auto — Full Pipeline via the Higgsfield API

This skill orchestrates the complete UGC ad video pipeline on Higgsfield through the bundled `higgsfield-mcp` server (MCP server name: `higgsfield`): generate a character image → animate it into a Seedance video. Both stages are asynchronous API jobs (submit → poll → read the output URL) — no browser automation.

---

## Pipeline Overview

```
Phase 1: Generate the character image
  generate_image(prompt, character_id?) → job_set_id
  poll get_generation_status(job_set_id) → full_quality_url  (a public HTTPS URL)

Phase 2: Animate it into a UGC video
  generate_video_seedance(image_url = full_quality_url, prompt) → request_id
  poll get_request_status(request_id) → final UGC video URL
```

The image URL from Phase 1 is already public, so it feeds straight into Phase 2 as `image_url` — no download or upload step.

---

## Prerequisites

- The **higgsfield-automation** plugin is installed (it bundles the `higgsfield-mcp` server).
- `HF_API_KEY` and `HF_SECRET` are set in the environment. Get them at https://cloud.higgsfield.ai/api-keys.
- Run `debug_credentials` once to verify the credentials are loaded. If anything fails with an auth error, check this first.
- Generation **consumes credits** (image 720p ~1.5 cr, 1080p ~3 cr; Seedance video typically more than an image; character creation a one-time ~40 cr). Results are retained 7 days.
- MCP tools may be **deferred** in this harness. Before first use, load them with `ToolSearch` — e.g. `ToolSearch(query: "select:generate_image,get_generation_status,generate_video_seedance,get_request_status")` or a keyword search for `higgsfield`.

---

## Input Requirements

The user provides:
1. **Character description** OR a pre-made image prompt (invoke `/ugc-hot-girl` to generate one).
2. **Product/brand context** — what the UGC video is advertising.
3. **Video style** — testimonial, product showcase, unboxing, reaction, etc.

Optional:
- **Quality** (image): `1080p` (default) or `720p`.
- **character_id**: for a consistent face across shots (see Phase 1, Step 0).
- **Video prompt style**: best crafted via `/seedance-ecommerce-ad` or `/seedance-social-hook` from the **higgsfield-prompts** plugin.

---

## Full Automation Flow

### Phase 1: Generate the Character Image

#### Step 0 (optional): Register a consistent character

If the campaign needs the same face across several shots, create the character once and reuse its id:

```
create_character(name: "<name>", image_urls: ["<1-5 reference URLs>"]) → character_id
```

Poll its readiness (status flows `not_ready` → `queued` → `in_progress` → `completed`) via `get_character(character_id)` before using it. This is a one-time ~40 credit cost.

#### Step 1: Submit the image job

If the user hasn't provided an image prompt, invoke `/ugc-hot-girl` first to generate one.

```
generate_image(
  prompt: "<character image prompt>",
  quality: "1080p",
  character_id: "<optional, from Step 0>"
)
→ returns { job_set_id }
```

**Confirm with the user before submitting** — this consumes credits.

#### Step 2: Poll until the image is ready

```
get_generation_status(job_set_id: "<job_set_id>")
→ returns { status, preview_url?, full_quality_url? }
```

Statuses: `queued` → `in_progress` → `completed` (also `failed`, `nsfw`). When `completed`, capture the **`full_quality_url`** — that is the public image URL for Phase 2.

---

### Phase 2: Animate the Image into a UGC Video

#### Step 3: Craft the video (motion) prompt

The Seedance prompt describes **movement/action**, not a static scene. Craft it with a higgsfield-prompts sub-skill — for UGC ads, `/seedance-ecommerce-ad` or `/seedance-social-hook` are the best fits. Reference the subject naturally (e.g. "the woman in the image …").

**UGC Video Prompt Templates** (pick based on style):

**Testimonial / Talking Head:**
```
The woman in the image talks directly to camera with natural hand gestures, warm golden hour lighting, casual authentic vibe. She speaks enthusiastically, leaning in slightly for emphasis. Soft bokeh background, shallow depth of field. Natural skin texture, realistic lip movement, TikTok UGC testimonial style. Smooth handheld camera.
```

**Product Showcase:**
```
The woman in the image holds up a product toward the camera, turning it to show different angles. Excited genuine expression, eyes wide. Ring light illumination, clean background. She points at the product features, nodding enthusiastically. Close-up selfie framing, iPhone-quality video, authentic UGC feel.
```

**Reaction / Unboxing:**
```
The woman in the image opens a package with excited anticipation, pulling out a product and reacting with genuine delight. Surprised expression, mouth open, then breaking into a wide smile. Natural bedroom lighting, casual setting. Handheld camera feel, authentic unboxing energy, TikTok style.
```

**Before/After:**
```
The woman in the image starts looking skeptical, touching her face doubtfully. Then she applies a product, and her expression transforms to amazement, touching her skin in disbelief. Soft ring light, bathroom mirror setting. Genuine transformation moment, UGC testimonial.
```

**Lifestyle / Day-in-the-Life:**
```
The woman in the image walks through a bright modern space, casually interacting with a product as part of her routine. Natural morning light, relaxed movement, authentic candid energy. Camera follows with gentle tracking, shallow depth of field. Aspirational but relatable lifestyle content.
```

#### Step 4: Submit the Seedance video job

The `full_quality_url` from Phase 1 is already a public HTTPS URL — pass it directly:

```
generate_video_seedance(
  image_url: "<full_quality_url from Phase 1>",
  prompt: "<UGC motion prompt>"
)
→ returns { request_id }
```

**Confirm with the user before submitting** — video generation costs more credits than images.

#### Step 5: Poll until the video is ready

```
get_request_status(request_id: "<request_id>")
→ returns { status, output_url? }
```

Statuses: `queued` → `in_progress` → `completed` (also `failed`, `nsfw`, `cancelled`). Video jobs take longer than images, so allow several poll cycles.

#### Step 6: Report the result

When `status == "completed"`, give the user the finished **UGC video URL**.

---

## Error Handling

- **Auth error / 401**: Run `debug_credentials`. Ensure `HF_API_KEY` and `HF_SECRET` are exported.
- **Image `status: failed`/`nsfw`**: Retry / simplify / revise the prompt before moving to Phase 2.
- **`image_url` rejected in Phase 2**: It must be a reachable public HTTPS URL. The Phase-1 `full_quality_url` qualifies; a local file would need `upload_image` first.
- **Video `status: failed`/`nsfw`**: Retry or revise the motion prompt.
- **Need to cancel a video job**: `cancel_request(request_id)` works **only while it is still `queued`**.
- **Tool not found**: Load it with `ToolSearch` and retry.
- **Character not ready**: Poll `get_character(character_id)` until `completed` before passing the id to `generate_image`.

---

## Example End-to-End Workflow

```
User: "Create a UGC ad video with a hot girl promoting my new skincare serum"

1. Invoke /ugc-hot-girl → beauty/skincare image prompt:
   "Attractive young woman, early 20s, clear dewy skin, dark brown hair in
    messy bun... ring light illumination... photorealistic..."

2. Phase 1 — Image:
   → generate_image(prompt, quality: "1080p") → job_set_id
   → Confirm with user before submitting
   → poll get_generation_status until completed → full_quality_url ✓

3. Phase 2 — Video:
   → Craft motion prompt via /seedance-ecommerce-ad, e.g.:
     "The woman in the image holds up a small serum bottle, examining it
      with genuine curiosity. She applies a drop to her fingertip, touches
      her cheek, and her expression lights up with delight..."
   → generate_video_seedance(image_url: full_quality_url, prompt) → request_id
   → Confirm with user before submitting
   → poll get_request_status until completed → final video URL ✓

4. Report: "Your UGC video is ready: <video URL>"
```

---

## Pipeline Skills Reference

| Step | Skill | What it does |
|---|---|---|
| 1 | `/ugc-hot-girl` | Generates the character image prompt |
| 2 | `/higgsfield-image-auto` | Submits just the image job (`generate_image`) and returns its URL |
| 3 | `/seedance-auto-generate` | Submits just the video job (`generate_video_seedance`) from an image URL |
| **Full** | **`/ugc-video-auto`** | **This skill — runs the entire image→video pipeline end-to-end** |

You can use the individual skills separately, or invoke `/ugc-video-auto` to run everything in one go.
