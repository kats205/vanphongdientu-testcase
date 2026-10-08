import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_007_zero_width_username(utc_plain_page):
    """UTC-LOGIN-NEG-007: Tên đăng nhập chỉ chứa ký tự zero-width U+200B."""
    utc_plain_page.enter_credentials("​", "utc-dummy-password")
    utc_plain_page.set_persistent(False)
    utc_plain_page.assert_rejected()
