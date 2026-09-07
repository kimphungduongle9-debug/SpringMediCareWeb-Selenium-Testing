from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class MedicalRecordPage(BasePage):
    """
    Page Object cho chức năng Hồ sơ bệnh án.

    Mapping Test Case -> Step -> Method:

    TC-APPOINTMENT-009
    - Step 4: Kiểm tra hồ sơ bệnh án vừa được lưu
      + get_page_title()
      + get_diagnosis_information()
      + get_treatment_information()
    - Step 6: Mở lại hồ sơ và kiểm tra dữ liệu đã lưu
      + open_page()
      + get_diagnosis_information()
      + get_treatment_information()

    TC-MEDICAL-001
    - Step 8: Kiểm tra mở trang Chi tiết hồ sơ bệnh án sau khi lưu
      + get_page_title()
    - Step 9: Kiểm tra Chẩn đoán và Hướng điều trị đã lưu
      + get_diagnosis_information()
      + get_treatment_information()

    TC-MEDICAL-004
    - Step 5: Kiểm tra hồ sơ bệnh án hiện có
      + get_page_title()
      + get_diagnosis_information()
      + get_treatment_information()
    - Step 8: Mở lại hồ sơ và kiểm tra dữ liệu không thay đổi
      + open_page()
      + get_diagnosis_information()
      + get_treatment_information()

    TC-MEDICAL-005
    - Step 5: Kiểm tra mở đúng trang Chi tiết hồ sơ bệnh án
      + get_page_title()
    - Step 6: Kiểm tra đúng bệnh nhân và bác sĩ phụ trách
      + get_patient_name()
      + get_doctor_information()
    - Step 7: Kiểm tra Chẩn đoán và Hướng điều trị
      + get_diagnosis_information()
      + get_treatment_information()
    - Step 8: Mở lại hồ sơ và kiểm tra dữ liệu không thay đổi
      + open_page()
      + get_diagnosis_information()
      + get_treatment_information()

    TC-MEDICAL-006
    - Step 2: Mở hồ sơ và ghi nhận dữ liệu hiện tại
      + open_page()
      + get_page_title()
      + get_diagnosis_information()
      + get_treatment_information()
    - Step 3: Mở form Cập nhật hồ sơ
      + is_edit_button_present()
      + click_edit_button()
      + is_edit_form_present()
    - Step 4: Kiểm tra dữ liệu preload trên form
      + get_diagnosis_input_value()
      + get_treatment_input_value()
    - Step 5: Nhập Chẩn đoán và Hướng điều trị mới
      + enter_diagnosis()
      + enter_treatment()
      + get_diagnosis_input_value()
      + get_treatment_input_value()
    - Step 6: Lưu thay đổi
      + click_save_changes()
    - Step 7: Kiểm tra cập nhật thành công
      + get_update_success_message()
      + is_edit_form_present()
    - Step 8: Mở lại hồ sơ và kiểm tra dữ liệu mới
      + open_page()
      + get_diagnosis_information()
      + get_treatment_information()
    - Step 9: Kiểm tra hồ sơ vẫn thuộc đúng bệnh nhân và bác sĩ
      + get_patient_name()
      + get_doctor_information()
    - Step 10: Kiểm tra dữ liệu cập nhật vẫn được giữ
      + open_page()
      + get_diagnosis_information()
      + get_treatment_information()

    TC-MEDICAL-007
    - Step 1: Doctor A mở hồ sơ và ghi nhận dữ liệu hiện tại
      + open_page()
      + get_page_title()
      + get_patient_name()
      + get_doctor_information()
      + get_diagnosis_information()
      + get_treatment_information()
    - Step 5: Doctor B truy cập trực tiếp URL hồ sơ
      + open_page()
    - Step 6: Kiểm tra Doctor B bị từ chối truy cập
      + get_access_denied_message()
      + is_medical_record_information_present()
      + is_edit_button_present()
    - Step 8: Doctor A mở lại và kiểm tra dữ liệu không thay đổi
      + open_page()
      + get_patient_name()
      + get_doctor_information()
      + get_diagnosis_information()
      + get_treatment_information()

    TC-MEDICAL-008
    - Step 1: Doctor A mở hồ sơ và ghi nhận dữ liệu hiện tại
      + open_page()
      + get_page_title()
      + get_patient_name()
      + get_doctor_information()
      + get_diagnosis_information()
      + get_treatment_information()
    - Step 3: Doctor B truy cập trực tiếp URL hồ sơ
      + open_page()
    - Step 4: Kiểm tra Doctor B không được xem/cập nhật hồ sơ
      + get_access_denied_message()
      + is_medical_record_information_present()
      + is_edit_button_present()
    - Step 6: Doctor A mở lại hồ sơ
      + open_page()
      + get_page_title()
    - Step 7: Kiểm tra dữ liệu không bị thay đổi
      + get_diagnosis_information()
      + get_treatment_information()
    - Step 8: Kiểm tra hồ sơ vẫn thuộc Doctor A
      + get_patient_name()
      + get_doctor_information()

    TC-MEDICAL-009
    - Step 2: Mở hồ sơ và ghi nhận dữ liệu ban đầu
      + open_page()
      + get_page_title()
      + get_patient_name()
      + get_doctor_information()
      + get_diagnosis_information()
      + get_treatment_information()
    - Step 3: Mở form cập nhật
      + is_edit_button_present()
      + click_edit_button()
      + is_edit_form_present()
    - Step 4: Kiểm tra dữ liệu preload
      + get_diagnosis_input_value()
      + get_treatment_input_value()
    - Step 5: Nhập dữ liệu tạm mới
      + enter_diagnosis()
      + enter_treatment()
      + get_diagnosis_input_value()
      + get_treatment_input_value()
    - Step 6: Hủy cập nhật
      + click_cancel_edit()
    - Step 7: Kiểm tra form đóng và dữ liệu tạm không được lưu
      + is_edit_form_present()
      + get_diagnosis_information()
      + get_treatment_information()
    - Step 8: Mở lại và kiểm tra dữ liệu ban đầu
      + open_page()
      + get_diagnosis_information()
      + get_treatment_information()
    - Step 9: Kiểm tra hồ sơ vẫn thuộc đúng bệnh nhân và bác sĩ
      + get_patient_name()
      + get_doctor_information()
    """

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

