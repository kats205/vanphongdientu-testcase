import pytest


pytestmark = [pytest.mark.login, pytest.mark.utc_login]


def test_neg_026_plain_to_captcha_rejections(utc_captcha_transition_page, record_property):
    """UTC-LOGIN-NEG-026: Chuyển từ không CAPTCHA sang CAPTCHA sau từ chối rồi gửi dữ liệu rỗng."""
    page, attempts = utc_captcha_transition_page
    record_property("captcha_setup_attempts", attempts)
    page.enter_credentials("", "")
    page.enter_captcha("")
    page.set_persistent(False)
    page.assert_rejected()
