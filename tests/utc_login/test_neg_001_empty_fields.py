import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_001_empty_fields(utc_plain_page):
    """UTC-LOGIN-NEG-001: Bỏ trống cả hai trường."""
    utc_plain_page.enter_credentials("", "")
    utc_plain_page.set_persistent(False)
    utc_plain_page.assert_rejected()
