# _CONTENT-WORKFLOW.md
# Logic tạo nội dung cho gopropreels.com

---

## Bước 1 — Audit trước *(Claude Code làm, không phải AI)*

Mở `_AUDIT-BEFORE-WRITING.md` và chạy các lệnh kiểm tra:

- Coupon firm đó **đã tồn tại chưa?** → Nếu có, cập nhật file cũ, đừng tạo mới
- Firm **đã có trong `affiliate_links.json` chưa?** → Nếu chưa, thêm vào trước
- Coupon code **đã verify chưa?** → Kiểm tra trên trang firm trước khi chạy script
- Tìm **bài liên quan** để cross-link sau

---

## Bước 2 — Generate nội dung *(AI làm qua script)*

```bash
python generate_content.py
```

Script chạy **2 API call**:

1. **Call 1** → AI trả về JSON metadata (firm_name, coupon_code, features, theme_color, v.v.)
2. **Call 2** → AI viết `seo_content` HTML đầy đủ (4-5 đoạn)

Script tự tạo:

- **Coupon** → lưu vào `src/content/coupons/[slug]-[5chars].json`
- **Blog/News/Review** → lưu vào `src/content/blog/[slug].md`

> Không cần tạo ảnh — gopropreels không dùng ảnh trong seo_content.

---

## Bước 3 — Verify & Edit thủ công

Mở file vừa tạo, kiểm tra:

- `coupon_code`: Không được có `[VERIFY]` trước khi publish
- `affiliate_link`: Paste vào browser, kiểm tra còn sống
- `expiration_date`: Cập nhật hoặc đặt `null` nếu không có hạn
- `seo_content`: Đọc lướt, sửa nếu AI viết sai tên/giá

---

## Bước 4 — Build & Preview

Chạy `GoPropReels_Build.bat` → bấm **BUILD AND PREVIEW** → kiểm tra trang mới tại `localhost:4321`

Kiểm tra:
- Trang coupon: `localhost:4321/coupon/[canonical_slug]`
- Trang blog: `localhost:4321/blog/[slug]`

---

## Bước 5 — Deploy

Chạy `GoPropReels_Deploy.bat` → bấm **DEPLOY TO CLOUDFLARE**

---

## Sơ đồ nhanh

```
Ý tưởng (firm + coupon code)
  → Audit (_AUDIT-BEFORE-WRITING.md)
  → generate_content.py (AI sinh .json hoặc .md)
  → Verify thủ công (sửa [VERIFY], check link)
  → GoPropReels_Build.bat → Preview
  → GoPropReels_Deploy.bat → Live
```

---

## Loại content & menu script

| Menu | Loại | Output | Thư mục |
|:----:|:-----|:-------|:--------|
| 1 | Coupon | `[slug]-[5chars].json` | `src/content/coupons/` |
| 2 | Blog (Knowledge) | `[slug].md` | `src/content/blog/` |
| 3 | News | `[slug].md` | `src/content/blog/` |
| 4 | Review | `[slug].md` | `src/content/blog/` |

---

## Coupon category

| Giá trị | Khi nào dùng |
|:--------|:-------------|
| `forex` | Firm chỉ trade forex/crypto/indices |
| `futures` | Firm có sản phẩm futures (CME, CBOT, v.v.) |

---

## Provider AI

Script đọc `PROVIDER` từ `.env`. Mặc định: `chiasegpu-claude-sonnet-4.6`.

Fallback chain: `opus-4.6` → `sonnet-4.6` → `gemini-3-flash` → `gemini-3.1-pro` → `deepseek`
