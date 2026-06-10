---
name: higgsfield-image-auto
description: Generate an AI image on Higgsfield via the official Higgsfield API (higgsfield-mcp server). Use when the user has an image prompt and wants to generate it on Higgsfield Soul or Seedream. Triggers on requests like "generate image on higgsfield", "create image", "auto-generate image", "make the image on higgsfield", or any request to submit an image generation job. Requires HF_API_KEY/HF_SECRET and consumes credits.
---

# Higgsfield Image Auto-Generate via the Higgsfield API

This skill generates an AI image through the official Higgsfield API, exposed via the bundled `higgsfield-mcp` server (MCP server name: `higgsfield`). It submits an asynchronous generation job, polls until it completes, and returns the finished image URL — no browser automation involved.

---

## Prerequisites

- The **higgsfield-automation** plugin is installed (it bundles the `higgsfield-mcp` server).
- `HF_API_KEY` and `HF_SECRET` are set in the environment. Get them at https://cloud.higgsfield.ai/api-keys.
- Run `debug_credentials` once to verify the credentials are loaded. If generation fails with an auth error, this is the first thing to check.
- Generation **consumes credits** (image 720p ~1.5 cr / ~$0.09, image 1080p ~3 cr / ~$0.19). Results are retained for 7 days.
- MCP tools may be **deferred** in this harness. Before first use, load them with `ToolSearch` — e.g. `ToolSearch(query: "select:generate_image,get_generation_status")` or a keyword search for `higgsfield`.

---

## Input Requirements

The user provides:
1. **A text prompt** for the image (or invoke `/ugc-hot-girl` first to generate one).

Optional:
- **Quality**: `1080p` (default) or `720p` — for `generate_image` (Soul model).
- **character_id**: register a face with `create_character` and pass its id for consistent characters across shots.
- **style_id**: from `list_styles` (or the `higgsfield://styles` resource).
- **Aspect ratio**: only available on the Seedream path (see Alternative below). The Soul `generate_image` tool has no `aspect_ratio` parameter.

---

## Primary Flow — Soul model (`generate_image`)

This is the default path. It is asynchronous: submit a job, get back a `job_set_id`, poll `get_generation_status` until `completed`.

### Step 1: Submit the generation job

```
generate_image(
  prompt: "<the image prompt>",
  quality: "1080p",          // or "720p"
  character_id: "<optional>", // for a consistent face
  style_id: "<optional>"      // from list_styles
)
→ returns { job_set_id }
```

**Confirm with the user before submitting** — this consumes credits.

### Step 2: Poll for completion

```
get_generation_status(job_set_id: "<job_set_id>")
→ returns { status, preview_url?, full_quality_url? }
```

Poll every few seconds. The `status` moves through:
- `queued` — accepted, waiting for a worker
- `in_progress` — rendering
- `completed` — done; `preview_url` and `full_quality_url` are populated
- `failed` — generation error (suggest retry / simpler prompt)
- `nsfw` — blocked by the safety filter (suggest revising the prompt)

### Step 3: Return the result

When `status == "completed"`, give the user the **`full_quality_url`** (use `preview_url` only for a quick thumbnail). If this is part of the UGC pipeline, note that they can now feed this URL into `/seedance-auto-generate` to animate it into a video.

---

## Alternative Flow — Seedream (`generate_image_seedream`)

Use this when the user wants a **specific aspect ratio**. The Soul `generate_image` tool cannot set aspect ratio; Seedream can. Seedream uses the "new API" and therefore polls with `get_request_status` (not `get_generation_status`).

### Step 1: Submit

```
generate_image_seedream(
  prompt: "<the image prompt>",
  aspect_ratio: "9:16",   // "1:1" | "16:9" | "9:16" | "4:3" | "3:4" (default 16:9)
  resolution: "1080p"     // "720p" | "1080p" (default 1080p)
)
→ returns { request_id }
```

### Step 2: Poll

```
get_request_status(request_id: "<request_id>")
→ returns { status, output_url? }
```

Statuses: `queued`, `in_progress`, `completed`, `failed`, `nsfw`, `cancelled`. When `completed`, return the output image URL.

`generate_image_reve` works the same way (also polls with `get_request_status`) and is another aspect-ratio-capable alternative.

---

## Error Handling

- **Auth error / 401**: Run `debug_credentials`. Ensure `HF_API_KEY` and `HF_SECRET` are exported and the plugin can see them.
- **`status: failed`**: The render errored. Suggest retrying or simplifying the prompt.
- **`status: nsfw`**: The safety filter blocked it. Suggest revising the prompt.
- **Tool not found**: The MCP tool wasn't loaded yet — run `ToolSearch` for it and retry.
- **Stuck in `queued`/`in_progress`**: Keep polling; image jobs usually finish in well under a minute.

---

## Pipeline Integration

This skill is step 2 of the UGC pipeline:

1. **`/ugc-hot-girl`** — Generates the character image prompt.
2. **`/higgsfield-image-auto`** ← You are here — generates the image via the Higgsfield API and returns its URL.
3. **`/seedance-auto-generate`** — Takes the image URL and animates it into a Seedance video.

### How the image flows to video

The `full_quality_url` returned by `get_generation_status` is a **public HTTPS URL**. You can pass it directly as the `image_url` argument to `generate_video_seedance` — no download or re-upload needed. That URL is what links image generation to video creation in the API workflow.
