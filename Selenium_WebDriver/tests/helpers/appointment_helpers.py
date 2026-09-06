import time

from pages.LoginPage import LoginPage
from pages.DoctorPage import DoctorPage
from pages.BookingPage import BookingPage
from datetime import datetime, timedelta

from api.MedicalRecordApi import MedicalRecordApi
from api.DoctorScheduleApi import DoctorScheduleApi

HOME_URL = "http://localhost:3000/"
LOGIN_URL = "http://localhost:3000/login"

BOOKING_URL = (
    "http://localhost:3000/"
    "booking?doctorId=1"
)

ADMIN_USERNAME = "admin_system"
ADMIN_PASSWORD = "Abc@123"

DOCTOR_USERNAME = "doctor_minh"
DOCTOR_PASSWORD = "Abc@123"

OTHER_DOCTOR_USERNAME = "doctor_binh"
OTHER_DOCTOR_PASSWORD = "Abc@123"

PATIENT_USERNAME = "patient_an"
PATIENT_PASSWORD = "Abc@123"


def login_account(driver, username, password):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login(username, password)

    time.sleep(2)

    assert driver.current_url == HOME_URL, (
        f"Đăng nhập thất bại | "
        f"Actual URL: {driver.current_url}"
    )


def login_admin(driver):
    login_account(
        driver,
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )


def login_doctor(driver):
    login_account(
        driver,
        DOCTOR_USERNAME,
        DOCTOR_PASSWORD
    )


def login_other_doctor(driver):
    login_account(
        driver,
        OTHER_DOCTOR_USERNAME,
        OTHER_DOCTOR_PASSWORD
    )


def login_patient(driver):
    login_account(
        driver,
        PATIENT_USERNAME,
        PATIENT_PASSWORD
    )


def logout_current_user(driver):
    login_page = LoginPage(driver)
    login_page.logout()

    time.sleep(2)

    assert driver.current_url == LOGIN_URL, (
        f"Đăng xuất thất bại | "
        f"Actual URL: {driver.current_url}"
    )


def open_tran_binh_booking_page(driver):
    doctor_page = DoctorPage(driver)
    doctor_page.open_page()

    time.sleep(2)

    doctor_page.book_tran_binh()

    assert driver.current_url == BOOKING_URL, (
        f"Không mở được trang Đặt lịch | "
        f"Actual URL: {driver.current_url}"
    )

    return BookingPage(driver)

def get_or_create_booking_slot(
    doctor_id,
    doctor_name,
    schedule_note
):
    """
    Tìm slot còn trống cho bác sĩ.
    Nếu không còn schedule tương lai thì tự tạo schedule test.
    """

    medical_record_api = MedicalRecordApi()

    try:
        return medical_record_api.find_available_booking_slot(
            doctor_id
        )

    except AssertionError:
        doctor_schedule_api = DoctorScheduleApi()

        admin_token = doctor_schedule_api.get_token(
            ADMIN_USERNAME,
            ADMIN_PASSWORD
        )

        created_work_date = None

        for days_ahead in range(1, 31):
            work_date = (
                datetime.now().date()
                + timedelta(days=days_ahead)
            ).strftime("%Y-%m-%d")

            existing_schedule = doctor_schedule_api.find_schedule(
                doctor_name=doctor_name,
                work_date=work_date,
                shift="morning"
            )

            if existing_schedule is None:
                doctor_schedule_api.create_schedule(
                    doctor_name=doctor_name,
                    work_date=work_date,
                    shift="morning",
                    start_time="07:00:00",
                    end_time="11:30:00",
                    status="available",
                    note=schedule_note,
                    token=admin_token
                )

                created_work_date = work_date
                break

        assert created_work_date is not None, (
            f"{schedule_note} | "
            "Không thể chuẩn bị lịch làm việc cho bác sĩ."
        )

        return medical_record_api.find_available_booking_slot(
            doctor_id
        )