import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_011_captcha_zero_width(utc_captcha_page):
    """UTC-LOGIN-NEG-011: Form CAPTCHA: mã bảo mật chỉ có zero-width, thông tin đăng nhập rỗng."""
    utc_captcha_page.enter_credentials("", "")
    utc_captcha_page.enter_captcha("\u200b")
    utc_captcha_page.set_persistent(False)
    utc_captcha_page.assert_rejected()
