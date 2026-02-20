# 🏛️ STUDIOS & FIRMS: DATABASE MANAGEMENT

Tài liệu quản lý thông tin các quỹ liên kết (Firm Profiles) trên **GoPropReels**.

---

## 1. THE FIRM CATALOG
Dữ liệu quỹ hiện tại được quản lý thông qua hai nguồn:
1.  **Metadata trong Coupon**: Mỗi file JSON trong `src/content/coupons/` chứa thông số của quỹ tại thời điểm đó.
2.  **Affiliate Central**: Tệp `affiliate_links.json` (nếu có) chứa danh sách link tổng hợp.

## 2. VISUAL ASSETS (Logo Standards)
Để trang web đạt chuẩn "Premium Cinematic", logo cần tuân thủ:
- **Định dạng**: Ưu tiên `.svg` để sắc nét trên màn hình 4K. Nếu dùng `.png`, phải là nền trong suốt (Alpha channel).
- **Vị trí**: Lưu vào thư mục `public/images/logos/`.
- **Naming**: Đặt tên theo slug (ví dụ: `apex-trader-funding.svg`).

## 3. UPDATING SPECS
Khi một quỹ thay đổi chính sách (ví dụ: từ 80% lên 90% profit split):
- Bạn cần update trường `features` và `seo_content` trong file Coupon tương ứng.
- **Quan trọng**: Luôn kiểm tra `affiliate_link` xem có bị "dead link" hay không để bảo vệ thu nhập của bạn.

## 4. SEO & LINKING STRATEGY
Trang chi tiết coupon của GoPropReels được thiết kế để trở thành một "Showcase".
- Luôn có link trỏ về trang chủ hoặc trang so sánh để giữ chân người dùng trong "vũ trụ" của chúng ta.
- Sử dụng thẻ `<h3>` cho các tiêu đề phụ trong phần Review để cấu trúc bài viết chuyên nghiệp như một bản tin điện ảnh.
