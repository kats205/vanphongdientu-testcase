# Automation kiểm thử với Selenium và Pytest

Dự án dùng Python, Selenium WebDriver, Pytest và Page Object Model. Bộ UTC gồm **26 test case lỗi**, đánh số liên tục `UTC-LOGIN-NEG-001` đến `UTC-LOGIN-NEG-026`; mỗi case nằm trong một file riêng. Các test mẫu SauceDemo và test đóng/mở Edge vẫn nằm trong dự án.

## Tài liệu và trạng thái kiểm tra

- [CSV test case UTC](docs/utc_login_negative_test_cases.csv): dữ liệu, bước thực hiện, kết quả mong đợi và trạng thái từng case.
- [Báo cáo automation UTC](docs/utc_login_automation_report.md): selector, bao phủ hai trạng thái CAPTCHA, bảng đổi số, case đã loại và bằng chứng kiểm tra.

Đã kiểm tra cấu trúc 26 file và selector trên HTML tham chiếu bằng Chrome headless. Đã thử cả headless và có cửa sổ. Chạy trên UTC thật hiện bị chặn bởi `net::ERR_NETWORK_ACCESS_DENIED` trong môi trường thực thi; chưa có kết quả pass nghiệp vụ UTC. Thu thập test và kiểm tra HTML tham chiếu không thay thế kết quả chạy trên website thật.

## Cấu trúc

```text
TestCase/
├── config/config.py                  # Cấu hình môi trường
├── pages/
│   ├── base_page.py                   # Thao tác Selenium dùng chung
│   ├── utc_login_page.py              # Form UTC có và không có CAPTCHA
│   ├── login_page.py                  # Đăng nhập SauceDemo
│   └── inventory_page.py              # Sản phẩm SauceDemo
├── tests/
│   ├── utc_login/                     # 26 file, mỗi file một case UTC
│   │   └── conftest.py                # Fixture hai trạng thái và chuyển CAPTCHA
│   ├── test_login.py                  # Test mẫu SauceDemo
│   ├── test_inventory.py              # Test mẫu SauceDemo
│   └── test_edge_browser.py           # Đóng/mở Edge
├── docs/
│   ├── utc_login_negative_test_cases.csv
│   └── utc_login_automation_report.md
├── utils/                            # WebDriver và log
├── reports/                          # Kết quả chạy, log và ảnh lỗi
├── conftest.py                       # Setup/teardown và hook báo cáo
├── pytest.ini
├── requirements.txt
├── .env.example
└── README.md
```

## Cài đặt

Cần Python, Chrome hoặc Edge và khả năng truy cập website kiểm thử. Khi tạo môi trường mới trên Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Nếu đã có `.venv`, dùng môi trường đó. Có thể tạo `.env` từ `.env.example` khi chưa có file cấu hình. Selenium dùng driver trên `PATH` nếu tìm thấy; nếu không, Selenium Manager tìm driver phù hợp. Driver phải tương thích với trình duyệt.

## Cấu hình

| Biến | Ý nghĩa |
| --- | --- |
| `BROWSER` | `chrome` hoặc `edge`; mặc định `chrome` |
| `HEADLESS` | `false` mặc định trong .env.example: có cửa sổ; `true`: chạy headless. --headless trên lệnh chạy ghi đè giá trị này |
| `BASE_URL` | Dùng cho test mẫu SauceDemo; bộ UTC dùng URL riêng trong `UtcLoginPage` |
| `TIMEOUT` | Thời gian chờ thao tác và tải trang; mặc định 10 giây |
| `UTC_CAPTCHA_SETUP_ATTEMPTS` | Ngân sách chuẩn bị CAPTCHA, mặc định 3, cho phép 0–10; đọc từ biến môi trường |

`UTC_CAPTCHA_SETUP_ATTEMPTS` là giới hạn của bộ test, không phải ngưỡng CAPTCHA đã xác nhận của UTC. Fixture dùng thông tin tổng hợp để nhận phản hồi từ chối và dừng nếu không đạt tiền điều kiện. Không đọc hoặc giải CAPTCHA.

## Chạy test

Thu thập toàn bộ test, không mở trình duyệt:

```powershell
.\.venv\Scripts\python.exe -m pytest --collect-only --strict-markers
```

