import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_013_captcha_empty_after_refresh(utc_captcha_page):
    """UTC-LOGIN-NEG-013: Form CAPTCHA: dữ liệu rỗng sau khi đổi ảnh mã bảo mật."""
    utc_captcha_page.refresh_captcha()
    utc_captcha_page.enter_credentials("", "")
    utc_captcha_page.enter_captcha("")
    utc_captcha_page.set_persistent(False)
    utc_captcha_page.assert_rejected()
