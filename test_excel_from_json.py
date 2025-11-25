"""
Test xuất Excel từ attendance_log.json
"""
from attendance_logger import AttendanceLogger
import os

print("=" * 70)
print("TEST XUẤT EXCEL TỪ ATTENDANCE_LOG.JSON")
print("=" * 70)

# Kiểm tra file attendance_log.json
if os.path.exists('attendance_log.json'):
    print("\n✓ File attendance_log.json tồn tại")
    
    # Đọc dữ liệu
    logger = AttendanceLogger()
    print(f"✓ Số bản ghi trong file: {len(logger.data)}")
    
    # Hiển thị dữ liệu
    print("\n" + "=" * 70)
    print("DỮ LIỆU HIỆN TẠI:")
    print("=" * 70)
    
    for i, record in enumerate(logger.data, 1):
        print(f"\n[{i}] {record['name']}")
        print(f"    Ngày:        {record['date']}")
        print(f"    Giờ vào:     {record['check_in']}")
        print(f"    Giờ ra:      {record['check_out']}")
        print(f"    Tổng giờ:    {record['working_hours']} giờ")
    
    # Xuất Excel
    print("\n" + "=" * 70)
    print("XUẤT EXCEL:")
    print("=" * 70)
    
    filepath = logger.export_to_excel()
    
    if filepath:
        print(f"\n✅ ĐÃ XUẤT THÀNH CÔNG!")
        print(f"📁 Vị trí file: {os.path.abspath(filepath)}")
        print(f"📂 Thư mục: {os.path.dirname(os.path.abspath(filepath))}")
        
        # Mở thư mục excel
        import subprocess
        excel_dir = os.path.dirname(os.path.abspath(filepath))
        print(f"\n💡 Mở thư mục excel:")
        print(f"   explorer {excel_dir}")
        
    else:
        print("\n❌ Không thể xuất Excel (không có dữ liệu)")

else:
    print("\n❌ File attendance_log.json không tồn tại")
    print("💡 Hãy check in và check out trước để tạo dữ liệu")

print("\n" + "=" * 70)
