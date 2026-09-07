from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.BasePage import BasePage


class DoctorPage(BasePage):
    """
    Page Object cho chức năng xem và tìm kiếm Bác sĩ.

    Mapping Test Case -> Step -> Method:

    TC-DOCTOR-001
    - Step 1: Mở trang Bác sĩ
      + open_page()
      + wait_until_doctors_loaded()
    - Step 2: Kiểm tra tiêu đề và số lượng bác sĩ
      + get_title()
      + get_displayed_count()
    - Step 3: Kiểm tra danh sách card bác sĩ
      + get_doctor_cards()
    - Step 4: Kiểm tra thông tin từng bác sĩ
      + get_doctor_card_information()

    TC-DOCTOR-002
    - Step 1: Mở trang Bác sĩ
      + open_page()
    - Step 2: Nhập từ khóa tìm kiếm
      + enter_search_keyword()
    - Step 3: Thực hiện tìm kiếm
      + click_search()
      + wait_for_search_results()
    - Step 4: Kiểm tra kết quả tìm kiếm
      + get_doctor_cards()
      + get_displayed_count()
      + get_doctor_card_information()

    TC-DOCTOR-003
    - Step 1: Mở trang Bác sĩ
      + open_page()
    - Step 2: Nhập tên bác sĩ không tồn tại
      + enter_search_keyword()
    - Step 3: Thực hiện tìm kiếm
      + click_search()
      + wait_for_no_results()
    - Step 4: Kiểm tra trạng thái không có kết quả
      + get_displayed_count()
      + get_card_count()
      + get_no_result_message()

    TC-DOCTOR-004
    - Step 1: Mở trang Bác sĩ
      + open_page()
    - Step 2: Chọn bác sĩ
      + get_doctor_card_by_name()
    - Step 3: Nhấn Đặt lịch hẹn
      + click_booking_of_doctor()
    - Step 5: Kiểm tra đúng bác sĩ trên trang Đặt lịch
      + get_booking_doctor_name()
    """

    URL = "http://localhost:3000/doctor"

    PAGE_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Danh sách bác sĩ']"
    )

    DOCTOR_COUNT = (
        By.XPATH,
        "//p[contains(., 'Số lượng bác sĩ:')]/span"
    )

    DOCTOR_CARDS = (
        By.CSS_SELECTOR,
        "div.feature-card"
    )

    SEARCH_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='Nhập tên bác sĩ cần tìm...']"
    )

    SEARCH_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Tìm kiếm']"
    )

    NO_RESULT_MESSAGE = (
        By.XPATH,
        "//*[normalize-space()='KHÔNG có kết quả phù hợp!']"
    )

    BOOKING_DOCTOR_NAME = (
        By.CSS_SELECTOR,
        ".booking-card h3"
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

    def get_title(self):
        return self.find(
            *self.PAGE_TITLE
        ).text.strip()

    def get_displayed_count(self):
        self.wait.until(
            lambda driver:
            driver.find_element(
                *self.DOCTOR_COUNT
            ).text.strip() != ""
        )

        text = self.find(
            *self.DOCTOR_COUNT
        ).text.strip()

        return int(text)

    def get_doctor_cards(self):
        self.wait.until(
            lambda driver:
            len(driver.find_elements(*self.DOCTOR_CARDS)) > 0
        )

        return self.driver.find_elements(
            *self.DOCTOR_CARDS
        )

    def get_card_count(self):
        return len(
            self.driver.find_elements(
                *self.DOCTOR_CARDS
            )
        )

    def get_doctor_card_by_name(self, doctor_name):
        locator = (
            By.XPATH,
            "//div[contains(@class,'feature-card')]"
            f"[.//h3[normalize-space()='{doctor_name}']]"
        )

        return self.wait.until(
            EC.visibility_of_element_located(
                locator
            )
        )

    def get_doctor_card_information(self, card):
        image = card.find_element(
            By.CSS_SELECTOR,
            "img.doctor-img"
        )

        name = card.find_element(
            By.CSS_SELECTOR,
            "h3.card-title-shared"
        ).text.strip()

        specialty = card.find_element(
            By.XPATH,
            ".//strong[normalize-space()='Chuyên khoa:']"
            "/following-sibling::span"
        ).text.strip()

        experience = card.find_element(
            By.XPATH,
            ".//strong[normalize-space()='Kinh nghiệm:']"
            "/following-sibling::span"
        ).text.strip()

        booking_button = card.find_element(
            By.XPATH,
            ".//button[normalize-space()='Đặt lịch hẹn']"
        )

        return {
            "image": image.get_attribute("src"),
            "name": name,
            "specialty": specialty,
            "experience": experience,
            "booking_button_displayed":
                booking_button.is_displayed()
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
            len(driver.find_elements(*self.DOCTOR_CARDS)) > 0
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

    def click_booking_of_doctor(self, doctor_name):
        card = self.get_doctor_card_by_name(
            doctor_name
        )

        button = card.find_element(
            By.XPATH,
            ".//button[normalize-space()='Đặt lịch hẹn']"
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        self.wait.until(
            lambda driver:
            "/booking?doctorId=" in driver.current_url
        )

    def get_booking_doctor_name(self):
        return self.wait.until(
            EC.visibility_of_element_located(
                self.BOOKING_DOCTOR_NAME
            )
        ).text.strip()

    def wait_until_doctors_loaded(self):
        self.wait.until(
            lambda driver:
            int(
                driver.find_element(
                    *self.DOCTOR_COUNT
                ).text.strip()
            ) > 0
        )

    def book_tran_binh(self, delay=0):
        """
        Tương thích với các test cũ đang đặt lịch bác sĩ Tran Binh.
        Sử dụng lại hàm tổng quát sau khi DoctorPage được refactor.
        """
        self.click_booking_of_doctor("Tran Binh")