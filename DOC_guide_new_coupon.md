# 🎬 DIRECTING THE DEAL: NEW COUPON PRODUCTION

Hướng dẫn tạo và thiết lập coupon mới cho hệ thống **GoPropReels**. Chúng ta sử dụng cấu trúc **Astro Data Collection** để tối ưu hóa tốc độ và độ tin cậy.

---

## 1. SCENE SELECTION (Data Creation)
Mọi deal mới phải là một file `.json` riêng biệt đặt tại:
`src/content/coupons/[firm-slug]-[id].json`

### Phim trường JSON (Template):
```json
{
  "id": "aquafunded-40-off-feb-2026",
  "firm_name": "AquaFunded",
  "category": "forex", 
  "discount_highlight": "40% OFF",
  "coupon_code": "AQUA40",
  "theme_color": "#00FFFF",
  "features": ["90% Profit Split", "Express Payouts"],
  "affiliate_link": "https://aquafunded.com/?aff=REELS",
  "firm_logo": "/images/logos/aquafunded.png",
  "seo_content": "<h3>High-Performance Forex Funding</h3><p>AquaFunded is disrupting the space with...</p>",
  "created_at": "2026-02-20T10:00:00Z"
}
```

## 2. CINEMATIC RULES (Quy định bắt buộc)
1.  **Chỉnh màu (theme_color)**: Sử dụng mã HEX đại diện cho thương hiệu của quỹ để Poster hiển thị đẹp mắt.
2.  **Hậu đề (seo_content)**: Viết nội dung review theo dạng HTML để tạo độ sâu cho trang chi tiết. Đừng chỉ để code không.
3.  **Phân loại (category)**: Chỉ chấp nhận `"forex"` hoặc `"futures"`. Sai giá trị này hệ thống sẽ từ chối Build.

---

## 3. PRODUCTION WORKFLOW (Quy trình)
1.  **Khởi tạo**: Tạo file `.json` như mẫu trên.
2.  **Đồng bộ**: Chạy lệnh `npx astro sync` để kiểm tra tính hợp lệ của schema.
3.  **Kiểm tra (Preview)**: Chạy `npm run dev` và xem thẻ "DynamicPoster" mới xuất hiện trên trang chủ.
4.  **Phát hành (Export)**:
    ```bash
    git add .
    git commit -m "prod: launch new coupon [Firm]"
    git push origin main
    ```

## 4. PRO-TIP: THE DYNAMIC POSTER
Hệ thống **PropReels** sẽ tự động vẽ logo, mã code và highlight lên hình nền poster dựa trên `theme_color` bạn cung cấp. Hãy chọn màu sắc có độ tương phản tốt với chữ trắng/đen.
