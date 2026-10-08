# Báo cáo automation lỗi đăng nhập UTC

Ngày cập nhật: 08/10/2026. [Website UTC](https://vanphongdientu.utc.edu.vn/Login?r=https%3A%2F%2Fvanphongdientu.utc.edu.vn%2F).

## Kết quả

Bộ hiện có **26 case lỗi / 26 file riêng**, đánh số liên tục **001–026**, vượt yêu cầu ít nhất 20. [CSV](utc_login_negative_test_cases.csv) có cột trạng thái form ban đầu. Mỗi file đúng một hàm test, luôn kiểm tra từ chối; không gộp nhiều case bằng parametrize. Không viết unit test; chưa stage hoặc commit.

**Chưa có case nghiệp vụ UTC nào pass.** Chrome khởi động được ở cả chế độ headless và có cửa sổ, nhưng truy cập UTC bị chặn với net::ERR_NETWORK_ACCESS_DENIED. Kiểm tra HTML tham chiếu và thu thập Pytest không được tính thành pass trên website thật.

| Hạng mục | Bằng chứng |
| --- | --- |
| Case/file UTC | 26/26; ID và đường dẫn duy nhất |
| Không CAPTCHA | 13 case; fixture utc_plain_page |
| Có CAPTCHA | 12 case; fixture utc_captcha_page |
| Không CAPTCHA chuyển sang có CAPTCHA | 1 case; fixture utc_captcha_transition_page |
| Tính riêng biệt | 26 tổ hợp trạng thái, dữ liệu và chuỗi thao tác khác nhau |
| Thu thập toàn dự án | 36 test: 26 UTC + 10 mẫu cũ |
| Tham chiếu headless | Selector, phân biệt trạng thái, nhập/xóa, checkbox và đổi src ảnh đạt |
| Lượt live mới | Không headless: case 001/008/026 có 3 ERROR setup; chưa gửi form |
| Pass nghiệp vụ | 0 |
| Git | Giữ lịch sử 6 commit; chưa có commit mới |

## Bao phủ hai trạng thái

| Nhóm | Nội dung | Kỹ thuật |
| --- | --- | --- |
| Không CAPTCHA | Trường rỗng, mật khẩu thiếu, dấu cách, NBSP/zero-width ở tên, Enter, xóa tên/mật khẩu đã nhập, giữ đăng nhập | Phân vùng tương đương, biên 0 ký tự, bảng quyết định, đoán lỗi, chuyển trạng thái nhập liệu |
| Có CAPTCHA | Mã rỗng/trắng/Unicode, mã không rỗng cùng thông tin đăng nhập rỗng, thiếu một trường đăng nhập, xóa mã đã nhập, đổi ảnh trước khi gửi, Enter, checkbox | Phân vùng tương đương, biên 0 ký tự, bảng quyết định, chuyển trạng thái, đoán lỗi |
| Chuyển trạng thái | Bắt đầu không CAPTCHA, gửi thông tin tổng hợp bị từ chối, quan sát CAPTCHA xuất hiện, ghi số lần rồi gửi dữ liệu rỗng | Chuyển trạng thái |

Case 015–026 bổ sung 12 tình huống còn thiếu. Nhập rồi xóa và nhập rỗng ngay có dữ liệu cuối giống nhau nhưng kiểm tra hai chuỗi thao tác khác nhau, gồm nguy cơ giá trị cũ còn được gửi. Enter và click là hai đường gửi form. Không nhân bản cùng trạng thái/dữ liệu/thao tác để tăng số lượng.

Chuỗi tài khoản/mật khẩu/mã tổng hợp không được coi là dữ liệu đúng hoặc sai đã xác nhận của tài khoản thật. Các case có trường bắt buộc rỗng chỉ kiểm tra từ chối tổ hợp đó. Case 025 không khẳng định mã tổng hợp là CAPTCHA sai; hai trường đăng nhập rỗng là dữ liệu lỗi.

## Selector

HTML CAPTCHA được người dùng cung cấp cho thấy các trường username, userpwd, persistent và submit_login không đổi; bổ sung captcha, ảnh, link đổi mã và .error.

| Thành phần | CSS selector |
| --- | --- |
| Form | `form[action="/Login"][method="post"]` |
| Tên | `form[action="/Login"] input[name="username"][type="text"]` |
| Mật khẩu | `form[action="/Login"] input[name="userpwd"][type="password"]` |
| Checkbox | `form[action="/Login"] input#persistent[name="persistent"][type="checkbox"]` |
| Nhãn checkbox | `form[action="/Login"] label[for="persistent"]:not(.check)` |
| Submit | `form[action="/Login"] input.submit_login[type="submit"]` |
| Lỗi | `form[action="/Login"] .error` |
| CAPTCHA input | `form[action="/Login"] input[name="captcha"][type="text"]` |
| CAPTCHA image | `form[action="/Login"] img#captcha` |
| Đổi mã | `form[action="/Login"] a[onclick*="getElementById"][onclick*="captcha"]` |

[Page Object](../pages/utc_login_page.py) xác minh control chung và các control CAPTCHA khi xuất hiện. require_plain bắt buộc chưa có CAPTCHA; require_captcha bắt buộc đã có. Sau một lần từ chối ở form thường, CAPTCHA được phép xuất hiện và được kiểm tra như trạng thái mới.

Đã đối chiếu bằng Chrome headless trên HTML CAPTCHA được cung cấp và một biến thể bỏ CAPTCHA/.error. Biến thể thường là bản dựng tham chiếu, không phải snapshot DOM live độc lập. Chưa đối chiếu selector trên website thật.

Nhấn nhãn ngoài để đổi checkbox ẩn. Ảnh kiểm tra theo phần tử và src; không coi ảnh không tải trên data URL local là selector sai. Refresh kiểm tra src đổi theo onclick, không suy luận mã cũ hết hiệu lực hoặc ô nhập tự xóa.

Giữ [Page Object SauceDemo](../pages/login_page.py) cho các test mẫu cũ.

## Phản hồi lỗi mới

Form CAPTCHA có thể đã chứa “Tài khoản hoặc mật khẩu không đúng.” trước khi gửi tiếp. assert_rejected không pass chỉ vì thấy câu lỗi cũ.

Validation native hoặc dialog lỗi được nhận biết sau thao tác gửi. Với .error, phải thấy form cũ stale, node lỗi được thay hoặc nội dung lỗi đổi. Cùng câu lỗi sau reload vẫn được nhận biết; lỗi cũ đứng yên thì timeout/fail. Sau đó phải ở /Login của UTC với control hợp lệ. Đã thêm xử lý stale element trong lúc chờ render.

Luồng phản hồi này chưa được xác minh trên UTC live vì mạng bị chặn.

## Fixture và CAPTCHA sau nhiều lần sai

[Fixture UTC](../tests/utc_login/conftest.py) tách trạng thái:

- utc_plain_page xác minh chưa có CAPTCHA.
- utc_captcha_page dùng CAPTCHA sẵn hoặc chuẩn bị có giới hạn.
- utc_captcha_transition_page bắt đầu không CAPTCHA, yêu cầu ít nhất một phản hồi từ chối trước khi thấy CAPTCHA. Case 026 ghi captcha_setup_attempts vào JUnit XML.

prepare_captcha dùng tên tổng hợp UUID và mật khẩu mẫu, không nhắm tài khoản thật và không coi tên đó là U_NONE đã xác nhận. Mỗi lần gửi phải có bằng chứng từ chối; nếu không thì dừng.

UTC_CAPTCHA_SETUP_ATTEMPTS mặc định 3, cho phép 0–10. **Đây là ngân sách setup, không phải ngưỡng UTC.** Hết ngân sách mà chưa có CAPTCHA thì báo thiếu tiền điều kiện, không kết luận bug hoặc pass giả. Chưa xác minh bộ đếm theo phiên/IP/tài khoản.

Không giải CAPTCHA, dùng OCR, xóa control hoặc sửa request để bỏ qua CAPTCHA.

## Kết quả thực tế của 26 case trong CSV

Đã bổ sung đầy đủ hai cột Kết quả thực tế và Trạng thái cho 26 dòng, đối chiếu tất cả báo cáo HTML và JUnit hiện có. Phân biệt case đã bắt đầu thực thi với case chỉ được thu thập.

| Trạng thái hiện tại | Số case | ID |
| --- | --- | --- |
| Chặn bởi môi trường: ERROR setup | 4 | 001, 008, 015, 026 |
| Chưa thực thi | 22 | Các ID còn lại trong 001–026 |
| Pass nghiệp vụ được xác minh | 0 | Không có |

Bốn case có bằng chứng lỗi driver.get với net::ERR_NETWORK_ACCESS_DENIED, chưa gửi form. CSV ghi lượt chạy mới nhất theo timestamp JUnit, chế độ trình duyệt, thời gian case và đường dẫn bằng chứng. 22 case còn lại được ghi Chưa thực thi, không gán lỗi của case khác hoặc coi kiểm tra cú pháp/thu thập là pass. Chưa có reports/utc_login_local_results.xml hoặc reports/utc_login_local_report.html tại thời điểm đối chiếu.

Giữ nguyên ID, tên file, dữ liệu, các bước và kết quả mong đợi. [Audit đối chiếu kết quả CSV](../reports/utc_login_csv_result_audit.log).

## Mapping mỗi case một file

| ID | Trạng thái đầu | Nội dung | File automation | Trạng thái kiểm tra |
| --- | --- | --- | --- | --- |
| UTC-LOGIN-NEG-001 | Không CAPTCHA | Bỏ trống cả hai trường | [test_neg_001_empty_fields.py](../tests/utc_login/test_neg_001_empty_fields.py) | Chặn bởi môi trường |
| UTC-LOGIN-NEG-002 | Không CAPTCHA | Tên đăng nhập chỉ chứa dấu cách | [test_neg_002_whitespace_username.py](../tests/utc_login/test_neg_002_whitespace_username.py) | Chưa thực thi |
| UTC-LOGIN-NEG-003 | Không CAPTCHA | Cả hai trường chỉ chứa dấu cách | [test_neg_003_whitespace_fields.py](../tests/utc_login/test_neg_003_whitespace_fields.py) | Chưa thực thi |
| UTC-LOGIN-NEG-004 | Không CAPTCHA | Tên đăng nhập chỉ chứa NBSP U+00A0 | [test_neg_004_nbsp_username.py](../tests/utc_login/test_neg_004_nbsp_username.py) | Chưa thực thi |
| UTC-LOGIN-NEG-005 | Không CAPTCHA | Tên đăng nhập dài 0 ký tự | [test_neg_005_zero_length_username.py](../tests/utc_login/test_neg_005_zero_length_username.py) | Chưa thực thi |
| UTC-LOGIN-NEG-006 | Không CAPTCHA | Dữ liệu rỗng khi chọn giữ đăng nhập | [test_neg_006_empty_fields_persistent.py](../tests/utc_login/test_neg_006_empty_fields_persistent.py) | Chưa thực thi |
| UTC-LOGIN-NEG-007 | Không CAPTCHA | Tên đăng nhập chỉ chứa zero-width U+200B | [test_neg_007_zero_width_username.py](../tests/utc_login/test_neg_007_zero_width_username.py) | Chưa thực thi |
| UTC-LOGIN-NEG-008 | Có CAPTCHA | Form CAPTCHA: để trống mã bảo mật và thông tin đăng nhập | [test_neg_008_captcha_empty.py](../tests/utc_login/test_neg_008_captcha_empty.py) | Chặn bởi môi trường |
| UTC-LOGIN-NEG-009 | Có CAPTCHA | Form CAPTCHA: mã bảo mật chỉ có dấu cách, thông tin đăng nhập rỗng | [test_neg_009_captcha_whitespace.py](../tests/utc_login/test_neg_009_captcha_whitespace.py) | Chưa thực thi |
| UTC-LOGIN-NEG-010 | Có CAPTCHA | Form CAPTCHA: mã bảo mật chỉ có NBSP, thông tin đăng nhập rỗng | [test_neg_010_captcha_nbsp.py](../tests/utc_login/test_neg_010_captcha_nbsp.py) | Chưa thực thi |
| UTC-LOGIN-NEG-011 | Có CAPTCHA | Form CAPTCHA: mã bảo mật chỉ có zero-width, thông tin đăng nhập rỗng | [test_neg_011_captcha_zero_width.py](../tests/utc_login/test_neg_011_captcha_zero_width.py) | Chưa thực thi |
| UTC-LOGIN-NEG-012 | Có CAPTCHA | Form CAPTCHA: dữ liệu rỗng khi chọn giữ đăng nhập | [test_neg_012_captcha_empty_persistent.py](../tests/utc_login/test_neg_012_captcha_empty_persistent.py) | Chưa thực thi |
| UTC-LOGIN-NEG-013 | Có CAPTCHA | Form CAPTCHA: dữ liệu rỗng sau khi đổi ảnh mã bảo mật | [test_neg_013_captcha_empty_after_refresh.py](../tests/utc_login/test_neg_013_captcha_empty_after_refresh.py) | Chưa thực thi |
| UTC-LOGIN-NEG-014 | Có CAPTCHA | Form CAPTCHA: dữ liệu rỗng khi gửi bằng phím Enter | [test_neg_014_captcha_empty_enter.py](../tests/utc_login/test_neg_014_captcha_empty_enter.py) | Chưa thực thi |
| UTC-LOGIN-NEG-015 | Không CAPTCHA | Không CAPTCHA: tên đăng nhập không rỗng và mật khẩu trống | [test_neg_015_plain_empty_password.py](../tests/utc_login/test_neg_015_plain_empty_password.py) | Chặn bởi môi trường |
| UTC-LOGIN-NEG-016 | Không CAPTCHA | Không CAPTCHA: tên đăng nhập trống và mật khẩu chỉ có dấu cách | [test_neg_016_plain_empty_username_space_password.py](../tests/utc_login/test_neg_016_plain_empty_username_space_password.py) | Chưa thực thi |
| UTC-LOGIN-NEG-017 | Không CAPTCHA | Không CAPTCHA: gửi hai trường rỗng bằng phím Enter | [test_neg_017_plain_empty_fields_enter.py](../tests/utc_login/test_neg_017_plain_empty_fields_enter.py) | Chưa thực thi |
| UTC-LOGIN-NEG-018 | Không CAPTCHA | Không CAPTCHA: xóa mật khẩu đã nhập trước khi gửi | [test_neg_018_plain_clear_password.py](../tests/utc_login/test_neg_018_plain_clear_password.py) | Chưa thực thi |
| UTC-LOGIN-NEG-019 | Không CAPTCHA | Không CAPTCHA: xóa tên đăng nhập đã nhập trước khi gửi | [test_neg_019_plain_clear_username.py](../tests/utc_login/test_neg_019_plain_clear_username.py) | Chưa thực thi |
| UTC-LOGIN-NEG-020 | Không CAPTCHA | Không CAPTCHA: gửi hai trường chỉ chứa dấu cách bằng Enter | [test_neg_020_plain_space_fields_enter.py](../tests/utc_login/test_neg_020_plain_space_fields_enter.py) | Chưa thực thi |
| UTC-LOGIN-NEG-021 | Có CAPTCHA | Có CAPTCHA: tên không rỗng, mật khẩu và CAPTCHA trống | [test_neg_021_captcha_empty_password.py](../tests/utc_login/test_neg_021_captcha_empty_password.py) | Chưa thực thi |
| UTC-LOGIN-NEG-022 | Có CAPTCHA | Có CAPTCHA: tên trống, mật khẩu mẫu và CAPTCHA trống | [test_neg_022_captcha_empty_username.py](../tests/utc_login/test_neg_022_captcha_empty_username.py) | Chưa thực thi |
| UTC-LOGIN-NEG-023 | Có CAPTCHA | Có CAPTCHA: tên trống, mật khẩu và mã chỉ chứa dấu cách | [test_neg_023_captcha_space_password_and_code.py](../tests/utc_login/test_neg_023_captcha_space_password_and_code.py) | Chưa thực thi |
| UTC-LOGIN-NEG-024 | Có CAPTCHA | Có CAPTCHA: xóa mã đã nhập rồi gửi thông tin đăng nhập rỗng | [test_neg_024_captcha_clear_code.py](../tests/utc_login/test_neg_024_captcha_clear_code.py) | Chưa thực thi |
| UTC-LOGIN-NEG-025 | Có CAPTCHA | Có CAPTCHA: mã không rỗng nhưng hai trường đăng nhập rỗng | [test_neg_025_captcha_nonempty_code_empty_credentials.py](../tests/utc_login/test_neg_025_captcha_nonempty_code_empty_credentials.py) | Chưa thực thi |
| UTC-LOGIN-NEG-026 | Không CAPTCHA → Có CAPTCHA | Chuyển từ không CAPTCHA sang CAPTCHA sau từ chối rồi gửi dữ liệu rỗng | [test_neg_026_plain_to_captcha_rejections.py](../tests/utc_login/test_neg_026_plain_to_captcha_rejections.py) | Chặn bởi môi trường |

Mỗi file có thể thành một commit riêng khi được yêu cầu sau này. Các thay đổi Page Object, fixture, CSV và báo cáo là phần dùng chung; lần này chưa commit.

## Các mục chưa đủ điều kiện

| Mục còn thiếu | Điều kiện chưa có |
| --- | --- |
| Mật khẩu sai của tài khoản tồn tại | Tài khoản kiểm thử và dữ liệu đã xác nhận |
| CAPTCHA sai riêng với thông tin đăng nhập đúng | Tài khoản hợp lệ, đáp án/tiêu chí xác định mã sai |
| Hoa/thường, độ dài CAPTCHA | Chính sách và đáp án đã xác nhận |
| Mã cũ sau refresh, hết hạn CAPTCHA | Chính sách vô hiệu hóa/hết hạn và đáp án |
| Ngưỡng sau K lần | K và phạm vi bộ đếm |
| Cookie/session, logout, tài khoản khóa/vô hiệu hóa | Phiên/tài khoản và chính sách phù hợp |

Các case CAPTCHA với thông tin đăng nhập cũng rỗng không tách riêng nguyên nhân CAPTCHA. Không tự tạo các giả định này để bổ sung test.

