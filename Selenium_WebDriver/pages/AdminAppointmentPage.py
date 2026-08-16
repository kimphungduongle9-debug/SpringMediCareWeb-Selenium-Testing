from selenium.webdriver.common.by import By

from pages.BasePage import BasePage

from selenium.webdriver.support import expected_conditions as EC
class AdminAppointmentPage(BasePage):

    PAGE_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Quản lý lịch hẹn']"
    )

    CONFIRM_SUCCESS_MESSAGE = (
        By.XPATH,
        "//div[contains(@class, 'alert') "
        "and contains(normalize-space(.), "
        "'Xác nhận lịch hẹn thành công.')]"
    )

    CANCEL_SUCCESS_MESSAGE = (
        By.XPATH,
        "//div[contains(@class, 'alert') "
        "and contains(normalize-space(.), "
        "'Hủy lịch hẹn thành công.')]"
    )

    URL = (
        "http://localhost:3000/"
        "admin-appointments"
    )

    def get_appointment_row_by_note(self, note):
        return self.find(
            By.XPATH,
            f"//tbody/tr[td[normalize-space()='{note}']]"
        )

    def get_appointment_id_by_note(self, note):
        row = self.get_appointment_row_by_note(note)

        return row.find_element(
            By.XPATH,
            "./td[1]"
        ).text

    def open_page(self):
        self.open(self.URL)

    def get_page_title(self):
        return self.find(
            *self.PAGE_TITLE
        ).text
    def get_patient_name_by_note(self, note):
        row = self.get_appointment_row_by_note(note)

        return row.find_element(
            By.XPATH,
            "./td[2]"
        ).text

    def get_doctor_name_by_note(self, note):
        row = self.get_appointment_row_by_note(note)

        return row.find_element(
            By.XPATH,
            "./td[3]"
        ).text

    def get_appointment_time_by_note(self, note):
        row = self.get_appointment_row_by_note(note)

        return row.find_element(
            By.XPATH,
            "./td[4]"
        ).text

    def get_status_by_note(self, note):
        row = self.get_appointment_row_by_note(note)

        return row.find_element(
            By.XPATH,
            "./td[5]"
        ).text

    def is_confirm_button_present(self, note):
        row = self.get_appointment_row_by_note(note)

        buttons = row.find_elements(
            By.XPATH,
            ".//button[normalize-space()='Xác nhận']"
        )

        return len(buttons) > 0

    def is_cancel_button_present(self, note):
        row = self.get_appointment_row_by_note(note)

        buttons = row.find_elements(
            By.XPATH,
            ".//button[normalize-space()='Hủy']"
        )

        return len(buttons) > 0

    def click_confirm(self, note):
        button_locator = (
            By.XPATH,
            f"//tbody/tr[td[normalize-space()='{note}']]"
            "//button[normalize-space()='Xác nhận']"
        )

        self.click(*button_locator)

    def click_cancel(self, note):
        button_locator = (
            By.XPATH,
            f"//tbody/tr[td[normalize-space()='{note}']]"
            "//button[normalize-space()='Hủy']"
        )

        self.click(*button_locator)

        alert = self.wait.until(
            EC.alert_is_present()
        )

        alert.accept()

    def get_confirm_success_message(self):
        return self.find(
            *self.CONFIRM_SUCCESS_MESSAGE
        ).text

    def get_cancel_success_message(self):
        return self.find(
            *self.CANCEL_SUCCESS_MESSAGE
        ).text