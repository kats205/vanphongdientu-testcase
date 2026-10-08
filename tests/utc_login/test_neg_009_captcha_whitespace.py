import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_009_captcha_whitespace(utc_captcha_page):
    """UTC-LOGIN-NEG-009: Form CAPTCHA: mã bảo mật chỉ có dấu cách, thông tin đăng nhập rỗng."""
    utc_captcha_page.enter_credentials("", "")
    utc_captcha_page.enter_captcha("   ")
    utc_captcha_page.set_persistent(False)
    utc_captcha_page.assert_rejected()
