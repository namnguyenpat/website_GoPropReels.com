# GUIDE: GoPropReels Definitive Workflow (v2.0)

This guide is the **Source of Truth** for managing [GoPropReels.com](file:///d:/Dropbox/@Code%20_offical/New_skills/website_GoPropReels.com). It covers data structure, UI standards, and the deployment pipeline.

## 1. Core Architecture
The site is built with **Astro Content Collections** for maximum performance and type safety.
-   **Coupons**: Data-driven `.json` files in `src/content/coupons/`.
-   **Blog**: Content-driven `.md` files in `src/content/blog/`.
-   **Schema**: Managed in `src/content/config.ts`. Validation happens during build.

## 2. Coupon Management (JSON)
Every deal must be a JSON file. Use the following schema:

```json
{
  "id": "firm-name-discount-code",
  "firm_name": "Apex Trader Funding",
  "category": "futures", 
  "discount_highlight": "80% OFF",
  "coupon_code": "APEX80",
  "theme_color": "#D4AF37",
  "features": ["1-Step Evaluation", "No Daily Drawdown"],
  "affiliate_link": "https://...",
  "firm_logo": "/images/logos/apex.svg",
  "seo_content": "<h3>High impact title</h3><p>Detailed review content...</p>",
  "created_at": "2026-02-19T20:00:00Z"
}
```

### Critical Rules:
1.  **Category Enum**: Must be exactly `"forex"` or `"futures"`. Other values will break the build.
2.  **ID Unicity**: The `id` string inside the JSON must match the filename exactly.
3.  **SEO Content**: Use HTML tags (`<h3>`, `<p>`, `<ul>`) for the deep-review section.

## 3. Blog Management (Markdown)
The blog is optimized for **Typographic Excellence** (No images).

### Frontmatter Template:
```markdown
---
title: "Article Title"
description: "Compelling 2-line summary."
pubDate: 2026-02-19
category: "News" 
tags: ["News", "Trading"]
---
```
-   **Category**: Must be `"News"` or `"Knowledge"`.
-   **No Hero Image**: Do not add `heroImage`. The layout is designed to be purely text-based for premium speed.

## 4. UI Layout Standards
-   **ReelCard**: Displays a `DynamicPoster` background.
-   **Detail Page**: Group of [CTA + Trust Signals] is placed directly under the Title.
-   **Logos**: Use original colored logos. No background pads or borders.

## 5. Deployment Pipeline
The website is synced via Git and deployed via Vercel.

### Steps to Deploy Changes:
1.  **Commit locally**:
    ```powershell
    git add .
    git commit -m "feat: new coupon added and content update"
    ```
2.  **Push to GitHub**:
    ```powershell
    git push origin main
    ```
3.  **Vercel Auto-Deploy**: Vercel monitors the GitHub repo and starts building immediately. Check the dashboard at [vercel.com](https://vercel.com) for status.

---
**Build Fix Tip**: If the Vercel build fails, run `npx astro sync` locally to catch schema errors before pushing.
