---
name: gpt-image-ppt-creator
description: Create pure-image PowerPoint decks from a user idea, topic, brief, or outline using GPT Image 2 / Codex image generation. Use when the user wants Codex to confirm needed slide roles first, plan and confirm a PPT outline, confirm visual style, generate a style sheet, generate one full-slide image per page with strict role-specific density and consistency rules, enforce transition-slide master-template consistency, continue automatically after generation interruptions, and package images into a non-editable .pptx.
---

# GPT Image PPT Creator

## Purpose

Create image-only PowerPoint decks. Each PPT page contains exactly one generated full-slide image. Do not create editable PowerPoint text, charts, or shapes unless the user explicitly changes the requirement.

For Chinese conversations or Chinese decks, read `references/workflow-zh.md` first and treat it as the authoritative workflow guide. Keep this file ASCII-only for tool compatibility.

## Required Confirmation Gates

Do not skip these gates.

1. Confirm slide role types before drafting the outline.
   - Explain the common roles briefly: cover, agenda, transition/section, content, summary, closing.
   - Ask which roles the user wants to include or exclude.
   - If the user already specifies roles, restate the selected roles and proceed.
2. Draft the outline only after role selection is clear.
3. Ask the user to confirm or revise the outline.
4. Propose visual style directions only after the outline is confirmed.
5. Ask the user to confirm one style.
6. Generate a style confirmation sheet only after style confirmation.
7. Ask the user to confirm the style sheet before generating final pages.

## Slide Roles

Use these role labels in outlines and manifests:

- `cover`: cover/title slide
- `agenda`: agenda/table-of-contents slide
- `transition`: transition/section divider slide
- `content`: content slide
- `summary`: summary/conclusion slide
- `closing`: closing/thank-you slide

When presenting Chinese outlines to users, display Chinese role names from `references/chinese-role-copy.md`. Keep manifest role labels in English.

## Role Selection Logic

Before generating the outline:

- Ask the user which role types are needed.
- If the user is unsure, recommend `cover`, `agenda`, `content`, and `closing` as the minimal complete deck.
- Add `transition` only when the deck has clear sections and the user wants chapter breaks.
- Add `summary` when the deck is an academic defense, business report, research report, proposal, review, or decision document.

During outline drafting, check whether transition pages still make sense:

- If every main content heading has only one content slide, ask whether to remove transition pages.
- If the deck has three or more modules/sections, ask whether to remove transition pages to reduce page count and repetition.
- If both conditions are true, strongly recommend removing transition pages unless the user needs a formal chaptered deck.

## Outline Requirements

Each slide must include slide number, role, module or section name when applicable, main title, subtitle when useful, body points or key content, conclusion or takeaway when useful, and visual intent.

Before drafting the slide list, choose and record `content_title_mode`:

- Default: `topic-only`. Content slide `main_title` is the specific content topic without module number.
- User-requested: `module-plus-topic`. Content slide `main_title` is the module number plus module title, and `subtitle` is the specific content topic.

Use one mode across all content slides unless the user explicitly asks for mixed title hierarchy.

For agenda pages, list the main titles of later content modules or content pages. Keep agenda wording aligned with transition and content page titles.

Use `references/slide-manifest-schema.md` when creating `outline.json`.

## Information Density Rules

Use a deliberate density hierarchy:

`content` > `agenda` >= `cover` > `transition` and `closing`

### Cover Pages

Keep cover pages concise and clear. Include at most main title, secondary subtitle, and tertiary key phrase or short context. Do not expand the topic into many bullets or dense explanatory text. Do not render slide numbers, section numbers, or decorative number badges on cover pages unless the user explicitly asks for them.

### Agenda Pages

Use agenda pages to show the deck structure. Prioritize the main titles of subsequent content sections/pages. Optional secondary notes must be short. Agenda density may be equal to or slightly greater than the cover, but clearly lower than content slides. Agenda items are peer items by default: keep their typography, color, contrast, icon treatment, container style, and emphasis level consistent. Do not highlight the last item, lower-positioned items, or visually convenient items by default. Use contrast or accent-color emphasis on an agenda item only when the user or outline explicitly marks it as key, core, priority, focus, or current.

### Transition / Section Pages

Use transition pages only to introduce a section/module. Show one section title, such as `01 Background`, `II. Method Design`, or `3. Key Practice Scenarios`. Keep visual and text density lower than agenda and cover pages. Use at least 50% less information than content pages. Keep all transition pages stylistically similar, with only small differences in background, decorative imagery, and supporting elements.

When transition pages are included:

- Create one transition page for every agenda module unless the user explicitly confirms an omission.
- Generate the first transition page as the transition master template.
- After the first transition page is accepted, use it as the primary visual reference for every later transition page when the image tool supports image inputs.
- Later transition pages may change only the visible section number, section title, background imagery, and minor decorative/supporting elements.
- Do not change the title-area layout, number placement, number style, title baseline, title alignment, font family/style, font size, font color, glow/outline treatment, divider line, title container shape, title block proportions, main visual structure, or page whitespace.
- Reference the most recent accepted transition page as a secondary consistency reference when available.
- If a later transition page visibly drifts from the master template, regenerate that transition page before continuing.
- Do not let later transition pages drift into content-slide layouts.

### Content Pages

Use content pages for the real explanatory substance. Keep the main title in the upper-left corner. Keep main title position, size, style, and color treatment consistent across all content pages; only the text changes. Keep title styles consistent for related modules under the same section. Adapt body layout to the outline.

Content slide title hierarchy can use either of these deck-wide patterns:

