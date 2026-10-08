import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_023_captcha_space_password_and_code(utc_captcha_page):
    """UTC-LOGIN-NEG-023: Có CAPTCHA: tên trống, mật khẩu và mã chỉ chứa dấu cách."""
    utc_captcha_page.enter_credentials("", "   ")
    utc_captcha_page.enter_captcha("   ")
    utc_captcha_page.set_persistent(False)
    utc_captcha_page.assert_rejected()
