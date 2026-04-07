"""
generate_content.py  — gopropreels.com
=======================================
Input ý tưởng → AI tạo coupon JSON hoặc blog MD → lưu file

Cách dùng:
  python generate_content.py

Yêu cầu:
  pip install openai python-dotenv requests
  File .env phải có CHIASEGPU_CLAUDE_KEY và CHIASEGPU_BASE_URL
"""

import os
import sys
import re
import json
import time
import random
import string
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    from dotenv import load_dotenv
    import requests as _requests
except ImportError:
    print("Thiếu thư viện. Chạy: pip install python-dotenv requests")
    sys.exit(1)

# ── Đường dẫn gốc ────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent
ENV_PATH     = PROJECT_ROOT / ".env"

OUTPUT_COUPONS = PROJECT_ROOT / "src" / "content" / "coupons"
OUTPUT_BLOG    = PROJECT_ROOT / "src" / "content" / "blog"
AFFILIATE_FILE = PROJECT_ROOT / "affiliate_links.json"

# ── Load .env ─────────────────────────────────────────────────────────────────
if not ENV_PATH.exists():
    print(f"Không tìm thấy .env tại: {ENV_PATH}")
    sys.exit(1)

load_dotenv(ENV_PATH, override=True)

_PROVIDERS = {
    "chiasegpu-claude-sonnet-4.6": {
        "api_key":  os.getenv("CHIASEGPU_CLAUDE_KEY", ""),
        "base_url": os.getenv("CHIASEGPU_BASE_URL", "https://llm.chiasegpu.vn/v1"),
        "model":    os.getenv("CHIASEGPU_CLAUDE_MODEL", "claude-sonnet-4.6"),
    },
    "chiasegpu-claude-opus-4.6": {
        "api_key":  os.getenv("CHIASEGPU_OPUS_KEY", ""),
        "base_url": os.getenv("CHIASEGPU_BASE_URL", "https://llm.chiasegpu.vn/v1"),
        "model":    os.getenv("CHIASEGPU_OPUS_MODEL", "claude-opus-4.6"),
    },
    "chiasegpu-gemini-3-flash-preview": {
        "api_key":  os.getenv("CHIASEGPU_GEMINI_FLASH_KEY", ""),
        "base_url": os.getenv("CHIASEGPU_BASE_URL", "https://llm.chiasegpu.vn/v1"),
        "model":    os.getenv("CHIASEGPU_GEMINI_FLASH_MODEL", "gemini-3-flash-preview"),
    },
    "chiasegpu-gpt-5.4": {
        "api_key":  os.getenv("CHIASEGPU_GPT54_KEY", ""),
        "base_url": os.getenv("CHIASEGPU_BASE_URL", "https://llm.chiasegpu.vn/v1"),
        "model":    os.getenv("CHIASEGPU_GPT54_MODEL", "gpt-5.4"),
    },
    "openclaude-gemini-3.1-pro-preview": {
        "api_key":  os.getenv("OPENCLAUDE_API_KEY", ""),
        "base_url": os.getenv("OPENCLAUDE_BASE_URL", "https://open-claude.com/v1"),
        "model":    os.getenv("OPENCLAUDE_GEMINI_PRO_MODEL", "gemini-3.1-pro-preview"),
    },
    "deepseek-deepseek-chat": {
        "api_key":  os.getenv("DEEPSEEK_API_KEY", ""),
        "base_url": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        "model":    os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
    },
}

_provider_name = os.getenv("PROVIDER", "chiasegpu-claude-sonnet-4.6")
_active = _PROVIDERS.get(_provider_name)
if not _active:
    print(f"PROVIDER '{_provider_name}' không hợp lệ. Chọn một trong: {list(_PROVIDERS)}")
    sys.exit(1)
if not _active["api_key"]:
    print(f"API key cho '{_provider_name}' trống. Kiểm tra .env")
    sys.exit(1)

MODEL    = _active["model"]

