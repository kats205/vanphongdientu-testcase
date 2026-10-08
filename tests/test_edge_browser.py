import time
import pytest
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from utils.driver_factory import DriverFactory
from utils.logger import get_logger

logger = get_logger("TestEdgeBrowser")

@pytest.mark.edge
class TestEdgeBrowser:
    """Bộ kiểm tra chức năng khởi chạy, điều hướng và đóng trình duyệt Microsoft Edge."""

    def test_open_and_close_edge_standalone(self):
        """Test Case 1: Tự khởi tạo và đóng trình duyệt Microsoft Edge bằng Selenium chuẩn."""
        logger.info("=== BẮT ĐẦU: Test mở và đóng trình duyệt Edge (Standalone) ===")
        
        # 1. Cấu hình trình duyệt Edge
        options = EdgeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        
        # 2. Khởi tạo WebDriver Edge (Mở trình duyệt)
        logger.info("Đang mở trình duyệt Microsoft Edge...")
        driver = webdriver.Edge(options=options)
        
        try:
            # 3. Điều hướng tới trang web kiểm tra
            target_url = "https://www.saucedemo.com"
            logger.info(f"Điều hướng tới trang: {target_url}")
            driver.get(target_url)

            # Dừng 2 giây để người dùng quan sát cửa sổ trình duyệt (nếu chạy có giao diện)
            time.sleep(2)

            # 4. Kiểm tra (Assert) xem trình duyệt đã mở và tải trang thành công chưa
            current_url = driver.current_url
            page_title = driver.title
            logger.info(f"Trình duyệt đã mở thành công! Tiêu đề trang: '{page_title}' | URL: '{current_url}'")

            assert "saucedemo.com" in current_url, f"URL không đúng: {current_url}"
            assert len(page_title) > 0, "Tiêu đề trang web đang bị rỗng"

        finally:
            # 5. Đóng trình duyệt (Teardown an toàn luôn được gọi kể cả khi test fail)
            logger.info("Đang đóng trình duyệt Microsoft Edge...")
            driver.quit()
            logger.info("Đã đóng trình duyệt Microsoft Edge thành công.")

    def test_open_and_close_edge_via_factory(self):
        """Test Case 2: Mở và đóng Edge thông qua DriverFactory của dự án."""
        logger.info("=== BẮT ĐẦU: Test mở và đóng Edge thông qua DriverFactory ===")
        
        # 1. Khởi tạo Edge thông qua DriverFactory
        driver = DriverFactory.get_driver(browser_name="edge")
        
        try:
            target_url = "https://www.google.com"
            logger.info(f"Điều hướng tới: {target_url}")
            driver.get(target_url)

            time.sleep(2)

            assert "google" in driver.current_url.lower(), f"URL không hợp lệ: {driver.current_url}"
            logger.info(f"Tiêu đề trang: {driver.title}")

        finally:
            # 2. Đóng trình duyệt
            logger.info("Đang đóng trình duyệt Edge...")
            driver.quit()
            logger.info("Đã đóng trình duyệt Edge thành công.")

if __name__ == "__main__":
    # Cho phép chạy trực tiếp bằng lệnh: python tests/test_edge_browser.py
    test = TestEdgeBrowser()
    test.test_open_and_close_edge_standalone()
