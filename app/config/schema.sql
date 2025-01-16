-- User roles table
CREATE TABLE IF NOT EXISTS phan_quyen (
    ma_quyen INT PRIMARY KEY AUTO_INCREMENT,
    ten_quyen VARCHAR(50) NOT NULL UNIQUE,
    mo_ta TEXT
);

-- Insert default roles
INSERT INTO user_roles (role_name, description) VALUES
('administrator', 'Full access to all system features'),
('registered_user', 'Wait for approval'),
('user', 'View only'),
('manager', 'Rights to manage all except users'); 

-- Users table
CREATE TABLE IF NOT EXISTS nguoi_dung (
    ma_nguoi_dung INT PRIMARY KEY AUTO_INCREMENT,
    ten_dang_nhap VARCHAR(50) NOT NULL UNIQUE,
    mat_khau VARCHAR(255) NOT NULL,
    ho_ten VARCHAR(255) NOT NULL,
    ma_quyen INT NOT NULL,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ma_quyen) REFERENCES phan_quyen(ma_quyen)
);

-- Categories table
CREATE TABLE IF NOT EXISTS danh_muc (
    ma_danh_muc INT PRIMARY KEY AUTO_INCREMENT,
    ten VARCHAR(100) NOT NULL UNIQUE,
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Suppliers table
CREATE TABLE IF NOT EXISTS nha_cung_cap (
    ma_ncc INT PRIMARY KEY AUTO_INCREMENT,
    ten VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    dien_thoai VARCHAR(20),
    dia_chi TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


-- Products table
CREATE TABLE IF NOT EXISTS san_pham (
    ma_san_pham INT PRIMARY KEY AUTO_INCREMENT,
    ten VARCHAR(100) NOT NULL,
    mo_ta TEXT,
    ma_danh_muc INT,
    ma_ncc INT,
    don_gia DECIMAL(10, 2) NOT NULL,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ma_danh_muc) REFERENCES danh_muc(ma_danh_muc),
    FOREIGN KEY (ma_ncc) REFERENCES nha_cung_cap(ma_ncc)
);

-- Inventory table
CREATE TABLE IF NOT EXISTS kho_hang (
    ma_kho INT PRIMARY KEY AUTO_INCREMENT,
    ma_san_pham INT NOT NULL,
    so_luong INT NOT NULL DEFAULT 0,
    ngay_nhap_cuoi TIMESTAMP,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ma_san_pham) REFERENCES san_pham(ma_san_pham)
);

-- Orders table
CREATE TABLE IF NOT EXISTS don_hang (
    ma_don_hang INT PRIMARY KEY AUTO_INCREMENT,
    ma_nguoi_dung INT NOT NULL,
    ngay_dat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tong_tien DECIMAL(10, 2) NOT NULL,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ma_nguoi_dung) REFERENCES nguoi_dung(ma_nguoi_dung)
);

-- Order details table
CREATE TABLE IF NOT EXISTS chi_tiet_don_hang (
    ma_chi_tiet INT PRIMARY KEY AUTO_INCREMENT,
    ma_don_hang INT NOT NULL,
    ma_san_pham INT NOT NULL,
    so_luong INT NOT NULL,
    don_gia DECIMAL(10, 2) NOT NULL,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ma_don_hang) REFERENCES don_hang(ma_don_hang),
    FOREIGN KEY (ma_san_pham) REFERENCES san_pham(ma_san_pham)
);
