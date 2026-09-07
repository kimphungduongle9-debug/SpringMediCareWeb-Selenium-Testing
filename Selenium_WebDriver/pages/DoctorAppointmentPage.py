from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class DoctorAppointmentPage(BasePage):

    """
    Page Object cho chức năng quản lý lịch hẹn của Doctor.

    Mapping Test Case -> Step -> Method:

    TC-APPOINTMENT-004
    - Step 2: Mở danh sách và tìm đúng lịch hẹn
      + open_page()
      + get_note_by_id()
      + get_patient_name_by_note()
    - Step 3: Kiểm tra trạng thái và quyền thao tác
      + get_status_by_id()
      + is_examine_button_present()
      + is_patient_profile_button_present()
    - Step 4: Mở hồ sơ bệnh nhân
      + click_view_medical_record()

    TC-APPOINTMENT-005
    - Step 2: Kiểm tra lịch đang Chờ xác nhận
      + open_page()
      + get_status_by_id()
      + get_note_by_id()
    - Step 5: Kiểm tra trạng thái lịch không thay đổi
      + open_page()
      + get_status_by_id()

    TC-APPOINTMENT-006
    - Step 2: Mở danh sách và tìm đúng lịch hẹn
      + open_page()
      + get_note_by_id()
    - Step 3: Kiểm tra lịch đã xác nhận và quyền khám
      + get_status_by_id()
      + is_examine_button_present()
    - Step 4: Mở chức năng Khám bệnh
      + click_examine()

    TC-APPOINTMENT-007
    - Step 2: Kiểm tra lịch của bác sĩ khác không xuất hiện
      + open_page()
      + is_appointment_present_by_note()

    TC-APPOINTMENT-008
    - Step 2: Tìm lịch đã hủy
      + open_page()
      + is_appointment_present_by_note()
    - Step 3: Kiểm tra trạng thái và quyền khám
      + get_status_by_note()
      + is_examine_button_present()

    TC-APPOINTMENT-009
    - Step 1: Mở lịch đã xác nhận của bác sĩ
      + open_page()
      + get_note_by_id()
      + get_status_by_id()
    - Step 2: Kiểm tra và mở chức năng Khám bệnh
      + is_examine_button_present()
      + click_examine()
    - Step 5: Kiểm tra lịch sau khi hoàn thành
      + open_page()
      + get_status_by_id()
      + is_examine_button_present()

    TC-MEDICAL-001
    - Step 3: Mở danh sách và tìm đúng lịch hẹn
      + open_page()
      + get_note_by_id()
    - Step 4: Kiểm tra trạng thái và nút Khám bệnh
      + get_status_by_id()
      + is_examine_button_present()
    - Step 5: Mở chức năng Khám bệnh
      + click_examine()
    - Step 9: Kiểm tra lịch sau khi tạo hồ sơ
      + open_page()
      + get_status_by_id()
      + is_view_medical_record_button_present_by_id()
      + is_examine_button_present()

    TC-MEDICAL-002
    - Step 3: Mở đúng lịch đã xác nhận và vào Khám bệnh
      + open_page()
      + get_note_by_id()
      + get_status_by_id()
      + is_examine_button_present()
      + click_examine()
    - Step 7: Kiểm tra lịch vẫn ở trạng thái Đã xác nhận
      + open_page()
      + get_status_by_id()
      + is_examine_button_present()
      + is_view_medical_record_button_present_by_id()

    TC-MEDICAL-003
    - Step 3: Mở đúng lịch đã xác nhận và vào Khám bệnh
      + open_page()
      + get_note_by_id()
      + get_status_by_id()
      + is_examine_button_present()
      + click_examine()
    - Step 7: Kiểm tra lịch vẫn ở trạng thái Đã xác nhận
      + open_page()
      + get_status_by_id()
      + is_examine_button_present()
      + is_view_medical_record_button_present_by_id()

    TC-MEDICAL-004
    - Step 3: Mở danh sách và tìm đúng lịch đã hoàn thành
      + open_page()
      + get_note_by_id()
    - Step 4: Kiểm tra trạng thái và nút thao tác
      + get_status_by_id()
      + is_view_medical_record_button_present_by_id()
      + is_examine_button_present()
    - Step 5: Mở hồ sơ bệnh án hiện có
      + click_view_medical_record()

    TC-MEDICAL-005
    - Step 3: Mở danh sách và tìm đúng lịch đã hoàn thành
      + open_page()
      + get_note_by_id()
      + get_status_by_id()
    - Step 4: Kiểm tra nút Xem hồ sơ
      + is_view_medical_record_button_present_by_id()
    - Step 5: Mở hồ sơ bệnh án
      + click_view_medical_record()

    TC-MEDICAL-007
    - Step 3: Doctor B mở trang Lịch hẹn bệnh nhân
      + open_page()
    - Step 4: Kiểm tra lịch của Doctor A không xuất hiện
      + get_note_by_id()
    """

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