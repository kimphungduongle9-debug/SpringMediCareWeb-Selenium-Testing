from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class BasePage:
    """
    Lớp Page Object cơ sở.

    Cung cấp các thao tác dùng chung cho các Page Object:
    - Mở trang.
    - Tìm phần tử bằng explicit wait.
    - Nhập dữ liệu.
    - Click phần tử.
    - Tìm nhiều phần tử.
    - Cuộn đến phần tử.
    """
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)

    def find(self, by, value):
        return self.wait.until(
            EC.visibility_of_element_located((by, value))
        )

    def typing(self, by, value, text):
        element = self.find(by, value)
        element.clear()
        element.send_keys(text)

    def click(self, by, value):
        element = self.wait.until(
            EC.element_to_be_clickable((by, value))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

    def finds(self, by, value):
        return self.driver.find_elements(by, value)

    def scroll_to_element(self, by, value):
        element = self.find(by, value)

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

        return element