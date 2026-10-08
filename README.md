# Automation kiểm thử với Selenium và Pytest

Dự án kiểm thử tự động sử dụng Python, Selenium WebDriver, Pytest và mô hình Page Object Model (POM). Bộ kiểm thử UTC gồm **26 test case tiêu cực (negative)**, đánh số liên tục từ `UTC-LOGIN-NEG-001` đến `UTC-LOGIN-NEG-026`; mỗi test case được tổ chức trong một file kiểm thử riêng biệt. Ngoài ra, dự án còn tích hợp các bài test mẫu trên SauceDemo và kịch bản đóng/mở trình duyệt Microsoft Edge.

## Tài liệu và kết quả kiểm tra

- [CSV danh sách test case UTC](docs/utc_login_negative_test_cases.csv): Bảng dữ liệu chi tiết, các bước thực hiện, kết quả mong đợi, kết quả thực tế và trạng thái thực thi của toàn bộ 26 test case (100% Đạt).
- [Báo cáo kết quả thực thi kiểm thử UTC](docs/utc_login_execution_report.md): Báo cáo tổng hợp chi tiết đợt chạy thực tế trên Google Chrome có giao diện (26/26 Đạt, thời gian chạy 14 phút 25 giây).
- [Báo cáo đặc tả automation UTC](docs/utc_login_automation_report.md): Phân tích selector, độ bao phủ hai trạng thái (có và không có CAPTCHA), xử lý phản hồi lỗi và bằng chứng đối chiếu.
- [Báo cáo HTML trực quan](reports/utc_login_local_report.html): Báo cáo kiểm thử dạng HTML sinh tự động bởi pytest-html.
- [Báo cáo JUnit XML](reports/utc_login_local_results.xml): Kết quả kiểm thử chuẩn XML phục vụ tích hợp CI/CD và theo dõi thời gian thực thi.

## Cấu trúc thư mục

```text
TestCase/
├── config/
│   ├── __init__.py
│   └── config.py                      # Cấu hình môi trường và biến hệ thống
├── pages/
│   ├── __init__.py
│   ├── base_page.py                   # Thao tác Selenium dùng chung (POM Base)
│   └── utc_login_page.py              # Page Object trang đăng nhập UTC (có/không CAPTCHA)
├── tests/
│   ├── utc_login/                     # 26 file kiểm thử cho 26 test case UTC riêng biệt
│   │   ├── conftest.py                # Fixture quản lý trạng thái form thường và CAPTCHA
│   │   ├── test_neg_001_empty_fields.py
│   │   ├── ...
│   │   └── test_neg_026_plain_to_captcha_rejections.py
│   └── test_edge_browser.py           # Test case đóng/mở Microsoft Edge
├── docs/
│   ├── utc_login_negative_test_cases.csv
│   ├── utc_login_automation_report.md
│   └── utc_login_execution_report.md
├── utils/
│   ├── __init__.py
│   ├── driver_factory.py              # Quản lý khởi tạo WebDriver (Chrome/Edge)
│   └── logger.py                      # Tiện ích ghi log UTF-8 ra console và file
├── reports/                           # Kết quả chạy kiểm thử, log và ảnh chụp lỗi
│   ├── utc_login_local_report.html    # Báo cáo HTML chạy live UTC
│   ├── utc_login_local_results.xml    # Báo cáo JUnit XML chạy live UTC
│   ├── test_report.html               # Báo cáo HTML chung của dự án
│   └── screenshots/                   # Thư mục lưu ảnh khi có test case thất bại
├── open_close_edge.py                 # Script tự động mở và đóng Edge trực quan
├── conftest.py                        # Cấu hình pytest fixture toàn cục và hook báo cáo
├── pytest.ini                         # Cấu hình pytest và khai báo marker
├── requirements.txt                   # Danh sách thư viện phụ thuộc
├── .env.example                       # File mẫu biến môi trường
├── .gitignore                         # Danh sách file và thư mục loại trừ
└── README.md
```

## Cài đặt môi trường

Yêu cầu máy tính đã cài đặt Python (>= 3.10), Google Chrome hoặc Microsoft Edge.

