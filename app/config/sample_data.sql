-- Insert roles
INSERT INTO phan_quyen (ten_quyen, mo_ta) VALUES
('administrator', 'Quyền truy cập đầy đủ vào tất cả tính năng'),
('registered_user', 'Chờ phê duyệt'),
('user', 'Chỉ xem'),
('manager', 'Quyền quản lý tất cả trừ người dùng');

-- Insert users
INSERT INTO nguoi_dung (ten_dang_nhap, mat_khau, ho_ten, ma_quyen) VALUES
('quanly1', '$2b$12$KIXQ1e1G1J1Q1e1G1J1Q1e1G1J1Q1e1G1J1Q1e1G1J1Q1e1G1J1Q1', 'Nguyễn Văn Quản Lý', 2),
('nguoidung1', '$2b$12$KIXQ1e1G1J1Q1e1G1J1Q1e1G1J1Q1e1G1J1Q1e1G1J1Q1e1G1J1Q1', 'Trần Thị Người Dùng', 3);

-- Insert categories
INSERT INTO danh_muc (ten, mo_ta) VALUES
('Điện tử', 'Thiết bị và phụ kiện điện tử'),
('Nội thất', 'Nội thất nhà và văn phòng'),
('Thời trang', 'Quần áo và phụ kiện');

-- Insert suppliers
INSERT INTO nha_cung_cap (ten, email, dien_thoai, dia_chi) VALUES
('Công ty TNHH Điện tử ABC', 'contact@abctech.com', '0123456789', 'Số 123 Đường Điện tử'),
('Nội thất Hoàng Gia', 'info@hoanggiafurniture.com', '0987654321', 'Số 456 Đường Nội thất'),
('Thời trang Phong Cách', 'support@phongcachfashion.com', '0555123456', 'Số 789 Đường Thời trang');

-- Insert products
INSERT INTO san_pham (ten, mo_ta, ma_danh_muc, ma_ncc, don_gia) VALUES
('Điện thoại thông minh', 'Điện thoại thông minh mới nhất', 1, 1, 16000000),
('Ghế văn phòng', 'Ghế văn phòng công thái học', 2, 2, 3500000),
('Áo thun', 'Áo thun cotton cao cấp', 3, 3, 450000);

-- Insert inventory
INSERT INTO kho_hang (ma_san_pham, so_luong, ngay_cap_nhat) VALUES
(1, 50, '2023-10-01'),
(2, 20, '2023-10-02'),
(3, 100, '2023-10-03');

-- Insert orders
INSERT INTO don_hang (ma_nguoi_dung, ngay_dat, tong_tien) VALUES
(1, '2023-10-01', 3500000),
(1, '2023-10-02', 4600000),
(1, '2023-10-03', 7000000);

-- Insert order details
INSERT INTO chi_tiet_don_hang (ma_don_hang, ma_san_pham, so_luong, don_gia) VALUES
(1, 1, 1, 16000000),
(2, 2, 2, 3500000),
(3, 3, 5, 450000); 