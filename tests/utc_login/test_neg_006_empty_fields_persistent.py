import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_006_empty_fields_persistent(utc_plain_page):
    """UTC-LOGIN-NEG-006: Dữ liệu rỗng khi chọn giữ đăng nhập."""
    utc_plain_page.enter_credentials("", "")
    utc_plain_page.set_persistent(True)
    utc_plain_page.assert_rejected()
