import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Cấu hình chung cho dự án Automation Test."""
    # Trình duyệt mặc định: 'chrome' hoặc 'edge'
    BROWSER = os.getenv("BROWSER", "chrome").lower()
    
    # Chế độ chạy ngầm (Headless): True hoặc False
    HEADLESS = os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes")
    
    # URL ứng dụng cần test (mặc định dùng SauceDemo)
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    
    # Thời gian chờ mặc định (giây) cho WebDriverWait
    TIMEOUT = int(os.getenv("TIMEOUT", "10"))
    
    # Thư mục lưu báo cáo & ảnh chụp màn hình
    REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
    SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")
