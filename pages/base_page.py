import os
from typing import List, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import Config
from utils.logger import get_logger

class BasePage:
    """Base Page chứa các phương thức dùng chung cho tất cả các trang web theo Page Object Model (POM)."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = get_logger(self.__class__.__name__)
        self.timeout = Config.TIMEOUT

    def open(self, url: str) -> None:
        """Mở trang theo đường dẫn URL."""
        self.logger.info(f"Điều hướng tới URL: {url}")
        self.driver.get(url)

    def find_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Tìm 1 element với Explicit Wait."""
        wait_time = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.error(f"Không tìm thấy element hiển thị với locator: {locator} sau {wait_time}s")
            raise

    def find_elements(self, locator: Tuple[str, str], timeout: int = None) -> List[WebElement]:
        """Tìm danh sách các element với Explicit Wait."""
        wait_time = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            self.logger.warning(f"Không tìm thấy danh sách elements với locator: {locator}")
            return []

    def click(self, locator: Tuple[str, str], timeout: int = None) -> None:
        """Chờ element có thể click được và click."""
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            self.logger.info(f"Click vào element: {locator}")
            element.click()
        except TimeoutException:
            self.logger.error(f"Không thể click vào element: {locator}")
            raise

    def type_text(self, locator: Tuple[str, str], text: str, clear_first: bool = True, timeout: int = None) -> None:
        """Nhập nội dung vào input field."""
        element = self.find_element(locator, timeout)
        if clear_first:
            element.clear()
        self.logger.info(f"Nhập dữ liệu vào {locator}: '{text}'")
        element.send_keys(text)

    def get_text(self, locator: Tuple[str, str], timeout: int = None) -> str:
        """Lấy text của element."""
        element = self.find_element(locator, timeout)
        text = element.text.strip()
        self.logger.info(f"Lấy text từ {locator}: '{text}'")
        return text

    def is_visible(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """Kiểm tra xem element có hiển thị hay không (trả về True/False thay vì ném ngoại lệ)."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def get_current_url(self) -> str:
        """Lấy URL hiện tại."""
        return self.driver.current_url

    def get_title(self) -> str:
        """Lấy tiêu đề trang web."""
        return self.driver.title

    def scroll_to_element(self, locator: Tuple[str, str]) -> None:
        """Cuộn màn hình tới vị trí element."""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def take_screenshot(self, name: str) -> str:
        """Chụp ảnh màn hình lưu vào thư mục reports/screenshots."""
        os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)
        file_path = os.path.join(Config.SCREENSHOTS_DIR, f"{name}.png")
        self.driver.save_screenshot(file_path)
        self.logger.info(f"Đã lưu ảnh chụp màn hình: {file_path}")
        return file_path
