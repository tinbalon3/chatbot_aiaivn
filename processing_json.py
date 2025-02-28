import os
from bs4 import BeautifulSoup

# Hàm trích xuất văn bản từ file HTML
def extract_text_from_html(file_path):
    try:
        # Đọc nội dung file HTML
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Phân tích HTML bằng BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Lấy tất cả các thẻ chứa văn bản có ý nghĩa
        tags = soup.find_all(['h1', 'h2', 'h3', 'p'])  # Tiêu đề và đoạn văn
        
        # Trích xuất text từ các thẻ, loại bỏ khoảng trắng thừa
        text_data = [tag.get_text().strip() for tag in tags if tag.get_text().strip()]
        
        if not text_data:
            print(f"Không tìm thấy nội dung trong file: {file_path}")
            return []
        
        return text_data

    except Exception as e:
        print(f"Lỗi khi đọc file HTML {file_path}: {e}")
        return []

# Hàm xử lý tất cả file HTML trong thư mục và lưu vào file text
def process_html_folder(folder_path="aiaivn_data_html", output_file="html_extracted.txt"):
    text_data_all = []
    
    # Tạo thư mục nếu chưa tồn tại
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Đã tạo thư mục {folder_path}")
    
    # Duyệt qua tất cả file trong thư mục
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            file_path = os.path.join(folder_path, filename)
            text_data = extract_text_from_html(file_path)
            if text_data:
                text_data_all.extend(text_data)
    
    # Lưu tất cả dữ liệu vào file text, mỗi dòng là một đoạn
    if text_data_all:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for text in text_data_all:
                    f.write(f"{text}\n")  # Mỗi đoạn trên một dòng
            print(f"Dữ liệu đã được lưu vào {output_file}")
        except IOError as e:
            print(f"Lỗi khi lưu file: {e}")
    else:
        print("Không có dữ liệu để lưu! Vui lòng thêm file HTML vào thư mục.")
    
    return text_data_all

# Chạy thử
if __name__ == "__main__":
    process_html_folder("aiaivn_data_html", "html_extracted.txt")
    print("Xử lý hoàn tất!")