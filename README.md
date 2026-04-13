# **Claude Code + Higgsfield — The Complete UGC Pipeline**

Automate the entire UGC ad creation workflow: character generation, image creation, and video production. No tab switching, no copy-pasting, no manual clicking. One command, full pipeline.

---

## **Overview**

Claude Code is an AI assistant that runs in your terminal. Combined with **Playwright MCP** (a tool that gives Claude control over a real browser) and a library of **custom skills**, it can:

- Generate photorealistic UGC character images on Higgsfield
- Automatically select those images for video creation
- Write production-grade Seedance 2.0 video prompts
- Click Generate and monitor the result

You define your workflow once. Claude reads it every session. That's it.

---

## **What You Get**

### **21 Custom Skills**

| Category | Skills | What They Do |
|---|---|---|
| **UGC Pipeline** | `/ugc-hot-girl`, `/higgsfield-image-auto`, `/ugc-video-auto` | End-to-end UGC ad creation — character image → video |
| **Video Automation** | `/seedance-auto-generate` | Automates Seedance 2.0 video generation via Playwright |
| **Creative Styles** | `/01-cinematic` through `/05-fight-scenes`, `/08-anime-action` | 6 artistic style prompt generators |
| **Commercial** | `/06-motion-design-ad`, `/07-ecommerce-ad`, `/09-product-360`, `/11-social-hook`, `/12-brand-story` | 5 marketing-focused prompt generators |
| **Industry** | `/10-music-video`, `/13-fashion-lookbook`, `/14-food-beverage`, `/15-real-estate` | 4 vertical-specific prompt generators |

Every prompt skill generates **15-25 line production prompts** with 2-second hooks, camera movements, lighting, sound design, and platform optimization.

---

## **Requirements**

- Mac or Windows
- VS Code, Cursor, or any terminal
- Chrome installed
- A Higgsfield account (free tier works)
- Node.js

---

## **Setup**

### **Step 1: Install Node.js**

