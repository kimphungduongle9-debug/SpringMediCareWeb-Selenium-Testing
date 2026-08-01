from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class DoctorAppointmentPage(BasePage):

    URL = "http://localhost:3000/doctor-appointments"

    PAGE_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Lịch hẹn bệnh nhân']"
    )

    def open_page(self):
        self.open(self.URL)

    def get_appointment_row(self, note):
        return self.find(
            By.XPATH,
            f"//tbody/tr[td[normalize-space()='{note}']]"
        )

    def get_status_by_note(self, note):
        row = self.get_appointment_row(note)

        return row.find_element(
            By.XPATH,
            "./td[4]"
        ).text

    def get_patient_name_by_note(self, note):
        row = self.get_appointment_row(note)

        return row.find_element(
            By.XPATH,
            "./td[2]"
        ).text

    def is_view_medical_record_button_present(
            self,
            note):
        row = self.get_appointment_row(note)

        buttons = row.find_elements(
            By.XPATH,
            ".//button[normalize-space()='Xem hồ sơ']"
        )

        return len(buttons) > 0

    def click_view_medical_record(self, note):
        button_locator = (
            By.XPATH,
            f"//tbody/tr[td[normalize-space()='{note}']]"
            "//button[normalize-space()='Xem hồ sơ']"
        )

        self.click(
            *button_locator
        )

    def get_appointment_row_by_id(
            self,
            appointment_id):
        return self.find(
            By.XPATH,
            f"//tbody/tr[td[1][normalize-space()="
            f"'{appointment_id}']]"
        )

    def get_status_by_id(
            self,
            appointment_id):
        row = self.get_appointment_row_by_id(
            appointment_id
        )

        return row.find_element(
            By.XPATH,
            "./td[4]"
        ).text

    def get_note_by_id(
            self,
            appointment_id):
        row = self.get_appointment_row_by_id(
            appointment_id
        )

        return row.find_element(
            By.XPATH,
            "./td[5]"
        ).text

    def is_examine_button_present(
            self,
            appointment_id):
        row = self.get_appointment_row_by_id(
            appointment_id
        )

        buttons = row.find_elements(
            By.XPATH,
            ".//button[normalize-space()='Khám bệnh']"
        )

        return len(buttons) > 0

    def click_examine(
            self,
            appointment_id):
        button_locator = (
            By.XPATH,
            f"//tbody/tr[td[1][normalize-space()="
            f"'{appointment_id}']]"
            "//button[normalize-space()='Khám bệnh']"
        )

        self.click(
            *button_locator
        )

    def is_view_medical_record_button_present_by_id(
            self,
            appointment_id):
        row = self.get_appointment_row_by_id(
            appointment_id
        )

        buttons = row.find_elements(
            By.XPATH,
            ".//button[normalize-space()='Xem hồ sơ']"
        )

        return len(buttons) > 0

    def is_appointment_present_by_note(
            self,
            note):
        rows = self.finds(
            By.XPATH,
            f"//tbody/tr[td[normalize-space()='{note}']]"
        )

        return len(rows) > 0

    def is_patient_profile_button_present(
            self,
            appointment_id):
        buttons = self.finds(
            By.XPATH,
            "//tbody/tr"
            f"[td[normalize-space()='{appointment_id}']]"
            "//*[self::a or self::button]"
            "[contains(normalize-space(.), 'Xem hồ sơ') "
            "or contains(normalize-space(.), 'Lịch sử khám')]"
        )

        return len(buttons) > 0