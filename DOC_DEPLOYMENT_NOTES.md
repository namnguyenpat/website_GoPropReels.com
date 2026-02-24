# Deployment Notes - GoPropReels

## 🚀 Cloudflare Pages Deployment

### Live URLs
- **Production**: https://website-gopropreels-com.pages.dev/
- **Workers**: https://gopropreels.misaluom.workers.dev/
- **Custom Domain**: https://gopropreels.com (planned)

### Git Repository
- **Repo**: https://github.com/namnguyenpat/website_GoPropReels.com.git
- **Branch**: `main` (auto-deploy enabled)

---

## ⚠️ Critical Issue Fixed: Routing Problem

### Problem
- `/blog` redirected to home instead of blog page
- `/coupons/[id]` redirected to home instead of coupon detail
- Clicking coupon cards redirected to home

### Root Cause
Cloudflare Pages không tự động serve `index.html` trong subfolders khi không có file `_redirects`.

**Cấu trúc build:**
```
dist/
  index.html
  blog/index.html
  coupons/aqua-funded-welcome-50/index.html
```

**Hành vi mặc định của Cloudflare Pages:**
- Request `/blog` → không tìm thấy file → fallback về `/index.html` (home)
- Request `/coupons/aqua-funded-welcome-50` → không tìm thấy → fallback về home

### Solution
Tạo file `public/_redirects` với routing rules:

```
# Blog routes
/blog /blog/index.html 200
/blog/:page /blog/:page/index.html 200

# Coupon detail pages
/coupons/:id /coupons/:id/index.html 200

# Compare pages
/compare/:slug /compare/:slug/index.html 200
```

**Commit**: `3db9019` - "Add Cloudflare Pages _redirects file to fix routing"

---

## 📝 Build Configuration

### Cloudflare Pages Settings
- **Framework**: Astro
- **Build command**: `npm run build`
- **Build output directory**: `dist`
- **Node version**: 18.x or higher

### Important Files
- `wrangler.jsonc` - Cloudflare Workers config (không dùng cho Pages routing)
- `public/_redirects` - Cloudflare Pages routing rules (CRITICAL!)
- `astro.config.mjs` - Astro configuration

---

## 🔧 Local Development

```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 📦 Deployment Process

1. **Push to Git**:
   ```bash
   git add .
   git commit -m "Your message"
   git push origin main
   ```

2. **Auto-deploy**: Cloudflare Pages tự động detect commit và deploy (1-2 phút)

3. **Verify**: Check deployment status tại Cloudflare Dashboard

---

## 🐛 Troubleshooting

### Issue: Routes redirect về home
**Solution**: Kiểm tra file `public/_redirects` có tồn tại và đúng format

### Issue: Build fails
**Solution**: 
- Check Node version >= 18
- Run `npm install` lại
- Check `astro.config.mjs` syntax

### Issue: 404 errors
**Solution**: Verify file paths trong `_redirects` match với cấu trúc `dist/`

---

## 📚 References

- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
- [Cloudflare Pages Redirects](https://developers.cloudflare.com/pages/configuration/redirects/)
- [Astro Docs](https://docs.astro.build/)

---

## 📅 Change Log

### 2026-02-24
- ✅ Fixed routing issue với `_redirects` file
- ✅ Verified `/blog` và `/coupons/[id]` routes work correctly
- ✅ Commit `3db9019` deployed successfully

### 2026-02-23
- ❌ Attempted `wrangler.jsonc` config changes (không hiệu quả)
- ❌ Tried different `html_handling` options (không giải quyết được)
- 🔍 Identified root cause: missing `_redirects` file
