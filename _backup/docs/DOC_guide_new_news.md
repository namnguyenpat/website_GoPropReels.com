# 📡 NEWS BROADCAST: PREMIUM UPDATES

Hướng dẫn đăng tải tin tức thị trường và thông tin nóng hổi (News) trên **GoPropReels Newsroom**.

---

## 1. PRE-PRODUCTION (Tạo file)
Tạo tệp Markdown tại: `src/content/blog/[slug].md`

### Script Header (Frontmatter):
```markdown
---
title: "Prop Firm Market Update: The Q1 Revolution"
description: "Analysis of the new regulatory framework impacting funded traders."
pubDate: 2026-02-20
category: "News" 
tags: ["News", "Market", "Regulation"]
---
```
*Lưu ý: Trường `category` phải là `"News"` (viết hoa chữ cái đầu).*

---

## 2. BROADCAST STYLE (Quy tắc viết)
- **Tiêu đề Cinematic**: Sử dụng những từ ngữ mạnh mẽ (Revolution, Breakthrough, Warning, Spotlight).
- **Không dùng ảnh đại diện (No Hero Image)**: Giao diện GoPropReels được tối ưu theo phong cách "Minimalist Typography" để đạt tốc độ tải trang 100 điểm.
- **Nội dung súc tích**: Chia nhỏ thông tin bằng các bullet points và Heading 2/3.

## 3. LINKING FLOW
Tin tức là cách tốt nhất để dẫn người dùng đến các Deal:
- Hãy chèn liên kết đến trang Coupon liên quan ở cuối bài viết.
- Luôn có link "Back to Home" hoặc trỏ về Hub tin tức tổng hợp.

## 4. AIRING THE NEWS (Deployment)
1.  Viết bài trong file `.md`.
2.  Commit bài viết mới.
3.  Vercel sẽ tự động render trang tin tức trong vài giây.

```bash
git add src/content/blog/new-article.md
git commit -m "news: airing [Title]"
git push origin main
```
