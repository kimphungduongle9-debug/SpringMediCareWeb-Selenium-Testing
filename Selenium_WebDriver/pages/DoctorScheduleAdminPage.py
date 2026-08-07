from selenium.webdriver.common.by import By

from pages.BasePage import BasePage

import time

class DoctorScheduleAdminPage(BasePage):

    URL = "http://localhost:3000/doctor-schedules"

    FORM_TITLE = (
        By.XPATH,
        "//h3[normalize-space()='Thêm lịch làm việc']"
    )

    DOCTOR_SELECT = (
        By.XPATH,
        "//label[normalize-space()='Bác sĩ']/following-sibling::select"
    )

    WORK_DATE_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='dd/mm/yyyy']"
    )

    SHIFT_SELECT = (
        By.XPATH,
        "//label[normalize-space()='Ca làm việc']/following-sibling::select"
    )

    STATUS_SELECT = (
        By.XPATH,
        "//label[normalize-space()='Trạng thái']/following-sibling::select"
    )

    NOTE_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='Ví dụ: Ca sáng, ca chiều, nghỉ phép...']"
    )

    ADD_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Thêm lịch']"
    )
    SUCCESS_MESSAGE = (
        By.CSS_SELECTOR,
        "div.alert.alert-info"
    )

    WORK_DATE_DAY_8 = (
        By.XPATH,
        "//div[contains(@class, 'react-datepicker__day') "
        "and not(contains(@class, 'react-datepicker__day--outside-month')) "
        "and normalize-space()='8']"
    )

    UPDATE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Cập nhật']"
    )

    CANCEL_EDIT_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Hủy sửa']"
    )
    def open_page(self):
        self.open(self.URL)

    def get_form_title(self):
        return self.find(
            *self.FORM_TITLE
        ).text

    def is_doctor_select_displayed(self):
        return self.find(
            *self.DOCTOR_SELECT
        ).is_displayed()

    def is_work_date_input_displayed(self):
        return self.find(
            *self.WORK_DATE_INPUT
        ).is_displayed()

    def is_shift_select_displayed(self):
        return self.find(
            *self.SHIFT_SELECT
        ).is_displayed()

    def is_status_select_displayed(self):
        return self.find(
            *self.STATUS_SELECT
        ).is_displayed()

    def is_note_input_displayed(self):
        return self.find(
            *self.NOTE_INPUT
        ).is_displayed()

    def is_add_button_displayed(self):
        return self.find(
            *self.ADD_BUTTON
        ).is_displayed()

    def is_update_button_present(self):
        return len(
            self.finds(
                *self.UPDATE_BUTTON
            )
        ) > 0

    def is_cancel_edit_button_present(self):
        return len(
            self.finds(
                *self.CANCEL_EDIT_BUTTON
            )
        ) > 0

    def get_doctor_options(self):
        doctor_select = self.find(
            *self.DOCTOR_SELECT
        )

        options = doctor_select.find_elements(
            By.TAG_NAME,
            "option"
        )

        return [
            option.text
            for option in options
        ]

    def get_selected_doctor_value(self):
        return self.find(
            *self.DOCTOR_SELECT
        ).get_attribute("value")

    def get_work_date_value(self):
        return self.find(
            *self.WORK_DATE_INPUT
        ).get_attribute("value")

    def get_shift_options(self):
        shift_select = self.find(
            *self.SHIFT_SELECT
        )

        options = shift_select.find_elements(
            By.TAG_NAME,
            "option"
        )

        return [
            option.text
            for option in options
        ]

    def get_selected_shift_value(self):
        return self.find(
            *self.SHIFT_SELECT
        ).get_attribute("value")

    def get_status_options(self):
        status_select = self.find(
            *self.STATUS_SELECT
        )

        options = status_select.find_elements(
            By.TAG_NAME,
            "option"
        )

        return [
            option.text
            for option in options
        ]

    def get_selected_status_value(self):
        return self.find(
            *self.STATUS_SELECT
        ).get_attribute("value")

    def get_note_value(self):
        return self.find(
            *self.NOTE_INPUT
        ).get_attribute("value")

    def select_doctor(self, doctor_name):
        doctor_select = self.find(
            *self.DOCTOR_SELECT
        )

        options = doctor_select.find_elements(
            By.TAG_NAME,
            "option"
        )

        for option in options:
            if option.text == doctor_name:
                option.click()
                return

    def select_shift(self, shift_name):
        shift_select = self.find(
            *self.SHIFT_SELECT
        )

        options = shift_select.find_elements(
            By.TAG_NAME,
            "option"
        )

        for option in options:
            if option.text == shift_name:
                option.click()
                return

    def select_status(self, status_name):
        status_select = self.find(
            *self.STATUS_SELECT
        )

        options = status_select.find_elements(
            By.TAG_NAME,
            "option"
        )

        for option in options:
            if option.text == status_name:
                option.click()
                return

    def get_selected_doctor_text(self):
        doctor_select = self.find(
            *self.DOCTOR_SELECT
        )

        options = doctor_select.find_elements(
            By.TAG_NAME,
            "option"
        )

        for option in options:
            if option.is_selected():
                return option.text

        return ""

    def get_selected_shift_text(self):
        shift_select = self.find(
            *self.SHIFT_SELECT
        )

        options = shift_select.find_elements(
            By.TAG_NAME,
            "option"
        )

        for option in options:
            if option.is_selected():
                return option.text

        return ""

    def get_selected_status_text(self):
        status_select = self.find(
            *self.STATUS_SELECT
        )

        options = status_select.find_elements(
            By.TAG_NAME,
            "option"
        )

        for option in options:
            if option.is_selected():
                return option.text

        return ""

    def click_doctor_select(self):
        self.find(
            *self.DOCTOR_SELECT
        ).click()

    def click_shift_select(self):
        self.find(
            *self.SHIFT_SELECT
        ).click()

    def click_status_select(self):
        self.find(
            *self.STATUS_SELECT
        ).click()

    def click_work_date_input(self):
        self.click(
            *self.WORK_DATE_INPUT
        )

    def select_work_date_day_8(self):
        self.find(
            *self.WORK_DATE_INPUT
        ).click()

        time.sleep(1)

        self.find(
            *self.WORK_DATE_DAY_8
        ).click()

        time.sleep(1)

    def enter_note(self, note):
        self.typing(
            *self.NOTE_INPUT,
            note
        )

    def click_add_button(self):
        self.click(
            *self.ADD_BUTTON
        )

        time.sleep(2)

    def get_success_message(self):
        return self.find(
            *self.SUCCESS_MESSAGE
        ).text