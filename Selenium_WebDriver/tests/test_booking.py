from pages.LoginPage import LoginPage
from pages.BookingPage import BookingPage
from pages.DoctorPage import DoctorPage
from selenium.webdriver.common.by import By
import time


VALID_USERNAME = "patient_an"
VALID_PASSWORD = "Abc@123"

SECOND_USERNAME = "patient_chi"
SECOND_PASSWORD = "Abc@123"

BOOKING_URL = "http://localhost:3000/booking?doctorId=1"


def login_account(driver, username, password):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        username,
        password
    )

    time.sleep(2)

    assert driver.current_url == "http://localhost:3000/"


def login_patient(driver):
    login_account(
        driver,
        VALID_USERNAME,
        VALID_PASSWORD
    )


def login_second_patient(driver):
    login_account(
        driver,
        SECOND_USERNAME,
        SECOND_PASSWORD
    )

def open_tran_binh_booking_page(driver):
    doctor_page = DoctorPage(driver)

    doctor_page.open_page()

    time.sleep(2)

    doctor_page.book_tran_binh()

    assert driver.current_url == BOOKING_URL

    return BookingPage(driver)

def logout_patient(driver):
    login_page = LoginPage(driver)

    login_page.logout()

    time.sleep(2)

    assert driver.current_url == "http://localhost:3000/login"

def test_open_booking_page(driver):
    """
    Kiểm tra mở trang đặt lịch của bác sĩ Tran Binh.
    """

    login_patient(driver)

    booking_page = open_tran_binh_booking_page(driver)

    assert booking_page.find(
        *booking_page.DATE_INPUT
    ).is_displayed()

    assert booking_page.find(
        *booking_page.TIME_INPUT
    ).is_displayed()

    assert booking_page.find(
        *booking_page.NOTES_INPUT
    ).is_displayed()

    assert booking_page.find(
        *booking_page.BOOKING_BUTTON
    ).is_displayed()


def test_booking_success(driver):
    """
    TC-BOOKING-001:
    Đặt lịch thành công.
    """

    login_patient(driver)

    booking_page = open_tran_binh_booking_page(driver)

    booking_page.enter_date("11/04/2026")

    booking_page.enter_time("09:00")

    assert booking_page.get_time_value() == "09:00"

    booking_page.enter_notes(
        "Đau đầu và sốt nhẹ."
    )

    booking_page.click_booking_button()

    message = booking_page.get_message()

    assert "Đặt lịch thành công" in message


def test_booking_without_date(driver):
    """
    TC-BOOKING-002:
    Bỏ trống ngày khám.
    """

    login_patient(driver)

    booking_page = open_tran_binh_booking_page(driver)

    assert booking_page.get_warning_message() == (
        "Vui lòng chọn ngày khám để tiếp tục."
    )

    assert booking_page.is_booking_button_disabled()


def test_booking_without_time(driver):
    """
    TC-BOOKING-003:
    Bỏ trống giờ khám.
    """

    login_patient(driver)

    booking_page = open_tran_binh_booking_page(driver)

    booking_page.enter_date("11/04/2026")

    assert booking_page.get_time_warning_message() == (
        "Vui lòng chọn giờ khám để tiếp tục."
    )

    assert booking_page.is_booking_button_disabled()


def test_booking_without_notes(driver):
    """
    TC-BOOKING-004:
    Đặt lịch không nhập ghi chú.
    """

    login_patient(driver)

    booking_page = open_tran_binh_booking_page(driver)

    booking_page.enter_date("11/04/2026")

    booking_page.enter_time("09:30")

    assert booking_page.get_time_value() == "09:30"

    booking_page.click_booking_button()

    message = booking_page.get_message()

    assert "Đặt lịch thành công" in message

def test_booking_on_day_without_schedule(driver):
    """
    TC-BOOKING-005:
    Chọn ngày bác sĩ không có lịch làm việc.
    """

    login_patient(driver)

    booking_page = open_tran_binh_booking_page(driver)

    booking_page.enter_date("13/04/2026")

    time.sleep(2)

    assert booking_page.get_no_schedule_message() == (
        "Bác sĩ không có lịch làm việc trong ngày này."
    )

def test_booking_outside_working_hours(driver):
    """
    TC-BOOKING-006:
    Chọn giờ ngoài lịch làm việc của bác sĩ.
    """

    login_patient(driver)

    booking_page = open_tran_binh_booking_page(driver)

    booking_page.enter_date("11/04/2026")

    booking_page.enter_time("12:00")

    assert booking_page.get_time_value() == "12:00"

    booking_page.click_booking_button()

    message = booking_page.get_message()

    assert (
        "Giờ khám không nằm trong lịch làm việc của bác sĩ"
        in message
    )

def test_booking_duplicate_time(driver):
    """
    TC-BOOKING-007:
    Đặt lịch trùng đúng giờ đã có người đặt.
    """

    login_patient(driver)

    booking_page = open_tran_binh_booking_page(driver)

    booking_page.enter_date("11/04/2026")

    time.sleep(2)

    booked_time = booking_page.get_first_booked_time()

    booking_page.enter_time(booked_time)

    assert booking_page.get_time_value() == booked_time

    booking_page.click_booking_button()

    message = booking_page.get_message()

    assert "Khung giờ này đã có người đặt" in message

def test_booking_within_thirty_minutes(driver):
    """
    TC-BOOKING-008:
    Đặt lịch cách lịch đã có dưới 30 phút.
    """

    # patient_an đặt lịch lúc 15:30
    login_patient(driver)

    booking_page = open_tran_binh_booking_page(driver)

    booking_page.enter_date("11/04/2026")

    booking_page.enter_time("15:30")

    assert booking_page.get_time_value() == "15:30"

    booking_page.click_booking_button()

    message = booking_page.get_message()

    assert "Đặt lịch thành công" in message

    # Đăng xuất patient_an
    logout_patient(driver)

    # patient_chi đăng nhập và đặt lúc 15:31
    login_second_patient(driver)

    booking_page = open_tran_binh_booking_page(driver)

    booking_page.enter_date("11/04/2026")

    booking_page.enter_time("15:31")

    assert booking_page.get_time_value() == "15:31"

    booking_page.click_booking_button()

    message = booking_page.get_message()

    assert "30 phút" in message