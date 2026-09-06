from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.BasePage import BasePage


class SpecialtyPage(BasePage):

    URL = "http://localhost:3000/specialty"

    PAGE_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Danh mục chuyên khoa']"
    )

    SPECIALTY_COUNT = (
        By.XPATH,
        "//p[contains(., 'Số lượng hiển thị:')]/span"
    )

    SPECIALTY_CARDS = (
        By.CSS_SELECTOR,
        "div.feature-card"
    )

    SEARCH_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='Nhập tên chuyên khoa cần tìm...']"
    )

    SEARCH_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Tìm kiếm']"
    )

    NO_RESULT_MESSAGE = (
        By.XPATH,
        "//*[normalize-space()='Không tìm thấy chuyên khoa nào phù hợp với từ khóa của bạn.']"
    )

    DOCTOR_SPECIALTY_TITLE = (
        By.XPATH,
        "//h2[contains(normalize-space(), 'Bác sĩ thuộc chuyên khoa')]"
    )

    DETAIL_TITLE = (
        By.XPATH,
        "//h2[starts-with(normalize-space(), 'Chuyên khoa:')]"
    )

    DETAIL_DOCTOR_COUNT = (
        By.XPATH,
        "//p[contains(., 'Số lượng bác sĩ đang công tác:')]/span"
    )

    DETAIL_INTRO_TITLE = (
        By.XPATH,
        "//h3[normalize-space()='Thông tin giới thiệu']"
    )

    DETAIL_DOCTOR_TEAM_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Đội ngũ bác sĩ trực thuộc']"
    )

    def open_page(self):
        self.open(self.URL)

        self.wait.until(
            EC.visibility_of_element_located(
                self.PAGE_TITLE
            )
        )

        self.wait.until(
            lambda driver:
            not driver.find_elements(
                By.CSS_SELECTOR,
                ".spinner-border"
            )
        )

    def wait_until_specialties_loaded(self):
        self.wait.until(
            lambda driver:
            int(
                driver.find_element(
                    *self.SPECIALTY_COUNT
                ).text.strip()
            ) > 0
        )

    def get_title(self):
        return self.find(
            *self.PAGE_TITLE
        ).text.strip()

    def get_displayed_count(self):
        text = self.find(
            *self.SPECIALTY_COUNT
        ).text.strip()

        return int(text)

    def get_specialty_cards(self):
        return self.driver.find_elements(
            *self.SPECIALTY_CARDS
        )

    def get_card_count(self):
        return len(
            self.driver.find_elements(
                *self.SPECIALTY_CARDS
            )
        )

    def get_specialty_card_by_name(self, specialty_name):
        locator = (
            By.XPATH,
            "//div[contains(@class,'feature-card')]"
            f"[.//h3[normalize-space()='{specialty_name}']]"
        )

        return self.wait.until(
            EC.visibility_of_element_located(
                locator
            )
        )

    def get_specialty_card_information(self, card):
        image = card.find_element(
            By.CSS_SELECTOR,
            "img.specialty-img"
        )

        name = card.find_element(
            By.CSS_SELECTOR,
            "h3.card-title-shared"
        ).text.strip()

        description = card.find_element(
            By.CSS_SELECTOR,
            "p.card-text-shared"
        ).text.strip()

        doctor_button = card.find_element(
            By.XPATH,
            ".//button[normalize-space()='Xem bác sĩ thuộc khoa']"
        )

        detail_button = card.find_element(
            By.XPATH,
            ".//button[normalize-space()='Xem chi tiết khoa']"
        )

        return {
            "image": image.get_attribute("src"),
            "name": name,
            "description": description,
            "doctor_button_displayed":
                doctor_button.is_displayed(),
            "detail_button_displayed":
                detail_button.is_displayed()
        }

    def enter_search_keyword(self, keyword):
        search = self.find(
            *self.SEARCH_INPUT
        )

        search.clear()
        search.send_keys(keyword)

    def click_search(self):
        self.click(
            *self.SEARCH_BUTTON
        )

    def wait_for_search_results(self):
        self.wait.until(
            lambda driver:
            len(
                driver.find_elements(
                    *self.SPECIALTY_CARDS
                )
            ) > 0
        )

    def wait_for_no_results(self):
        self.wait.until(
            EC.visibility_of_element_located(
                self.NO_RESULT_MESSAGE
            )
        )

    def get_no_result_message(self):
        return self.find(
            *self.NO_RESULT_MESSAGE
        ).text.strip()

    def click_view_doctors(self, specialty_name):
        card = self.get_specialty_card_by_name(
            specialty_name
        )

        button = card.find_element(
            By.XPATH,
            ".//button[normalize-space()='Xem bác sĩ thuộc khoa']"
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        self.wait.until(
            lambda driver:
            "/specialties/" in driver.current_url
            and "/doctors" in driver.current_url
        )

    def get_doctor_specialty_title(self):
        return self.wait.until(
            EC.visibility_of_element_located(
                self.DOCTOR_SPECIALTY_TITLE
            )
        ).text.strip()

    def get_doctor_cards(self):
        self.wait.until(
            lambda driver:
            not driver.find_elements(
                By.CSS_SELECTOR,
                ".spinner-border"
            )
        )

        return self.driver.find_elements(
            *self.SPECIALTY_CARDS
        )

    def get_doctor_names(self):
        cards = self.get_doctor_cards()

        names = []

        for card in cards:
            name = card.find_element(
                By.CSS_SELECTOR,
                "h3.card-title-shared"
            ).text.strip()

            names.append(name)

        return names

    def click_view_details(self, specialty_name):
        card = self.get_specialty_card_by_name(
            specialty_name
        )

        button = card.find_element(
            By.XPATH,
            ".//button[normalize-space()='Xem chi tiết khoa']"
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        self.wait.until(
            EC.visibility_of_element_located(
                self.DETAIL_TITLE
            )
        )

    def get_detail_title(self):
        return self.find(
            *self.DETAIL_TITLE
        ).text.strip()

    def get_detail_doctor_count(self):
        return int(
            self.find(
                *self.DETAIL_DOCTOR_COUNT
            ).text.strip()
        )

    def is_intro_displayed(self):
        return self.find(
            *self.DETAIL_INTRO_TITLE
        ).is_displayed()

    def is_doctor_team_displayed(self):
        return self.find(
            *self.DETAIL_DOCTOR_TEAM_TITLE
        ).is_displayed()

    def wait_for_specialty_count(self, expected_count):
        self.wait.until(
            lambda driver:
            int(
                driver.find_element(
                    *self.SPECIALTY_COUNT
                ).text.strip()
            ) == expected_count
        )