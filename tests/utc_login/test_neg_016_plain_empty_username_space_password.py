import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_016_plain_empty_username_space_password(utc_plain_page):
    """UTC-LOGIN-NEG-016: Không CAPTCHA: tên đăng nhập trống và mật khẩu chỉ có dấu cách."""
    utc_plain_page.enter_credentials("", "   ")
    utc_plain_page.set_persistent(False)
    utc_plain_page.assert_rejected()
