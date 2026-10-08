from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config

class LoginPage(BasePage):
    """Page Object cho màn hình Login của SauceDemo."""

    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = Config.BASE_URL

    def navigate_to_login(self) -> "LoginPage":
        """Mở trang đăng nhập."""
        self.open(self.url)
        return self

    def enter_username(self, username: str) -> "LoginPage":
        """Nhập tên đăng nhập."""
        self.type_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """Nhập mật khẩu."""
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        """Nhấn nút đăng nhập."""
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """Hàm tiện ích thực hiện toàn bộ luồng đăng nhập."""
        if username:
            self.enter_username(username)
        if password:
            self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        """Lấy thông báo lỗi khi đăng nhập không thành công."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """Kiểm tra xem thông báo lỗi có hiển thị không."""
        return self.is_visible(self.ERROR_MESSAGE)