_FALLBACK_CHAIN = [
    "chiasegpu-claude-opus-4.6",
    "chiasegpu-claude-sonnet-4.6",
    "chiasegpu-gemini-3-flash-preview",
    "openclaude-gemini-3.1-pro-preview",
    "deepseek-deepseek-chat",
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def random_suffix(n=5) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")

def load_affiliate_links() -> dict[str, str]:
    """Load affiliate_links.json → {firm_name_lower: affiliate_link}"""
    if not AFFILIATE_FILE.exists():
        return {}
    with open(AFFILIATE_FILE, encoding="utf-8") as f:
        data = json.load(f)
    result = {}
    for entry in data:
        key = entry.get("firm_name", "").lower().strip()
        result[key] = entry.get("affiliate_link", "")
    return result

# ── API call ──────────────────────────────────────────────────────────────────
MAX_RETRIES = 3
CALL_DELAY  = 5

def call_api(system: str, user: str, api_key: str, model: str, base_url: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "gopropreels-generator/1.0",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        "temperature": 0.7,
        "max_tokens": 6000,
        "stream": True,
    }
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            chunks = []
            with _requests.post(
                f"{base_url.rstrip('/')}/chat/completions",
                headers=headers,
                json=payload,
                stream=True,
                timeout=(10, 120),
            ) as resp:
                if not resp.ok:
                    raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:300]}")
                for line in resp.iter_lines():
                    if not line:
                        continue
                    line = line.decode("utf-8") if isinstance(line, bytes) else line
                    if not line.startswith("data: "):
                        continue
                    data_str = line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        delta = json.loads(data_str)["choices"][0].get("delta", {})
                        token = delta.get("content")
                        if token:
                            chunks.append(token)
                            print(token, end="", flush=True)
                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue
            print()
            content = "".join(chunks).strip()
            if not content:
                raise ValueError("Empty response (no tokens received)")
            time.sleep(CALL_DELAY)
            return content
        except Exception as e:
            print(f"\n  [retry {attempt}/{MAX_RETRIES}] {type(e).__name__}: {str(e)[:100]}")
            if attempt < MAX_RETRIES:
                time.sleep(CALL_DELAY * attempt)
            else:
                raise

def call_api_with_fallback(system: str, user: str) -> tuple[str, str, str]:
    providers_to_try = [_provider_name] + [p for p in _FALLBACK_CHAIN if p != _provider_name]
    last_err = None
    for pname in providers_to_try:
        cfg = _PROVIDERS.get(pname)
        if not cfg or not cfg["api_key"]:
            continue
        print(f"\n  → Dung provider: {pname} ({cfg['model']})")
        try:
            content = call_api(system, cfg["api_key"], cfg["model"], cfg["base_url"]) if False else \
                      call_api(system, user, cfg["api_key"], cfg["model"], cfg["base_url"])
            return content, cfg["model"], pname
        except Exception as e:
            print(f"  [fallback] {pname} that bai: {str(e)[:120]}")
            last_err = e
            time.sleep(CALL_DELAY)
    raise RuntimeError(f"Tat ca provider deu that bai. Loi cuoi: {last_err}")

# ── System prompts ────────────────────────────────────────────────────────────
SYSTEM_COUPON = """You are an expert prop trading content writer for gopropreels.com, a prop firm coupon aggregator.

Your job is to generate accurate, compelling coupon entries for prop trading firms.
You write in English only. Your audience is retail traders looking for the best deals.
Your style is direct, factual, and trader-focused — no hype, no vague claims.

CRITICAL JSON OUTPUT RULES:
- Output ONLY a valid JSON object. No markdown fences, no explanation, no preamble.
- seo_content must be a valid JSON string with escaped quotes, no raw newlines inside the string value.
- Use \\n between HTML paragraphs within the seo_content string if needed, but ensure it's valid JSON.
- All HTML in seo_content must use only: <h3>, <p>, <b>, <ul>, <li> tags.
- Never invent coupon codes — use the code provided by the user or mark as [VERIFY].
- Keep affiliate_link exactly as provided by the user — never modify it."""

SYSTEM_BLOG = """You are an expert prop trading content writer for gopropreels.com.

You write informative, SEO-optimized blog posts about prop trading in English only.
Your audience is retail traders at beginner-to-intermediate level.
Your style is authoritative, practical, and concrete — no filler, no vague advice.
Output ONLY the completed markdown file content. No explanation, no preamble."""

