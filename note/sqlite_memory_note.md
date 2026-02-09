# Ghi chú: Sử dụng SQLite ":memory:" trong Unit Test

- Khi viết unit test cho các repository, ta thường dùng SQLite với tham số ":memory:" để tạo database tạm thời trong RAM.
- Cách dùng: `db = DBConnect(":memory:")`
- Ý nghĩa:
    - Database sẽ chỉ tồn tại trong bộ nhớ RAM, không tạo file .db trên ổ đĩa.
    - Khi test kết thúc, database này sẽ tự động bị xóa.
    - Đảm bảo mỗi test function có database sạch, không bị ảnh hưởng bởi dữ liệu cũ.
- Lợi ích:
    - Test chạy nhanh hơn, không để lại file rác.
    - Đảm bảo tính độc lập giữa các test.

**Tóm lại:**
- Sử dụng `":memory:"` giúp kiểm thử database an toàn, nhanh chóng, không ảnh hưởng đến dữ liệu thật hoặc tạo file không cần thiết.
