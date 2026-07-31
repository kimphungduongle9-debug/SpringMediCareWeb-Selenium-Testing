from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class DoctorExaminationPage(BasePage):

    PAGE_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Khám bệnh']"
    )

    APPOINTMENT_INFORMATION_TITLE = (
        By.XPATH,
        "//h4[normalize-space()='Thông tin lịch hẹn']"
    )

    CREATE_RECORD_FORM_TITLE = (
        By.XPATH,
        "//h4[normalize-space()='Ghi nhận kết quả khám']"
    )

    DIAGNOSIS_TEXTAREA = (
        By.XPATH,
        "//textarea[@placeholder="
        "'Nhập kết quả chẩn đoán']"
    )

    TREATMENT_TEXTAREA = (
        By.XPATH,
        "//textarea[@placeholder="
        "'Nhập hướng điều trị']"
    )

    SAVE_MEDICAL_RECORD_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Lưu hồ sơ bệnh án']"
    )
    VALIDATION_MESSAGE = (
        By.XPATH,
        "//div[contains(@class, 'alert') "
        "and contains(normalize-space(.), "
        "'Vui lòng nhập đầy đủ chẩn đoán "
        "và hướng điều trị.')]"
    )
    URL = (
        "http://localhost:3000/"
        "doctor-examination?appointmentId={}"
    )
    INVALID_APPOINTMENT_MESSAGE = (
        By.XPATH,
        "//div[contains(@class, 'alert') "
        "and contains(normalize-space(.), "
        "'Lịch hẹn chưa được xác nhận hoặc đã bị hủy.')]"
    )
    def get_page_title(self):
        return self.find(
            *self.PAGE_TITLE
        ).text

    def is_appointment_information_present(self):
        return len(
            self.finds(
                *self.APPOINTMENT_INFORMATION_TITLE
            )
        ) > 0

    def is_create_record_form_present(self):
        return len(
            self.finds(
                *self.CREATE_RECORD_FORM_TITLE
            )
        ) > 0

    def enter_diagnosis(self, diagnosis):
        textarea = self.find(
            *self.DIAGNOSIS_TEXTAREA
        )

        textarea.clear()
        textarea.send_keys(diagnosis)

    def enter_treatment(self, treatment):
        textarea = self.find(
            *self.TREATMENT_TEXTAREA
        )

        textarea.clear()
        textarea.send_keys(treatment)

    def click_save_medical_record(self):
        self.click(
            *self.SAVE_MEDICAL_RECORD_BUTTON
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
        examine_button = (
            By.XPATH,
            f"//tbody/tr[td[1][normalize-space()="
            f"'{appointment_id}']]"
            "//button[normalize-space()='Khám bệnh']"
        )

        self.click(
            *examine_button
        )

    def get_validation_message(self):
        return self.find(
            *self.VALIDATION_MESSAGE
        ).text

    def open_page(self, appointment_id):
        self.open(
            self.URL.format(appointment_id)
        )

    def get_invalid_appointment_message(self):
        return self.find(
            *self.INVALID_APPOINTMENT_MESSAGE
        ).text