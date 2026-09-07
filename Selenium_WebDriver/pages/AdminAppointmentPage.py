from selenium.webdriver.common.by import By

from pages.BasePage import BasePage

from selenium.webdriver.support import expected_conditions as EC

class AdminAppointmentPage(BasePage):
    """
    Page Object cho chức năng Quản lý lịch hẹn của Admin.

    Mapping Test Case -> Step -> Method:

    TC-APPOINTMENT-001
    - Step 5: Mở trang Quản lý lịch hẹn và tìm lịch vừa tạo
      + open_page()
      + get_page_title()
      + get_appointment_id_by_note()
    - Step 6: Kiểm tra thông tin, trạng thái và nút thao tác
      + get_patient_name_by_note()
      + get_doctor_name_by_note()
      + get_appointment_time_by_note()
      + get_status_by_note()
      + is_confirm_button_present()
      + is_cancel_button_present()

    TC-APPOINTMENT-002
    - Step 1: Mở trang Quản lý lịch hẹn
      + open_page()
      + get_page_title()
    - Step 2: Tìm lịch đang Chờ xác nhận
      + get_appointment_id_by_note()
      + get_status_by_note()
      + is_confirm_button_present()
    - Step 3: Xác nhận lịch hẹn
      + click_confirm()
    - Step 4: Kiểm tra thông báo xác nhận thành công
      + get_confirm_success_message()
    - Step 5: Kiểm tra trạng thái và dữ liệu sau xác nhận
      + get_status_by_note()
      + is_confirm_button_present()
      + is_cancel_button_present()
      + get_patient_name_by_note()
      + get_doctor_name_by_note()
      + get_appointment_time_by_note()

    TC-APPOINTMENT-003
    - Step 1: Mở trang Quản lý lịch hẹn
      + open_page()
      + get_page_title()
    - Step 2: Tìm lịch đang Chờ xác nhận
      + get_appointment_id_by_note()
      + get_status_by_note()
      + is_cancel_button_present()
    - Step 3: Hủy lịch hẹn
      + click_cancel()
    - Step 4: Kiểm tra thông báo hủy thành công
      + get_cancel_success_message()
    - Step 5: Kiểm tra trạng thái và dữ liệu sau khi hủy
      + get_status_by_note()
      + is_confirm_button_present()
      + is_cancel_button_present()
      + get_patient_name_by_note()
      + get_doctor_name_by_note()
      + get_appointment_time_by_note()
    """

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

    def wait_for_status_by_note(
            self,
            note,
            expected_status):
        status_locator = (
            By.XPATH,
            f"//tbody/tr[td[normalize-space()='{note}']]/td[5]"
        )

        self.wait.until(
            EC.text_to_be_present_in_element(
                status_locator,
                expected_status
            )
        )

        return self.get_status_by_note(note)