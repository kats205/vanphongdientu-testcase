import os
import pytest
from datetime import datetime
from utils.driver_factory import DriverFactory
from utils.logger import get_logger
from config.config import Config

logger = get_logger("Conftest")

def pytest_addoption(parser):
    """Thêm tham số dòng lệnh tùy chỉnh cho pytest."""
    parser.addoption(
        "--browser",
        action="store",
        default=Config.BROWSER,
        help="Trình duyệt để chạy test: chrome hoặc edge"
    )
    parser.addoption(
        "--headless",
        action="store",
        default=str(Config.HEADLESS).lower(),
        help="Chạy ở chế độ không giao diện (headless): true hoặc false"
    )

@pytest.fixture(scope="function")
def driver(request):
    """Fixture khởi tạo WebDriver trước mỗi test case và tự động đóng sau khi test xong."""
    browser_param = request.config.getoption("--browser")
    headless_param = request.config.getoption("--headless").lower() in ("true", "1", "yes")

    web_driver = DriverFactory.get_driver(browser_name=browser_param, headless=headless_param)
    
    # Gắn driver vào test class hoặc item nếu cần
    if request.cls:
        request.cls.driver = web_driver

    yield web_driver

    try:
        web_driver.quit()
        logger.info("Đã đóng trình duyệt an toàn.")
    except Exception as e:
        logger.warning(f"Lỗi khi đóng trình duyệt: {e}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook chụp ảnh màn hình tự động khi test case bị FAILED và đính kèm vào báo cáo pytest-html."""
    outcome = yield
    report = outcome.get_result()
    
    # Chỉ xử lý khi test case thực thi xong (call phase) và bị fail
    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture:
            os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name.replace(" ", "_")
            screenshot_name = f"FAILED_{test_name}_{timestamp}.png"
            file_path = os.path.join(Config.SCREENSHOTS_DIR, screenshot_name)
            
            try:
                driver_fixture.save_screenshot(file_path)
                logger.error(f"Test case '{item.name}' thất bại! Đã chụp màn hình tại: {file_path}")
                
                # Đính kèm ảnh vào pytest-html report
                html_plugin = item.config.pluginmanager.getplugin("html")
                if html_plugin:
                    extra = getattr(report, "extra", [])
                    extra.append(html_plugin.extras.image(file_path))
                    report.extra = extra
            except Exception as e:
                logger.warning(f"Không thể chụp ảnh màn hình lỗi: {e}")
