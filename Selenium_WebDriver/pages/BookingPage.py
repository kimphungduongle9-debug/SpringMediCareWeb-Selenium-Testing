from selenium.webdriver.common.by import By

from pages.BasePage import BasePage

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

class BookingPage(BasePage):
    """
    Page Object cho chức năng Đặt lịch khám của Patient.

    Mapping Test Case -> Step -> Method:

    TC-BOOKING-001
    - Step 3: Kiểm tra các trường trên form Đặt lịch
      + find() với DATE_INPUT, TIME_INPUT, NOTES_INPUT, BOOKING_BUTTON
    - Step 4: Chọn ngày và giờ khám hợp lệ
      + enter_date()
      + enter_time()
      + get_time_value()
    - Step 5: Nhập ghi chú và thực hiện đặt lịch
      + enter_notes()
      + click_booking_button()
    - Step 6: Kiểm tra thông báo kết quả
      + get_message()

    TC-BOOKING-002
    - Step 3: Kiểm tra trường Ngày khám đang để trống
      + find() với DATE_INPUT
    - Step 4: Kiểm tra validation khi chưa chọn ngày
      + get_warning_message()
    - Step 5-6: Kiểm tra không cho phép đặt lịch
      + is_booking_button_disabled()
      + get_warning_message()

    TC-BOOKING-003
    - Step 3: Chọn ngày bác sĩ có lịch làm việc
      + enter_date()
    - Step 4: Kiểm tra trường Giờ khám đang để trống
      + get_time_value()
    - Step 5-6: Kiểm tra không cho phép đặt lịch khi thiếu giờ
      + is_booking_button_disabled()
      + get_time_warning_message()

    TC-BOOKING-004
    - Step 3: Chọn ngày và giờ hợp lệ
      + enter_date()
      + enter_time()
      + get_time_value()
    - Step 4: Kiểm tra Ghi chú đang để trống
      + find() với NOTES_INPUT
    - Step 5: Thực hiện đặt lịch
      + click_booking_button()
    - Step 6: Kiểm tra kết quả đặt lịch
      + get_message()

    TC-BOOKING-005
    - Step 3: Chọn ngày bác sĩ không có lịch làm việc
      + enter_date()
    - Step 4: Kiểm tra thông báo không có lịch làm việc
      + get_no_schedule_message()
    - Step 5-6: Kiểm tra không cho phép đặt lịch
      + is_booking_button_disabled()
      + get_no_schedule_message()

    TC-BOOKING-006
    - Step 3: Chọn ngày bác sĩ có lịch làm việc
      + enter_date()
    - Step 4: Nhập giờ ngoài ca làm việc
      + enter_time()
      + get_time_value()
    - Step 5: Thực hiện đặt lịch
      + click_booking_button()
    - Step 6: Kiểm tra hệ thống từ chối
      + get_message()

    TC-BOOKING-007
    - Step 4: Chọn ngày và giờ đã có lịch hẹn
      + enter_date()
      + enter_time()
      + get_time_value()
    - Step 5: Thực hiện đặt lịch
      + click_booking_button()
    - Step 6: Kiểm tra hệ thống từ chối lịch trùng
      + get_message()

    TC-BOOKING-008
    - Step 4: Chọn thời gian cách lịch hiện có dưới 30 phút
      + enter_date()
      + enter_time()
      + get_time_value()
    - Step 5: Thực hiện đặt lịch
      + click_booking_button()
    - Step 6: Kiểm tra hệ thống từ chối
      + get_message()
    """

    URL = "http://localhost:3000/booking?doctorId=1"

    DATE_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='Chọn ngày khám']"
    )

    TIME_INPUT = (
        By.CSS_SELECTOR,
        "input[type='time']"
    )

    NOTES_INPUT = (
        By.CSS_SELECTOR,
        "textarea[placeholder='Nhập triệu chứng hoặc yêu cầu nếu có...']"
    )

    BOOKING_BUTTON = (
        By.XPATH,
        "//button[@type='submit' and normalize-space()='Đặt lịch']"
    )

    WARNING_MESSAGE = (
        By.CSS_SELECTOR,
        "div[role='alert'].alert-warning"
    )

    MESSAGE = (
        By.CSS_SELECTOR,
        "div.alert.alert-info"
    )

    NO_SCHEDULE_MESSAGE = (
        By.XPATH,
        "//p[contains(@class, 'text-warning') "
        "and normalize-space()='Bác sĩ không có lịch làm việc trong ngày này.']"
    )

    BOOKED_TIME_ITEMS = (
        By.CSS_SELECTOR,
        "span.badge.bg-danger"
    )
    def open_page(self):
        self.open(self.URL)

    def get_warning_message(self):
        element = self.wait.until(
            EC.visibility_of_element_located(
                self.WARNING_MESSAGE
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

        return element.text

    def is_booking_button_disabled(self):
        button = self.find(
            *self.BOOKING_BUTTON
        )

        return button.get_attribute("disabled") is not None

    def enter_date(self, date):
        date_input = self.find(
            *self.DATE_INPUT
        )

        date_input.click()

        date_input.send_keys(
            Keys.CONTROL,
            "a"
        )

        date_input.send_keys(date)

        date_input.send_keys(Keys.ENTER)

    def get_time_warning_message(self):
        element = self.wait.until(
            EC.visibility_of_element_located(
                self.WARNING_MESSAGE
            )
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

        return element.text

    def enter_time(self, booking_time):
        time_input = self.find(
            *self.TIME_INPUT
        )

        self.driver.execute_script(
            """
            const input = arguments[0];
            const value = arguments[1];

            const setter = Object.getOwnPropertyDescriptor(
                HTMLInputElement.prototype,
                'value'
            ).set;

            setter.call(input, value);

            input.dispatchEvent(
                new Event('input', {bubbles: true})
            );

            input.dispatchEvent(
                new Event('change', {bubbles: true})
            );
            """,
            time_input,
            booking_time
        )

    def enter_notes(self, notes):
        self.typing(
            *self.NOTES_INPUT,
            notes
        )

    def click_booking_button(self):
        self.click(
            *self.BOOKING_BUTTON
        )

    def get_time_value(self):
        return self.find(
            *self.TIME_INPUT
        ).get_attribute("value")

    def get_message(self):
        message = self.find(
            *self.MESSAGE
        )

        self.driver.execute_script(
            "window.scrollTo(0, 0);"
        )

        return message.text

    def get_no_schedule_message(self):
        element = self.find(
            *self.NO_SCHEDULE_MESSAGE
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

        return element.text

    def get_first_booked_time(self):
        booked_slots = self.finds(*self.BOOKED_TIME_ITEMS)

        assert len(booked_slots) > 0, (
            "Ngày đã chọn chưa có lịch hẹn nào để kiểm tra trùng giờ."
        )

        booked_time = booked_slots[0].text.strip()

        return booked_time

    def get_time_one_minute_after_first_booked_time(self):
        booked_time = self.get_first_booked_time()

        hour, minute = map(int, booked_time.split(":"))

        total_minutes = hour * 60 + minute + 1

        new_hour = total_minutes // 60
        new_minute = total_minutes % 60

        return f"{new_hour:02d}:{new_minute:02d}"

    def open_page_by_doctor(self, doctor_id):
        self.open(
            f"http://localhost:3000/booking?doctorId={doctor_id}"
        )


