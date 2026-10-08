import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.mark.login
class TestLogin:
    """Bộ kiểm thử cho chức năng Đăng nhập."""

    @pytest.mark.smoke
    def test_login_success(self, driver):
        """TC01: Đăng nhập thành công với tài khoản hợp lệ."""
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_at_inventory_page(), "Không chuyển hướng đến trang sản phẩm (Products)"
        assert "inventory.html" in driver.current_url, f"URL hiện tại không đúng: {driver.current_url}"

    def test_login_locked_out_user(self, driver):
        """TC02: Đăng nhập với tài khoản đã bị khóa (locked_out_user)."""
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        login_page.login("locked_out_user", "secret_sauce")

        assert login_page.is_error_displayed(), "Thông báo lỗi không hiển thị"
        error_msg = login_page.get_error_message()
        assert "Sorry, this user has been locked out" in error_msg, f"Nội dung lỗi không khớp: {error_msg}"

    def test_login_invalid_password(self, driver):
        """TC03: Đăng nhập với mật khẩu không chính xác."""
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        login_page.login("standard_user", "wrong_password_123")

        assert login_page.is_error_displayed(), "Thông báo lỗi không hiển thị"
        error_msg = login_page.get_error_message()
        assert "Username and password do not match any user in this service" in error_msg, f"Nội dung lỗi không khớp: {error_msg}"

    def test_login_empty_username(self, driver):
        """TC04: Đăng nhập bỏ trống tên người dùng (Username is required)."""
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        login_page.login("", "secret_sauce")

        assert login_page.is_error_displayed(), "Thông báo lỗi không hiển thị"
        error_msg = login_page.get_error_message()
        assert "Username is required" in error_msg, f"Nội dung lỗi không khớp: {error_msg}"

    def test_login_empty_password(self, driver):
        """TC05: Đăng nhập bỏ trống mật khẩu (Password is required)."""
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        login_page.login("standard_user", "")

        assert login_page.is_error_displayed(), "Thông báo lỗi không hiển thị"
        error_msg = login_page.get_error_message()
        assert "Password is required" in error_msg, f"Nội dung lỗi không khớp: {error_msg}"
