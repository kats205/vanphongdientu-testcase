import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_012_captcha_empty_persistent(utc_captcha_page):
    """UTC-LOGIN-NEG-012: Form CAPTCHA: dữ liệu rỗng khi chọn giữ đăng nhập."""
    utc_captcha_page.enter_credentials("", "")
    utc_captcha_page.enter_captcha("")
    utc_captcha_page.set_persistent(True)
    utc_captcha_page.assert_rejected()