Chạy riêng 26 case UTC bằng Chrome headless và dừng khi gặp lỗi đầu tiên:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/utc_login --browser=chrome --headless=true --strict-markers --maxfail=1 --html=reports/utc_login_report.html --self-contained-html --junitxml=reports/utc_login_results.xml
```

Chạy riêng UTC có cửa sổ (không headless):

```powershell
.\.venv\Scripts\python.exe -m pytest tests/utc_login --browser=chrome --headless=false --strict-markers --maxfail=1 --html=reports/utc_login_headed_report.html --self-contained-html --junitxml=reports/utc_login_headed_results.xml
```

Marker UTC không ép chế độ trình duyệt. Lượt kiểm tra có cửa sổ đã chạy case 001/008/026: cả ba lỗi setup khi tải UTC, chưa gửi form. Xem bằng chứng trong báo cáo automation.

Chạy case chuyển từ không CAPTCHA sang có CAPTCHA:

```powershell
$env:UTC_CAPTCHA_SETUP_ATTEMPTS = "3"
.\.venv\Scripts\python.exe -m pytest tests/utc_login/test_neg_026_plain_to_captcha_rejections.py --browser=chrome --headless=true --strict-markers
```

Case không CAPTCHA yêu cầu form ban đầu chưa có CAPTCHA. Case có CAPTCHA phải quan sát được CAPTCHA trước khi thực hiện. Case 026 bắt buộc bắt đầu không CAPTCHA và quan sát CAPTCHA xuất hiện sau phản hồi từ chối. Thiếu tiền điều kiện là lỗi setup; không tính là pass hoặc tự kết luận bug sản phẩm.

Chạy test mẫu hoặc nhóm Edge:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_login.py tests/test_inventory.py --browser=chrome --headless=true
.\.venv\Scripts\python.exe -m pytest tests/test_edge_browser.py --headless=true
```

Chạy toàn dự án gồm cả UTC, SauceDemo và Edge:

```powershell
.\.venv\Scripts\python.exe -m pytest --headless=true
```

Marker `login` gồm cả UTC và SauceDemo; dùng `-m utc_login` để chọn riêng UTC. Các marker khác được khai báo trong `pytest.ini`.

## Chế độ trình duyệt và lỗi truy cập

Mặc định đã đặt HEADLESS=false trong .env.example và cấu hình .env cục bộ theo yêu cầu chạy có cửa sổ. Không cần truyền --headless=false khi dùng cấu hình này; có thể truyền rõ cờ để ghi đè. Đã xác minh Chrome thực sự không có tham số --headless khi khởi động với cấu hình mặc định.

Lỗi truy cập được kiểm tra độc lập với Selenium: cả kết nối TCP cổng 443 và HTTPS đến UTC đều bị PermissionError / WinError 10013 (quyền socket bị từ chối) trong môi trường thực thi hiện tại. Đổi chế độ trình duyệt không khắc phục được hạn chế này. Chạy trên môi trường truy cập được UTC để kiểm chứng nghiệp vụ; nếu website tải được mà test vẫn lỗi, cần log của lượt chạy đó để sửa đúng case/selector.

Người dùng đã xác nhận mở trang UTC bằng Chrome thường được. Việc Selenium chạy trong Codex bị chặn mạng không chứng minh máy người dùng hoặc website bị lỗi. Để lấy kết quả nghiệp vụ, mở PowerShell trực tiếp trên máy tại thư mục dự án, rồi chạy:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/utc_login --browser=chrome --headless=false --strict-markers --maxfail=3 --html=reports/utc_login_local_report.html --self-contained-html --junitxml=reports/utc_login_local_results.xml
```

Các file local_report.html và local_results.xml được tạo bởi lượt chạy này; chưa có kết quả trước khi lệnh được thực thi. Bộ test giữ nguyên URL HTTPS, kiểm tra phản hồi mới và tiền điều kiện CAPTCHA.

## Báo cáo kết quả

Mặc định Pytest tạo `reports/test_report.html`. Các lệnh UTC bên trên tạo HTML và JUnit XML riêng. Log được lưu trong `reports/`; ảnh lỗi nằm trong `reports/screenshots/`.

Hook chụp ảnh khi test thất bại ở bước thực thi (`call`) và driver còn hoạt động. Lỗi setup khi tải trang không được hook này chụp ảnh. Phân biệt lỗi setup (`ERROR`) với assertion thất bại (`FAILED`) khi đọc báo cáo.

## Thêm test case

Tạo Page Object trong `pages/`, kế thừa `BasePage`. Với UTC, tạo một file `test_neg_NNN_<mo_ta>.py` chứa đúng một hàm test, gắn marker `login` và `utc_login`, rồi dùng fixture phù hợp với trạng thái form. Kiểm tra bằng chứng từ chối mới thay vì chỉ nhìn thông báo lỗi còn lại từ lần gửi trước.

Cập nhật đồng thời CSV và bảng mapping trong báo cáo. Chỉ thêm case có dữ liệu và chính sách đủ để xác định kết quả mong đợi. Không thêm unit test hoặc case bỏ qua để tăng số lượng.
