import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.LoginPage import LoginPage
from pages.BookingPage import BookingPage
from pages.MyAppointmentPage import MyAppointmentPage
from pages.AdminAppointmentPage import AdminAppointmentPage
from api.AppointmentApi import AppointmentApi
from api.MedicalRecordApi import MedicalRecordApi
from pages.DoctorAppointmentPage import DoctorAppointmentPage
from pages.DoctorExaminationPage import DoctorExaminationPage

PATIENT_USERNAME = "patient_trinh"
PATIENT_PASSWORD = "Abc@123"
ADMIN_USERNAME = "admin_system"
ADMIN_PASSWORD = "Abc@123"
DOCTOR_USERNAME = "doctor_thinh"
DOCTOR_PASSWORD = "Abc@123"
PATIENT_B_USERNAME = "patient_thu"
PATIENT_B_PASSWORD = "Abc@123"
DOCTOR_ID = 4

HOME_URL = "http://localhost:3000/"


def login_patient(driver):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        PATIENT_USERNAME,
        PATIENT_PASSWORD
    )

    WebDriverWait(driver, 10).until(
        EC.url_to_be(HOME_URL)
    )

    assert driver.current_url == HOME_URL

def login_admin(driver):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )

    WebDriverWait(driver, 10).until(
        EC.url_to_be(HOME_URL)
    )

    assert driver.current_url == HOME_URL

def login_doctor(driver):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        DOCTOR_USERNAME,
        DOCTOR_PASSWORD
    )
    WebDriverWait(driver, 10).until(
        EC.url_to_be(HOME_URL)
    )
    assert driver.current_url == HOME_URL

def logout_current_user(driver):
    login_page = LoginPage(driver)

    login_page.logout()

    WebDriverWait(driver, 10).until(
        EC.url_contains("/login")
    )
def login_patient_b(driver):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        PATIENT_B_USERNAME,
        PATIENT_B_PASSWORD
    )

    WebDriverWait(driver, 10).until(
        EC.url_to_be(HOME_URL)
    )

    assert driver.current_url == HOME_URL

