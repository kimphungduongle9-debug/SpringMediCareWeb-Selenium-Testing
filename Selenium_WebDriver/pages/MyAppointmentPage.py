from selenium.webdriver.common.by import By

from pages.BasePage import BasePage
from selenium.webdriver.support.ui import WebDriverWait

class MyAppointmentPage(BasePage):

    URL = "http://localhost:3000/my-appointments"

    PAGE_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Lịch hẹn của tôi']"
    )

    APPOINTMENT_ROWS = (
        By.XPATH,
        "//table/tbody/tr"
    )

    EMPTY_MESSAGE = (
        By.XPATH,
        "//*[normalize-space()='Bạn chưa có lịch hẹn nào.']"
    )

    def open_page(self):
        self.open(self.URL)

    def get_page_title(self):
        return self.find(*self.PAGE_TITLE).text

    def get_appointment_by_note(self, note):
        rows = self.finds(
            *self.APPOINTMENT_ROWS
        )

        for row in rows:
            cells = row.find_elements(
                By.TAG_NAME,
                "td"
            )

            if len(cells) < 5:
                continue

            if cells[4].text == note:
                return {
                    "id": cells[0].text,
                    "doctor": cells[1].text,
                    "time": cells[2].text,
                    "status": cells[3].text,
                    "note": cells[4].text
                }

        return None

    def wait_for_appointment_by_note(self, note, timeout=10):
        def find_appointment(driver):
            appointment = self.get_appointment_by_note(note)

            if appointment is not None:
                return appointment

            return False

        return WebDriverWait(
            self.driver,
            timeout
        ).until(find_appointment)