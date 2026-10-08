import re
from urllib.parse import urlsplit
from uuid import uuid4

from selenium.common.exceptions import NoAlertPresentException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class UtcLoginPage(BasePage):
    """Hai trạng thái của form UTC theo HTML người dùng cung cấp."""

    URL = "https://vanphongdientu.utc.edu.vn/Login?r=https%3A%2F%2Fvanphongdientu.utc.edu.vn%2F"
    FORM = (By.CSS_SELECTOR, 'form[action="/Login"][method="post"]')
    USERNAME_INPUT = (By.CSS_SELECTOR, 'form[action="/Login"] input[name="username"][type="text"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'form[action="/Login"] input[name="userpwd"][type="password"]')
    PERSISTENT_INPUT = (By.CSS_SELECTOR, 'form[action="/Login"] input#persistent[name="persistent"][type="checkbox"]')
    PERSISTENT_LABEL = (By.CSS_SELECTOR, 'form[action="/Login"] label[for="persistent"]:not(.check)')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'form[action="/Login"] input.submit_login[type="submit"]')
    ERROR_MESSAGE = (By.CSS_SELECTOR, 'form[action="/Login"] .error')
    CAPTCHA_INPUT = (By.CSS_SELECTOR, 'form[action="/Login"] input[name="captcha"][type="text"]')
    CAPTCHA_IMAGE = (By.CSS_SELECTOR, 'form[action="/Login"] img#captcha')
    CAPTCHA_REFRESH = (By.CSS_SELECTOR, 'form[action="/Login"] a[onclick*="getElementById"][onclick*="captcha"]')
    ERROR_TEXT = re.compile(
        r"vui lòng|hãy nhập|chưa nhập|không hợp lệ|không đúng|không chính xác|"
        r"không tồn tại|sai|lỗi|thất bại|bắt buộc|required|invalid|incorrect|failed|error",
        re.IGNORECASE,
    )

    def navigate_to_login(self):
        self.open(self.URL)
        self.validate_controls()
        return self

    def validate_controls(self):
        """Control chung là bắt buộc; CAPTCHA được kiểm tra khi xuất hiện."""
        for locator in (
            self.FORM, self.USERNAME_INPUT, self.PASSWORD_INPUT,
            self.PERSISTENT_INPUT, self.PERSISTENT_LABEL, self.LOGIN_BUTTON,
        ):
            self._unique(locator)
        assert self.find_element(self.USERNAME_INPUT).get_attribute("placeholder") == "Tên đăng nhập"
        assert self.find_element(self.PASSWORD_INPUT).get_attribute("placeholder") == "Mật khẩu"
        assert self.find_element(self.LOGIN_BUTTON).get_attribute("value") == "Đăng nhập"
        assert self.driver.find_element(*self.PERSISTENT_INPUT).get_attribute("value") == "1"
        assert len(self.driver.find_elements(*self.ERROR_MESSAGE)) <= 1, "Thông báo lỗi không khớp duy nhất"
        if self.has_captcha():
            for locator in (self.CAPTCHA_INPUT, self.CAPTCHA_IMAGE, self.CAPTCHA_REFRESH):
                self._unique(locator)
            assert self.find_element(self.CAPTCHA_INPUT).get_attribute("placeholder") == "Mã bảo mật"
            image = self._unique(self.CAPTCHA_IMAGE)
            assert urlsplit(image.get_dom_attribute("src")).path == "/login/index/captcha"
            self.find_element(self.CAPTCHA_REFRESH)
        else:
            assert not self.driver.find_elements(*self.CAPTCHA_IMAGE), "Có ảnh nhưng thiếu ô nhập CAPTCHA"

    def _unique(self, locator):
        matches = self.driver.find_elements(*locator)
        assert len(matches) == 1, f"Selector không khớp duy nhất: {locator}; thấy {len(matches)}"
        return matches[0]

    def has_captcha(self):
        return bool(self.driver.find_elements(*self.CAPTCHA_INPUT))

    def require_plain(self):
        assert not self.has_captcha(), "Chưa đạt tiền điều kiện: form không CAPTCHA"
        self.validate_controls()
        return self

    def prepare_captcha(self, max_attempts):
        """Ngân sách setup không phải ngưỡng của UTC; không nhắm tài khoản thật."""
        setup_username = "utc_" + uuid4().hex
        for attempt in range(max_attempts + 1):
            if self.has_captcha():
                self.require_captcha()
                return attempt
            if attempt == max_attempts:
                break
            self.enter_credentials(setup_username, "utc-dummy-password")
            self.set_persistent(False)
            self.assert_rejected()
        raise AssertionError(
            "CAPTCHA chưa xuất hiện trong ngân sách setup; chưa đạt tiền điều kiện. "
            "Không kết luận ngưỡng CAPTCHA hoặc lỗi sản phẩm từ giới hạn này."
        )

    def require_captcha(self):
        assert self.has_captcha(), "Chưa đạt tiền điều kiện: form có CAPTCHA"
        self.validate_controls()
        return self

    def _enter(self, locator, value):
        # Không ghi nội dung mật khẩu hoặc CAPTCHA vào log.
        element = self.find_element(locator)
        element.clear()
        if value:
            element.send_keys(value)
        assert element.get_attribute("value") == value, "Dữ liệu nhập không khớp case"

    def enter_credentials(self, username, password):
        self._enter(self.USERNAME_INPUT, username)
        self._enter(self.PASSWORD_INPUT, password)

    def clear_username(self):
        self._enter(self.USERNAME_INPUT, "")

    def clear_password(self):
        self._enter(self.PASSWORD_INPUT, "")

    def clear_captcha(self):
        self.require_captcha()
        self._enter(self.CAPTCHA_INPUT, "")

    def enter_captcha(self, value):
        self.require_captcha()
        self._enter(self.CAPTCHA_INPUT, value)

    def refresh_captcha(self):
        self.require_captcha()
        previous = self._unique(self.CAPTCHA_IMAGE).get_dom_attribute("src")
        self.click(self.CAPTCHA_REFRESH)
        WebDriverWait(self.driver, self.timeout).until(
            lambda driver: driver.find_element(*self.CAPTCHA_IMAGE).get_dom_attribute("src") != previous,
            "Liên kết đổi mã không thay đổi src của ảnh CAPTCHA",
        )
        # HTML chỉ đổi src; không giả định ô CAPTCHA được xóa tự động.

    def set_persistent(self, selected):
        checkbox = self.driver.find_element(*self.PERSISTENT_INPUT)
        if checkbox.is_selected() != selected:
            self.click(self.PERSISTENT_LABEL)
        assert checkbox.is_selected() == selected, "Không đổi được trạng thái giữ đăng nhập"

    def assert_rejected(self, via_enter=False):
        """Chấp nhận lỗi lặp sau phản hồi mới; không chấp nhận lỗi cũ đứng yên."""
        previous_form = self._unique(self.FORM)
        previous_errors = self.driver.find_elements(*self.ERROR_MESSAGE)
        previous_error = previous_errors[0] if previous_errors else None
        previous_error_text = previous_error.text.strip() if previous_error else ""
        before = set(self.driver.find_element(By.TAG_NAME, "body").text.splitlines())
        if via_enter:
            target = self.CAPTCHA_INPUT if self.has_captcha() else self.PASSWORD_INPUT
            self.find_element(target).send_keys(Keys.ENTER)
        else:
            self.click(self.LOGIN_BUTTON)

        def rejection_message(driver):
            try:
                alert = driver.switch_to.alert
                text = alert.text.strip()
                alert.accept()
                assert text and self.ERROR_TEXT.search(text), f"Dialog chưa chứng minh từ chối: {text!r}"
                return text
            except NoAlertPresentException:
                pass
            locators = [self.USERNAME_INPUT, self.PASSWORD_INPUT, self.CAPTCHA_INPUT]
            for locator in locators:
                for element in driver.find_elements(*locator):
                    message = element.get_property("validationMessage")
                    if message:
                        return message
            new_response = EC.staleness_of(previous_form)(driver)
            error_replaced = previous_error is None or EC.staleness_of(previous_error)(driver)
            for element in driver.find_elements(*self.ERROR_MESSAGE):
                text = element.text.strip()
                if element.is_displayed() and self.ERROR_TEXT.search(text):
                    if new_response or error_replaced or text != previous_error_text:
                        return text
            bodies = driver.find_elements(By.TAG_NAME, "body")
            lines = bodies[0].text.splitlines() if bodies else []
            return next(
                (line.strip() for line in lines if line not in before and self.ERROR_TEXT.search(line)),
                False,
            )

        message = WebDriverWait(
            self.driver, self.timeout, ignored_exceptions=(StaleElementReferenceException,)
        ).until(
            rejection_message, "Không có bằng chứng mới về việc từ chối đăng nhập"
        )
        destination = urlsplit(self.driver.current_url)
        assert destination.scheme == "https" and destination.hostname == "vanphongdientu.utc.edu.vn"
        assert destination.path.rstrip("/").lower() == "/login", "Thông tin lỗi đã rời trang Login"
        self.validate_controls()
        return message
