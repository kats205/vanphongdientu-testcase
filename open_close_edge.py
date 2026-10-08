import sys
import time

# Đảm bảo terminal Windows hiển thị được tiếng Việt và ký tự UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from selenium import webdriver
from selenium.webdriver.edge.options import Options

def open_and_close_edge(wait_seconds: int = 3):
    """
    Tự động bật cửa sổ trình duyệt Edge trên màn hình,
    giữ mở trong vài giây rồi tự động tắt hoàn toàn.
    """
    print("=" * 60)
    print("[1] DANG KHOI CHAY TRINH DUYET MICROSOFT EDGE...")
    print("=" * 60)

    # Cấu hình để mở cửa sổ Edge trực quan (không dùng headless)
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    # BƯỚC 1: TỰ ĐỘNG BẬT CỬA SỔ TRÌNH DUYỆT EDGE
    driver = webdriver.Edge(options=options)

    try:
        # BƯỚC 2: ĐIỀU HƯỚNG TỚI TRANG WEB
        target_url = "https://www.bing.com"
        print(f"[2] Dang truy cap trang: {target_url}")
        driver.get(target_url)

        print(f"[+] Edge da mo thanh cong!")
        print(f"[+] Tieu de trang: '{driver.title}'")
        print(f"[3] Cua so Edge se tu dong tat sau {wait_seconds} giay:")

        # Đếm ngược để người dùng quan sát trên màn hình
        for i in range(wait_seconds, 0, -1):
            print(f"    --> Tu dong dong sau {i} giay...")
            time.sleep(1)

    finally:
        # BƯỚC 3: TỰ ĐỘNG ĐÓNG TRÌNH DUYỆT EDGE
        print("\n[4] Dang tat trinh duyet Edge...")
        driver.quit()
        print("[5] DA DONG TRINH DUYET EDGE THANH CONG!")
        print("=" * 60)

if __name__ == "__main__":
    open_and_close_edge(wait_seconds=3)
