import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_002_whitespace_username(utc_plain_page):
    """UTC-LOGIN-NEG-002: Tên đăng nhập chỉ chứa dấu cách."""
    utc_plain_page.enter_credentials("   ", "utc-dummy-password")
    utc_plain_page.set_persistent(False)
    utc_plain_page.assert_rejected()
