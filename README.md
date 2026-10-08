# 🚀 Dự Án Automation Testing Với Selenium & Pytest

Dự án kiểm thử tự động (Automation Test) được xây dựng bằng **Python**, **Selenium WebDriver** và **Pytest**, áp dụng mô hình chuẩn **Page Object Model (POM)** trong ngành kiểm thử phần mềm.

---

## 📁 Cấu Trúc Thư Mục (Project Structure)

```text
TestCase/
│
├── .venv/                   # Môi trường ảo Python
├── config/
│   ├── __init__.py
│   └── config.py            # Cấu hình dự án (Browser, Headless, Base URL, Timeout)
│
├── pages/                   # Lớp Page Object Model (POM)
│   ├── __init__.py
│   ├── base_page.py         # Chứa các phương thức dùng chung (click, type, wait, screenshot)
│   ├── login_page.py        # Quản lý phần tử và hành vi trang Đăng nhập
│   └── inventory_page.py    # Quản lý phần tử và hành vi trang Danh sách sản phẩm
│
├── tests/                   # Các kịch bản kiểm thử (Test Cases)
│   ├── __init__.py
│   ├── test_login.py        # Test case chức năng Đăng nhập (TC01 -> TC05)
│   ├── test_inventory.py    # Test case chức năng Sản phẩm & Giỏ hàng (TC06 -> TC08)
│   └── test_edge_browser.py # Test case kiểm tra đóng mở trình duyệt Microsoft Edge
│
├── utils/                   # Tiện ích bổ trợ
│   ├── __init__.py
│   ├── driver_factory.py    # Khởi tạo WebDriver (Chrome, Edge, Headless mode)
│   └── logger.py            # Hệ thống ghi log khi chạy test
│
├── reports/                 # Chứa kết quả kiểm thử
│   ├── test_report.html     # Báo cáo kiểm thử HTML trực quan
│   ├── test_execution.log   # File log chi tiết quá trình chạy
│   └── screenshots/         # Ảnh chụp màn hình khi có test case bị FAILED
│
├── .env                     # Biến môi trường hiện tại
├── .env.example             # File mẫu biến môi trường
├── .gitignore               # Danh sách file/thư mục bỏ qua khi dùng Git
├── conftest.py              # Pytest fixture (Setup/Teardown browser, chụp ảnh khi fail)
├── pytest.ini               # Cấu hình tùy chọn chạy Pytest và HTML report
├── requirements.txt         # Danh sách thư viện phụ thuộc
└── README.md                # Tài liệu hướng dẫn sử dụng
```

---

## 🛠️ Cài Đặt Môi Trường

### 1. Kích hoạt môi trường ảo (Virtual Environment)
Môi trường ảo `.venv` đã được tạo sẵn trong project. Để kích hoạt:

- **Trên Windows PowerShell:**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **Trên Windows Command Prompt (CMD):**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```

### 2. Cài đặt các thư viện (nếu cần trên máy khác)
```bash
pip install -r requirements.txt
```

---

## ⚙️ Cấu Hình Môi Trường (.env)

Bạn có thể chỉnh sửa file `.env` theo nhu cầu:
- `BROWSER`: `chrome` hoặc `edge`
- `HEADLESS`: `true` (chạy ngầm, không mở cửa sổ browser) hoặc `false` (mở cửa sổ trực tiếp)
- `BASE_URL`: URL trang web cần kiểm thử (mặc định: `https://www.saucedemo.com`)
- `TIMEOUT`: Thời gian chờ tối đa (giây) khi tìm kiếm element

---

## ▶️ Cách Chạy Test

### 1. Chạy toàn bộ các test case:
```powershell
.\.venv\Scripts\pytest
```

### 2. Chạy test và mở cửa sổ trình duyệt (bỏ chế độ headless):
```powershell
.\.venv\Scripts\pytest --headless=false
```

### 3. Chạy test trên trình duyệt Edge:
```powershell
.\.venv\Scripts\pytest --browser=edge
```

### 4. Chạy theo nhóm Marker:
- **Chỉ chạy Smoke Test:**
  ```powershell
  .\.venv\Scripts\pytest -m smoke
  ```
- **Chỉ chạy nhóm Login:**
  ```powershell
  .\.venv\Scripts\pytest -m login
  ```
- **Chỉ chạy nhóm Inventory:**
  ```powershell
  .\.venv\Scripts\pytest -m inventory
  ```

### 5. Chạy một file test cụ thể:
```powershell
.\.venv\Scripts\pytest tests/test_login.py
```

---

## 📊 Xem Báo Cáo Kiểm Thử (HTML Report & Screenshot)

Sau khi chạy xong, Pytest sẽ tự động tạo báo cáo HTML tại:
- `reports/test_report.html`

Bạn có thể mở file này trực tiếp bằng bất kỳ trình duyệt nào để xem:
- Tổng số test case Pass / Fail / Skipped.
- Thời gian thực thi của từng test case.
- Log chi tiết cho từng bước test.
- **Tự động chụp và đính kèm ảnh màn hình** vào báo cáo đối với các test case bị lỗi (**FAILED**).

---

## ✍️ Hướng Dẫn Thêm Test Case Mới

1. **Tạo Page Object** trong thư mục `pages/` kế thừa từ `BasePage`:
   ```python
   from pages.base_page import BasePage
   from selenium.webdriver.common.by import By

   class MyNewPage(BasePage):
       SUBMIT_BUTTON = (By.ID, "submit")

       def click_submit(self):
           self.click(self.SUBMIT_BUTTON)
   ```

2. **Tạo file test** trong thư mục `tests/` với tiền tố `test_*.py`:
   ```python
   import pytest
   from pages.my_new_page import MyNewPage

   def test_my_feature(driver):
       page = MyNewPage(driver)
       page.open("https://example.com")
       page.click_submit()
       assert ...
   ```
