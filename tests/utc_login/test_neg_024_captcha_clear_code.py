import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_024_captcha_clear_code(utc_captcha_page):
    """UTC-LOGIN-NEG-024: Có CAPTCHA: xóa mã đã nhập rồi gửi thông tin đăng nhập rỗng."""
    utc_captcha_page.enter_credentials("", "")
    utc_captcha_page.enter_captcha("utc-code-placeholder")
    utc_captcha_page.clear_captcha()
    utc_captcha_page.set_persistent(False)
    utc_captcha_page.assert_rejected()
