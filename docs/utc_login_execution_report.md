# Báo cáo kết quả kiểm thử tự động đăng nhập UTC

Ngày lập báo cáo: 08/10/2026.
Hệ thống kiểm thử: Văn phòng điện tử UTC (https://vanphongdientu.utc.edu.vn/Login).

## 1. Tổng quan đợt kiểm thử

Đợt kiểm thử tự động được thực hiện trực tiếp trên hệ thống website Văn phòng điện tử UTC nhằm kiểm tra toàn bộ các kịch bản tiêu cực (negative test cases) đối với chức năng đăng nhập và cơ chế kích hoạt bảo vệ CAPTCHA.

- Công cụ kiểm thử: Python 3.14, Selenium WebDriver, Pytest.
- Trình duyệt: Google Chrome (Phiên bản trình duyệt trực quan, tham số --headless=false).
- Tổng số test case: 26 test cases (tương ứng với 26 file test riêng biệt).
- Lệnh thực thi:
  python -m pytest tests/utc_login --browser=chrome --headless=false --maxfail=3 --html=reports/utc_login_local_report.html --junitxml=reports/utc_login_local_results.xml
- Thời gian bắt đầu: 17:07:38 ngày 08/10/2026.
- Tổng thời gian chạy: 865.53 giây (tương đương 14 phút 25 giây).

## 2. Kết quả thực thi tổng hợp

| Chỉ số | Giá trị | Tỷ lệ |
| --- | --- | --- |
| Tổng số test case đã chạy | 26 | 100% |
| Số test case Đạt (Pass) | 26 | 100% |
| Số test case Thất bại (Fail) | 0 | 0% |
| Số test case Bị lỗi (Error) | 0 | 0% |
| Số test case Bị bỏ qua (Skipped) | 0 | 0% |
| Số lượng cảnh báo (Warning) | 1 | PytestWarning về phương thức record_property trong xunit2 |

Tất cả 26 test case đều hoàn thành thành công, được kiểm tra thực tế trên trình duyệt Chrome mở trực quan trên màn hình, xác thực đầy đủ các tiêu chí từ chối đăng nhập và kiểm tra giao diện hệ thống.

## 3. Phân loại theo trạng thái và nhóm chức năng

### 3.1. Nhóm form ban đầu không có CAPTCHA (13 test cases)
Bao gồm các test case từ UTC-LOGIN-NEG-001 đến 007 và UTC-LOGIN-NEG-015 đến 020:
- Kiểm tra bỏ trống các trường bắt buộc (tên đăng nhập, mật khẩu).
- Kiểm tra chuỗi khoảng trắng thông thường, ký tự trắng đặc biệt (NBSP U+00A0, Zero-Width Space U+200B).
- Kiểm tra giá trị biên độ dài 0 ký tự.
- Kiểm tra thao tác gửi form bằng phím Enter thay vì nhấp chuột.
- Kiểm tra thao tác nhập dữ liệu rồi xóa trước khi gửi.
- Kiểm tra tùy chọn ghi nhớ đăng nhập (checkbox persistent).

Kết quả: 13/13 test cases Đạt (Pass).

### 3.2. Nhóm form ban đầu có CAPTCHA (12 test cases)
Bao gồm các test case từ UTC-LOGIN-NEG-008 đến 014 và UTC-LOGIN-NEG-021 đến 025:
- Kiểm tra bỏ trống mã bảo mật cùng thông tin đăng nhập.
- Kiểm tra mã bảo mật chứa khoảng trắng, ký tự trắng NBSP, Zero-Width space.
- Kiểm tra mã bảo mật được nhập hợp lệ về mặt ký tự nhưng để trống thông tin đăng nhập.
- Kiểm tra làm mới ảnh CAPTCHA qua liên kết đổi mã trước khi gửi.
- Kiểm tra gửi form có CAPTCHA bằng phím Enter.
- Kiểm tra thao tác nhập mã CAPTCHA rồi xóa trước khi gửi.

Kết quả: 12/12 test cases Đạt (Pass).

### 3.3. Nhóm chuyển trạng thái kích hoạt CAPTCHA (1 test case)
Bao gồm test case UTC-LOGIN-NEG-026:
- Khởi đầu tại trang Login ở trạng thái không có CAPTCHA.
- Thực hiện gửi thông tin đăng nhập không hợp lệ để ghi nhận phản hồi từ chối từ máy chủ.
- Xác minh và ghi nhận CAPTCHA xuất hiện sau đúng 3 lần gửi sai liên tiếp (captcha_setup_attempts = 3).
- Sau khi CAPTCHA xuất hiện, gửi dữ liệu rỗng để xác minh hệ thống tiếp tục chặn truy cập và giữ nguyên các thành phần kiểm soát CAPTCHA.

Kết quả: 1/1 test case Đạt (Pass).

## 4. Bảng chi tiết kết quả 26 test cases

| Mã test case | Tên test case | Trạng thái form | Thời gian (s) | Kết quả | Ghi chú kết quả thực tế |
| --- | --- | --- | --- | --- | --- |
| UTC-LOGIN-NEG-001 | Bỏ trống cả hai trường | Không CAPTCHA | 33.87 | Đạt | Từ chối đăng nhập, hiển thị thông báo lỗi/validation, giữ nguyên tại /Login |
| UTC-LOGIN-NEG-002 | Tên đăng nhập chỉ chứa dấu cách | Không CAPTCHA | 27.78 | Đạt | Từ chối đăng nhập, hiển thị thông báo lỗi/validation, giữ nguyên tại /Login |
| UTC-LOGIN-NEG-003 | Cả hai trường chỉ chứa dấu cách | Không CAPTCHA | 28.06 | Đạt | Từ chối đăng nhập, hiển thị thông báo lỗi/validation, giữ nguyên tại /Login |
| UTC-LOGIN-NEG-004 | Tên đăng nhập chứa NBSP U+00A0 | Không CAPTCHA | 28.27 | Đạt | Từ chối đăng nhập, hiển thị thông báo lỗi/validation, giữ nguyên tại /Login |
| UTC-LOGIN-NEG-005 | Tên đăng nhập dài 0 ký tự | Không CAPTCHA | 27.99 | Đạt | Từ chối đăng nhập, hiển thị thông báo lỗi/validation, giữ nguyên tại /Login |
| UTC-LOGIN-NEG-006 | Dữ liệu rỗng khi chọn giữ đăng nhập | Không CAPTCHA | 28.23 | Đạt | Từ chối đăng nhập, hiển thị thông báo lỗi/validation, giữ nguyên tại /Login |
| UTC-LOGIN-NEG-007 | Tên đăng nhập chứa zero-width U+200B | Không CAPTCHA | 28.38 | Đạt | Từ chối đăng nhập, hiển thị thông báo lỗi/validation, giữ nguyên tại /Login |
| UTC-LOGIN-NEG-008 | Form CAPTCHA: để trống toàn bộ | Có CAPTCHA | 38.75 | Đạt | Từ chối đăng nhập, xác nhận form CAPTCHA hiển thị đúng và giữ nguyên tại trang |
| UTC-LOGIN-NEG-009 | Form CAPTCHA: mã chỉ chứa dấu cách | Có CAPTCHA | 38.26 | Đạt | Từ chối đăng nhập, xác nhận form CAPTCHA hiển thị đúng và giữ nguyên tại trang |
| UTC-LOGIN-NEG-010 | Form CAPTCHA: mã chứa NBSP | Có CAPTCHA | 36.17 | Đạt | Từ chối đăng nhập, xác nhận form CAPTCHA hiển thị đúng và giữ nguyên tại trang |
| UTC-LOGIN-NEG-011 | Form CAPTCHA: mã chứa zero-width | Có CAPTCHA | 36.66 | Đạt | Từ chối đăng nhập, xác nhận form CAPTCHA hiển thị đúng và giữ nguyên tại trang |
| UTC-LOGIN-NEG-012 | Form CAPTCHA: chọn giữ đăng nhập | Có CAPTCHA | 37.11 | Đạt | Từ chối đăng nhập, xác nhận form CAPTCHA hiển thị đúng và giữ nguyên tại trang |
| UTC-LOGIN-NEG-013 | Form CAPTCHA: đổi ảnh mã bảo mật | Có CAPTCHA | 36.73 | Đạt | Đường dẫn ảnh CAPTCHA đổi thành công, từ chối đăng nhập khi dữ liệu rỗng |
| UTC-LOGIN-NEG-014 | Form CAPTCHA: gửi bằng phím Enter | Có CAPTCHA | 36.52 | Đạt | Gửi form bằng Enter thành công, hệ thống từ chối đăng nhập hợp lệ |
| UTC-LOGIN-NEG-015 | Không CAPTCHA: mật khẩu trống | Không CAPTCHA | 27.41 | Đạt | Từ chối đăng nhập, hiển thị thông báo lỗi/validation, giữ nguyên tại /Login |
| UTC-LOGIN-NEG-016 | Không CAPTCHA: mật khẩu dấu cách | Không CAPTCHA | 27.77 | Đạt | Từ chối đăng nhập, hiển thị thông báo lỗi/validation, giữ nguyên tại /Login |
| UTC-LOGIN-NEG-017 | Không CAPTCHA: Enter với trường rỗng | Không CAPTCHA | 30.00 | Đạt | Gửi form bằng Enter thành công, hệ thống từ chối đăng nhập hợp lệ |
| UTC-LOGIN-NEG-018 | Không CAPTCHA: xóa mật khẩu đã nhập | Không CAPTCHA | 27.92 | Đạt | Thao tác xóa mật khẩu chính xác, form gửi dữ liệu rỗng và bị từ chối |
| UTC-LOGIN-NEG-019 | Không CAPTCHA: xóa tên đã nhập | Không CAPTCHA | 27.92 | Đạt | Thao tác xóa tên đăng nhập chính xác, form gửi bị từ chối hợp lệ |
| UTC-LOGIN-NEG-020 | Không CAPTCHA: Enter với dấu cách | Không CAPTCHA | 30.05 | Đạt | Gửi form bằng Enter thành công, hệ thống từ chối đăng nhập hợp lệ |
| UTC-LOGIN-NEG-021 | Có CAPTCHA: mật khẩu và mã trống | Có CAPTCHA | 36.87 | Đạt | Từ chối đăng nhập, giữ nguyên tại /Login với các điều khiển CAPTCHA đầy đủ |
| UTC-LOGIN-NEG-022 | Có CAPTCHA: tên và mã trống | Có CAPTCHA | 38.04 | Đạt | Từ chối đăng nhập, giữ nguyên tại /Login với các điều khiển CAPTCHA đầy đủ |
| UTC-LOGIN-NEG-023 | Có CAPTCHA: mật khẩu và mã dấu cách | Có CAPTCHA | 38.03 | Đạt | Từ chối đăng nhập, giữ nguyên tại /Login với các điều khiển CAPTCHA đầy đủ |
| UTC-LOGIN-NEG-024 | Có CAPTCHA: xóa mã đã nhập | Có CAPTCHA | 37.42 | Đạt | Thao tác xóa mã bảo mật chính xác, gửi form và bị từ chối hợp lệ |
| UTC-LOGIN-NEG-025 | Có CAPTCHA: mã không rỗng, user rỗng | Có CAPTCHA | 36.12 | Đạt | Từ chối đăng nhập khi thông tin đăng nhập để trống |
| UTC-LOGIN-NEG-026 | Chuyển trạng thái sang có CAPTCHA | Chuyển đổi | 45.08 | Đạt | Xác nhận CAPTCHA xuất hiện sau 3 lần thử; từ chối đăng nhập sau đó |

## 5. Nhận xét và đánh giá kỹ thuật

1. Độ tin cậy của hệ thống xác thực:
- Hệ thống Văn phòng điện tử UTC hoạt động ổn định trong suốt 14 phút kiểm thử liên tục.
- Tất cả các tổ hợp dữ liệu tiêu cực đều bị chặn chính xác ở phía giao diện hoặc phía máy chủ, không cấp phiên đăng nhập sai trái.
- Không xảy ra tình trạng sập ứng dụng, không xuất hiện lỗi máy chủ nội bộ (HTTP 500, 502, 503).

2. Cơ chế kích hoạt CAPTCHA:
- Cơ chế phát hiện truy cập bất thường và bắt buộc nhập CAPTCHA hoạt động đúng theo thiết kế bảo mật. Sau khi phát hiện các lần đăng nhập sai liên tiếp, hệ thống tự động bổ sung trường nhập mã bảo mật và ảnh CAPTCHA.
- Chức năng thay đổi ảnh CAPTCHA (liên kết đổi mã) cập nhật đường dẫn ảnh mới chính xác khi người dùng yêu cầu.

3. Tính toàn vẹn của giao diện:
- Các phần tử nhập liệu (input name=username, input name=userpwd, input name=captcha, nút submit, checkbox persistent) giữ nguyên cấu trúc DOM và không bị lỗi hiển thị sau khi nhận thông báo từ chối.

## 6. Các tài liệu và bằng chứng kèm theo

- File kết quả chi tiết định dạng JUnit XML:
  reports/utc_login_local_results.xml
- File báo cáo trực quan định dạng HTML:
  reports/utc_login_local_report.html
- File danh sách test case cập nhật kết quả:
  docs/utc_login_negative_test_cases.csv
