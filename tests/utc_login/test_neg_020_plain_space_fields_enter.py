import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_020_plain_space_fields_enter(utc_plain_page):
    """UTC-LOGIN-NEG-020: Không CAPTCHA: gửi hai trường chỉ chứa dấu cách bằng Enter."""
    utc_plain_page.enter_credentials("   ", "   ")
    utc_plain_page.set_persistent(False)
    utc_plain_page.assert_rejected(via_enter=True)
