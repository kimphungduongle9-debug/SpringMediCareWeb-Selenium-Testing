from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class DoctorExaminationPage(BasePage):

    """
    Page Object cho chức năng Khám bệnh của Doctor.

    Mapping Test Case -> Step -> Method:

    TC-APPOINTMENT-005
    - Step 3: Truy cập trực tiếp trang khám của lịch chưa xác nhận
      + open_page()
      + get_invalid_appointment_message()
    - Step 4: Kiểm tra không hiển thị dữ liệu và form khám
      + is_appointment_information_present()
      + is_create_record_form_present()

    TC-APPOINTMENT-006
    - Step 4: Kiểm tra mở đúng trang Khám bệnh
      + get_page_title()
    - Step 5: Kiểm tra form khám bệnh
      + is_create_record_form_present()

    TC-APPOINTMENT-007
    - Step 3: Truy cập trực tiếp trang khám bằng appointmentId
      + open_page()
    - Step 4: Kiểm tra hệ thống từ chối quyền truy cập
      + get_access_denied_message()
    - Step 5: Kiểm tra không hiển thị dữ liệu và form khám
      + is_appointment_information_present()
      + is_create_record_form_present()

    TC-APPOINTMENT-008
    - Step 4: Truy cập lịch đã hủy và kiểm tra hệ thống chặn
      + open_page()
      + get_invalid_appointment_message()
    - Step 5: Kiểm tra không hiển thị dữ liệu và form khám
      + is_appointment_information_present()
      + is_create_record_form_present()

    TC-APPOINTMENT-009
    - Step 2: Kiểm tra mở đúng trang Khám bệnh
      + get_page_title()
    - Step 3: Kiểm tra form và nhập kết quả khám
      + is_create_record_form_present()
      + enter_diagnosis()
      + enter_treatment()
    - Step 4: Lưu hồ sơ bệnh án
      + click_save_medical_record()

    TC-MEDICAL-001
    - Step 6: Kiểm tra trang Khám bệnh
      + get_page_title()
      + is_appointment_information_present()
      + is_create_record_form_present()
    - Step 7: Nhập Chẩn đoán và Hướng điều trị
      + enter_diagnosis()
      + enter_treatment()
    - Step 8: Lưu hồ sơ bệnh án
      + click_save_medical_record()

    TC-MEDICAL-002
    - Step 3: Kiểm tra mở đúng trang Khám bệnh
      + get_page_title()
    - Step 4: Để trống Chẩn đoán và nhập Hướng điều trị
      + enter_diagnosis()
      + enter_treatment()
    - Step 5: Thực hiện lưu hồ sơ
      + click_save_medical_record()
    - Step 6: Kiểm tra validation và form vẫn hiển thị
      + get_validation_message()
      + is_create_record_form_present()

    TC-MEDICAL-003
    - Step 3: Kiểm tra mở đúng trang Khám bệnh
      + get_page_title()
    - Step 4: Nhập Chẩn đoán và để trống Hướng điều trị
      + enter_diagnosis()
      + enter_treatment()
    - Step 5: Thực hiện lưu hồ sơ
      + click_save_medical_record()
    - Step 6: Kiểm tra validation và form vẫn hiển thị
      + get_validation_message()
      + is_create_record_form_present()

    TC-MEDICAL-004
    - Step 6: Truy cập trực tiếp trang Khám bệnh của lịch đã hoàn thành
      + open_page()
    - Step 7: Kiểm tra hệ thống chặn tạo hồ sơ mới
      + get_invalid_appointment_message()
      + is_create_record_form_present()
    """

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

    PATIENT_NAME = (
        By.XPATH,
        "//p[normalize-space()='Bệnh nhân']"
        "/preceding-sibling::h5"
    )

    APPOINTMENT_NOTE = (
        By.XPATH,
        "//strong[normalize-space()='Lý do khám:']"
        "/parent::p"
    )

    APPOINTMENT_STATUS = (
        By.XPATH,
        "//strong[normalize-space()='Trạng thái:']"
        "/parent::p"
    )
    ACCESS_DENIED_MESSAGE = (
        By.XPATH,
        "//div[contains(@class, 'alert') "
        "and contains(normalize-space(.), "
        "'Bạn không có quyền khám lịch hẹn này.')]"
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

    def get_patient_name(self):
        return self.find(
            *self.PATIENT_NAME
        ).text

    def get_appointment_note(self):
        return self.find(
            *self.APPOINTMENT_NOTE
        ).text

    def get_appointment_status(self):
        return self.find(
            *self.APPOINTMENT_STATUS
        ).text

    def get_access_denied_message(self):
        return self.find(
            *self.ACCESS_DENIED_MESSAGE
        ).text