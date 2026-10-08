import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_003_whitespace_fields(utc_plain_page):
    """UTC-LOGIN-NEG-003: Cả hai trường chỉ chứa dấu cách."""
    utc_plain_page.enter_credentials("   ", "   ")
    utc_plain_page.set_persistent(False)
    utc_plain_page.assert_rejected()
