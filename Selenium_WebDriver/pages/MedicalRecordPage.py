from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class MedicalRecordPage(BasePage):

    URL = (
        "http://localhost:3000/"
        "doctor-medical-record?appointmentId={}"
    )

    PAGE_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Chi tiết hồ sơ bệnh án']"
    )

    ACCESS_DENIED_MESSAGE = (
        By.XPATH,
        "//div[contains(@class, 'alert') "
        "and contains(normalize-space(.), "
        "'Bạn không có quyền xem hồ sơ bệnh án này.')]"
    )

    MEDICAL_RECORD_INFORMATION = (
        By.XPATH,
        "//h4[normalize-space()='Thông tin khám bệnh']"
    )

    EDIT_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Cập nhật hồ sơ']"
    )

    DOCTOR_INFORMATION = (
        By.XPATH,
        "//strong[normalize-space()='Bác sĩ phụ trách:']"
        "/parent::p"
    )

    DIAGNOSIS_INFORMATION = (
        By.XPATH,
        "//strong[normalize-space()='Chẩn đoán:']"
        "/parent::p"
    )

    TREATMENT_INFORMATION = (
        By.XPATH,
        "//strong[normalize-space()='Hướng điều trị:']"
        "/parent::p"
    )
    PATIENT_NAME = (
        By.XPATH,
        "//p[normalize-space()='Bệnh nhân']"
        "/preceding-sibling::h5"
    )
    EDIT_FORM_TITLE = (
        By.XPATH,
        "//h4[normalize-space()='Cập nhật hồ sơ bệnh án']"
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

    SAVE_CHANGES_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Lưu thay đổi']"
    )

    CANCEL_EDIT_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Hủy']"
    )

    UPDATE_SUCCESS_MESSAGE = (
        By.XPATH,
        "//div[contains(@class, 'alert') "
        "and contains(normalize-space(.), "
        "'Cập nhật hồ sơ bệnh án thành công.')]"
    )
    def open_page(self, appointment_id):
        self.open(
            self.URL.format(appointment_id)
        )

    def get_page_title(self):
        return self.find(
            *self.PAGE_TITLE
        ).text

    def get_access_denied_message(self):
        return self.find(
            *self.ACCESS_DENIED_MESSAGE
        ).text

    def is_medical_record_information_present(self):
        return len(
            self.finds(
                *self.MEDICAL_RECORD_INFORMATION
            )
        ) > 0

    def is_edit_button_present(self):
        return len(
            self.finds(
                *self.EDIT_BUTTON
            )
        ) > 0

    def get_doctor_information(self):
        return self.find(
            *self.DOCTOR_INFORMATION
        ).text

    def get_diagnosis_information(self):
        return self.find(
            *self.DIAGNOSIS_INFORMATION
        ).text

    def get_treatment_information(self):
        return self.find(
            *self.TREATMENT_INFORMATION
        ).text

    def get_patient_name(self):
        return self.find(
            *self.PATIENT_NAME
        ).text

    def click_edit_button(self):
        self.click(
            *self.EDIT_BUTTON
        )

    def is_edit_form_present(self):
        return len(
            self.finds(*self.EDIT_FORM_TITLE)
        ) > 0

    def get_diagnosis_input_value(self):
        return self.find(
            *self.DIAGNOSIS_TEXTAREA
        ).get_attribute("value")

    def get_treatment_input_value(self):
        return self.find(
            *self.TREATMENT_TEXTAREA
        ).get_attribute("value")

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

    def click_save_changes(self):
        self.click(
            *self.SAVE_CHANGES_BUTTON
        )

    def click_cancel_edit(self):
        self.click(
            *self.CANCEL_EDIT_BUTTON
        )

    def get_update_success_message(self):
        return self.find(
            *self.UPDATE_SUCCESS_MESSAGE
        ).text