Để thiết lập môi trường trên Windows PowerShell:

```powershell
# Tạo môi trường ảo
py -m venv .venv

# Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

Nếu đã có sẵn `.venv`, bạn chỉ cần kích hoạt và sử dụng. Có thể sao chép file `.env.example` thành `.env` để điều chỉnh cấu hình theo nhu cầu:

```powershell
Copy-Item .env.example .env
```

## Cấu hình hệ thống

Các thiết lập trong file `.env` hoặc [config/config.py](config/config.py):

| Biến môi trường | Giá trị mặc định | Ý nghĩa |
| --- | --- | --- |
| `BROWSER` | `chrome` | Trình duyệt thực thi: `chrome` hoặc `edge` |
| `HEADLESS` | `false` | `false`: mở cửa sổ trình duyệt; `true`: chạy ngầm không hiển thị cửa sổ |
| `BASE_URL` | `https://www.saucedemo.com` | URL cơ sở dùng cho các test mẫu |
| `TIMEOUT` | `10` | Thời gian chờ tối đa (giây) cho các thao tác tìm kiếm phần tử |
| `UTC_CAPTCHA_SETUP_ATTEMPTS` | `3` | Số lần thử gửi form sai để kích hoạt CAPTCHA (từ 0 đến 10) |

## Hướng dẫn chạy kiểm thử

### 1. Chạy toàn bộ 26 test case UTC (có giao diện trực quan)

```powershell
.\.venv\Scripts\python.exe -m pytest tests/utc_login --browser=chrome --headless=false --strict-markers --maxfail=3 --html=reports/utc_login_local_report.html --self-contained-html --junitxml=reports/utc_login_local_results.xml
```

### 2. Chạy riêng từng test case UTC

Chạy test case cụ thể (ví dụ case 001 - Bỏ trống cả hai trường):

```powershell
.\.venv\Scripts\python.exe -m pytest tests/utc_login/test_neg_001_empty_fields.py --browser=chrome --headless=false
```

Chạy test case kiểm tra chuyển trạng thái từ form thường sang CAPTCHA (case 026):

```powershell
$env:UTC_CAPTCHA_SETUP_ATTEMPTS = "3"
.\.venv\Scripts\python.exe -m pytest tests/utc_login/test_neg_026_plain_to_captcha_rejections.py --browser=chrome --headless=false
```

### 3. Chạy các bài test khác trong dự án

Chạy bài test kiểm tra đóng mở trình duyệt Edge:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_edge_browser.py
# Hoặc chạy script trực tiếp:
.\.venv\Scripts\python.exe open_close_edge.py
```

Chạy toàn bộ tất cả các test trong dự án:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Báo cáo và kết quả thực thi

Sau khi chạy xong, kết quả sẽ được ghi nhận tại các đường dẫn:

- Báo cáo HTML trực quan: [reports/utc_login_local_report.html](reports/utc_login_local_report.html)
- Báo cáo kết quả kiểm thử Markdown: [docs/utc_login_execution_report.md](docs/utc_login_execution_report.md)
- Bảng danh sách và trạng thái chi tiết: [docs/utc_login_negative_test_cases.csv](docs/utc_login_negative_test_cases.csv)
- Dữ liệu kết quả XML: [reports/utc_login_local_results.xml](reports/utc_login_local_results.xml)
- File nhật ký thực thi chi tiết: `reports/test_execution.log`
- Ảnh chụp màn hình khi có lỗi: `reports/screenshots/`

## Thêm test case mới

1. Định nghĩa hoặc bổ sung các selector và phương thức tương tác vào Page Object tương ứng trong [pages/](pages/).
2. Tạo file kiểm thử mới trong thư mục [tests/](tests/) (hoặc [tests/utc_login/](tests/utc_login/)) theo tiền tố `test_*.py`. Mỗi file kiểm thử chứa đúng 1 hàm test độc lập để phục vụ commit và theo dõi riêng biệt.
3. Cập nhật mã test case và kết quả tương ứng vào [docs/utc_login_negative_test_cases.csv](docs/utc_login_negative_test_cases.csv).
