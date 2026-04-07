# _AUDIT-BEFORE-WRITING.md
# Audit trước khi viết bài — gopropreels.com

Chạy các lệnh dưới đây **trước** khi tạo bất kỳ coupon hay blog mới.

---

## 1. Kiểm tra coupon đã tồn tại chưa?

```bash
# Liệt kê tất cả coupon hiện có (theo canonical_slug)
grep -r '"canonical_slug"' src/content/coupons/ | sed 's/.*"canonical_slug": "\(.*\)".*/\1/' | sort

# Tìm coupon của 1 firm cụ thể (ví dụ: ftmo)
grep -rl '"canonical_slug": "ftmo"' src/content/coupons/

# Tìm theo coupon code
grep -rl '"coupon_code": "FTMO30"' src/content/coupons/
```

**Nếu đã tồn tại:** Dừng, cập nhật file cũ thay vì tạo file mới.

---

## 2. Kiểm tra blog đã tồn tại chưa?

```bash
# Liệt kê tất cả slug blog
ls src/content/blog/

# Tìm bài cùng chủ đề
grep -rl "ftmo" src/content/blog/
```

---

## 3. Kiểm tra affiliate link

```bash
# Tìm firm trong affiliate_links.json
python -c "
import json
data = json.load(open('affiliate_links.json'))
for e in data:
    if 'FIRM_NAME' in e['firm_name'].lower():
        print(e)
"
```

Thay `FIRM_NAME` bằng tên firm đang cần.

**Nếu chưa có:** Thêm vào `affiliate_links.json` trước khi chạy generate_content.py.

---

## 4. Tìm bài liên quan để cross-link

```bash
# Tìm bài blog đề cập đến loại firm (forex/futures)
grep -rl "forex" src/content/blog/
grep -rl "futures" src/content/blog/

# Tìm coupon cùng category
grep -rl '"category": "futures"' src/content/coupons/
```

---

## 5. Checklist trước khi publish

- [ ] Coupon code đã được verify (không còn `[VERIFY]`)
- [ ] `affiliate_link` đúng và hoạt động
- [ ] `canonical_slug` chưa bị trùng
- [ ] `expiration_date` còn hợp lệ hoặc set `null`
- [ ] `firm_logo` file đã có tại `public/images/logos/[slug].svg`
- [ ] `seo_content` HTML hợp lệ (thử paste vào browser console)

---

## 6. Số lượng content hiện tại

```bash
echo "Coupons:" && ls src/content/coupons/*.json 2>/dev/null | wc -l
echo "Blog posts:" && ls src/content/blog/*.md 2>/dev/null | wc -l
```
