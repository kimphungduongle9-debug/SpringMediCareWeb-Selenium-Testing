from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from pages.BasePage import BasePage
from pages.LoginPage import LoginPage


class StatPage(BasePage):

    BASE_URL = "http://localhost:3000"

    DRUG_STAT_URL = (
        "http://localhost:3000/admin-drugs/statistics"
    )

    ADMIN_STAT_URL = (
        "http://localhost:3000/admin-statistics"
    )

    SPINNER = (
        By.CSS_SELECTOR,
        ".spinner-border"
    )

    DRUG_STAT_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Thống kê thuốc']"
    )

    ADMIN_STAT_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Thống kê và báo cáo']"
    )

    YEAR_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='Nhập năm cần xem']"
    )

    REVENUE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Xem doanh thu']"
    )

    def login_admin(
        self,
        username="admin_system",
        password="Abc@123"
    ):
        login_page = LoginPage(self.driver)

        login_page.open_page()

        login_page.login(
            username,
            password,
            delay=0
        )

        self.wait.until(
            lambda driver:
            driver.current_url
            == "http://localhost:3000/"
        )

    def wait_loading_finished(self):
        self.wait.until(
            lambda driver:
            len(
                driver.find_elements(
                    *self.SPINNER
                )
            ) == 0
        )

    def open_drug_statistics(self):
        self.open(self.DRUG_STAT_URL)

        self.wait.until(
            EC.visibility_of_element_located(
                self.DRUG_STAT_TITLE
            )
        )

        self.wait_loading_finished()

    def open_admin_statistics(self):
        self.open(self.ADMIN_STAT_URL)

        self.wait.until(
            EC.visibility_of_element_located(
                self.ADMIN_STAT_TITLE
            )
        )

        self.wait_loading_finished()

    def get_section(self, title):
        locator = (
            By.XPATH,
            "//div[contains(@class,'feature-card')]"
            f"[.//h3[normalize-space()='{title}']]"
        )

        return self.wait.until(
            EC.visibility_of_element_located(
                locator
            )
        )

    def get_table_headers(self, title):
        section = self.get_section(title)

        return [
            element.text.strip()
            for element in section.find_elements(
                By.CSS_SELECTOR,
                "table thead th"
            )
        ]

    def get_table_rows(self, title):
        section = self.get_section(title)

        rows = section.find_elements(
            By.CSS_SELECTOR,
            "table tbody tr"
        )

        result = []

        for row in rows:
            cells = row.find_elements(
                By.TAG_NAME,
                "td"
            )

            if len(cells) >= 2:
                result.append([
                    cells[0].text.strip(),
                    cells[1].text.strip()
                ])

        return result

    def is_chart_displayed(self, title):
        section = self.get_section(title)

        charts = section.find_elements(
            By.CSS_SELECTOR,
            "svg.recharts-surface"
        )

        return (
            len(charts) > 0
            and charts[0].is_displayed()
        )

    def get_chart_labels(self, title):
        section = self.get_section(title)

        labels = section.find_elements(
            By.CSS_SELECTOR,
            ".recharts-cartesian-axis-tick-value"
        )

        result = []

        for label in labels:
            text = label.text.strip()

            if not text:
                text = self.driver.execute_script(
                    "return arguments[0].textContent;",
                    label
                ).strip()

            if text:
                result.append(text)

        return result

    def get_bar_count(self, title):
        section = self.get_section(title)

        return len(
            section.find_elements(
                By.CSS_SELECTOR,
                ".recharts-bar-rectangle"
            )
        )

    def enter_year(self, year):
        field = self.find(
            *self.YEAR_INPUT
        )

        field.clear()
        field.send_keys(str(year))

    def click_view_revenue(self):
        self.click(
            *self.REVENUE_BUTTON
        )

        self.wait_loading_finished()

    def scroll_to_section(self, title):
        section = self.get_section(title)

        self.driver.execute_script(
            "arguments[0].scrollIntoView("
            "{block:'center'});",
            section
        )

        return section

    def is_currency_format(self, value):
        text = value.replace(".", "").replace(",", "")

        return (
            value.endswith("VNĐ")
            and any(char.isdigit() for char in text)
        )

    def scroll_inside_section(self, title):
        section = self.get_section(title)

        responsive = section.find_elements(
            By.CSS_SELECTOR,
            ".table-responsive"
        )

        if responsive:
            self.driver.execute_script(
                "arguments[0].scrollTop = "
                "arguments[0].scrollHeight;",
                responsive[0]
            )

        return section.is_displayed()