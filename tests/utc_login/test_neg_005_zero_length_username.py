import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_005_zero_length_username(utc_plain_page):
    """UTC-LOGIN-NEG-005: Tên đăng nhập dài 0 ký tự."""
    utc_plain_page.enter_credentials("", "utc-dummy-password")
    utc_plain_page.set_persistent(False)
    utc_plain_page.assert_rejected()
