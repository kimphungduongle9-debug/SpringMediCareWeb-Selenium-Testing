from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class BasePage:
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
        element.click()

    def finds(self, by, value):
        return self.driver.find_elements(by, value)