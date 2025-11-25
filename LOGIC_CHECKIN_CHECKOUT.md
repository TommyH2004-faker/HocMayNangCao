# ✅ LOGIC HOẠT ĐỘNG CHẤM CÔNG MỚI

## 🔄 QUY TRÌNH

### Bước 1: CHECK IN
```
👤 Người dùng đứng trước camera
   ↓
🎯 Hệ thống nhận diện khuôn mặt
   ↓
👆 Bấm nút "Check In"
   ↓
📸 Lưu ảnh vào: image_data/Tên_Người/HH-MM-SS DD-MM-YYYY.jpg
   ↓
❌ CHƯA LƯU VÀO JSON (đợi checkout)
```

### Bước 2: CHECK OUT
```
👤 Người dùng đứng trước camera (cùng người)
   ↓
🎯 Hệ thống nhận diện khuôn mặt
   ↓
👆 Bấm nút "Check Out"
   ↓
📂 Lấy thời gian Check In từ tên file ảnh
   ↓
🕐 Lấy thời gian Check Out hiện tại
   ↓
⏱️ Tính tổng giờ làm việc: Checkout - Checkin
   ↓
💾 LƯU VÀO attendance_log.json với đầy đủ:
   • Tên người
   • Ngày làm việc
   • Thời gian vào
   • Thời gian ra
   • Tổng giờ làm
   ↓
🗑️ XÓA ảnh check in
```

### Bước 3: XUẤT EXCEL
```
👆 Bấm nút "Xuất EXCEL"
   ↓
📖 Đọc dữ liệu từ attendance_log.json
   ↓
📊 Tạo bảng Excel với các cột:
   • Họ và Tên
   • Ngày
   • Giờ Vào
   • Giờ Ra
   • Tổng Giờ Làm
   ↓
💾 Lưu file: excel/ChamCong_DD-MM-YYYY_HH-MM-SS.xlsx
   ↓
✅ Hiển thị popup thông báo
```

## 📋 VÍ DỤ THỰC TẾ

### Scenario: Nhân viên Nguyễn Văn A làm việc 1 ngày

```
08:30:00  → Check In
          • Lưu ảnh: image_data/Nguyen Van A/08-30-00 09-11-2025.jpg
          • JSON: [] (trống)

17:30:00  → Check Out
          • Đọc thời gian từ ảnh: "08:30:00 09-11-2025"
          • Lấy thời gian hiện tại: "17:30:00 09-11-2025"
          • Tính giờ: 17:30:00 - 08:30:00 = 9.0 giờ
          • Lưu JSON:
            {
              "name": "Nguyen Van A",
              "date": "09-11-2025",
              "check_in": "08:30:00 09-11-2025",
              "check_out": "17:30:00 09-11-2025",
              "working_hours": 9.0
            }
          • Xóa ảnh

17:35:00  → Xuất Excel
          • Tạo file: excel/ChamCong_09-11-2025_17-35-00.xlsx
          • Nội dung:
            | Họ và Tên    | Ngày       | Giờ Vào    | Giờ Ra     | Tổng Giờ |
            |--------------|------------|------------|------------|----------|
            | Nguyen Van A | 09-11-2025 | 08:30:00   | 17:30:00   | 9.0      |
```

## 🔑 ĐIỂM QUAN TRỌNG

### ✅ Ưu điểm của logic mới:

1. **Đầy đủ dữ liệu**: 
   - Khi checkout mới lưu → Luôn có cả thời gian vào và ra
   - Không có bản ghi thiếu thông tin

2. **Tính toán chính xác**:
   - Tổng giờ làm = Checkout - Checkin
   - Tính ngay khi checkout, không phải tính lại

3. **Quản lý tốt**:
   - Chỉ những người đã checkout mới có trong Excel
   - Người chỉ checkin (chưa checkout) không xuất hiện

4. **Không bị trùng**:
   - Mỗi lần checkout chỉ tạo 1 bản ghi
   - Không bị log 2 lần (1 lần checkin, 1 lần checkout)

### ⚠️ Lưu ý:

1. **Phải checkout mới có trong Excel**:
   - Nếu chỉ checkin → Không có trong JSON → Không xuất Excel
   - Chỉ có ảnh trong `image_data/`

2. **Thứ tự phải đúng**:
   - Bước 1: Check in (lưu ảnh)
   - Bước 2: Check out (lưu JSON + xóa ảnh)
   - Không thể checkout nếu chưa checkin

3. **Thời gian lấy từ tên file ảnh**:
   - Format: `HH-MM-SS DD-MM-YYYY.jpg`
   - Chuyển thành: `HH:MM:SS DD-MM-YYYY` để tính toán

## 📂 CẤU TRÚC DỮ LIỆU

### Khi đang checkin (chưa checkout):
```
image_data/
├── Nguyen Van A/
│   └── 08-30-00 09-11-2025.jpg  ← Có ảnh
└── Tran Van B/
    └── 09-00-00 09-11-2025.jpg  ← Có ảnh

attendance_log.json: []  ← Trống
```

### Sau khi checkout:
```
image_data/
└── Tran Van B/
    └── 09-00-00 09-11-2025.jpg  ← Chưa checkout

attendance_log.json:
[
  {
    "name": "Nguyen Van A",
    "date": "09-11-2025",
    "check_in": "08:30:00 09-11-2025",
    "check_out": "17:30:00 09-11-2025",
    "working_hours": 9.0
  }
]
```

### Sau khi xuất Excel:
```
excel/
└── ChamCong_09-11-2025_17-35-00.xlsx
    ↓
    Có: Nguyen Van A (đã checkout)
    Không có: Tran Van B (chưa checkout)
```

## 🧪 TEST KẾT QUẢ

```bash
python test_checkin_checkout.py
```

Output:
```
✓ Nguyen Van A check in
✓ Tran Van B check in
→ JSON: 0 bản ghi ✓

✓ Nguyen Van A check out
  • Check in:  08:30:00 09-11-2025
  • Check out: 17:30:00 09-11-2025
  • Làm việc:  9.0 giờ
→ JSON: 1 bản ghi ✓

✓ Xuất Excel thành công
  • Có: Nguyen Van A ✓
  • Không có: Tran Van B ✓ (vì chưa checkout)
```

## 📊 FORMAT FILE JSON

```json
[
  {
    "name": "Nguyen Van A",
    "date": "09-11-2025",
    "check_in": "08:30:00 09-11-2025",
    "check_out": "17:30:00 09-11-2025",
    "working_hours": 9.0,
    "image_path": "image_data/Nguyen Van A"
  },
  {
    "name": "Tran Van B",
    "date": "09-11-2025",
    "check_in": "09:15:30 09-11-2025",
    "check_out": "18:00:15 09-11-2025",
    "working_hours": 8.75,
    "image_path": "image_data/Tran Van B"
  }
]
```

## 🎯 KẾT LUẬN

**Logic hoạt động hoàn hảo theo yêu cầu:**

✅ Checkin → Lưu ảnh với thời gian
✅ Checkout → Lấy thời gian từ ảnh → Tính giờ làm → Lưu JSON
✅ Xuất Excel → Có đầy đủ: Vào + Ra + Tổng giờ

**Dữ liệu luôn đầy đủ và chính xác!** 🎉
