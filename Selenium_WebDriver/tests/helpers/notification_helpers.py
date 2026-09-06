import time
from datetime import datetime, timedelta

from selenium.webdriver.support.ui import WebDriverWait

from api.AppointmentApi import AppointmentApi
from api.DoctorScheduleApi import DoctorScheduleApi
from api.MedicalRecordApi import MedicalRecordApi

from pages.AdminAppointmentPage import AdminAppointmentPage
from pages.BookingPage import BookingPage
from pages.DoctorPage import DoctorPage
from pages.LoginPage import LoginPage
from pages.NotificationPage import NotificationPage
from pages.DoctorAppointmentPage import DoctorAppointmentPage
from pages.DoctorExaminationPage import DoctorExaminationPage
from pages.MedicalRecordPage import MedicalRecordPage

HOME_URL = "http://localhost:3000/"
LOGIN_URL = "http://localhost:3000/login"


def login_account(driver, username, password):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login(username, password)

    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == HOME_URL
    )

    assert driver.current_url == HOME_URL, (
        "LOGIN FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual URL: {driver.current_url}"
    )


def logout_current_user(driver):
    login_page = LoginPage(driver)
    login_page.logout()

    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == LOGIN_URL
    )

    assert driver.current_url == LOGIN_URL, (
        "LOGOUT FAILED | "
        f"Expected URL: {LOGIN_URL} | "
        f"Actual URL: {driver.current_url}"
    )


def switch_account(driver, username, password):
    logout_current_user(driver)
    login_account(driver, username, password)


def get_or_create_booking_slot(
        doctor_id,
        test_data,
        schedule_note):

    medical_record_api = MedicalRecordApi()

    try:
        return medical_record_api.find_available_booking_slot(
            doctor_id
        )

    except AssertionError:
        doctor_schedule_api = DoctorScheduleApi()

        admin_token = doctor_schedule_api.get_token(
            test_data["admin_username"],
            test_data["admin_password"]
        )

        created_work_date = None

        for days_ahead in range(1, 31):
            work_date = (
                datetime.now().date()
                + timedelta(days=days_ahead)
            ).strftime("%Y-%m-%d")

            existing_schedule = doctor_schedule_api.find_schedule(
                doctor_name="Tran Binh",
                work_date=work_date,
                shift="morning"
            )

            if existing_schedule is not None:
                continue

            doctor_schedule_api.create_schedule(
                doctor_name="Tran Binh",
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


def create_pending_appointment(
        driver,
        test_data,
        test_case_id):

    doctor_id = int(test_data["doctor_id"])

    booking_slot = get_or_create_booking_slot(
        doctor_id=doctor_id,
        test_data=test_data,
        schedule_note=f"SELENIUM-{test_case_id}"
    )

    note = (
        test_data["note_prefix"]
        + str(int(time.time()))
    )

    doctor_page = DoctorPage(driver)
    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage(driver)
    booking_page.enter_date(
        booking_slot["booking_date"]
    )
    booking_page.enter_time(
        booking_slot["booking_time"]
    )

    actual_booking_time = booking_page.get_time_value()

    booking_page.enter_notes(note)
    booking_page.click_booking_button()

    booking_message = booking_page.get_message()

    appointment = AppointmentApi().find_appointment_by_note(
        doctor_id=doctor_id,
        note=note
    )

    return {
        "appointment_id": appointment["appointmentId"],
        "status": appointment.get("status"),
        "note": note,
        "booking_message": booking_message,
        "expected_time": booking_slot["booking_time"],
        "actual_time": actual_booking_time,
    }


def confirm_appointment(driver, note):
    admin_page = AdminAppointmentPage(driver)
    admin_page.open_page()

    status_before = admin_page.get_status_by_note(note)

    admin_page.click_confirm(note)

    success_message = (
        admin_page.get_confirm_success_message()
    )

    status_after = admin_page.wait_for_status_by_note(
        note,
        "Đã xác nhận"
    )

    return {
        "page_title": admin_page.get_page_title(),
        "status_before": status_before,
        "status_after": status_after,
        "success_message": success_message,
    }


def cancel_appointment(driver, note):
    admin_page = AdminAppointmentPage(driver)
    admin_page.open_page()

    status_before = admin_page.get_status_by_note(note)

    admin_page.click_cancel(note)

    success_message = (
        admin_page.get_cancel_success_message()
    )

    admin_page.open_page()

    status_after = admin_page.get_status_by_note(note)

    return {
        "page_title": admin_page.get_page_title(),
        "status_before": status_before,
        "status_after": status_after,
        "success_message": success_message,
    }


def open_notification_page(driver):
    notification_page = NotificationPage(driver)
    notification_page.open_page()

    return notification_page


def get_notification_data(
        notification_page,
        appointment_id):

    notification = (
        notification_page
        .get_notification_by_appointment_id(
            appointment_id
        )
    )

    if notification is None:
        return {
            "element": None,
            "type": "",
            "content": "",
            "time": "",
        }

    return {
        "element": notification,
        "type": notification_page.get_notification_type(
            notification
        ),
        "content": notification_page.get_notification_content(
            notification
        ),
        "time": notification_page.get_notification_time(
            notification
        ),
    }

def create_completed_medical_record(
        driver,
        test_data,
        test_case_id):

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    booking = create_pending_appointment(
        driver,
        test_data,
        test_case_id
    )

    appointment_id = booking["appointment_id"]
    note = booking["note"]

    switch_account(
        driver,
        test_data["admin_username"],
        test_data["admin_password"]
    )

    confirm_result = confirm_appointment(
        driver,
        note
    )

    switch_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    appointment_page = DoctorAppointmentPage(driver)
    appointment_page.open_page()

    actual_note = appointment_page.get_note_by_id(
        appointment_id
    )

    doctor_status = appointment_page.get_status_by_id(
        appointment_id
    )

    appointment_page.click_examine(
        appointment_id
    )

    examination_page = DoctorExaminationPage(driver)

    unique_value = str(int(time.time()))

    diagnosis = (
        test_data["diagnosis_prefix"]
        + unique_value
    )

    treatment = (
        test_data["treatment_prefix"]
        + unique_value
    )

    examination_page.enter_diagnosis(
        diagnosis
    )

    examination_page.enter_treatment(
        treatment
    )

    examination_page.click_save_medical_record()

    medical_record_page = MedicalRecordPage(driver)

    return {
        "appointment_id": appointment_id,
        "note": note,
        "booking_status": booking["status"],
        "confirm_status": confirm_result["status_after"],
        "doctor_status": doctor_status,
        "actual_note": actual_note,
        "record_page_title": medical_record_page.get_page_title(),
        "diagnosis": diagnosis,
        "treatment": treatment,
        "actual_diagnosis": (
            medical_record_page.get_diagnosis_information()
        ),
        "actual_treatment": (
            medical_record_page.get_treatment_information()
        ),
        "medical_record_page": medical_record_page,
        "unique_value": unique_value,
    }