**Mac:**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js
brew install node
```

**Windows:**

Download from [nodejs.org](https://nodejs.org) or use winget:
```powershell
winget install OpenJS.NodeJS
```

Verify:
```bash
node --version
npm --version
```

### **Step 2: Install Claude Code**

```bash
npm install -g @anthropic-ai/claude-code
```

Start it:
```bash
claude
```

### **Step 3: Install Playwright MCP**

This is the critical piece. Playwright MCP gives Claude the ability to control a real browser — clicking, typing, navigating — without you touching the keyboard.

```bash
claude mcp add playwright npx '@playwright/mcp@latest'
```

You should see:
```
Added stdio MCP server playwright with command: npx @playwright/mcp@latest to local config
```

Restart Claude and verify:
```bash
exit
claude
/mcp
```

You should see `playwright` listed. If it's missing, re-run the install command and restart.

> **Why a separate browser?** Playwright opens its own controlled browser window, not your personal Chrome. This is normal and expected.

### **Step 4: Install the Skills**

Clone this repo into your project:

```bash
git clone https://github.com/AKCodez/higgsfield-claude-skills
```

Copy all skills into your project's `.claude/skills/` directory:

```bash
mkdir -p .claude/skills
cp -r higgsfield-claude-skills/* .claude/skills/
rm .claude/skills/README.md  # Don't need the readme in skills
```

All 19 skills are included — 15 prompt generators + 4 automation skills:

```
.claude/skills/
├── 01-cinematic/SKILL.md          # Cinematic film prompts
├── 02-3d-cgi/SKILL.md             # 3D CGI prompts
├── 03-cartoon/SKILL.md            # Cartoon & animation prompts
├── 04-comic-to-video/SKILL.md     # Comic to video prompts
├── 05-fight-scenes/SKILL.md       # Action & fight prompts
├── 06-motion-design-ad/SKILL.md   # SaaS/software ad prompts
├── 07-ecommerce-ad/SKILL.md       # E-commerce product ad prompts
├── 08-anime-action/SKILL.md       # Anime style prompts
├── 09-product-360/SKILL.md        # Product turntable prompts
├── 10-music-video/SKILL.md        # Music video prompts
├── 11-social-hook/SKILL.md        # Viral social hook prompts
├── 12-brand-story/SKILL.md        # Brand narrative prompts
├── 13-fashion-lookbook/SKILL.md   # Fashion lookbook prompts
├── 14-food-beverage/SKILL.md      # Food & beverage prompts
├── 15-real-estate/SKILL.md        # Real estate tour prompts
├── seedance-auto-generate/SKILL.md   # Video generation automation
├── higgsfield-image-auto/SKILL.md    # Image generation automation
├── ugc-hot-girl/SKILL.md             # UGC character prompt generator
└── ugc-video-auto/SKILL.md           # Full UGC pipeline orchestrator
```

### **Step 5: Create Your CLAUDE.md**

This file lives in your project root. Claude reads it automatically every session.

```markdown
# Higgsfield UGC Pipeline

## Tools
- Image generation: Higgsfield Soul 2.0 (/image/soul-v2)
- Video generation: Seedance 2.0 (/create/video?model=seedance_2_0)
- UGC Factory: /lipsync-studio?ugc-studio=true

## Default Image Settings
- Model: Soul 2.0
- Aspect ratio: 3:4 (portrait for UGC characters)
- Resolution: 2K
- Count: 1

## Default Video Settings
- Model: Seedance 2.0
- Duration: 8s
- Ratio: 9:16 (vertical for TikTok/Reels)
- Resolution: 720p

## Workflow Rules
- Always clear the prompt bar via JS before typing a new prompt
- Always screenshot after clearing to confirm it's empty
- Always ask for confirmation before clicking Generate (costs credits)
- Use @image1 in video prompts to reference the uploaded image
- For batch runs, update SESSION-RESUME.md after each generation

## Pipeline Order
1. /ugc-hot-girl → generates character image prompt
2. /higgsfield-image-auto → creates the image on Higgsfield
3. /seedance-auto-generate or /ugc-video-auto → creates the video
```

---

## **The UGC Pipeline**

This is the main workflow. Three skills, one pipeline.

### **Step 1: Generate the Character Prompt**

```
/ugc-hot-girl

"I need a girl for my skincare brand, early 20s, beauty/wellness vibe"
```

Claude generates a detailed image prompt optimized for Soul 2.0:

```
Attractive young woman, early 20s, clear dewy skin, dark brown hair
in messy bun with loose face-framing pieces. Healthy natural complexion,
no visible makeup, fresh-faced morning look. Excited expression, eyes
wide with delight. Wearing oversized white cotton tee, thin gold chain
necklace. Soft ring light illumination, even facial lighting, bright
catchlights in both eyes. Tight close-up, face fills most of frame.
Clean white bathroom background, slightly blurred. Photorealistic, 4K,
ultra detailed skin texture with visible pores, natural dewy finish
```

### **Step 2: Generate the Image**

```
/higgsfield-image-auto

Use that prompt to generate the image on Soul 2.0
```

Claude opens Higgsfield, navigates to `/image/soul-v2`, types the prompt, and clicks Generate. The image appears in your History grid in ~15 seconds.

### **Step 3: Create the UGC Video**

```
/ugc-video-auto

Take that image and create a UGC testimonial video, skincare product, 9:16 for TikTok
```

Or run the whole thing in one shot:

```
/ugc-video-auto

Create a UGC ad video with an attractive girl promoting my new vitamin C serum.
TikTok format, testimonial style.
```

Claude will:
1. Generate the character image on Soul 2.0
2. Navigate to the Seedance 2.0 video page
3. Open the upload dialog → click "Image Generations" tab
4. Select the most recent image
5. Clear the old prompt, type a UGC video prompt
6. Set ratio to 9:16
7. Ask for your confirmation, then click Generate

---

## **Using the Prompt Skills**

The 15 prompt engineering skills turn Claude into a specialized director for each video style. Each one generates large, production-grade Seedance 2.0 prompts with:

- **2-second hook framework** — scroll-stopping openers
- **Timeline segmentation** — beat-by-beat breakdown up to 15s
- **Camera movement encyclopedia** — 15-20+ techniques
- **Lighting & atmosphere** — mood-setting setups
- **Sound design** — ambient, foley, music guidance
- **5+ example prompts** — 15-25 lines each, ready to use

### **Example: Real Estate Video**

```
/15-real-estate

Create a video for this luxury modern home [attach image]
```

Claude generates a cinematic real estate prompt, then `/seedance-auto-generate` handles the automation.

### **Example: E-Commerce Product Ad**

```
/07-ecommerce-ad

TikTok ad for my new wireless earbuds, premium feel, unboxing style
```

### **Example: Anime Fight Scene**

```
/08-anime-action

Turn this character art into a shonen-style battle scene [attach image]
```

---

## **The Prompt Bar Fix**

**This is the most important technical detail.** When running batches, the Higgsfield prompt bar (a Lexical contenteditable editor) doesn't clear properly between generations. Text from the previous prompt bleeds into the next one.

The fix is to always clear via JavaScript before typing:

### **Image Generation Page** (`/image/*`)

The image page uses a standard input:
```javascript
// Find and clear the image prompt textbox
const input = document.querySelector('[id="hf:tour-image-prompt"]');
input.value = '';
input.dispatchEvent(new Event('input', { bubbles: true }));
```

### **Video Creation Page** (`/create/video`)

The video page uses a **Lexical rich text editor** (contenteditable):
```javascript
// Clear the Lexical editor
const editor = document.querySelector('[data-lexical-editor]');
editor.focus();
document.execCommand('selectAll');
document.execCommand('delete');
```

Or the keyboard approach (more reliable):
1. Focus the editor via `browser_evaluate`
2. Press `Ctrl+A` to select all
3. Press `Backspace` to delete
4. Take a screenshot to verify it's empty

### **Per-Prompt Workflow**

1. Run the JS clear snippet
2. Screenshot and confirm the bar is empty
3. If not empty, clear again and re-verify
4. Type the prompt (use `slowly: true` for the video Lexical editor)
5. Click Generate
6. Run JS clear immediately after Generate
7. Wait 7 seconds
8. Repeat

Add this to your CLAUDE.md so Claude never skips it.

---

## **Key Technical Details**

### **How Image → Video Selection Works**

You don't need to download and re-upload images. Higgsfield's internal asset system connects them:

1. Generate an image on `/image/soul-v2`
2. Navigate to `/create/video?model=seedance_2_0`
3. Click the upload area → dialog opens
4. Click **"Image Generations"** tab
5. Your most recent image is the **first item** (shows as "Check eligibility" button)
6. Click it → transforms to selected state (green checkmark)
7. Press Escape → image loads into the video form

**No file download needed.**

### **Model URLs**

| Model | URL Path |
|---|---|
| Soul 2.0 (best for portraits) | `/image/soul-v2` |
| Soul Cinema | `/image/soul-cinematic` |
| Nano Banana Pro (best 4K) | `/image/nano-banana-pro` |
| Nano Banana 2 (fast) | `/image/nano-banana-2` |
| Seedream 5.0 lite | `/image/seedream_v5_lite` |
| GPT Image 1.5 | `/image/openai_hazel` |
| Grok Imagine | `/image/grok_image` |
| FLUX.2 | `/image/flux_2` |
| Seedance 2.0 (video) | `/create/video?model=seedance_2_0` |

### **Element Patterns**

Playwright uses accessibility snapshots to find elements. These patterns help:

| Element | How to Find |
|---|---|
| Image prompt bar | `textbox` with ID `hf:tour-image-prompt` |
| Video prompt bar | `[data-lexical-editor]` contenteditable div |
| Generate button (image) | `button "Generate XXXX free gens left"` |
| Generate button (video) | `button "Generate XX XX"` with credit cost |
| Upload dialog | `dialog` after clicking the upload area |
| Image Generations tab | `button "Image Generations"` in dialog |

---

## **Crash Recovery**

Claude Code sessions can crash mid-batch. Use a `SESSION-RESUME.md` file:

```markdown
# Session Resume

## Current Task
UGC batch for skincare brand

## Model
Soul 2.0 for images, Seedance 2.0 for video

## Settings
- Image: 3:4, 2K
- Video: 9:16, 8s, 720p

## Progress

| # | Character | Image | Video | Status |
|---|-----------|-------|-------|--------|
| 1 | Beauty girl, dewy skin | ✓ Generated | ✓ Generated | Done |
| 2 | Fitness girl, athletic | ✓ Generated | Pending | In Progress |
| 3 | Luxury girl, editorial | Pending | Pending | Queued |

## Next: #2 — video generation step
```

If Claude crashes:
```
Read SESSION-RESUME.md and continue from where we left off.
```

---

## **Example Workflows**

### **Single UGC Ad (fastest)**

```
/ugc-video-auto

Create a UGC testimonial video. Girl promoting a vitamin C serum.
Casual bathroom setting, TikTok vertical.
```

### **Batch UGC Characters (image only)**

```
Generate 5 different UGC girl characters using /ugc-hot-girl and /higgsfield-image-auto:
1. Beauty/skincare type — dewy, fresh-faced
2. Fitness type — athletic, post-workout glow
3. Fashion type — editorial, confident
4. Lifestyle type — casual, girl-next-door
5. Luxury type — elegant, minimal glam

Use Soul 2.0, 3:4 portrait, 2K. Update SESSION-RESUME.md after each.
```

### **Product Video with Custom Style**

```
/07-ecommerce-ad

Create an e-commerce ad for wireless earbuds. Premium unboxing feel.
Then use /seedance-auto-generate to make the video with that prompt.
```

### **Real Estate Tour**

```
/15-real-estate

Create a cinematic property tour video for this house photo.
Use Seedance 2.0, 16:9 landscape, 10 second duration.
```

---

## **Common Issues**

| Issue | Fix |
|---|---|
| `/mcp` doesn't show playwright | Re-run the install command and restart Claude |
| Claude opens a new browser window | Normal — Playwright uses its own controlled browser |
| Prompt bar not clearing between prompts | Add the JS clear to your CLAUDE.md workflow. Claude skips it if not explicit |
| Image doesn't load into video form | After clicking the image in the dialog, make sure it shows a green checkmark before pressing Escape |
| "Check eligibility" doesn't transform | The image may not be compatible. Try regenerating or using a different image |
| Lexical editor won't accept typed text | Use `slowly: true` flag. The Lexical editor needs keypress events, not fill |
| Image prompt bar missing | Intermittent platform bug. Refresh the page and retry |
| Session crashed mid-batch | Use SESSION-RESUME.md — tell Claude to read it and continue |
| Not logged in | Log in manually in the Playwright browser window, or run `! open https://higgsfield.ai` |

---

## **Skills Reference**

### **Pipeline Skills (Automation)**

| Slash Command | Description |
|---|---|
| `/ugc-hot-girl` | Generates detailed image prompts for attractive female UGC characters. Covers beauty, fitness, fashion, luxury, and diverse variants |
| `/higgsfield-image-auto` | Playwright automation for Higgsfield image generation. Supports all models (Soul 2.0, Nano Banana, etc.) |
| `/seedance-auto-generate` | Playwright automation for Seedance 2.0 video generation from a local image file |
| `/ugc-video-auto` | Full end-to-end pipeline — image generation → image selection → video prompt → video generation |

### **Prompt Engineering Skills (15 styles)**

| Slash Command | Style | Best For |
|---|---|---|
| `/01-cinematic` | Cinematic Film | Dramatic lighting, anamorphic, noir, epic |
| `/02-3d-cgi` | 3D CGI | Pixar, Unreal Engine, ray tracing |
| `/03-cartoon` | Cartoon & Animation | Cel-shaded, hand-drawn, vector, watercolor |
| `/04-comic-to-video` | Comic to Video | Manga, webtoons, storyboards, graphic novels |
| `/05-fight-scenes` | Fight & Action | Martial arts, chase scenes, superhero battles |
| `/06-motion-design-ad` | Motion Design Ad | SaaS launches, feature showcases, app promos |
| `/07-ecommerce-ad` | E-Commerce Ad | Product ads, fashion, beauty, TikTok Shop |
| `/08-anime-action` | Anime | Shonen, mecha, magical girl, anime openings |
| `/09-product-360` | Product 360° | Turntable, multi-angle, product reveal |
| `/10-music-video` | Music Video | Beat-synced, performance, concert visuals |
| `/11-social-hook` | Social Hook | TikTok, Reels, Shorts, scroll-stopping hooks |
| `/12-brand-story` | Brand Story | Origin stories, company culture, founder stories |
| `/13-fashion-lookbook` | Fashion Lookbook | Model walks, outfit showcases, runway clips |
| `/14-food-beverage` | Food & Beverage | Restaurant promos, recipe content, food ASMR |
| `/15-real-estate` | Real Estate | Property tours, architecture, interior design |

> Prompt skills adapted from [beshuaxian/higgsfield-seedance2-jineng](https://github.com/beshuaxian/higgsfield-seedance2-jineng). Automation skills (pipeline, image auto, video auto, UGC) created by [@AKCodez](https://github.com/AKCodez).

---

## **The Core Idea**

`CLAUDE.md` defines the rules. Skills define the expertise. Playwright gives Claude hands.

Instead of:

> Idea → write prompt → open Higgsfield → paste → configure settings → generate → wait → download → open video page → upload → write video prompt → configure → generate → wait

You get:

> **Idea → Claude → done**

Define it once. Run it forever.