def test_patient_sees_new_pending_appointment(driver):
    """
    TC-MYAPPOINTMENT-001:
    Patient đặt lịch thành công và thấy lịch mới
    trong Lịch hẹn của tôi với trạng thái
    Chờ xác nhận.
    """

    appointment_api = AppointmentApi()
    medical_record_api = MedicalRecordApi()

    booking_slot = (
        medical_record_api
        .find_available_booking_slot(DOCTOR_ID)
    )

    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    note = (
        "TC-MYAPPOINTMENT-001-"
    )

    login_patient(driver)

    booking_page = BookingPage(driver)

    try:
        booking_page.open_page_by_doctor(
            DOCTOR_ID
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

        message = booking_page.get_message()

        assert "Đặt lịch thành công" in message

        my_appointment_page = MyAppointmentPage(
            driver
        )

        my_appointment_page.open_page()

        appointment = (
            my_appointment_page
            .wait_for_appointment_by_note(note)
        )

        appointment = (
            my_appointment_page
            .get_appointment_by_note(note)
        )

        assert appointment is not None

        assert appointment["doctor"] == "Vu Thinh"

        assert booking_date in appointment["time"]
        assert booking_time in appointment["time"]

        assert (
            appointment["status"]
            == "Chờ xác nhận"
        )

        assert appointment["note"] == note
    finally:
        try:
            created_appointment = (

                appointment_api.find_appointment_by_note(

                    DOCTOR_ID,

                    note

                )
            )
            appointment_api.cancel_appointment(

                created_appointment["appointmentId"]
            )
        except AssertionError:

            pass

def test_patient_sees_cancelled_appointment_after_admin_cancel(driver):
    """
    TC-MYAPPOINTMENT-002:
    Sau khi Admin hủy lịch,
    Patient thấy trạng thái Đã hủy.
    """

    appointment_api = AppointmentApi()
    medical_record_api = MedicalRecordApi()

    booking_slot = (
        medical_record_api
        .find_available_booking_slot(DOCTOR_ID)
    )

    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    note = (
        "TC-MYAPPOINTMENT-002-"
    )

    appointment = (
        medical_record_api.create_appointment(
            patient_id=6,
            doctor_id=DOCTOR_ID,
            booking_date=booking_date,
            booking_time=booking_time,
            notes=note
        )
    )

    appointment_id = appointment["appointmentId"]

    # Patient kiểm tra lịch đang chờ xác nhận
    login_patient(driver)

    my_page = MyAppointmentPage(driver)
    my_page.open_page()

    patient_appointment = (
        my_page.wait_for_appointment_by_note(note)
    )

    assert (
        patient_appointment["status"]
        == "Chờ xác nhận"
    )

    logout_current_user(driver)

    # Admin hủy lịch
    login_admin(driver)

    admin_page = AdminAppointmentPage(driver)
    admin_page.open_page()

    assert (
        admin_page.get_status_by_note(note)
        == "Chờ xác nhận"
    )

    assert (
        admin_page.is_cancel_button_present(note)
    )

    admin_page.click_cancel(note)

    assert (
        admin_page.get_cancel_success_message()
        == "Hủy lịch hẹn thành công."
    )

    logout_current_user(driver)

    # Patient đăng nhập lại
    login_patient(driver)

    my_page = MyAppointmentPage(driver)
    my_page.open_page()

    cancelled_appointment = (
        my_page.wait_for_appointment_by_note(note)
    )

    assert (
        cancelled_appointment["status"]
        == "Đã hủy"
    )

def test_patient_sees_confirmed_appointment_after_admin_confirm(driver):
    """
    TC-MYAPPOINTMENT-003:
    Sau khi Admin xác nhận lịch,
    Patient thấy trạng thái Đã xác nhận.
    """

    appointment_api = AppointmentApi()
    medical_record_api = MedicalRecordApi()

    booking_slot = (
        medical_record_api
        .find_available_booking_slot(DOCTOR_ID)
    )

    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    note = (
        "TC-MYAPPOINTMENT-003-"
    )

    appointment = (
        medical_record_api.create_appointment(
            patient_id=6,
            doctor_id=DOCTOR_ID,
            booking_date=booking_date,
            booking_time=booking_time,
            notes=note
        )
    )

    appointment_id = appointment["appointmentId"]

    try:
        # Patient thấy lịch đang chờ
        login_patient(driver)

        my_page = MyAppointmentPage(driver)
        my_page.open_page()

        pending_appointment = (
            my_page.wait_for_appointment_by_note(note)
        )

        assert (
            pending_appointment["status"]
            == "Chờ xác nhận"
        )

        logout_current_user(driver)

        # Admin xác nhận
        login_admin(driver)

        admin_page = AdminAppointmentPage(driver)
        admin_page.open_page()

        assert (
            admin_page.get_status_by_note(note)
            == "Chờ xác nhận"
        )

        assert (
            admin_page.is_confirm_button_present(note)
        )

        admin_page.click_confirm(note)

        assert (
            admin_page.get_confirm_success_message()
            == "Xác nhận lịch hẹn thành công."
        )

        logout_current_user(driver)

        # Patient thấy trạng thái mới
        login_patient(driver)

        my_page = MyAppointmentPage(driver)
        my_page.open_page()

        confirmed_appointment = (
            my_page.wait_for_appointment_by_note(note)
        )

        assert (
            confirmed_appointment["status"]
            == "Đã xác nhận"
        )

    finally:
        appointment_api.cancel_appointment(
            appointment_id
        )

def test_patient_sees_completed_appointment_after_examination(driver):
    """
    TC-MYAPPOINTMENT-004:
    Patient đặt lịch, Admin xác nhận,
    Doctor khám bệnh và Patient thấy
    trạng thái Đã hoàn thành.
    """

    medical_record_api = MedicalRecordApi()
    appointment_api = AppointmentApi()

    booking_slot = (
        medical_record_api
        .find_available_booking_slot(DOCTOR_ID)
    )

    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    note = ("TC-MYAPPOINTMENT-004-")

    login_patient(driver)

    booking_page = BookingPage(driver)

    booking_page.open_page_by_doctor(
        DOCTOR_ID
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

    assert (
        "Đặt lịch thành công"
        in booking_page.get_message()
    )

    my_page = MyAppointmentPage(driver)
    my_page.open_page()

    created_appointment = (
        my_page.wait_for_appointment_by_note(
            note
        )
    )

    assert (
        created_appointment["status"]
        == "Chờ xác nhận"
    )

    original_id = (
        created_appointment["id"]
    )

    original_doctor = (
        created_appointment["doctor"]
    )

    original_time = (
        created_appointment["time"]
    )

    original_note = (
        created_appointment["note"]
    )
    logout_current_user(driver)

    # Admin xác nhận lịch
    login_admin(driver)

    admin_page = AdminAppointmentPage(driver)
    admin_page.open_page()

    assert (
        admin_page.get_status_by_note(note)
        == "Chờ xác nhận"
    )

    assert (
        admin_page.is_confirm_button_present(note)
    )

    admin_page.click_confirm(note)

    assert (
        admin_page.get_confirm_success_message()
        == "Xác nhận lịch hẹn thành công."
    )

    # Mở lại để kiểm tra trạng thái mới
    admin_page.open_page()

    assert (
        admin_page.get_status_by_note(note)
        == "Đã xác nhận"
    )
    logout_current_user(driver)

    # Doctor khám bệnh
    login_doctor(driver)

    doctor_page = DoctorAppointmentPage(driver)
    doctor_page.open_page()

    assert (
        doctor_page.get_status_by_id(
            original_id
        )
        == "Đã xác nhận"
    )

    assert (
        doctor_page.is_examine_button_present(
            original_id
        )
    )

    doctor_page.click_examine(
        original_id
    )

    examination_page = DoctorExaminationPage(
        driver
    )

    assert (
        examination_page.get_page_title()
        == "Khám bệnh"
    )

    assert (
        f"appointmentId={original_id}"
        in driver.current_url
    )

    diagnosis = (
        "Chẩn đoán TC-MYAPPOINTMENT-004 "
        + str(int(time.time()))
    )

    treatment = (
        "Hướng điều trị TC-MYAPPOINTMENT-004"
    )

    examination_page.enter_diagnosis(
        diagnosis
    )

    examination_page.enter_treatment(
        treatment
    )

    examination_page.click_save_medical_record()

    logout_current_user(driver)

    # Patient kiểm tra lịch đã hoàn thành
    login_patient(driver)

    my_page = MyAppointmentPage(driver)
    my_page.open_page()

    completed_appointment = (
        my_page.wait_for_appointment_by_note(
            note
        )
    )

    assert (
        completed_appointment["status"]
        == "Đã hoàn thành"
    )

    assert (
        completed_appointment["id"]
        == original_id
    )

    assert (
        completed_appointment["doctor"]
        == original_doctor
    )

    assert (
        completed_appointment["time"]
        == original_time
    )

    assert (
        completed_appointment["note"]
        == original_note
    )

def test_cancelled_slot_can_be_booked_by_another_patient(driver):
    """
    TC-MYAPPOINTMENT-005:
    Sau khi lịch bị hủy,
    bệnh nhân khác có thể đặt lại
    đúng khung giờ đó.
    """

    medical_record_api = MedicalRecordApi()

    booking_slot = (
        medical_record_api
        .find_available_booking_slot(DOCTOR_ID)
    )

    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    note_a = (
            "TC-MYAPPOINTMENT-005-A-"
            + str(int(time.time()))
    )

    # Patient A đặt lịch
    login_patient(driver)

    booking_page = BookingPage(driver)

    booking_page.open_page_by_doctor(
        DOCTOR_ID
    )

    booking_page.enter_date(
        booking_date
    )

    booking_page.enter_time(
        booking_time
    )

    booking_page.enter_notes(
        note_a
    )

    booking_page.click_booking_button()

    assert (
        "Đặt lịch thành công"
        in booking_page.get_message()
    )

    my_page = MyAppointmentPage(driver)
    my_page.open_page()

    appointment_a = (
        my_page.wait_for_appointment_by_note(
            note_a
        )
    )

    assert (
        appointment_a["status"]
        == "Chờ xác nhận"
    )

    appointment_a_id = (
        appointment_a["id"]
    )
    logout_current_user(driver)

    # Admin hủy lịch của Patient A
    login_admin(driver)

    admin_page = AdminAppointmentPage(driver)
    admin_page.open_page()

    assert (
        admin_page.get_status_by_note(note_a)
        == "Chờ xác nhận"
    )

    assert (
        admin_page.is_cancel_button_present(note_a)
    )

    admin_page.click_cancel(note_a)

    assert (
            admin_page.get_cancel_success_message()
            == "Hủy lịch hẹn thành công."
    )

    # Kiểm tra lịch A đã bị hủy ngay trên trang Admin
    admin_page.open_page()

    assert (
            admin_page.get_status_by_note(note_a)
            == "Đã hủy"
    )

    logout_current_user(driver)

    # Patient B đặt lại đúng slot vừa được hủy
    login_patient_b(driver)

    note_b = (
            "TC-MYAPPOINTMENT-005-B-"
            + str(int(time.time()))
    )

    booking_page = BookingPage(driver)

    booking_page.open_page_by_doctor(
        DOCTOR_ID
    )

    booking_page.enter_date(
        booking_date
    )

    booking_page.enter_time(
        booking_time
    )

    booking_page.enter_notes(
        note_b
    )

    booking_page.click_booking_button()

    assert (
        "Đặt lịch thành công"
        in booking_page.get_message()
    )

    # Patient B kiểm tra lịch mới
    my_page = MyAppointmentPage(driver)
    my_page.open_page()

    appointment_b = (
        my_page.wait_for_appointment_by_note(
            note_b
        )
    )

    assert appointment_b is not None

    assert (
        appointment_b["status"]
        == "Chờ xác nhận"
    )

    assert (
        appointment_b["doctor"]
        == "Vu Thinh"
    )

    assert (
        booking_date
        in appointment_b["time"]
    )

    assert (
        booking_time
        in appointment_b["time"]
    )

    assert (
        appointment_b["id"]
        != appointment_a_id
    )