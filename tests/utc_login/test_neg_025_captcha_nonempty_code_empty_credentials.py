import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_025_captcha_nonempty_code_empty_credentials(utc_captcha_page):
    """UTC-LOGIN-NEG-025: Có CAPTCHA: mã không rỗng nhưng hai trường đăng nhập rỗng."""
    utc_captcha_page.enter_credentials("", "")
    utc_captcha_page.enter_captcha("utc-code-placeholder")
    utc_captcha_page.set_persistent(False)
    utc_captcha_page.assert_rejected()
