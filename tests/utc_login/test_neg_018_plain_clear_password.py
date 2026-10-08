import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_018_plain_clear_password(utc_plain_page):
    """UTC-LOGIN-NEG-018: Không CAPTCHA: xóa mật khẩu đã nhập trước khi gửi."""
    utc_plain_page.enter_credentials("utc-input-placeholder", "utc-dummy-password")
    utc_plain_page.clear_password()
    utc_plain_page.set_persistent(False)
    utc_plain_page.assert_rejected()
