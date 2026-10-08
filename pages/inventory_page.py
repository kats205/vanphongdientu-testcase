from typing import List
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InventoryPage(BasePage):
    """Page Object cho màn hình Danh sách sản phẩm (Inventory/Home)."""

    PAGE_TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    INVENTORY_ITEMS = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove']")
    SHOPPING_CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def is_at_inventory_page(self) -> bool:
        """Kiểm tra xem đang ở đúng trang sản phẩm hay chưa."""
        if self.is_visible(self.PAGE_TITLE):
            return self.get_text(self.PAGE_TITLE).lower() == "products"
        return False

    def get_inventory_items_count(self) -> int:
        """Đếm số lượng sản phẩm hiển thị trên trang."""
        items = self.find_elements(self.INVENTORY_ITEMS)
        return len(items)

    def add_first_product_to_cart(self) -> None:
        """Thêm sản phẩm đầu tiên vào giỏ hàng."""
        self.click(self.ADD_TO_CART_BUTTONS)

    def get_cart_count(self) -> int:
        """Lấy số lượng item hiển thị trên icon giỏ hàng."""
        if self.is_visible(self.SHOPPING_CART_BADGE, timeout=3):
            badge_text = self.get_text(self.SHOPPING_CART_BADGE)
            return int(badge_text) if badge_text.isdigit() else 0
        return 0

    def logout(self) -> None:
        """Đăng xuất khỏi hệ thống."""
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
