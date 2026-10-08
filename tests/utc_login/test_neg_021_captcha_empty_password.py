import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_021_captcha_empty_password(utc_captcha_page):
    """UTC-LOGIN-NEG-021: Có CAPTCHA: tên không rỗng, mật khẩu và CAPTCHA trống."""
    utc_captcha_page.enter_credentials("utc-input-placeholder", "")
    utc_captcha_page.enter_captcha("")
    utc_captcha_page.set_persistent(False)
    utc_captcha_page.assert_rejected()
