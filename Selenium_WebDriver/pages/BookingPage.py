from selenium.webdriver.common.by import By

from pages.BasePage import BasePage

import time
from selenium.webdriver.common.keys import Keys


class BookingPage(BasePage):

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
        element = self.scroll_to_element(
            *self.WARNING_MESSAGE
        )

        time.sleep(2)

        return element.text

    def is_booking_button_disabled(self):
        button = self.find(
            *self.BOOKING_BUTTON
        )

        return button.get_attribute("disabled") is not None

    def enter_date(self, date, delay=1.5):
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

        time.sleep(delay)

    def get_time_warning_message(self):
        element = self.scroll_to_element(
            *self.WARNING_MESSAGE
        )

        time.sleep(2)

        return element.text

    def enter_time(self, booking_time, delay=1.5):
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

        time.sleep(delay)

    def enter_notes(self, notes, delay=1):
        self.typing(
            *self.NOTES_INPUT,
            notes
        )

        time.sleep(delay)

    def click_booking_button(self, delay=2):
        self.click(
            *self.BOOKING_BUTTON
        )

        time.sleep(delay)


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

        time.sleep(2)

        return message.text

    def get_no_schedule_message(self):
        element = self.find(
            *self.NO_SCHEDULE_MESSAGE
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

        time.sleep(1)

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


