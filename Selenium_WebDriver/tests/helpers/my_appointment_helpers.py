import time

from datetime import datetime, timedelta

from selenium.webdriver.support.ui import WebDriverWait

from pages.LoginPage import LoginPage
from pages.BookingPage import BookingPage

from api.AppointmentApi import AppointmentApi
from api.MedicalRecordApi import MedicalRecordApi
from api.DoctorScheduleApi import DoctorScheduleApi


HOME_URL = "http://localhost:3000/"
LOGIN_URL = "http://localhost:3000/login"


# ============================================================
# LOGIN
# ============================================================

def login_account(
        driver,
        username,
        password):

    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        username,
        password
    )

    WebDriverWait(
        driver,
        10
    ).until(
        lambda d:
        d.current_url == HOME_URL
    )

    assert driver.current_url == HOME_URL, (
        "LOGIN FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual URL: {driver.current_url}"
    )


def logout_current_user(driver):

    login_page = LoginPage(driver)

    login_page.logout()

    WebDriverWait(
        driver,
        10
    ).until(
        lambda d:
        "/login" in d.current_url
    )

    assert "/login" in driver.current_url, (
        "LOGOUT FAILED | "
        "Expected URL chứa /login | "
        f"Actual URL: {driver.current_url}"
    )


# ============================================================
# TEST DATA
# ============================================================

def create_unique_note(
        test_data,
        suffix=""):

    timestamp = str(
        int(time.time() * 1000)
    )

    if suffix:
        return (
            test_data["note_prefix"]
            + suffix
            + "-"
            + timestamp
        )

    return (
        test_data["note_prefix"]
        + timestamp
    )


# ============================================================
# BOOKING SLOT
# ============================================================

def get_or_create_booking_slot(
        test_data):

    doctor_id = int(
        test_data["doctor_id"]
    )

    doctor_name = (
        test_data["doctor_name"]
    )

    medical_record_api = (
        MedicalRecordApi()
    )

    try:
        return (
            medical_record_api
            .find_available_booking_slot(
                doctor_id
            )
        )

    except AssertionError:

        doctor_schedule_api = (
            DoctorScheduleApi()
        )

        admin_token = (
            doctor_schedule_api
            .get_token(
                test_data[
                    "admin_username"
                ],
                test_data[
                    "admin_password"
                ]
            )
        )

        created_work_date = None

        for days_ahead in range(
                1,
                31):

            work_date = (
                datetime.now().date()
                + timedelta(
                    days=days_ahead
                )
            ).strftime(
                "%Y-%m-%d"
            )

            existing_schedule = (
                doctor_schedule_api
                .find_schedule(
                    doctor_name=doctor_name,
                    work_date=work_date,
                    shift="morning"
                )
            )

            if existing_schedule is None:

                doctor_schedule_api.create_schedule(
                    doctor_name=doctor_name,
                    work_date=work_date,
                    shift="morning",
                    start_time="07:00:00",
                    end_time="11:30:00",
                    status="available",
                    note=(
                        test_data[
                            "note_prefix"
                        ]
                        + "SCHEDULE"
                    ),
                    token=admin_token
                )

                created_work_date = (
                    work_date
                )

                break

        assert (
            created_work_date
            is not None
        ), (
            "Không thể tạo schedule "
            "phục vụ MyAppointment test."
        )

        return (
            medical_record_api
            .find_available_booking_slot(
                doctor_id
            )
        )


# ============================================================
# BOOK APPOINTMENT BY UI
# ============================================================

def book_appointment_by_ui(
        driver,
        test_data,
        booking_date,
        booking_time,
        note):

    doctor_id = int(
        test_data["doctor_id"]
    )

    booking_page = (
        BookingPage(driver)
    )

    booking_page.open_page_by_doctor(
        doctor_id
    )

    booking_page.enter_date(
        booking_date
    )

    booking_page.enter_time(
        booking_time
    )

    booking_page.enter_notes(
        note
    )

    booking_page.click_booking_button()

    return (
        booking_page.get_message()
    )


# ============================================================
# CLEANUP
# ============================================================

def cleanup_appointment(
        test_data,
        note):

    appointment_api = (
        AppointmentApi()
    )

    doctor_id = int(
        test_data["doctor_id"]
    )

    try:
        appointment = (
            appointment_api
            .find_appointment_by_note(
                doctor_id=doctor_id,
                note=note
            )
        )

    except AssertionError:
        return

    status = str(
        appointment.get(
            "status",
            ""
        )
    ).lower()

    if status in (
        "cancelled",
        "completed"
    ):
        return

    appointment_api.cancel_appointment(
        appointment[
            "appointmentId"
        ]
    )