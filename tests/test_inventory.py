import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.mark.inventory
class TestInventory:
    """Bộ kiểm thử cho chức năng Trang sản phẩm và Giỏ hàng."""

    @pytest.fixture(autouse=True)
    def setup_logged_in(self, driver):
        """Pre-condition: Đăng nhập trước khi thực hiện các testcase trên trang sản phẩm."""
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        login_page.login("standard_user", "secret_sauce")
        self.inventory_page = InventoryPage(driver)
        assert self.inventory_page.is_at_inventory_page(), "Không thể đăng nhập vào trang sản phẩm"

    @pytest.mark.smoke
    def test_inventory_items_displayed(self, driver):
        """TC06: Kiểm tra các sản phẩm được hiển thị đầy đủ trong danh sách."""
        count = self.inventory_page.get_inventory_items_count()
        assert count > 0, "Không có sản phẩm nào hiển thị trên trang"
        assert count == 6, f"Mong đợi 6 sản phẩm nhưng hiển thị {count}"

    def test_add_product_to_cart(self, driver):
        """TC07: Thêm sản phẩm vào giỏ hàng và kiểm tra số lượng trên biểu tượng giỏ hàng."""
        initial_count = self.inventory_page.get_cart_count()
        assert initial_count == 0, "Giỏ hàng ban đầu phải trống"

        self.inventory_page.add_first_product_to_cart()
        new_count = self.inventory_page.get_cart_count()
        assert new_count == 1, f"Giỏ hàng phải có 1 sản phẩm, nhưng nhận được: {new_count}"

    def test_logout(self, driver):
        """TC08: Đăng xuất và kiểm tra quay lại màn hình Login thành công."""
        self.inventory_page.logout()
        login_page = LoginPage(driver)
        assert login_page.is_visible(LoginPage.LOGIN_BUTTON), "Không tìm thấy nút Login sau khi đăng xuất"
