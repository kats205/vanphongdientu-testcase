from shutil import which
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.remote.webdriver import WebDriver
from config.config import Config
from utils.logger import get_logger

logger = get_logger("DriverFactory")

class DriverFactory:
    """Factory để khởi tạo WebDriver theo trình duyệt và cấu hình mong muốn."""

    @staticmethod
    def get_driver(browser_name: str = None, headless: bool = None) -> WebDriver:
        browser = (browser_name or Config.BROWSER).lower()
        is_headless = Config.HEADLESS if headless is None else headless

        logger.info(f"Khởi tạo trình duyệt: {browser} (Headless: {is_headless})")

        if browser == "chrome":
            options = ChromeOptions()
            if is_headless:
                options.add_argument("--headless=new")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-notifications")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(service=ChromeService(executable_path=which("chromedriver")), options=options)

        elif browser == "edge":
            options = EdgeOptions()
            if is_headless:
                options.add_argument("--headless=new")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-notifications")
            driver = webdriver.Edge(service=EdgeService(executable_path=which("msedgedriver")), options=options)

        else:
            raise ValueError(f"Trình duyệt không hỗ trợ: '{browser}'. Vui lòng dùng 'chrome' hoặc 'edge'.")

        driver.implicitly_wait(2)
        return driver
