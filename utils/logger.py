import logging
import os
import sys

def get_logger(name: str = "TestAutomation") -> logging.Logger:
    """Tạo hoặc lấy logger chuẩn để theo dõi quá trình chạy test."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Thiết lập stdout hỗ trợ utf-8 trên Windows
        if hasattr(sys.stdout, "reconfigure"):
            try:
                sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
            except Exception:
                pass

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File Handler (lưu vào thư mục reports)
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
        os.makedirs(reports_dir, exist_ok=True)
        file_handler = logging.FileHandler(
            filename=os.path.join(reports_dir, "test_execution.log"),
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger
