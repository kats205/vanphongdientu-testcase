import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_015_plain_empty_password(utc_plain_page):
    """UTC-LOGIN-NEG-015: Không CAPTCHA: tên đăng nhập không rỗng và mật khẩu trống."""
    utc_plain_page.enter_credentials("utc-input-placeholder", "")
    utc_plain_page.set_persistent(False)
    utc_plain_page.assert_rejected()
