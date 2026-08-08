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

    WEEK_SCHEDULE_TABLE = (
        By.XPATH,
        "//h3[normalize-space()='Lịch làm việc theo tuần']"
        "/following::table[1]"
    )

    SCHEDULE_LIST_TABLE = (
        By.XPATH,
        "//h3[normalize-space()='Danh sách lịch làm việc']"
        "/following::table[1]"
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
    WORK_DATE_DAY_1 = (
        By.XPATH,
        "//div[contains(@class, 'react-datepicker__day') "
        "and not(contains(@class, 'react-datepicker__day--outside-month')) "
        "and normalize-space()='1']"
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

    def is_schedule_present_in_list(
            self,
            doctor_name,
            work_date,
            shift_name,
            status,
            note):

        schedule_table = self.find(
            *self.SCHEDULE_LIST_TABLE
        )

        rows = schedule_table.find_elements(
            By.CSS_SELECTOR,
            "tbody tr"
        )

        for row in rows:
            cells = row.find_elements(
                By.TAG_NAME,
                "td"
            )

            if len(cells) < 8:
                continue

            if (
                    cells[1].text.strip() == doctor_name
                    and cells[2].text.strip() == work_date
                    and cells[3].text.strip() == shift_name
                    and cells[6].text.strip() == status
                    and cells[7].text.strip() == note
            ):
                return True

        return False

    def is_schedule_present_in_week_view(
            self,
            doctor_name,
            work_date,
            shift_name,
            status,
            note):

        week_table = self.find(
            *self.WEEK_SCHEDULE_TABLE
        )

        headers = week_table.find_elements(
            By.CSS_SELECTOR,
            "thead th"
        )

        day_index = -1

        for index in range(1, len(headers)):
            small = headers[index].find_element(
                By.TAG_NAME,
                "small"
            )

            if small.text.strip() == work_date:
                day_index = index - 1
                break

        if day_index == -1:
            return False

        rows = week_table.find_elements(
            By.CSS_SELECTOR,
            "tbody tr"
        )

        for row in rows:
            shift_header = row.find_element(
                By.TAG_NAME,
                "th"
            )

            shift_label = shift_header.find_element(
                By.TAG_NAME,
                "div"
            ).text.strip()

            if shift_label != shift_name:
                continue

            cells = row.find_elements(
                By.TAG_NAME,
                "td"
            )

            if day_index >= len(cells):
                return False

            target_cell = cells[day_index]

            cell_text = target_cell.text

            return (
                    doctor_name in cell_text
                    and status in cell_text
                    and note in cell_text
            )

        return False

    def scroll_to_success_message(self):
        self.scroll_to_element(
            *self.SUCCESS_MESSAGE
        )

        time.sleep(1)

    def scroll_to_schedule_list(self):
        self.scroll_to_element(
            *self.SCHEDULE_LIST_TABLE
        )

        time.sleep(1)

    def scroll_to_schedule_in_list(
            self,
            doctor_name,
            work_date,
            shift_name,
            status,
            note):

        schedule_table = self.find(
            *self.SCHEDULE_LIST_TABLE
        )

        rows = schedule_table.find_elements(
            By.CSS_SELECTOR,
            "tbody tr"
        )

        for row in rows:
            cells = row.find_elements(
                By.TAG_NAME,
                "td"
            )

            if len(cells) < 8:
                continue

            if (
                    cells[1].text.strip() == doctor_name
                    and cells[2].text.strip() == work_date
                    and cells[3].text.strip() == shift_name
                    and cells[6].text.strip() == status
                    and cells[7].text.strip() == note
            ):
                self.driver.execute_script(
                    "arguments[0].scrollIntoView("
                    "{block: 'center'});",
                    row
                )

                time.sleep(2)

                return True

        return False

    def scroll_to_schedule_in_week_view(
            self,
            doctor_name,
            work_date,
            shift_name,
            status,
            note):

        week_table = self.find(
            *self.WEEK_SCHEDULE_TABLE
        )

        headers = week_table.find_elements(
            By.CSS_SELECTOR,
            "thead th"
        )

        day_index = -1

        for index in range(1, len(headers)):
            date_text = headers[index].find_element(
                By.TAG_NAME,
                "small"
            ).text.strip()

            if date_text == work_date:
                day_index = index - 1
                break

        if day_index == -1:
            return False

        rows = week_table.find_elements(
            By.CSS_SELECTOR,
            "tbody tr"
        )

        for row in rows:
            shift_header = row.find_element(
                By.TAG_NAME,
                "th"
            )

            shift_label = shift_header.find_element(
                By.TAG_NAME,
                "div"
            ).text.strip()

            if shift_label != shift_name:
                continue

            cells = row.find_elements(
                By.TAG_NAME,
                "td"
            )

            if day_index >= len(cells):
                return False

            target_cell = cells[day_index]

            schedules = target_cell.find_elements(
                By.CSS_SELECTOR,
                "div.border.rounded.p-2.mb-2"
            )

            for schedule in schedules:
                schedule_text = schedule.text

                if (
                        doctor_name in schedule_text
                        and status in schedule_text
                        and note in schedule_text
                ):
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView("
                        "{block: 'center'});",
                        schedule
                    )

                    time.sleep(2)

                    return True

        return False

    def is_doctor_value_missing(self):
        doctor_select = self.find(
            *self.DOCTOR_SELECT
        )

        return self.driver.execute_script(
            "return arguments[0].validity.valueMissing;",
            doctor_select
        )

    def scroll_to_doctor_select(self):
        doctor_select = self.find(
            *self.DOCTOR_SELECT
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView("
            "{block: 'center'});",
            doctor_select
        )

        time.sleep(2)

    def is_work_date_value_missing(self):
        work_date_input = self.find(
            *self.WORK_DATE_INPUT
        )

        return self.driver.execute_script(
            "return arguments[0].validity.valueMissing;",
            work_date_input
        )

    def scroll_to_work_date_input(self):
        work_date_input = self.find(
            *self.WORK_DATE_INPUT
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView("
            "{block: 'center'});",
            work_date_input
        )

        time.sleep(2)

    def select_work_date_day_1(self):
        self.find(
            *self.WORK_DATE_INPUT
        ).click()

        time.sleep(1)

        self.find(
            *self.WORK_DATE_DAY_1
        ).click()

        time.sleep(1)

    def click_add_button_multiple_times(
            self,
            times=3):

        add_button = self.find(
            *self.ADD_BUTTON
        )

        for _ in range(times):
            self.driver.execute_script(
                "arguments[0].click();",
                add_button
            )

        time.sleep(3)