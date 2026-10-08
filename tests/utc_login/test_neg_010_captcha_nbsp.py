import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_010_captcha_nbsp(utc_captcha_page):
    """UTC-LOGIN-NEG-010: Form CAPTCHA: mã bảo mật chỉ có NBSP, thông tin đăng nhập rỗng."""
    utc_captcha_page.enter_credentials("", "")
    utc_captcha_page.enter_captcha("\u00a0")
    utc_captcha_page.set_persistent(False)
    utc_captcha_page.assert_rejected()
