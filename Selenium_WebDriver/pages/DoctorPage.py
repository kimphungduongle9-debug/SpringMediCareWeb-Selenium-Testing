from selenium.webdriver.common.by import By

from pages.BasePage import BasePage

import time


class DoctorPage(BasePage):

    URL = "http://localhost:3000/doctor"

    TRAN_BINH_BOOKING_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'feature-card')]"
        "[.//h3[normalize-space()='Tran Binh']]"
        "//button[normalize-space()='Đặt lịch hẹn']"
    )

    def open_page(self):
        self.open(self.URL)

    def book_tran_binh(self, delay=2):
        button = self.scroll_to_element(
            *self.TRAN_BINH_BOOKING_BUTTON
        )

        time.sleep(1)

        button.click()

        time.sleep(delay)