- Default: use the specific content topic as the visible content-slide title, without the module number.
- User-requested alternative: use the module number plus module title as the primary title, and place the specific content topic as a secondary title.

Keep the chosen pattern consistent across all content slides. If a content slide uses only the module title, it must also include a specific content topic in `subtitle` or equivalent secondary title text. Do not mix numbered module-title pages and unnumbered topic-title pages in the same deck unless the user explicitly asks for that mixed hierarchy.

### Summary Pages

Use summary pages to synthesize conclusions, not introduce new detail. Present key conclusions, implications, recommendations, or answer to the core question. Use lower density than content pages.

### Closing Pages

Keep closing pages simple, similar in restraint to cover pages. Usually show only a short thank-you phrase, such as the Chinese phrases listed in `references/chinese-role-copy.md`. At most include deck title and subtitle. Do not add dense recap text unless the user explicitly requests it. Do not render slide numbers, section numbers, or decorative number badges on closing pages unless the user explicitly asks for them.

## Numbering Consistency

Select one numbering family and keep it unified across agenda, transition, and content titles:

- Chinese numerals: see `references/chinese-role-copy.md`
- Arabic numerals: `1. 2. 3.`
- Two-digit numerals: `01 02 03`

Do not mix numbering families within the same deck unless the user requests a hierarchy such as `01` for modules and `1.1` for subtopics.

Slide numbers in `outline.json` are internal sequencing metadata. Do not treat them as visible slide text. Only render numbers that are explicitly part of agenda, transition, or content title text.

## Image Generation Workflow

Use Codex's available GPT Image 2 / image generation capability directly when available. If only an OpenAI API path is exposed, use GPT Image 2 through the official image generation API and avoid unsupported parameters.

For the style confirmation sheet:

- Generate one 16:9 contact-sheet image containing 4-6 miniature slide previews.
- Include only roles selected by the user.
- Include representative roles such as cover, agenda, transition, content, summary, or closing only when they are part of the selected deck.
- Ask the user to approve or revise the style sheet.

For final slide images:

- Generate one complete 16:9 presentation slide image per page.
- Save files as `slide-001.png`, `slide-002.png`, etc.
- Use the approved style sheet as visual reference when the tool supports image input.
- Repeat the confirmed style rules in every prompt.
- Include the exact text that should appear on that slide.
- Require crisp, correctly spelled text large enough for projection.
- Do not render the internal slide number. For cover and closing slides, do not render any visible numeric badge unless it appears in the exact slide text approved by the user.
- For agenda slides, render all agenda items as equivalent by default. Do not emphasize any single item unless it is explicitly marked as highlighted in the outline or user request.
- For transition slides, use the first accepted transition page as the master template. Later transition slides should change only the number, title, background imagery, and minor decorations; keep title-area layout, number style, title typography, and main visual structure unchanged.
- For content slides, keep the visible title hierarchy consistent across the whole deck. Default to unnumbered specific topic titles; if the user asks for module-number titles, use the module title as the primary title and the specific topic as a secondary title on every content slide.

When transition pages are part of the deck, generate and review the first transition page before generating any later transition pages. Do not batch-generate all transition pages without a master template reference.

Read `references/visual-prompting.md` when writing prompts.

## Interruption Recovery

Long generation runs often fail after many pages. Make progress resumable.

Before final page generation, create or update `generation-state.json` with total slide count, output directory, completed slide numbers, failed slide numbers, and next slide number.

During generation:

- After each successful image, update `generation-state.json`.
- If generation stops and the user has not changed instructions, resume automatically from the first missing slide.
- Before resuming, inspect the slide image directory and skip existing valid `slide-###` files.
- Continue until all expected images exist, then package the deck.

If the user sends a new instruction during interruption, apply the newest instruction instead of blindly resuming.

## Source Image Authority

Treat the first approved final slide image directory as the source of truth. By default this is `slides/`.

- Package the PPTX directly from `slides/` after all expected images exist.
- Do not create derived directories such as `slides-final/`, `slides-rendered/`, or `slides-processed/`.
- Do not redraw text, overlays, panels, masks, or layout elements with PIL, canvas, HTML screenshots, or other local rendering after GPT Image has produced acceptable slide images.
- A contact-sheet preview is allowed only for review. Never use the preview or a post-processed preview directory as the PPTX source.
- If readability problems are found, ask whether to regenerate affected pages with GPT Image or package the existing approved images. Do not replace approved images with locally redrawn pages.

## File Conventions

Create a working folder for each deck. Store `outline.json`, `style.md`, `style-confirmation.png`, `generation-state.json`, `slides/slide-001.png`, and `deck.pptx`. Use `slides/` as the source directory for packaging.

Use `scripts/validate_manifest.py` before final generation when an `outline.json` exists.

## Packaging

Install packaging dependencies when needed:

```bash
python -m pip install -r scripts/requirements.txt
```

Package final slide images:

```bash
python scripts/images_to_pptx.py --images <slides-dir> --output <deck.pptx>
```

The script creates one 16:9 PPT slide per image and stretches each image to fill the slide.

## References

- Read `references/workflow-zh.md` first when the user works in Chinese or asks for a Chinese deck.
- Read `references/slide-manifest-schema.md` when creating or validating `outline.json`.
- Read `references/visual-prompting.md` when writing style-sheet or final slide prompts.
- Read `references/generation-state.md` when resuming interrupted generation.
- Read `references/chinese-role-copy.md` when presenting Chinese slide roles, section numbering, and closing phrases.