# ── Coupon generator (2-call chunked) ────────────────────────────────────────
def generate_coupon_chunked(idea: str, affiliate_links: dict) -> dict:
    """
    Call 1: Generate coupon metadata (JSON skeleton)
    Call 2: Generate full seo_content HTML
    Returns merged dict ready to save as .json
    """
    # Build affiliate hint
    firm_hint = ""
    for firm_key, link in affiliate_links.items():
        if any(word in idea.lower() for word in firm_key.split()):
            firm_hint = f"\nKnown affiliate link for this firm: {link}"
            break

    # ── Call 1: Metadata skeleton ──────────────────────────────────────────
    print(f"\n[1/2] Goi API ({MODEL}) — coupon metadata...")
    meta_prompt = f"""User brief for this coupon:
<brief>
{idea}
</brief>
{firm_hint}

OUTPUT ONLY a JSON object with these exact keys:
{{
  "firm_name": "Exact firm name as displayed on their website",
  "canonical_slug": "lowercase-hyphenated firm slug (e.g. 'ftmo', 'funded-next')",
  "category": "forex",
  "discount_highlight": "e.g. '30% OFF' or 'FREE TRIAL'",
  "title": "SEO title, 50-60 chars",
  "description": "Meta description, 120-155 chars",
  "coupon_code": "EXACT code or [VERIFY]",
  "expiration_date": "YYYY-MM-DD or null",
  "theme_color": "#hexcolor (firm brand color, best guess)",
  "features": ["feature 1", "feature 2", "feature 3", "feature 4", "feature 5"],
  "affiliate_link": "paste the affiliate link provided above, or leave empty string",
  "firm_logo": "/images/logos/[canonical_slug].svg",
  "youtube_metadata": {{
    "title": "YouTube video title for this coupon (under 70 chars)",
    "description": "YouTube video description (2 sentences, under 200 chars)"
  }}
}}

Rules:
- category must be "forex" or "futures"
- features: 5 concrete trader benefits (profit split %, platforms, drawdown rules, etc.)
- theme_color: use the firm's known brand color or a reasonable guess
- If affiliate_link is not provided and not in the brief, leave as empty string"""

    meta_raw, _m, _p = call_api_with_fallback(SYSTEM_COUPON, meta_prompt)
    meta_raw = re.sub(r"^```(?:json)?\s*", "", meta_raw.strip())
    meta_raw = re.sub(r"\s*```$", "", meta_raw.strip())
    try:
        meta = json.loads(meta_raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Call 1 JSON parse error: {e}\nRaw: {meta_raw[:500]}")

    firm_name = meta.get("firm_name", "Unknown Firm")
    canonical_slug = meta.get("canonical_slug", slugify(firm_name))
    coupon_code = meta.get("coupon_code", "[VERIFY]")
    discount_highlight = meta.get("discount_highlight", "")
    affiliate_link = meta.get("affiliate_link", "")

    # ── Call 2: seo_content HTML ───────────────────────────────────────────
    print(f"\n[2/2] Goi API ({MODEL}) — seo_content HTML...")
    seo_prompt = f"""Write the seo_content HTML for this prop firm coupon page:

Firm: {firm_name}
Coupon code: {coupon_code}
Discount: {discount_highlight}
Category: {meta.get('category', 'forex')}
Features: {', '.join(meta.get('features', []))}
Affiliate link: {affiliate_link}

OUTPUT ONLY a JSON object with one key:
{{
  "seo_content": "<h3>...</h3><p>...</p><p>...</p><p>...</p><p>...</p>"
}}

Rules for seo_content:
- Start with <h3>[Firm Name] [Discount] Deal</h3>
- Write 4-5 paragraphs in <p> tags
- Use <b> for key terms: firm name, coupon code, discount percentage, profit split
- Paragraph 1 (100-120 words): What the deal is, what code to use, what it covers
- Paragraph 2 (100-120 words): About the firm — background, reputation, evaluation structure
- Paragraph 3 (100-120 words): Specific pricing examples with discount applied (use realistic figures)
- Paragraph 4 (100-120 words): Trading conditions — profit split %, platforms, drawdown rules, trading styles allowed
- Paragraph 5 (60-80 words): How to claim + expiry note
- No line breaks inside the JSON string value — use a single continuous string
- Escape all quotes inside the HTML with \\"
- Do NOT use markdown formatting inside the HTML"""

    seo_raw, _m, _p = call_api_with_fallback(SYSTEM_COUPON, seo_prompt)
    seo_raw = re.sub(r"^```(?:json)?\s*", "", seo_raw.strip())
    seo_raw = re.sub(r"\s*```$", "", seo_raw.strip())
    try:
        seo_obj = json.loads(seo_raw)
    except json.JSONDecodeError as e:
        # Try to extract seo_content from malformed JSON
        match = re.search(r'"seo_content"\s*:\s*"(.*)"', seo_raw, re.DOTALL)
        if match:
            seo_obj = {"seo_content": match.group(1)}
        else:
            raise RuntimeError(f"Call 2 JSON parse error: {e}\nRaw: {seo_raw[:500]}")

    # Merge everything
    suffix = random_suffix(5)
    file_id = f"{canonical_slug}-{slugify(discount_highlight)}-{coupon_code.lower().replace('[verify]', 'coupon')}-{suffix}"
    # Clean up file_id
    file_id = re.sub(r"-+", "-", file_id).strip("-")

    result = {
        "id": file_id,
        "canonical_slug": canonical_slug,
        "firm_name": firm_name,
        "category": meta.get("category", "forex"),
        "discount_highlight": discount_highlight,
        "title": meta.get("title", f"{firm_name} {discount_highlight} Deal"),
        "description": meta.get("description", ""),
        "coupon_code": coupon_code,
        "expiration_date": meta.get("expiration_date"),
        "theme_color": meta.get("theme_color", "#00E5FF"),
        "features": meta.get("features", []),
        "affiliate_link": affiliate_link,
        "seo_content": seo_obj.get("seo_content", ""),
        "youtube_metadata": meta.get("youtube_metadata", {"title": "", "description": ""}),
        "firm_logo": meta.get("firm_logo", f"/images/logos/{canonical_slug}.svg"),
        "created_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    }
    return result, file_id

# ── Blog generator (2-call chunked) ──────────────────────────────────────────
def generate_blog_chunked(idea: str, category: str) -> str:
    """
    Call 1: frontmatter + section outline (JSON)
    Call 2: full markdown body
    Returns complete .md file content
    """
    # ── Call 1: Outline ────────────────────────────────────────────────────
    print(f"\n[1/2] Goi API ({MODEL}) — blog outline...")
    outline_prompt = f"""User idea for this blog post:
<idea>
{idea}
</idea>
Category: {category}
Target site: gopropreels.com (prop firm coupons & reviews)

OUTPUT ONLY a JSON object with these exact keys:
{{
  "title": "Blog post title (60-70 chars, include year 2026 if time-sensitive)",
  "description": "Meta description (120-155 chars)",
  "slug": "url-friendly-slug-no-year-unless-essential",
  "tags": ["tag1", "tag2", "tag3"],
  "sections": [
    {{"heading": "H2 heading", "notes": "1-sentence summary of content"}},
    ...
  ]
}}

Rules:
- sections: 6-9 H2s covering the topic thoroughly
- tags: 3-5 relevant prop trading tags
- Do NOT include year in slug
- category must be exactly: News, Knowledge, or Review"""

    outline_raw, _m, _p = call_api_with_fallback(SYSTEM_BLOG, outline_prompt)
    outline_raw = re.sub(r"^```(?:json)?\s*", "", outline_raw.strip())
    outline_raw = re.sub(r"\s*```$", "", outline_raw.strip())
    try:
        outline = json.loads(outline_raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Call 1 JSON parse error: {e}\nRaw: {outline_raw[:500]}")

    title       = outline.get("title", "Blog Post")
    description = outline.get("description", "")
    slug        = outline.get("slug", slugify(title)[:60])
    tags        = outline.get("tags", [])
    sections    = outline.get("sections", [])

    pub_date = datetime.now().strftime("%Y-%m-%d")
    tags_yaml = "\n".join(f'  - "{t}"' for t in tags)

    frontmatter = f"""---
title: "{title}"
description: "{description}"
pubDate: {pub_date}
author: "GoPropReels"
category: "{category}"
tags:
{tags_yaml}
featured: false
---"""

    sections_text = "\n".join(
        f"- H2: {s['heading']} — {s.get('notes', '')}" for s in sections
    )

    # ── Call 2: Full body ──────────────────────────────────────────────────
    print(f"\n[2/2] Goi API ({MODEL}) — blog full body...")
    body_prompt = f"""Write a complete blog post for gopropreels.com.

Frontmatter (include verbatim at top):
{frontmatter}

Article outline to follow:
{sections_text}

Requirements:
- Start immediately after the frontmatter
- Each section is H2 (##), sub-sections H3 (###)
- Target 1,200–1,800 words total
- Include internal links to relevant coupon pages like: [FTMO Coupon](/coupon/ftmo) — use realistic firm names
- Include at least 1 comparison table or structured list
- Be specific and practical — no generic filler
- Conclude with a CTA linking to the prop firm coupons listing
- Do NOT add image placeholders or IMAGE_PLAN blocks"""

    body_raw, _m, _p = call_api_with_fallback(SYSTEM_BLOG, body_prompt)

    # Ensure frontmatter is present
    body_raw = body_raw.strip()
    body_raw = re.sub(r"^```(?:markdown|md)?\n", "", body_raw)
    body_raw = re.sub(r"\n```$", "", body_raw)
    body_raw = body_raw.strip()

    if not body_raw.startswith("---"):
        full = frontmatter.strip() + "\n\n" + body_raw
    else:
        full = body_raw

    return full, slug

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 55)
    print("  gopropreels.com — Content Generator")
    print(f"  Provider: {_provider_name} ({MODEL})")
    print("=" * 55)

    print("\nChon loai content:")
    print("  1. Coupon  (src/content/coupons/[slug]-[5chars].json)")
    print("  2. Blog    (src/content/blog/[slug].md)  — category: Knowledge")
    print("  3. News    (src/content/blog/[slug].md)  — category: News")
    print("  4. Review  (src/content/blog/[slug].md)  — category: Review")
    choice = input("\nNhap 1, 2, 3, hoac 4: ").strip()

    if choice not in ("1", "2", "3", "4"):
        print("Lua chon khong hop le.")
        sys.exit(1)

    print("\nNhap y tuong / brief (Enter 2 lan de ket thuc):")
    lines = []
    try:
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
    except EOFError:
        pass
    idea = "\n".join(lines).strip()

    if not idea:
        print("Chua nhap y tuong.")
        sys.exit(1)

    if choice == "1":
        # ── Coupon ──────────────────────────────────────────────────────────
        affiliate_links = load_affiliate_links()
        result, file_id = generate_coupon_chunked(idea, affiliate_links)

        OUTPUT_COUPONS.mkdir(parents=True, exist_ok=True)
        out_path = OUTPUT_COUPONS / f"{file_id}.json"

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        print(f"\n[OK] Coupon: {out_path.relative_to(PROJECT_ROOT)}")
        print(f"     id: {result['id']}")
        print(f"     firm: {result['firm_name']}")
        print(f"     code: {result['coupon_code']}")
        if result.get("coupon_code") == "[VERIFY]":
            print("     [!] Coupon code marked [VERIFY] — update before publishing")

    else:
        # ── Blog / News / Review ─────────────────────────────────────────────
        category_map = {"2": "Knowledge", "3": "News", "4": "Review"}
        category = category_map[choice]

        content, slug = generate_blog_chunked(idea, category)

        OUTPUT_BLOG.mkdir(parents=True, exist_ok=True)
        out_path = OUTPUT_BLOG / f"{slug}.md"

        # Avoid overwrite
        if out_path.exists():
            suffix = random_suffix(5)
            out_path = OUTPUT_BLOG / f"{slug}-{suffix}.md"

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"\n[OK] Blog ({category}): {out_path.relative_to(PROJECT_ROOT)}")

    print("\nXong!")

if __name__ == "__main__":
    main()
