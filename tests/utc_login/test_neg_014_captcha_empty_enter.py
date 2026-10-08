import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_014_captcha_empty_enter(utc_captcha_page):
    """UTC-LOGIN-NEG-014: Form CAPTCHA: dữ liệu rỗng khi gửi bằng phím Enter."""
    utc_captcha_page.enter_credentials("", "")
    utc_captcha_page.enter_captcha("")
    utc_captcha_page.set_persistent(False)
    utc_captcha_page.assert_rejected(via_enter=True)
