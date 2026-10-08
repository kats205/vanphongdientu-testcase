import os

import pytest

from config.config import Config
from pages.utc_login_page import UtcLoginPage


def captcha_setup_limit():
    limit = int(os.getenv("UTC_CAPTCHA_SETUP_ATTEMPTS", "3"))
    if not 0 <= limit <= 10:
        raise ValueError("UTC_CAPTCHA_SETUP_ATTEMPTS phải từ 0 đến 10")
    return limit


@pytest.fixture
def utc_login_page(driver):
    driver.set_page_load_timeout(Config.TIMEOUT)
    return UtcLoginPage(driver).navigate_to_login()


@pytest.fixture
def utc_plain_page(utc_login_page):
    """Không cho test thường vô tình chạy trên form đã có CAPTCHA."""
    return utc_login_page.require_plain()


@pytest.fixture
def utc_captcha_page(utc_login_page):
    """Chỉ trả Page Object sau khi xác minh CAPTCHA thật đã xuất hiện."""
    utc_login_page.prepare_captcha(captcha_setup_limit())
    return utc_login_page


@pytest.fixture
def utc_captcha_transition_page(utc_plain_page):
    """Phải bắt đầu không CAPTCHA và quan sát chuyển trạng thái sau từ chối."""
    attempts = utc_plain_page.prepare_captcha(captcha_setup_limit())
    assert attempts > 0, "Chưa chứng minh CAPTCHA xuất hiện sau một lần từ chối"
    return utc_plain_page, attempts
