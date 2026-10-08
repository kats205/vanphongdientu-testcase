import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_008_captcha_empty(utc_captcha_page):
    """UTC-LOGIN-NEG-008: Form CAPTCHA: để trống mã bảo mật và thông tin đăng nhập."""
    utc_captcha_page.enter_credentials("", "")
    utc_captcha_page.enter_captcha("")
    utc_captcha_page.set_persistent(False)
    utc_captcha_page.assert_rejected()
