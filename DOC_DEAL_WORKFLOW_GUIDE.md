# GUIDE: GoPropReels Coupon Workflow

This guide explains the "Premium Reel" architecture of [GoPropReels.com](file:///d:/Dropbox/@Code%20_offical/New_skills/website_GoPropReels.com). It serves as the source of truth for AI agents creating or updating coupons.

## 1. Core Architecture
GoPropReels follows a **Data-Driven Architecture** using **Astro Content Collections**:
-   **Source of Truth**: Every coupon is its own `.json` file in [src/content/coupons/](file:///d:/Dropbox/@Code%20_offical/New_skills/website_GoPropReels.com/src/content/coupons/).
-   **Dynamic Rendering**: The route `coupons/[id].astro` automatically renders a landing page using data from the collection.
-   **AI Writing**: Agents must create a NEW JSON file for every deal, ensuring unique content in the `seo_content` field.

## 2. The "Reel" Aesthetic
The UI is built on a **Premium Dark/Carbon** theme.
-   **Card (ReelCard.astro)**: Compact, 9/16 aspect ratio, clean typography, stable background (no zoom on hover).
-   **Poster (DynamicPoster.astro)**: High-impact animated visual using CSS/SVG filters. Features:
    -   **Branding**: Logo at top.
    -   **Highlight**: Large, single-line discount (e.g., "80% OFF").
    -   **Context**: Category tag (e.g., "FUTURES") and Key Benefit (e.g., "1-STEP EVALUATION").
    -   **Transitions**: Smooth vertical slide-up (12px) on hover.

## 3. Coupon Data Structure (JSON)

When creating a new coupon file (e.g., `src/content/coupons/[id].json`), ensure these fields are populated:

```json
{
  "id": "unique-id-matches-filename",
  "firm_name": "Apex Trader Funding",
  "category": "futures",
  "discount_highlight": "80% OFF",
  "title": "Unique High-Impact Title (Critical for Conversion)",
  "description": "Unique 2-line teaser (Must be attractive, not generic).",
  "coupon_code": "APEX80",
  "expiration_date": "2026-03-01",
  "theme_color": "#D4AF37",
  "features": [
    "Feature 1",
    "Feature 2"
  ],
  "affiliate_link": "https://link.com",
  "seo_content": "<h3>HTML Title</h3><p>Persuasive article...</p>",
  "firm_logo": "/images/logos/filename.svg",
  "created_at": "2026-02-18T23:00:00.000Z"
}
```

## 4. Step-by-Step Workflow for New Coupons

### Step 1: Logo Acquisition
-   Check the [AI Agent Assets](file:///d:/Dropbox/@Code%20_offical/New_skills/website_AI_agent/public/logos/) for the firm's SVG logo.
-   **CRITICAL**: Use the **ORIGINAL** logo file. Do not redraw.
-   Copy to `website_GoPropReels.com/public/images/logos/[firm-slug].svg`.

### Step 2: Create Collection File
-   Create a new file in `src/content/coupons/`. Filename should be the `id`.
-   Fill out all fields. 
-   **Pro Tip**: Update the `created_at` to the current time to push it to the top.

### Step 3: AI Content Writing
-   Write the detailed article directly into the `seo_content` field using **HTML**.
-   **Prompt for AI**: "Write a high-converting, SEO-optimized landing page content for [Firm Name] [Discount]. Use <h3> for subheaders. Tone: Stoic, professional, and urgent."

### Step 4: Verification
-   **Home Card**: Check for text wrapping in `discount_highlight`. (Should be 1 line).
-   **Detail Page**: Verify [localhost:4322/coupons/[id]](http://localhost:4322/coupons/...) renders with the new the high-conversion layout.

## 5. UI Standardization Rules
1.  **Alignment**: Keep discount text on one line (`white-space: nowrap`).
2.  **Truncation**: Card descriptions are limited to 2 lines (`line-clamp-2`).
3.  **Stability**: NEVER re-introduce `scale-105` on card hover. 
4.  **Premium Colors**: Use curated accent colors (Gold, Cyber Blue, Ruby Red).
