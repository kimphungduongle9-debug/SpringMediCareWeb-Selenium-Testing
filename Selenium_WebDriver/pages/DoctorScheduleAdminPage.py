from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from pages.BasePage import BasePage


class DoctorScheduleAdminPage(BasePage):
    URL = "http://localhost:3000/doctor-schedules"

    PAGE_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Quản lý lịch làm việc bác sĩ']"
    )

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

    MESSAGE_ALERT = (
        By.CSS_SELECTOR,
        "div.alert.alert-info"
    )

    SCHEDULE_LIST_TABLE = (
        By.XPATH,
        "//h3[normalize-space()='Danh sách lịch làm việc']/following::table[1]"
    )
    WEEK_HEADER_DATES = (
        By.XPATH,
        "//h3[normalize-space()='Lịch làm việc theo tuần']"
        "/following::table[1]/thead/tr/th[position()>1]/small"
    )

    WEEK_SHIFT_ROWS = (
        By.XPATH,
        "//h3[normalize-space()='Lịch làm việc theo tuần']"
        "/following::table[1]/tbody/tr"
    )

    FILTER_DOCTOR_SELECT = (
        By.XPATH,
        "//h3[normalize-space()='Lọc lịch làm việc']"
        "/following::select[1]"
    )

    WEEK_VIEW_TABLE = (
        By.XPATH,
        "//h3[normalize-space()='Lịch làm việc theo tuần']"
        "/following::table[1]"
    )
    WEEK_RANGE_TEXT = (
        By.XPATH,
        "//label[normalize-space()='Tuần làm việc']"
        "/following::div[contains(@class,'text-center')][1]"
    )

    PREVIOUS_WEEK_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(), 'Tuần trước')]"
    )

    NEXT_WEEK_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(), 'Tuần sau')]"
    )
    UPDATE_FORM_TITLE = (
        By.XPATH,
        "//h3[normalize-space()='Cập nhật lịch làm việc']"
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
        self.wait.until(
            EC.visibility_of_element_located(self.PAGE_TITLE)
        )

    def get_page_title(self):
        return self.find(*self.PAGE_TITLE).text.strip()

    def get_form_title(self):
        return self.find(*self.FORM_TITLE).text.strip()

    def is_doctor_select_displayed(self):
        return self.find(*self.DOCTOR_SELECT).is_displayed()

    def is_work_date_input_displayed(self):
        return self.find(*self.WORK_DATE_INPUT).is_displayed()

    def is_shift_select_displayed(self):
        return self.find(*self.SHIFT_SELECT).is_displayed()

    def is_status_select_displayed(self):
        return self.find(*self.STATUS_SELECT).is_displayed()

    def is_note_input_displayed(self):
        return self.find(*self.NOTE_INPUT).is_displayed()

    def is_add_button_displayed(self):
        return self.find(*self.ADD_BUTTON).is_displayed()

    def wait_for_doctors_loaded(self):
        self.wait.until(
            lambda driver: len(
                Select(
                    driver.find_element(*self.DOCTOR_SELECT)
                ).options
            ) > 1
        )

    def get_doctor_options(self):
        self.wait_for_doctors_loaded()
        return [
            option.text.strip()
            for option in Select(
                self.find(*self.DOCTOR_SELECT)
            ).options
        ]

    def get_shift_options(self):
        return [
            option.text.strip()
            for option in Select(
                self.find(*self.SHIFT_SELECT)
            ).options
        ]

    def get_status_options(self):
        return [
            option.text.strip()
            for option in Select(
                self.find(*self.STATUS_SELECT)
            ).options
        ]

    def get_selected_doctor_text(self):
        return Select(
            self.find(*self.DOCTOR_SELECT)
        ).first_selected_option.text.strip()

    def get_selected_shift_text(self):
        return Select(
            self.find(*self.SHIFT_SELECT)
        ).first_selected_option.text.strip()

    def get_selected_status_text(self):
        return Select(
            self.find(*self.STATUS_SELECT)
        ).first_selected_option.text.strip()

    def get_work_date_value(self):
        return self.find(
            *self.WORK_DATE_INPUT
        ).get_attribute("value")

    def get_note_value(self):
        return self.find(
            *self.NOTE_INPUT
        ).get_attribute("value")

    def open_doctor_dropdown(self):
        self.wait.until(
            EC.element_to_be_clickable(self.DOCTOR_SELECT)
        ).click()

    def open_shift_dropdown(self):
        self.wait.until(
            EC.element_to_be_clickable(self.SHIFT_SELECT)
        ).click()

    def open_status_dropdown(self):
        self.wait.until(
            EC.element_to_be_clickable(self.STATUS_SELECT)
        ).click()

    def select_doctor(self, doctor_name):
        self.wait_for_doctors_loaded()
        doctor_select = self.wait.until(
            EC.element_to_be_clickable(self.DOCTOR_SELECT)
        )
        Select(doctor_select).select_by_visible_text(doctor_name)

    def select_shift(self, shift_name):
        shift_select = self.wait.until(
            EC.element_to_be_clickable(self.SHIFT_SELECT)
        )
        Select(shift_select).select_by_visible_text(shift_name)

    def select_status(self, status_name):
        status_select = self.wait.until(
            EC.element_to_be_clickable(self.STATUS_SELECT)
        )
        Select(status_select).select_by_visible_text(status_name)

    def select_work_date(self, target_date):
        """
        Chọn ngày trên React DatePicker.

        target_date:
            datetime.date
        """
        date_input = self.wait.until(
            EC.element_to_be_clickable(self.WORK_DATE_INPUT)
        )
        date_input.click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".react-datepicker")
            )
        )

        month_header_locator = (
            By.CSS_SELECTOR,
            ".react-datepicker__current-month"
        )

        next_button_locator = (
            By.CSS_SELECTOR,
            ".react-datepicker__navigation--next"
        )

        previous_button_locator = (
            By.CSS_SELECTOR,
            ".react-datepicker__navigation--previous"
        )

        for _ in range(24):
            current_month = self.wait.until(
                EC.visibility_of_element_located(
                    month_header_locator
                )
            ).text.strip()

            current_month_date = datetime.strptime(
                current_month,
                "%B %Y"
            ).date().replace(day=1)

            target_month_date = target_date.replace(day=1)

            if current_month_date == target_month_date:
                break

            locator = (
                next_button_locator
                if current_month_date < target_month_date
                else previous_button_locator
            )

            self.wait.until(
                EC.element_to_be_clickable(locator)
            ).click()

        day_locator = (
            By.XPATH,
            (
                "//div[contains(@class,'react-datepicker__day') "
                "and not(contains(@class,"
                "'react-datepicker__day--outside-month')) "
                f"and normalize-space()='{target_date.day}']"
            )
        )

        self.wait.until(
            EC.element_to_be_clickable(day_locator)
        ).click()

        expected_value = target_date.strftime("%d/%m/%Y")

        self.wait.until(
            lambda driver: driver.find_element(
                *self.WORK_DATE_INPUT
            ).get_attribute("value") == expected_value
        )

    def enter_note(self, note):
        note_input = self.wait.until(
            EC.visibility_of_element_located(self.NOTE_INPUT)
        )
        note_input.clear()
        note_input.send_keys(note)

    def click_add_button(self):
        button = self.wait.until(
            EC.presence_of_element_located(self.ADD_BUTTON)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )

        self.wait.until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, ".react-datepicker")
            )
        )

        self.wait.until(
            EC.element_to_be_clickable(self.ADD_BUTTON)
        ).click()

    def get_message(self):
        return self.wait.until(
            EC.visibility_of_element_located(
                self.MESSAGE_ALERT
            )
        ).text.strip()

    def is_schedule_present_in_list(
            self,
            doctor_name,
            work_date,
            shift_name,
            status,
            note
    ):
        table = self.wait.until(
            EC.visibility_of_element_located(
                self.SCHEDULE_LIST_TABLE
            )
        )

        rows = table.find_elements(
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

            actual_doctor = cells[1].text.strip()
            actual_date = cells[2].text.strip()
            actual_shift = cells[3].text.strip()
            actual_status = cells[6].text.strip()
            actual_note = cells[7].text.strip()

            if (
                    actual_doctor == doctor_name
                    and actual_date == work_date
                    and actual_shift == shift_name
                    and actual_status == status
                    and actual_note == note
            ):
                return True

        return False

    def get_work_date_validation_message(self):
        return self.find(
            *self.WORK_DATE_INPUT
        ).get_attribute("validationMessage")

    def scroll_to_message(self):
        message = self.wait.until(
            EC.visibility_of_element_located(
                self.MESSAGE_ALERT
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            message
        )

    def is_message_displayed(self):
        return self.find(
            *self.MESSAGE_ALERT
        ).is_displayed()

    def scroll_to_top(self):
        self.driver.execute_script(
            "window.scrollTo({top: 0, behavior: 'smooth'});"
        )

        self.wait.until(
            lambda driver:
            driver.execute_script("return window.scrollY") <= 5
        )

    def get_week_header_dates(self):
        elements = self.finds(
            *self.WEEK_HEADER_DATES
        )

        return [
            element.text.strip()
            for element in elements
        ]

    def is_schedule_present_in_week(
            self,
            doctor_name,
            work_date,
            shift_name
    ):
        dates = self.get_week_header_dates()

        rows = self.finds(
            *self.WEEK_SHIFT_ROWS
        )

        for row in rows:
            shift_info = row.find_element(
                By.TAG_NAME,
                "th"
            ).text.splitlines()

            if not shift_info:
                continue

            actual_shift = shift_info[0].strip()

            if actual_shift != shift_name:
                continue

            cells = row.find_elements(
                By.TAG_NAME,
                "td"
            )

            for index, cell in enumerate(cells):
                if index >= len(dates):
                    continue

                if dates[index].strip() != work_date:
                    continue

                cards = cell.find_elements(
                    By.XPATH,
                    "./div"
                )

                for card in cards:
                    strong_elements = card.find_elements(
                        By.TAG_NAME,
                        "strong"
                    )

                    if not strong_elements:
                        continue

                    actual_doctor = (
                        strong_elements[0].text.strip()
                    )

                    if actual_doctor == doctor_name:
                        return True

        return False

    def go_to_week_containing(self, target_date):
        """
        Chuyển bảng Lịch làm việc theo tuần
        đến tuần chứa target_date.
        """

        for _ in range(52):
            date_texts = self.get_week_header_dates()

            if not date_texts:
                raise AssertionError(
                    "Không đọc được các ngày "
                    "trong bảng Lịch làm việc theo tuần"
                )

            displayed_dates = [
                datetime.strptime(
                    value,
                    "%d/%m/%Y"
                ).date()
                for value in date_texts
            ]

            first_date = min(displayed_dates)
            last_date = max(displayed_dates)

            if first_date <= target_date <= last_date:
                return

            old_dates = date_texts.copy()
            if target_date > last_date:
                button = self.wait.until(
                    EC.presence_of_element_located(
                        self.NEXT_WEEK_BUTTON
                    )
                )

            else:
                button = self.wait.until(
                    EC.presence_of_element_located(
                        self.PREVIOUS_WEEK_BUTTON
                    )
                )

            # Đưa nút vào giữa màn hình để tránh footer che.
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                button
            )

            # Click bằng JavaScript để tránh footer/credit
            # chặn thao tác click vật lý của Selenium.
            self.driver.execute_script(
                "arguments[0].click();",
                button
            )

            self.wait.until(
                lambda driver:
                self.get_week_header_dates() != old_dates
            )

        raise AssertionError(
            "Không chuyển được bảng tuần tới ngày "
            f"{target_date.strftime('%d/%m/%Y')}"
        )

    def scroll_to_schedule_list(self):
        element = self.wait.until(
            EC.visibility_of_element_located(
                self.SCHEDULE_LIST_TABLE
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

    def click_add_button_multiple_times(self, click_count=3):
        button = self.wait.until(
            EC.element_to_be_clickable(
                self.ADD_BUTTON
            )
        )

        # Click lần đầu: tạo lịch
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        # Chờ hệ thống xử lý và form reset sau khi tạo thành công
        self.wait.until(
            lambda driver:
            self.get_selected_doctor_text() == "-- Chọn bác sĩ --"
        )

        # Các lần click tiếp theo xảy ra trên form đã reset.
        # Browser validation phải chặn vì chưa chọn bác sĩ/ngày.
        for _ in range(click_count - 1):
            button = self.wait.until(
                EC.presence_of_element_located(
                    self.ADD_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                button
            )

            button.click()

    def select_filter_doctor(self, doctor_name):
        filter_select = self.wait.until(
            EC.element_to_be_clickable(
                self.FILTER_DOCTOR_SELECT
            )
        )

        Select(
            filter_select
        ).select_by_visible_text(
            doctor_name
        )

    def get_selected_filter_doctor_text(self):
        return Select(
            self.find(
                *self.FILTER_DOCTOR_SELECT
            )
        ).first_selected_option.text.strip()

    def scroll_to_week_view(self):
        table = self.wait.until(
            EC.visibility_of_element_located(
                self.WEEK_VIEW_TABLE
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            table
        )

    def get_week_view_doctor_names(self):
        table = self.wait.until(
            EC.visibility_of_element_located(
                self.WEEK_VIEW_TABLE
            )
        )

        names = []

        strong_elements = table.find_elements(
            By.TAG_NAME,
            "strong"
        )

        for element in strong_elements:
            text = element.text.strip()

            if text:
                names.append(text)

        return names

    def get_week_range_text(self):
        return self.wait.until(
            EC.visibility_of_element_located(
                self.WEEK_RANGE_TEXT
            )
        ).text.strip()

    def click_previous_week(self):
        button = self.wait.until(
            EC.presence_of_element_located(
                self.PREVIOUS_WEEK_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )

        old_range = self.get_week_range_text()

        # JS click để tránh footer che nút
        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        self.wait.until(
            lambda d: self.get_week_range_text() != old_range
        )

    def click_next_week(self):
        button = self.wait.until(
            EC.presence_of_element_located(
                self.NEXT_WEEK_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )

        old_range = self.get_week_range_text()

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        self.wait.until(
            lambda d: self.get_week_range_text() != old_range
        )

    def get_update_form_title(self):
        return self.wait.until(
            EC.visibility_of_element_located(
                self.UPDATE_FORM_TITLE
            )
        ).text.strip()

    def click_update_button(self):
        button = self.wait.until(
            EC.presence_of_element_located(
                self.UPDATE_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )
    def click_edit_schedule_by_id(self, schedule_id):
        table = self.wait.until(
            EC.visibility_of_element_located(
                self.SCHEDULE_LIST_TABLE
            )
        )

        rows = table.find_elements(
            By.CSS_SELECTOR,
            "tbody tr"
        )

        for row in rows:
            cells = row.find_elements(
                By.TAG_NAME,
                "td"
            )

            if len(cells) < 9:
                continue

            if cells[0].text.strip() == str(schedule_id):
                edit_button = cells[8].find_element(
                    By.XPATH,
                    ".//button[normalize-space()='Sửa']"
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    edit_button
                )

                # Tránh footer che nút
                self.driver.execute_script(
                    "arguments[0].click();",
                    edit_button
                )

                self.wait.until(
                    EC.visibility_of_element_located(
                        self.UPDATE_FORM_TITLE
                    )
                )

                return True

        return False

    def click_cancel_edit_button(self):
        button = self.wait.until(
            EC.element_to_be_clickable(
                self.CANCEL_EDIT_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        self.wait.until(
            EC.visibility_of_element_located(
                self.FORM_TITLE
            )
        )

    def click_delete_schedule_by_id(self, schedule_id):
        table = self.wait.until(
            EC.visibility_of_element_located(
                self.SCHEDULE_LIST_TABLE
            )
        )

        rows = table.find_elements(
            By.CSS_SELECTOR,
            "tbody tr"
        )

        for row in rows:
            cells = row.find_elements(
                By.TAG_NAME,
                "td"
            )

            if len(cells) < 9:
                continue

            if cells[0].text.strip() == str(schedule_id):
                delete_button = cells[8].find_element(
                    By.XPATH,
                    ".//button[normalize-space()='Xóa']"
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    delete_button
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    delete_button
                )

                return True

        return False