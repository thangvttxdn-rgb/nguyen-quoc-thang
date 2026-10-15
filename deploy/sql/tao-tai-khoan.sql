-- Tạo tài khoản SQL Server cho web app Phân công toa xe.
-- Người quản trị CSDL chạy thủ công trong SSMS, SAU KHI đã đọc và điền các ô <điền>.
-- Nguyên tắc: ứng dụng chỉ được đọc và INSERT/UPDATE hai bảng nghiệp vụ, KHÔNG có quyền DELETE.

-- 1. Tạo login ở mức máy chủ (chạy trong master). Mật khẩu đặt mạnh, lưu ở nơi an toàn.
USE master;
CREATE LOGIN ems_phan_cong WITH PASSWORD = '<điền mật khẩu mạnh>', CHECK_POLICY = ON;

-- 2. Tạo user trong CSDL nghiệp vụ và cấp quyền tối thiểu.
USE [<điền tên CSDL>];
CREATE USER ems_phan_cong FOR LOGIN ems_phan_cong;

GRANT SELECT ON dbo.NhanSu TO ems_phan_cong;
GRANT UPDATE ON dbo.NhanSu TO ems_phan_cong;            -- xóa mềm: IsActive = 0 / 1
GRANT SELECT, INSERT, UPDATE ON dbo.PhanCong TO ems_phan_cong;
DENY DELETE ON dbo.NhanSu TO ems_phan_cong;
DENY DELETE ON dbo.PhanCong TO ems_phan_cong;

-- 3. Kiểm tra lại quyền đã cấp (phải không có DELETE).
SELECT dp.name AS nguoi_dung, o.name AS bang, p.permission_name, p.state_desc
FROM sys.database_permissions p
JOIN sys.database_principals dp ON dp.principal_id = p.grantee_principal_id
LEFT JOIN sys.objects o ON o.object_id = p.major_id
WHERE dp.name = 'ems_phan_cong'
ORDER BY o.name, p.permission_name;
