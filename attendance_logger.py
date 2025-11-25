import os
import json
from datetime import datetime
import pandas as pd

class AttendanceLogger():
    '''Class quản lý lịch sử check in/out và xuất Excel'''
    
    def __init__(self):
        self.log_file = 'attendance_log.json'
        self.excel_folder = 'excel'
        self.data = self.load_log()
        
    def load_log(self):
        '''Load dữ liệu từ file JSON'''
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_log(self):
        '''Lưu dữ liệu vào file JSON'''
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def log_check_in(self, name, time_str, image_path=None):
        '''Ghi nhận check in'''
        record = {
            'name': name,
            'check_in': time_str,
            'check_out': None,
            'date': datetime.now().strftime("%d-%m-%Y"),
            'image_path': image_path
        }
        self.data.append(record)
        self.save_log()
        print(f'Đã log check in: {name} lúc {time_str}')
    
    def log_check_out(self, name):
        '''Ghi nhận check out cho bản ghi check in gần nhất chưa có check out'''
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S %d-%m-%Y")
        
        # Tìm bản ghi check in gần nhất của người này chưa có check out
        for record in reversed(self.data):
            if record['name'] == name and record['check_out'] is None:
                record['check_out'] = time_str
                
                # Tính tổng giờ làm việc
                try:
                    check_in_time = datetime.strptime(record['check_in'], "%H:%M:%S %d-%m-%Y")
                    check_out_time = datetime.strptime(time_str, "%H:%M:%S %d-%m-%Y")
                    duration = check_out_time - check_in_time
                    hours = duration.total_seconds() / 3600
                    record['working_hours'] = round(hours, 2)
                except:
                    record['working_hours'] = 0
                
                self.save_log()
                print(f'Đã log check out: {name} lúc {time_str}')
                return True
        
        print(f'Không tìm thấy bản ghi check in cho {name}')
        return False
    
    def export_to_excel(self):
        '''Xuất dữ liệu ra file Excel'''
        if not self.data:
            print('Không có dữ liệu để xuất')
            return None
        
        # Tạo thư mục excel nếu chưa có
        os.makedirs(self.excel_folder, exist_ok=True)
        
        # Tạo tên file với ngày giờ hiện tại
        now = datetime.now()
        filename = f'ChamCong_{now.strftime("%d-%m-%Y_%H-%M-%S")}.xlsx'
        filepath = os.path.join(self.excel_folder, filename)
        
        # Chuyển đổi dữ liệu sang DataFrame
        df = pd.DataFrame(self.data)
        
        # Sắp xếp lại thứ tự cột
        columns_order = ['name', 'date', 'check_in', 'check_out', 'working_hours']
        available_columns = [col for col in columns_order if col in df.columns]
        df = df[available_columns]
        
        # Đổi tên cột sang tiếng Việt
        column_names = {
            'name': 'Họ và Tên',
            'date': 'Ngày',
            'check_in': 'Giờ Vào',
            'check_out': 'Giờ Ra',
            'working_hours': 'Tổng Giờ Làm'
        }
        df = df.rename(columns=column_names)
        
        # Xuất ra Excel
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Chấm Công')
            
            # Tự động điều chỉnh độ rộng cột
            worksheet = writer.sheets['Chấm Công']
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(str(col))
                )
                worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2
        
        print(f'Đã xuất file Excel: {filepath}')
        return filepath
    
    def get_today_records(self):
        '''Lấy các bản ghi của ngày hôm nay'''
        today = datetime.now().strftime("%d-%m-%Y")
        return [record for record in self.data if record.get('date') == today]
    
    def clear_old_records(self, days=30):
        '''Xóa các bản ghi cũ hơn X ngày'''
        cutoff_date = datetime.now()
        # Giữ lại các bản ghi mới, cần implement logic so sánh ngày nếu cần
        pass
