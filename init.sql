-- Khởi tạo các bảng dữ liệu
-- Sử dụng kiểu JSONB để tương thích hoàn toàn với cấu trúc linh hoạt của ứng dụng hiện tại

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(50) PRIMARY KEY,
    data JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS suppliers (
    id VARCHAR(50) PRIMARY KEY,
    data JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id VARCHAR(50) PRIMARY KEY,
    data JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS imports (
    id VARCHAR(50) PRIMARY KEY,
    data JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS exports (
    id VARCHAR(50) PRIMARY KEY,
    data JSONB NOT NULL
);
