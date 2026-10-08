import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_022_captcha_empty_username(utc_captcha_page):
    """UTC-LOGIN-NEG-022: Có CAPTCHA: tên trống, mật khẩu mẫu và CAPTCHA trống."""
    utc_captcha_page.enter_credentials("", "utc-dummy-password")
    utc_captcha_page.enter_captcha("")
    utc_captcha_page.set_persistent(False)
    utc_captcha_page.assert_rejected()
