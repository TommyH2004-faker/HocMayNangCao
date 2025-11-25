# HƯỚNG DẪN CHỨC NĂNG XUẤT EXCEL

## Tính Năng Mới

### 1. Tự động lưu lịch sử chấm công
- Khi bạn **Check In**: Hệ thống tự động ghi nhận thời gian vào
- Khi bạn **Check Out**: Hệ thống tự động ghi nhận thời gian ra và tính tổng giờ làm việc

### 2. File lưu trữ
- **attendance_log.json**: File JSON lưu toàn bộ lịch sử chấm công
- Vị trí: Thư mục gốc dự án `d:\yolo\timekeeping\attendance_log.json`

### 3. Xuất Excel
- Khi bấm nút **"Xuất EXCEL"**:
  - Tạo folder `excel/` (nếu chưa có)
  - Tạo file Excel với tên: `ChamCong_DD-MM-YYYY_HH-MM-SS.xlsx`
  - Ví dụ: `ChamCong_09-11-2025_14-30-45.xlsx`

### 4. Vị trí file Excel
```
d:\yolo\timekeeping\
├── excel/
│   ├── ChamCong_09-11-2025_14-30-45.xlsx
│   ├── ChamCong_09-11-2025_16-20-30.xlsx
│   └── ChamCong_10-11-2025_09-15-00.xlsx
├── attendance_log.json
└── handle_main.py
```

### 5. Nội dung file Excel
Các cột trong file Excel:
- **Họ và Tên**: Tên người được nhận diện
- **Ngày**: Ngày chấm công (DD-MM-YYYY)
- **Giờ Vào**: Thời gian check in (HH:MM:SS DD-MM-YYYY)
- **Giờ Ra**: Thời gian check out (HH:MM:SS DD-MM-YYYY)
- **Tổng Giờ Làm**: Số giờ làm việc (tính tự động)

### 6. Luồng hoạt động

```
1. Nhận diện khuôn mặt → Hiển thị tên
                         ↓
2. Bấm "Check In"    → Lưu ảnh + Log thời gian vào
                         ↓
3. Làm việc...
                         ↓
4. Bấm "Check Out"   → Xóa ảnh + Log thời gian ra + Tính giờ làm
                         ↓
5. Bấm "Xuất EXCEL"  → Tạo file Excel trong folder excel/
```

### 7. Ví dụ dữ liệu Excel

| Họ và Tên    | Ngày       | Giờ Vào              | Giờ Ra               | Tổng Giờ Làm |
|--------------|------------|----------------------|----------------------|--------------|
| Lê Việt Anh  | 09-11-2025 | 08:30:15 09-11-2025 | 17:45:30 09-11-2025 | 9.25         |
| Nguyễn Văn A | 09-11-2025 | 09:00:00 09-11-2025 | 18:00:00 09-11-2025 | 9.00         |
| Trần Văn B   | 09-11-2025 | 08:45:20 09-11-2025 | 17:30:10 09-11-2025 | 8.75         |

### 8. Thông báo

Khi bấm "Xuất EXCEL":
- ✅ **Thành công**: Hiện popup với đường dẫn file
- ⚠️ **Không có dữ liệu**: Hiện cảnh báo "Vui lòng check in/out trước"
- ❌ **Lỗi**: Hiện chi tiết lỗi

### 9. Cài đặt bổ sung

Đã thêm 2 thư viện mới vào `requirements.txt`:
```
pandas       # Xử lý dữ liệu và xuất Excel
openpyxl     # Engine để tạo file .xlsx
```

Cài đặt:
```bash
pip install pandas openpyxl
```

### 10. Files mới được tạo

- **attendance_logger.py**: Class quản lý logging và xuất Excel
- **attendance_log.json**: File lưu dữ liệu chấm công
- **excel/**: Folder chứa các file Excel đã xuất

## Cách Sử Dụng

1. **Check In**:
   - Đứng trước camera → Nhận diện
   - Bấm "Check In"
   - Thông tin được lưu tự động

2. **Check Out**:
   - Đứng trước camera → Nhận diện (cùng người)
   - Bấm "Check Out"
   - Thời gian ra và tổng giờ được tính tự động

3. **Xuất Excel**:
   - Bấm "Xuất EXCEL" bất kỳ lúc nào
   - File được tạo trong folder `excel/`
   - Mở file bằng Microsoft Excel hoặc LibreOffice

## Lưu Ý

- File JSON lưu **toàn bộ lịch sử**, không bị mất khi tắt phần mềm
- Mỗi lần xuất Excel tạo file **MỚI**, không ghi đè file cũ
- Có thể xuất Excel **nhiều lần** trong ngày
- Dữ liệu từ **tất cả các ngày** đều được xuất ra
