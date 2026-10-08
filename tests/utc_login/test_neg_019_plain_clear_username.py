import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_019_plain_clear_username(utc_plain_page):
    """UTC-LOGIN-NEG-019: Không CAPTCHA: xóa tên đăng nhập đã nhập trước khi gửi."""
    utc_plain_page.enter_credentials("utc-input-placeholder", "utc-dummy-password")
    utc_plain_page.clear_username()
    utc_plain_page.set_persistent(False)
    utc_plain_page.assert_rejected()
