import time
from pages.LoginPage import LoginPage
from pages.DoctorPage import DoctorPage
from pages.BookingPage import BookingPage
from pages.AdminAppointmentPage import AdminAppointmentPage
from pages.NotificationPage import NotificationPage
from datetime import datetime, timedelta
from api.AppointmentApi import AppointmentApi
from api.MedicalRecordApi import MedicalRecordApi
from pages.DoctorAppointmentPage import DoctorAppointmentPage
from pages.PrescriptionPage import PrescriptionPage
from api.DoctorScheduleApi import DoctorScheduleApi
from pages.TestResultPage import TestResultPage
import pytest
from utils.test_reporter import report_step
from utils.data_reader import (get_test_data_csv,NOTIFICATION_TEST_DATA_CSV)
from pages.DoctorExaminationPage import DoctorExaminationPage
from pages.MedicalRecordPage import MedicalRecordPage
from selenium.webdriver.support.ui import WebDriverWait
# ============================================================
# COMMON HELPERS
# Các thao tác dùng chung giữa nhiều bước của test case.
# ============================================================

def login_account(driver, username, password):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        username,
        password
    )

    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == "http://localhost:3000/"
    )

    assert driver.current_url == "http://localhost:3000/", (
        "LOGIN FAILED | "
        f"Expected: http://localhost:3000/ | "
        f"Actual: {driver.current_url}"
    )

def logout_current_user(driver):
    login_page = LoginPage(driver)

    login_page.logout()

    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == "http://localhost:3000/login"
    )

    assert driver.current_url == "http://localhost:3000/login", (
        "LOGOUT FAILED | "
        f"Expected: http://localhost:3000/login | "
        f"Actual: {driver.current_url}"
    )

def get_or_create_booking_slot(
        doctor_id,
        test_data,
        schedule_note
):
    """
    Tìm một slot đặt lịch còn trống.
    Nếu hết slot, tự tạo thêm một schedule test trong tương lai.
    """

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

        doctor_name = "Tran Binh"
        created_work_date = None

        for days_ahead in range(1, 31):
            work_date_obj = (
                datetime.now().date()
                + timedelta(days=days_ahead)
            )

            work_date = work_date_obj.strftime("%Y-%m-%d")

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
def test_tc_notification_001_patient_receives_notification_after_admin_confirms(
        driver):
    """
    TC-NOTIFICATION-001:
    Kiểm tra Patient nhận được thông báo đúng
    sau khi Admin xác nhận lịch hẹn mà Patient đã đặt.
    """

    test_case_id = "TC-NOTIFICATION-001"
    test_data = get_test_data_csv(
        NOTIFICATION_TEST_DATA_CSV,
        test_case_id
    )

    # ============================================================
    # Step 1: Patient đặt một lịch khám hợp lệ
    # ============================================================

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    doctor_id = int(test_data["doctor_id"])
    appointment_api = AppointmentApi()

    booking_slot = get_or_create_booking_slot(
        doctor_id=doctor_id,
        test_data=test_data,
        schedule_note="SELENIUM-TC-NOTIFICATION-001"
    )

    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    note = test_data["note_prefix"] + str(int(time.time()))

    doctor_page = DoctorPage(driver)
    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage(driver)
    booking_page.enter_date(booking_date)
    booking_page.enter_time(booking_time)

    actual_booking_time = booking_page.get_time_value()

    assert actual_booking_time == booking_time, (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected booking time: {booking_time} | "
        f"Actual: {actual_booking_time}"
    )

    booking_page.enter_notes(note)
    booking_page.click_booking_button()

    booking_message = booking_page.get_message()

    assert "Đặt lịch thành công" in booking_message, (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Không đặt được lịch. Actual message: {booking_message}"
    )

    appointment = appointment_api.find_appointment_by_note(
        doctor_id=doctor_id,
        note=note
    )

    appointment_id = appointment["appointmentId"]

    assert appointment.get("status") == "pending", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Appointment sau khi tạo không ở trạng thái pending. "
        f"Actual: {appointment.get('status')}"
    )

    report_step(
        test_case_id,
        1,
        f"Patient đặt lịch khám hợp lệ và appointment "
        f"#{appointment_id} ở trạng thái pending"
    )

    # ============================================================
    # Step 2: Đăng xuất Patient và đăng nhập Admin
    # ============================================================

    logout_current_user(driver)

    login_account(
        driver,
        test_data["admin_username"],
        test_data["admin_password"]
    )

    report_step(
        test_case_id,
        2,
        "Đăng xuất Patient và đăng nhập Admin thành công"
    )

    # ============================================================
    # Step 3: Admin xác nhận lịch vừa tạo
    # ============================================================

    admin_page = AdminAppointmentPage(driver)
    admin_page.open_page()

    assert admin_page.get_page_title() == "Quản lý lịch hẹn", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Không mở đúng trang Quản lý lịch hẹn."
    )

    assert admin_page.get_appointment_id_by_note(note) == str(appointment_id), (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Không tìm thấy appointment #{appointment_id} theo note."
    )

    assert admin_page.get_status_by_note(note) == "Chờ xác nhận", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Appointment không ở trạng thái Chờ xác nhận."
    )

    assert admin_page.is_confirm_button_present(note), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Không tìm thấy nút Xác nhận."
    )

    admin_page.click_confirm(note)

    confirm_message = admin_page.get_confirm_success_message()

    assert confirm_message == "Xác nhận lịch hẹn thành công.", (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Actual message: {confirm_message}"
    )

    admin_page.open_page()

    actual_status = admin_page.get_status_by_note(note)

    assert actual_status == "Đã xác nhận", (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: Đã xác nhận | Actual: {actual_status}"
    )

    report_step(
        test_case_id,
        3,
        f"Admin xác nhận appointment #{appointment_id} thành công"
    )

    # ============================================================
    # Step 4: Đăng xuất Admin và đăng nhập lại Patient
    # ============================================================

    logout_current_user(driver)

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    report_step(
        test_case_id,
        4,
        "Đăng xuất Admin và đăng nhập lại Patient thành công"
    )

    # ============================================================
    # Step 5: Patient mở trang Thông báo
    # ============================================================

    notification_page = NotificationPage(driver)
    notification_page.open_page()

    page_title = notification_page.get_page_title()

    assert page_title == "Thông báo của tôi", (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: Thông báo của tôi | Actual: {page_title}"
    )

    report_step(
        test_case_id,
        5,
        "Patient mở trang Thông báo thành công"
    )

    # ============================================================
    # Step 6: Tìm notification của lịch vừa được xác nhận
    # ============================================================

    notification = notification_page.get_notification_by_appointment_id(
        appointment_id
    )

    assert notification is not None, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Không tìm thấy notification của appointment #{appointment_id}"
    )

    report_step(
        test_case_id,
        6,
        f"Tìm thấy notification của appointment #{appointment_id}"
    )

    # ============================================================
    # Step 7: Kiểm tra loại, nội dung và thời gian notification
    # ============================================================

    notification_type = notification_page.get_notification_type(notification)
    notification_content = notification_page.get_notification_content(notification)
    notification_time = notification_page.get_notification_time(notification)

    assert notification_type == test_data["notification_type"], (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected notification type: {test_data['notification_type']} | "
        f"Actual: {notification_type}"
    )

    assert f"#{appointment_id}" in notification_content, (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Notification không chứa appointment #{appointment_id}. "
        f"Actual: {notification_content}"
    )

    assert test_data["expected_keyword"] in notification_content.lower(), (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected keyword: {test_data['expected_keyword']} | "
        f"Actual: {notification_content}"
    )

    assert notification_time.strip() != "", (
        f"{test_case_id} | STEP 7 FAILED | "
        "Notification không hiển thị thời gian."
    )

    try:
        datetime.strptime(
            notification_time,
            test_data["time_format"]
        )
    except ValueError as exc:
        pytest.fail(
            f"{test_case_id} | STEP 7 FAILED | "
            f"Thời gian '{notification_time}' không đúng format "
            f"'{test_data['time_format']}'. Error: {exc}"
        )

    report_step(
        test_case_id,
        7,
        "Notification đúng loại, đúng appointment, "
        "đúng nội dung và đúng định dạng thời gian"
    )
def test_tc_notification_002_patient_receives_notification_after_admin_cancels(
        driver):
    """
    TC-NOTIFICATION-002:
    Kiểm tra Patient nhận được thông báo phù hợp
    khi Admin thực hiện hủy lịch hẹn của Patient.
    """

    test_case_id = "TC-NOTIFICATION-002"

    test_data = get_test_data_csv( NOTIFICATION_TEST_DATA_CSV, test_case_id )

    # ============================================================
    # Step 1:
    # Patient đặt một lịch khám hợp lệ.
    # ============================================================

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    doctor_id = int( test_data["doctor_id"] )

    appointment_api = AppointmentApi()

    # ------------------------------------------------------------
    # Chuẩn bị slot đặt lịch.
    #
    # Nếu các schedule hiện tại đã hết giờ trống,
    # tự tạo thêm một schedule test trong tương lai.
    # ------------------------------------------------------------

    booking_slot = get_or_create_booking_slot(
        doctor_id=doctor_id,
        test_data=test_data,
        schedule_note="SELENIUM-TC-NOTIFICATION-002"
    )

    booking_date = booking_slot[ "booking_date" ]

    booking_time = booking_slot[ "booking_time" ]

    note = ( test_data["note_prefix"] + str(int(time.time())) )

    doctor_page = DoctorPage( driver )

    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage( driver )

    booking_page.enter_date( booking_date )

    booking_page.enter_time( booking_time )

    actual_booking_time = ( booking_page.get_time_value() )

    assert (
        actual_booking_time
        == booking_time
    ), (
        "TC-NOTIFICATION-002 | STEP 1 FAILED | "
        f"Expected booking time: {booking_time} | "
        f"Actual: {actual_booking_time}"
    )

    booking_page.enter_notes( note )

    booking_page.click_booking_button()

    booking_message = ( booking_page.get_message() )

    assert (
        "Đặt lịch thành công"
        in booking_message
    ), (
        "TC-NOTIFICATION-002 | STEP 1 FAILED | "
        f"Không đặt được lịch. Actual message: {booking_message}"
    )

    appointment = ( appointment_api .find_appointment_by_note( doctor_id=doctor_id, note=note ) )

    appointment_id = ( appointment["appointmentId"] )

    actual_status = ( appointment.get("status") )

    assert (
        actual_status
        == "pending"
    ), (
        "TC-NOTIFICATION-002 | STEP 1 FAILED | "
        "Appointment sau khi tạo không ở trạng thái pending. "
        f"Actual: {actual_status}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description=(
            "Patient đặt lịch khám hợp lệ và "
            f"appointment #{appointment_id} ở trạng thái pending"
        )
    )

    # ============================================================
    # Step 2:
    # Đăng xuất Patient và đăng nhập bằng Admin.
    # ============================================================

    logout_current_user( driver )

    login_account( driver, test_data["admin_username"], test_data["admin_password"] )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description=(
            "Đăng xuất Patient và đăng nhập Admin thành công"
        )
    )

    # ============================================================
    # Step 3:
    # Mở Quản lý lịch hẹn và hủy lịch vừa tạo.
    # ============================================================

    admin_page = AdminAppointmentPage( driver )

    admin_page.open_page()

    page_title = ( admin_page.get_page_title() )

    assert (
        page_title
        == "Quản lý lịch hẹn"
    ), (
        "TC-NOTIFICATION-002 | STEP 3 FAILED | "
        f"Expected page title: Quản lý lịch hẹn | "
        f"Actual: {page_title}"
    )

    actual_appointment_id = ( admin_page .get_appointment_id_by_note( note ) )

    assert (
        actual_appointment_id
        == str(appointment_id)
    ), (
        "TC-NOTIFICATION-002 | STEP 3 FAILED | "
        f"Expected appointment #{appointment_id} | "
        f"Actual: {actual_appointment_id}"
    )

    status_before_cancel = ( admin_page .get_status_by_note( note ) )

    assert (
        status_before_cancel
        == "Chờ xác nhận"
    ), (
        "TC-NOTIFICATION-002 | STEP 3 FAILED | "
        "Appointment không ở trạng thái Chờ xác nhận. "
        f"Actual: {status_before_cancel}"
    )

    assert (
        admin_page
        .is_cancel_button_present(
            note
        )
    ), (
        "TC-NOTIFICATION-002 | STEP 3 FAILED | "
        "Không tìm thấy nút Hủy lịch."
    )

    admin_page.click_cancel( note )

    cancel_message = ( admin_page .get_cancel_success_message() )

    assert (
        cancel_message
        == "Hủy lịch hẹn thành công."
    ), (
        "TC-NOTIFICATION-002 | STEP 3 FAILED | "
        "Không nhận được thông báo hủy lịch thành công. "
        f"Actual: {cancel_message}"
    )

    admin_page.open_page()

    status_after_cancel = ( admin_page .get_status_by_note( note ) )

    assert (
        status_after_cancel
        == "Đã hủy"
    ), (
        "TC-NOTIFICATION-002 | STEP 3 FAILED | "
        f"Expected: Đã hủy | Actual: {status_after_cancel}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            f"Admin hủy appointment #{appointment_id} thành công"
        )
    )

    # ============================================================
    # Step 4:
    # Đăng xuất Admin và đăng nhập lại bằng Patient.
    # ============================================================

    logout_current_user( driver )

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            "Đăng xuất Admin và đăng nhập lại Patient thành công"
        )
    )

    # ============================================================
    # Step 5:
    # Mở trang Thông báo.
    # ============================================================

    notification_page = NotificationPage( driver )

    notification_page.open_page()

    notification_page_title = ( notification_page .get_page_title() )

    assert (
        notification_page_title
        == "Thông báo của tôi"
    ), (
        "TC-NOTIFICATION-002 | STEP 5 FAILED | "
        f"Expected: Thông báo của tôi | "
        f"Actual: {notification_page_title}"
    )

    report_step( test_case_id=test_case_id, step_number=5, description=( "Patient mở trang Thông báo thành công" ) )

    # ============================================================
    # Step 6:
    # Tìm notification liên quan đến lịch vừa bị hủy.
    # ============================================================

    notification = ( notification_page .get_notification_by_appointment_id( appointment_id ) )

    assert (
        notification is not None
    ), (
        "TC-NOTIFICATION-002 | STEP 6 FAILED | "
        f"Không tìm thấy notification của appointment #{appointment_id}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            f"Tìm thấy notification của appointment #{appointment_id}"
        )
    )

    # ============================================================
    # Step 7:
    # Kiểm tra loại, nội dung và thời gian notification.
    # ============================================================

    notification_type = ( notification_page .get_notification_type( notification ) )

    notification_content = ( notification_page .get_notification_content( notification ) )

    notification_time = ( notification_page .get_notification_time( notification ) )

    # 7.1. Đúng loại notification.
    assert (
        notification_type
        == test_data["notification_type"]
    ), (
        "TC-NOTIFICATION-002 | STEP 7 FAILED | "
        f"Expected type: {test_data['notification_type']} | "
        f"Actual: {notification_type}"
    )

    # 7.2. Notification thuộc đúng appointment vừa bị hủy.
    assert (
        f"#{appointment_id}"
        in notification_content
    ), (
        "TC-NOTIFICATION-002 | STEP 7 FAILED | "
        f"Notification không chứa appointment #{appointment_id}. "
        f"Actual: {notification_content}"
    )

    # 7.3. Nội dung thể hiện lịch đã bị hủy.
    assert (
        test_data["expected_keyword"]
        in notification_content.lower()
    ), (
        "TC-NOTIFICATION-002 | STEP 7 FAILED | "
        f"Expected keyword: {test_data['expected_keyword']} | "
        f"Actual: {notification_content}"
    )

    # 7.4. Có thời gian notification.
    assert (
        notification_time.strip()
        != ""
    ), (
        "TC-NOTIFICATION-002 | STEP 7 FAILED | "
        "Notification không hiển thị thời gian."
    )

    # 7.5. Thời gian đúng định dạng.
    try:
        datetime.strptime( notification_time, test_data["time_format"] )

    except ValueError as exc:
        pytest.fail(
            "TC-NOTIFICATION-002 | STEP 7 FAILED | "
            f"Thời gian '{notification_time}' không đúng format "
            f"'{test_data['time_format']}'. Error: {exc}"
        )

    report_step(
        test_case_id=test_case_id,
        step_number=7,
        description=(
            "Notification đúng loại, đúng appointment, "
            "đúng nội dung hủy lịch và đúng định dạng thời gian"
        )
    )


def test_tc_notification_003_patient_receives_notification_after_doctor_updates_result(
        driver):
    """
    TC-NOTIFICATION-003:
    Kiểm tra Patient nhận được thông báo
    sau khi Doctor cập nhật kết quả khám.
    """

    test_case_id = "TC-NOTIFICATION-003"

    test_data = get_test_data_csv( NOTIFICATION_TEST_DATA_CSV, test_case_id )

    # ============================================================
    # Step 1:
    # Chuẩn bị Patient có lịch hẹn đã được Admin xác nhận.
    # ============================================================

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    doctor_id = int( test_data["doctor_id"] )

    appointment_api = AppointmentApi()

    # ------------------------------------------------------------
    # Chuẩn bị slot đặt lịch.
    # Nếu hết slot thì tự tạo schedule test mới.
    # ------------------------------------------------------------
    booking_slot = get_or_create_booking_slot(
        doctor_id=doctor_id,
        test_data=test_data,
        schedule_note="SELENIUM-TC-NOTIFICATION-003"
    )
    booking_date = booking_slot[ "booking_date" ]

    booking_time = booking_slot[ "booking_time" ]

    note = ( test_data["note_prefix"] + str(int(time.time())) )

    doctor_page = DoctorPage( driver )

    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage( driver )

    booking_page.enter_date( booking_date )

    booking_page.enter_time( booking_time )

    actual_booking_time = ( booking_page.get_time_value() )

    assert (
        actual_booking_time
        == booking_time
    ), (
        "TC-NOTIFICATION-003 | STEP 1 FAILED | "
        f"Expected booking time: {booking_time} | "
        f"Actual: {actual_booking_time}"
    )

    booking_page.enter_notes( note )

    booking_page.click_booking_button()

    booking_message = ( booking_page.get_message() )

    assert (
        "Đặt lịch thành công"
        in booking_message
    ), (
        "TC-NOTIFICATION-003 | STEP 1 FAILED | "
        f"Không đặt được lịch. Actual: {booking_message}"
    )

    appointment = ( appointment_api .find_appointment_by_note( doctor_id=doctor_id, note=note ) )

    appointment_id = ( appointment["appointmentId"] )

    assert (
        appointment.get("status")
        == "pending"
    ), (
        "TC-NOTIFICATION-003 | STEP 1 FAILED | "
        "Appointment sau khi tạo không ở trạng thái pending. "
        f"Actual: {appointment.get('status')}"
    )

    # Admin xác nhận lịch để hoàn thành tiền điều kiện.
    logout_current_user( driver )

    login_account( driver, test_data["admin_username"], test_data["admin_password"] )

    admin_page = AdminAppointmentPage( driver )

    admin_page.open_page()

    assert (
        admin_page.get_appointment_id_by_note(
            note
        )
        == str(appointment_id)
    ), (
        "TC-NOTIFICATION-003 | STEP 1 FAILED | "
        f"Không tìm thấy appointment #{appointment_id} trên trang Admin."
    )

    assert (
        admin_page.get_status_by_note(
            note
        )
        == "Chờ xác nhận"
    ), (
        "TC-NOTIFICATION-003 | STEP 1 FAILED | "
        "Appointment không ở trạng thái Chờ xác nhận."
    )

    admin_page.click_confirm( note )

    confirm_message = ( admin_page .get_confirm_success_message() )

    assert (
        confirm_message
        == "Xác nhận lịch hẹn thành công."
    ), (
        "TC-NOTIFICATION-003 | STEP 1 FAILED | "
        f"Actual confirm message: {confirm_message}"
    )

    admin_page.open_page()

    confirmed_status = ( admin_page.get_status_by_note( note ) )

    assert (
        confirmed_status
        == "Đã xác nhận"
    ), (
        "TC-NOTIFICATION-003 | STEP 1 FAILED | "
        f"Expected: Đã xác nhận | Actual: {confirmed_status}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description=(
            f"Chuẩn bị appointment #{appointment_id} "
            "và Admin xác nhận lịch thành công"
        )
    )

    # ============================================================
    # Step 2:
    # Đăng nhập Doctor phụ trách lịch hẹn.
    # ============================================================

    logout_current_user( driver )

    login_account( driver, test_data["doctor_username"], test_data["doctor_password"] )

    report_step( test_case_id=test_case_id, step_number=2, description="Đăng nhập Doctor phụ trách thành công" )

    # ============================================================
    # Step 3:
    # Mở lịch hẹn của Patient và chọn Khám bệnh.
    # ============================================================

    doctor_appointment_page = DoctorAppointmentPage( driver )

    doctor_appointment_page.open_page()

    actual_note = ( doctor_appointment_page .get_note_by_id( appointment_id ) )

    assert (
        actual_note
        == note
    ), (
        "TC-NOTIFICATION-003 | STEP 3 FAILED | "
        f"Expected note: {note} | Actual: {actual_note}"
    )

    actual_status = ( doctor_appointment_page .get_status_by_id( appointment_id ) )

    assert (
        actual_status
        == "Đã xác nhận"
    ), (
        "TC-NOTIFICATION-003 | STEP 3 FAILED | "
        f"Expected: Đã xác nhận | Actual: {actual_status}"
    )

    assert (
        doctor_appointment_page
        .is_examine_button_present(
            appointment_id
        )
    ), (
        "TC-NOTIFICATION-003 | STEP 3 FAILED | "
        "Không tìm thấy nút Khám bệnh."
    )

    doctor_appointment_page.click_examine( appointment_id )

    examination_page = DoctorExaminationPage( driver )

    page_title = ( examination_page.get_page_title() )

    assert (
        page_title
        == "Khám bệnh"
    ), (
        "TC-NOTIFICATION-003 | STEP 3 FAILED | "
        f"Expected page: Khám bệnh | Actual: {page_title}"
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        "TC-NOTIFICATION-003 | STEP 3 FAILED | "
        f"URL không chứa appointmentId={appointment_id}. "
        f"Actual URL: {driver.current_url}"
    )

    assert (
        examination_page
        .is_create_record_form_present()
    ), (
        "TC-NOTIFICATION-003 | STEP 3 FAILED | "
        "Không tìm thấy form tạo hồ sơ bệnh án."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            f"Doctor mở appointment #{appointment_id} "
            "và vào màn hình Khám bệnh thành công"
        )
    )

    # ============================================================
    # Step 4:
    # Nhập Chẩn đoán và Hướng điều trị hợp lệ.
    # ============================================================

    unique_time = str( int(time.time()) )

    diagnosis = ( test_data["diagnosis_prefix"] + unique_time )

    treatment = ( test_data["treatment_prefix"] + unique_time )

    examination_page.enter_diagnosis( diagnosis )

    examination_page.enter_treatment( treatment )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            "Doctor nhập Chẩn đoán và Hướng điều trị hợp lệ"
        )
    )

    # ============================================================
    # Step 5:
    # Lưu hồ sơ bệnh án.
    # ============================================================

    examination_page.click_save_medical_record()

    medical_record_page = MedicalRecordPage( driver )

    record_page_title = ( medical_record_page .get_page_title() )

    assert (
        record_page_title
        == "Chi tiết hồ sơ bệnh án"
    ), (
        "TC-NOTIFICATION-003 | STEP 5 FAILED | "
        f"Expected: Chi tiết hồ sơ bệnh án | "
        f"Actual: {record_page_title}"
    )

    actual_diagnosis = ( medical_record_page .get_diagnosis_information() )

    assert (
        diagnosis
        in actual_diagnosis
    ), (
        "TC-NOTIFICATION-003 | STEP 5 FAILED | "
        f"Không tìm thấy diagnosis vừa lưu. "
        f"Expected chứa: {diagnosis} | "
        f"Actual: {actual_diagnosis}"
    )

    actual_treatment = ( medical_record_page .get_treatment_information() )

    assert (
        treatment
        in actual_treatment
    ), (
        "TC-NOTIFICATION-003 | STEP 5 FAILED | "
        f"Không tìm thấy treatment vừa lưu. "
        f"Expected chứa: {treatment} | "
        f"Actual: {actual_treatment}"
    )

    report_step( test_case_id=test_case_id, step_number=5, description="Doctor lưu hồ sơ bệnh án thành công" )

    # ============================================================
    # Step 6:
    # Đăng xuất Doctor và đăng nhập lại bằng Patient.
    # ============================================================

    logout_current_user( driver )

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            "Đăng xuất Doctor và đăng nhập lại Patient thành công"
        )
    )

    # ============================================================
    # Step 7:
    # Mở trang Thông báo.
    # ============================================================

    notification_page = NotificationPage( driver )

    notification_page.open_page()

    notification_page_title = ( notification_page .get_page_title() )

    assert (
        notification_page_title
        == "Thông báo của tôi"
    ), (
        "TC-NOTIFICATION-003 | STEP 7 FAILED | "
        f"Expected: Thông báo của tôi | "
        f"Actual: {notification_page_title}"
    )

    report_step( test_case_id=test_case_id, step_number=7, description="Patient mở trang Thông báo thành công" )

    # ============================================================
    # Step 8:
    # Tìm và kiểm tra notification mới phát sinh
    # sau khi Doctor lưu hồ sơ bệnh án.
    # ============================================================

    notification = (
        notification_page
        .get_latest_notification_by_type_and_keyword(
            test_data["notification_type"],
            test_data["expected_keyword"]
        )
    )

    assert (
        notification is not None
    ), (
        "TC-NOTIFICATION-003 | STEP 8 FAILED | "
        "Không tìm thấy notification sau khi Doctor "
        "lưu hồ sơ bệnh án."
    )

    notification_type = ( notification_page .get_notification_type( notification ) )

    notification_content = ( notification_page .get_notification_content( notification ) )

    notification_time = ( notification_page .get_notification_time( notification ) )

    assert (
        notification_type
        == test_data["notification_type"]
    ), (
        "TC-NOTIFICATION-003 | STEP 8 FAILED | "
        f"Expected type: {test_data['notification_type']} | "
        f"Actual: {notification_type}"
    )

    normalized_expected = ( notification_page.normalize_text( test_data["expected_keyword"] ) )

    normalized_actual = ( notification_page.normalize_text( notification_content ) )

    assert (
        normalized_expected
        in normalized_actual
    ), (
        "TC-NOTIFICATION-003 | STEP 8 FAILED | "
        f"Expected keyword: {test_data['expected_keyword']} | "
        f"Actual content: {notification_content}"
    )

    assert (
        notification_time.strip()
        != ""
    ), (
        "TC-NOTIFICATION-003 | STEP 8 FAILED | "
        "Notification không hiển thị thời gian."
    )

    try:
        datetime.strptime( notification_time, test_data["time_format"] )

    except ValueError as exc:
        pytest.fail(
            "TC-NOTIFICATION-003 | STEP 8 FAILED | "
            f"Thời gian '{notification_time}' không đúng format "
            f"'{test_data['time_format']}'. Error: {exc}"
        )

    report_step(
        test_case_id=test_case_id,
        step_number=8,
        description=(
            "Tìm thấy notification cập nhật kết quả khám "
            "và kiểm tra loại, nội dung, thời gian thành công"
        )
    )


def test_tc_notification_004_notifications_are_stored_separately(
        driver):
    """
    TC-NOTIFICATION-004:
    Kiểm tra khi Patient phát sinh nhiều thông báo từ
    các sự kiện khác nhau, các thông báo được lưu riêng biệt
    và không ghi đè lẫn nhau.
    """

    test_case_id = "TC-NOTIFICATION-004"

    test_data = get_test_data_csv( NOTIFICATION_TEST_DATA_CSV, test_case_id )

    doctor_id = int( test_data["doctor_id"] )

    appointment_api = AppointmentApi()

    # ============================================================
    # Step 1:
    # Chuẩn bị Patient đã có ít nhất một notification trước đó.
    # - Patient tạo lịch hẹn thứ nhất.
    # - Admin xác nhận lịch hẹn thứ nhất.
    # - Patient kiểm tra notification cũ tồn tại.
    # ============================================================

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    # ------------------------------------------------------------
    # Chuẩn bị slot cho lịch thứ nhất.
    # Nếu hết slot thì tự tạo schedule mới.
    # ------------------------------------------------------------

    first_booking_slot = get_or_create_booking_slot(
        doctor_id=doctor_id,
        test_data=test_data,
        schedule_note="SELENIUM-TC-NOTIFICATION-004-FIRST"
    )
    first_booking_date = ( first_booking_slot["booking_date"] )

    first_booking_time = ( first_booking_slot["booking_time"] )

    first_note = ( test_data["note_prefix"] + "OLD-" + str(int(time.time())) )

    doctor_page = DoctorPage( driver )

    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage( driver )

    booking_page.enter_date( first_booking_date )

    booking_page.enter_time( first_booking_time )

    actual_first_time = ( booking_page.get_time_value() )

    assert (
        actual_first_time
        == first_booking_time
    ), (
        "TC-NOTIFICATION-004 | STEP 1 FAILED | "
        f"Expected first booking time: {first_booking_time} | "
        f"Actual: {actual_first_time}"
    )

    booking_page.enter_notes( first_note )

    booking_page.click_booking_button()

    first_booking_message = ( booking_page.get_message() )

    assert (
        "Đặt lịch thành công"
        in first_booking_message
    ), (
        "TC-NOTIFICATION-004 | STEP 1 FAILED | "
        "Không tạo được lịch hẹn thứ nhất. "
        f"Actual: {first_booking_message}"
    )

    first_appointment = ( appointment_api .find_appointment_by_note( doctor_id=doctor_id, note=first_note ) )

    first_appointment_id = ( first_appointment["appointmentId"] )

    assert (
        first_appointment.get("status")
        == "pending"
    ), (
        "TC-NOTIFICATION-004 | STEP 1 FAILED | "
        "Appointment thứ nhất không ở trạng thái pending."
    )

    # Admin xác nhận lịch thứ nhất.
    logout_current_user( driver )

    login_account( driver, test_data["admin_username"], test_data["admin_password"] )

    admin_page = AdminAppointmentPage( driver )

    admin_page.open_page()

    first_admin_appointment_id = ( admin_page.get_appointment_id_by_note( first_note ) )

    assert (
        first_admin_appointment_id
        == str(first_appointment_id)
    ), (
        "TC-NOTIFICATION-004 | STEP 1 FAILED | "
        f"Không tìm thấy appointment #{first_appointment_id} trên Admin."
    )

    first_status_before_confirm = ( admin_page.get_status_by_note( first_note ) )

    assert (
        first_status_before_confirm
        == "Chờ xác nhận"
    ), (
        "TC-NOTIFICATION-004 | STEP 1 FAILED | "
        "Appointment thứ nhất không ở trạng thái Chờ xác nhận. "
        f"Actual: {first_status_before_confirm}"
    )

    admin_page.click_confirm( first_note )

    first_confirm_message = ( admin_page .get_confirm_success_message() )

    assert (
        first_confirm_message
        == "Xác nhận lịch hẹn thành công."
    ), (
        "TC-NOTIFICATION-004 | STEP 1 FAILED | "
        f"Actual confirm message: {first_confirm_message}"
    )

    admin_page.open_page()

    first_status_after_confirm = ( admin_page.get_status_by_note( first_note ) )

    assert (
        first_status_after_confirm
        == "Đã xác nhận"
    ), (
        "TC-NOTIFICATION-004 | STEP 1 FAILED | "
        f"Expected: Đã xác nhận | "
        f"Actual: {first_status_after_confirm}"
    )

    # Patient kiểm tra notification cũ.
    logout_current_user( driver )

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    notification_page = NotificationPage( driver )

    notification_page.open_page()

    old_notification = ( notification_page .get_notification_by_appointment_id( first_appointment_id ) )

    assert (
        old_notification is not None
    ), (
        "TC-NOTIFICATION-004 | STEP 1 FAILED | "
        f"Không tìm thấy notification cũ của appointment "
        f"#{first_appointment_id}"
    )

    old_notification_content = ( notification_page .get_notification_content( old_notification ) )

    assert (
        f"#{first_appointment_id}"
        in old_notification_content
    ), (
        "TC-NOTIFICATION-004 | STEP 1 FAILED | "
        f"Notification cũ không chứa appointment "
        f"#{first_appointment_id}. "
        f"Actual: {old_notification_content}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description=(
            f"Tạo appointment cũ #{first_appointment_id}, "
            "Admin xác nhận và Patient nhận notification cũ"
        )
    )

    # ============================================================
    # Step 2:
    # Patient tạo thêm một lịch hẹn mới.
    # ============================================================

    second_booking_slot = get_or_create_booking_slot(
        doctor_id=doctor_id,
        test_data=test_data,
        schedule_note="SELENIUM-TC-NOTIFICATION-004-SECOND"
    )

    second_booking_date = ( second_booking_slot["booking_date"] )

    second_booking_time = ( second_booking_slot["booking_time"] )

    second_note = ( test_data["note_prefix"] + "NEW-" + str(int(time.time())) )

    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage( driver )

    booking_page.enter_date( second_booking_date )

    booking_page.enter_time( second_booking_time )

    actual_second_time = ( booking_page.get_time_value() )

    assert (
        actual_second_time
        == second_booking_time
    ), (
        "TC-NOTIFICATION-004 | STEP 2 FAILED | "
        f"Expected second booking time: {second_booking_time} | "
        f"Actual: {actual_second_time}"
    )

    booking_page.enter_notes( second_note )

    booking_page.click_booking_button()

    second_booking_message = ( booking_page.get_message() )

    assert (
        "Đặt lịch thành công"
        in second_booking_message
    ), (
        "TC-NOTIFICATION-004 | STEP 2 FAILED | "
        "Không tạo được lịch hẹn thứ hai. "
        f"Actual: {second_booking_message}"
    )

    second_appointment = ( appointment_api .find_appointment_by_note( doctor_id=doctor_id, note=second_note ) )

    second_appointment_id = ( second_appointment["appointmentId"] )

    assert (
        second_appointment.get("status")
        == "pending"
    ), (
        "TC-NOTIFICATION-004 | STEP 2 FAILED | "
        "Appointment thứ hai không ở trạng thái pending."
    )

    assert (
        second_appointment_id
        != first_appointment_id
    ), (
        "TC-NOTIFICATION-004 | STEP 2 FAILED | "
        "Hai appointment có cùng ID, không thể kiểm tra "
        "hai notification độc lập."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description=(
            f"Patient tạo appointment mới #{second_appointment_id}, "
            f"khác appointment cũ #{first_appointment_id}"
        )
    )

    # ============================================================
    # Step 3:
    # Admin xác nhận lịch hẹn mới.
    # ============================================================

    logout_current_user( driver )

    login_account( driver, test_data["admin_username"], test_data["admin_password"] )

    admin_page = AdminAppointmentPage( driver )

    admin_page.open_page()

    second_admin_appointment_id = ( admin_page .get_appointment_id_by_note( second_note ) )

    assert (
        second_admin_appointment_id
        == str(second_appointment_id)
    ), (
        "TC-NOTIFICATION-004 | STEP 3 FAILED | "
        f"Không tìm thấy appointment mới "
        f"#{second_appointment_id} trên Admin."
    )

    second_status_before_confirm = ( admin_page.get_status_by_note( second_note ) )

    assert (
        second_status_before_confirm
        == "Chờ xác nhận"
    ), (
        "TC-NOTIFICATION-004 | STEP 3 FAILED | "
        f"Expected: Chờ xác nhận | "
        f"Actual: {second_status_before_confirm}"
    )

    admin_page.click_confirm( second_note )

    second_confirm_message = ( admin_page .get_confirm_success_message() )

    assert (
        second_confirm_message
        == "Xác nhận lịch hẹn thành công."
    ), (
        "TC-NOTIFICATION-004 | STEP 3 FAILED | "
        f"Actual confirm message: {second_confirm_message}"
    )

    admin_page.open_page()

    second_status_after_confirm = ( admin_page.get_status_by_note( second_note ) )

    assert (
        second_status_after_confirm
        == "Đã xác nhận"
    ), (
        "TC-NOTIFICATION-004 | STEP 3 FAILED | "
        f"Expected: Đã xác nhận | "
        f"Actual: {second_status_after_confirm}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            f"Admin xác nhận appointment mới "
            f"#{second_appointment_id} thành công"
        )
    )

    # ============================================================
    # Step 4:
    # Đăng nhập lại bằng Patient.
    # ============================================================

    logout_current_user( driver )

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            "Đăng xuất Admin và đăng nhập lại Patient thành công"
        )
    )

    # ============================================================
    # Step 5:
    # Mở trang Thông báo.
    # ============================================================

    notification_page = NotificationPage( driver )

    notification_page.open_page()

    page_title = ( notification_page .get_page_title() )

    assert (
        page_title
        == "Thông báo của tôi"
    ), (
        "TC-NOTIFICATION-004 | STEP 5 FAILED | "
        f"Expected: Thông báo của tôi | "
        f"Actual: {page_title}"
    )

    report_step( test_case_id=test_case_id, step_number=5, description="Patient mở trang Thông báo thành công" )

    # ============================================================
    # Step 6:
    # Kiểm tra notification mới.
    # ============================================================

    new_notification = ( notification_page .get_notification_by_appointment_id( second_appointment_id ) )

    assert (
        new_notification is not None
    ), (
        "TC-NOTIFICATION-004 | STEP 6 FAILED | "
        f"Không tìm thấy notification mới của appointment "
        f"#{second_appointment_id}"
    )

    new_notification_type = ( notification_page .get_notification_type( new_notification ) )

    new_notification_content = ( notification_page .get_notification_content( new_notification ) )

    new_notification_time = ( notification_page .get_notification_time( new_notification ) )

    assert (
        new_notification_type
        == test_data["notification_type"]
    ), (
        "TC-NOTIFICATION-004 | STEP 6 FAILED | "
        f"Expected type: {test_data['notification_type']} | "
        f"Actual: {new_notification_type}"
    )

    assert (
        f"#{second_appointment_id}"
        in new_notification_content
    ), (
        "TC-NOTIFICATION-004 | STEP 6 FAILED | "
        f"Notification mới không chứa appointment "
        f"#{second_appointment_id}. "
        f"Actual: {new_notification_content}"
    )

    assert (
        test_data["expected_keyword"]
        in new_notification_content.lower()
    ), (
        "TC-NOTIFICATION-004 | STEP 6 FAILED | "
        f"Expected keyword: {test_data['expected_keyword']} | "
        f"Actual: {new_notification_content}"
    )

    assert (
        new_notification_time.strip()
        != ""
    ), (
        "TC-NOTIFICATION-004 | STEP 6 FAILED | "
        "Notification mới không hiển thị thời gian."
    )

    try:
        datetime.strptime( new_notification_time, test_data["time_format"] )

    except ValueError as exc:
        pytest.fail(
            "TC-NOTIFICATION-004 | STEP 6 FAILED | "
            f"Thời gian '{new_notification_time}' "
            f"không đúng format '{test_data['time_format']}'. "
            f"Error: {exc}"
        )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            f"Notification mới của appointment "
            f"#{second_appointment_id} hiển thị đúng"
        )
    )

    # ============================================================
    # Step 7:
    # Kiểm tra notification cũ vẫn tồn tại và
    # không bị notification mới ghi đè.
    # ============================================================

    old_notification_after = ( notification_page .get_notification_by_appointment_id( first_appointment_id ) )

    assert (
        old_notification_after is not None
    ), (
        "TC-NOTIFICATION-004 | STEP 7 FAILED | "
        f"Notification cũ của appointment "
        f"#{first_appointment_id} không còn tồn tại."
    )

    old_content_after = ( notification_page .get_notification_content( old_notification_after ) )

    assert (
        f"#{first_appointment_id}"
        in old_content_after
    ), (
        "TC-NOTIFICATION-004 | STEP 7 FAILED | "
        f"Notification cũ không còn chứa appointment "
        f"#{first_appointment_id}. "
        f"Actual: {old_content_after}"
    )

    assert (
        f"#{second_appointment_id}"
        not in old_content_after
    ), (
        "TC-NOTIFICATION-004 | STEP 7 FAILED | "
        "Notification cũ bị ghi đè bằng appointment mới."
    )

    assert (
        f"#{first_appointment_id}"
        not in new_notification_content
    ), (
        "TC-NOTIFICATION-004 | STEP 7 FAILED | "
        "Notification mới chứa nhầm ID appointment cũ."
    )

    assert (
        old_content_after
        != new_notification_content
    ), (
        "TC-NOTIFICATION-004 | STEP 7 FAILED | "
        "Nội dung notification cũ và notification mới "
        "bị trùng nhau."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=7,
        description=(
            f"Notification #{first_appointment_id} và "
            f"#{second_appointment_id} được lưu độc lập, "
            "không ghi đè nhau"
        )
    )


def test_tc_notification_005_notifications_are_isolated_between_patients(
        driver):
    """
    TC-NOTIFICATION-005:
    Kiểm tra danh sách notification hiển thị
    được phân tách giữa hai tài khoản Patient.
    """

    test_case_id = "TC-NOTIFICATION-005"

    test_data = get_test_data_csv( NOTIFICATION_TEST_DATA_CSV, test_case_id )

    patient_a_username = test_data[ "patient_username" ]

    patient_a_password = test_data[ "patient_password" ]

    patient_b_username = test_data[ "patient_b_username" ]

    patient_b_password = test_data[ "patient_b_password" ]

    # ============================================================
    # Step 1:
    # Đăng nhập bằng Patient A.
    # ============================================================

    login_account( driver, patient_a_username, patient_a_password )

    report_step( test_case_id=test_case_id, step_number=1, description=( "Đăng nhập Patient A thành công" ) )

    # ============================================================
    # Step 2:
    # Mở trang Thông báo và lấy danh sách
    # notification của Patient A.
    # ============================================================

    notification_page = NotificationPage( driver )

    notification_page.open_page()

    page_title_a = ( notification_page .get_page_title() )

    assert (
        page_title_a
        == "Thông báo của tôi"
    ), (
        "TC-NOTIFICATION-005 | STEP 2 FAILED | "
        f"Expected: Thông báo của tôi | "
        f"Actual: {page_title_a}"
    )

    patient_a_notifications = ( notification_page .get_all_notification_contents() )

    assert (
        len(patient_a_notifications)
        > 0
    ), (
        "TC-NOTIFICATION-005 | STEP 2 FAILED | "
        "Patient A không có notification nào để kiểm tra."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description=(
            f"Patient A có {len(patient_a_notifications)} notification"
        )
    )

    # ============================================================
    # Step 3:
    # Đăng xuất Patient A và đăng nhập bằng Patient B.
    # ============================================================

    logout_current_user( driver )

    login_account( driver, patient_b_username, patient_b_password )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            "Đăng xuất Patient A và đăng nhập Patient B thành công"
        )
    )

    # ============================================================
    # Step 4:
    # Mở trang Thông báo và lấy danh sách
    # notification của Patient B.
    # ============================================================

    notification_page = NotificationPage( driver )

    notification_page.open_page()

    page_title_b = ( notification_page .get_page_title() )

    assert (
        page_title_b
        == "Thông báo của tôi"
    ), (
        "TC-NOTIFICATION-005 | STEP 4 FAILED | "
        f"Expected: Thông báo của tôi | "
        f"Actual: {page_title_b}"
    )

    patient_b_notifications = ( notification_page .get_all_notification_contents() )

    assert (
        len(patient_b_notifications)
        > 0
    ), (
        "TC-NOTIFICATION-005 | STEP 4 FAILED | "
        "Patient B không có notification nào để kiểm tra."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            f"Patient B có {len(patient_b_notifications)} notification"
        )
    )

    # ============================================================
    # Step 5:
    # So sánh danh sách notification của hai Patient.
    # Danh sách phải được phân tách theo từng tài khoản.
    # ============================================================

    assert (
        patient_a_notifications
        != patient_b_notifications
    ), (
        "TC-NOTIFICATION-005 | STEP 5 FAILED | "
        "Danh sách notification của Patient A và Patient B "
        "giống nhau hoàn toàn, có nguy cơ dữ liệu bị lẫn giữa tài khoản."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            "Danh sách notification của Patient A và Patient B "
            "được phân tách, không giống nhau"
        )
    )


def test_tc_notification_006_patient_receives_notification_after_doctor_creates_prescription(
        driver):
    """
    TC-NOTIFICATION-006:
    Kiểm tra Patient nhận được thông báo đúng
    sau khi Doctor tạo và lưu đơn thuốc mới.
    """

    test_case_id = "TC-NOTIFICATION-006"

    test_data = get_test_data_csv( NOTIFICATION_TEST_DATA_CSV, test_case_id )

    # ============================================================
    # Step 1:
    # Chuẩn bị Patient có lịch hẹn đã được xác nhận.
    # - Patient đặt lịch.
    # - Admin xác nhận lịch.
    # ============================================================

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    doctor_id = int( test_data["doctor_id"] )

    appointment_api = AppointmentApi()

    # ------------------------------------------------------------
    # Chuẩn bị slot đặt lịch.
    # Nếu hết slot thì tự tạo schedule test.
    # ------------------------------------------------------------

    booking_slot = get_or_create_booking_slot(
        doctor_id=doctor_id,
        test_data=test_data,
        schedule_note="SELENIUM-TC-NOTIFICATION-006"
    )

    booking_date = ( booking_slot["booking_date"] )

    booking_time = ( booking_slot["booking_time"] )

    unique_time = str( int(time.time()) )

    note = ( test_data["note_prefix"] + unique_time )

    doctor_page = DoctorPage( driver )

    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage( driver )

    booking_page.enter_date( booking_date )

    booking_page.enter_time( booking_time )

    actual_booking_time = ( booking_page.get_time_value() )

    assert (
        actual_booking_time
        == booking_time
    ), (
        "TC-NOTIFICATION-006 | STEP 1 FAILED | "
        f"Expected booking time: {booking_time} | "
        f"Actual: {actual_booking_time}"
    )

    booking_page.enter_notes( note )

    booking_page.click_booking_button()

    booking_message = ( booking_page.get_message() )

    assert (
        "Đặt lịch thành công"
        in booking_message
    ), (
        "TC-NOTIFICATION-006 | STEP 1 FAILED | "
        f"Không đặt được lịch. Actual: {booking_message}"
    )

    appointment = ( appointment_api .find_appointment_by_note( doctor_id=doctor_id, note=note ) )

    appointment_id = ( appointment["appointmentId"] )

    assert (
        appointment.get("status")
        == "pending"
    ), (
        "TC-NOTIFICATION-006 | STEP 1 FAILED | "
        "Appointment sau khi tạo không ở trạng thái pending. "
        f"Actual: {appointment.get('status')}"
    )

    # Admin xác nhận lịch.
    logout_current_user( driver )

    login_account( driver, test_data["admin_username"], test_data["admin_password"] )

    admin_page = AdminAppointmentPage( driver )

    admin_page.open_page()

    assert (
        admin_page.get_appointment_id_by_note(
            note
        )
        == str(appointment_id)
    ), (
        "TC-NOTIFICATION-006 | STEP 1 FAILED | "
        f"Không tìm thấy appointment #{appointment_id} trên Admin."
    )

    assert (
        admin_page.get_status_by_note(
            note
        )
        == "Chờ xác nhận"
    ), (
        "TC-NOTIFICATION-006 | STEP 1 FAILED | "
        "Appointment không ở trạng thái Chờ xác nhận."
    )

    assert (
        admin_page.is_confirm_button_present(
            note
        )
    ), (
        "TC-NOTIFICATION-006 | STEP 1 FAILED | "
        "Không tìm thấy nút Xác nhận."
    )

    admin_page.click_confirm( note )

    confirm_message = ( admin_page .get_confirm_success_message() )

    assert (
        confirm_message
        == "Xác nhận lịch hẹn thành công."
    ), (
        "TC-NOTIFICATION-006 | STEP 1 FAILED | "
        f"Actual confirm message: {confirm_message}"
    )

    admin_page.open_page()

    confirmed_status = ( admin_page.get_status_by_note( note ) )

    assert (
        confirmed_status
        == "Đã xác nhận"
    ), (
        "TC-NOTIFICATION-006 | STEP 1 FAILED | "
        f"Expected: Đã xác nhận | Actual: {confirmed_status}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description=(
            f"Chuẩn bị appointment #{appointment_id} "
            "và Admin xác nhận lịch thành công"
        )
    )

    # ============================================================
    # Step 2:
    # Doctor đăng nhập.
    # ============================================================

    logout_current_user( driver )

    login_account( driver, test_data["doctor_username"], test_data["doctor_password"] )

    report_step( test_case_id=test_case_id, step_number=2, description="Đăng nhập Doctor thành công" )

    # ============================================================
    # Step 3:
    # Doctor mở đúng lịch hẹn của Patient.
    # ============================================================

    doctor_appointment_page = DoctorAppointmentPage( driver )

    doctor_appointment_page.open_page()

    actual_note = ( doctor_appointment_page .get_note_by_id( appointment_id ) )

    assert (
        actual_note
        == note
    ), (
        "TC-NOTIFICATION-006 | STEP 3 FAILED | "
        f"Expected note: {note} | Actual: {actual_note}"
    )

    actual_status = ( doctor_appointment_page .get_status_by_id( appointment_id ) )

    assert (
        actual_status
        == "Đã xác nhận"
    ), (
        "TC-NOTIFICATION-006 | STEP 3 FAILED | "
        f"Expected: Đã xác nhận | Actual: {actual_status}"
    )

    assert (
        doctor_appointment_page
        .is_examine_button_present(
            appointment_id
        )
    ), (
        "TC-NOTIFICATION-006 | STEP 3 FAILED | "
        "Không tìm thấy nút Khám bệnh."
    )

    doctor_appointment_page.click_examine( appointment_id )

    examination_page = DoctorExaminationPage( driver )

    examination_title = ( examination_page.get_page_title() )

    assert (
        examination_title
        == "Khám bệnh"
    ), (
        "TC-NOTIFICATION-006 | STEP 3 FAILED | "
        f"Expected page: Khám bệnh | Actual: {examination_title}"
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        "TC-NOTIFICATION-006 | STEP 3 FAILED | "
        f"URL không chứa appointmentId={appointment_id}. "
        f"Actual: {driver.current_url}"
    )

    assert (
        examination_page
        .is_create_record_form_present()
    ), (
        "TC-NOTIFICATION-006 | STEP 3 FAILED | "
        "Không tìm thấy form tạo hồ sơ bệnh án."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            f"Doctor mở appointment #{appointment_id} "
            "và vào màn hình Khám bệnh thành công"
        )
    )

    # ============================================================
    # Step 4:
    # Doctor nhập Chẩn đoán và Hướng điều trị.
    # ============================================================

    diagnosis = ( test_data["diagnosis_prefix"] + unique_time )

    treatment = ( test_data["treatment_prefix"] + unique_time )

    examination_page.enter_diagnosis( diagnosis )

    examination_page.enter_treatment( treatment )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            "Doctor nhập Chẩn đoán và Hướng điều trị hợp lệ"
        )
    )

    # ============================================================
    # Step 5:
    # Doctor lưu hồ sơ bệnh án.
    # ============================================================

    examination_page.click_save_medical_record()

    medical_record_page = MedicalRecordPage( driver )

    record_page_title = ( medical_record_page .get_page_title() )

    assert (
        record_page_title
        == "Chi tiết hồ sơ bệnh án"
    ), (
        "TC-NOTIFICATION-006 | STEP 5 FAILED | "
        f"Expected: Chi tiết hồ sơ bệnh án | "
        f"Actual: {record_page_title}"
    )

    actual_diagnosis = ( medical_record_page .get_diagnosis_information() )

    assert (
        diagnosis
        in actual_diagnosis
    ), (
        "TC-NOTIFICATION-006 | STEP 5 FAILED | "
        f"Không tìm thấy diagnosis vừa lưu. "
        f"Actual: {actual_diagnosis}"
    )

    actual_treatment = ( medical_record_page .get_treatment_information() )

    assert (
        treatment
        in actual_treatment
    ), (
        "TC-NOTIFICATION-006 | STEP 5 FAILED | "
        f"Không tìm thấy treatment vừa lưu. "
        f"Actual: {actual_treatment}"
    )

    report_step( test_case_id=test_case_id, step_number=5, description="Doctor lưu hồ sơ bệnh án thành công" )

    # ============================================================
    # Step 6:
    # Doctor mở chức năng kê đơn thuốc.
    # ============================================================

    prescription_page = PrescriptionPage( driver )

    prescription_page.open_prescription_tab()

    assert (
        prescription_page
        .is_prescription_form_present()
    ), (
        "TC-NOTIFICATION-006 | STEP 6 FAILED | "
        "Không tìm thấy form kê đơn thuốc."
    )

    report_step( test_case_id=test_case_id, step_number=6, description="Doctor mở form kê đơn thuốc thành công" )

    # ============================================================
    # Step 7:
    # Doctor tạo và lưu một đơn thuốc hợp lệ.
    # ============================================================

    selected_drug = ( prescription_page .select_drug_by_index( test_data["drug_option_index"] ) )

    assert ( selected_drug != "" ), ( "TC-NOTIFICATION-006 | STEP 7 FAILED | " "Không chọn được thuốc." )

    assert (
        "-- Chọn thuốc --"
        not in selected_drug
    ), (
        "TC-NOTIFICATION-006 | STEP 7 FAILED | "
        "Giá trị thuốc vẫn đang là option mặc định."
    )

    prescription_page.enter_quantity( test_data["prescription_quantity"] )

    prescription_page.enter_dosage( test_data["prescription_dosage"] )

    prescription_page.click_add_to_prescription()

    prescription_item_count = ( prescription_page .get_prescription_item_count() )

    assert (
        prescription_item_count
        == 1
    ), (
        "TC-NOTIFICATION-006 | STEP 7 FAILED | "
        f"Expected 1 thuốc trong đơn | "
        f"Actual: {prescription_item_count}"
    )

    prescription_page.click_save_prescription()

    prescription_message = ( prescription_page .get_prescription_success_message() )

    assert (
        prescription_message
        == "Kê đơn thuốc thành công."
    ), (
        "TC-NOTIFICATION-006 | STEP 7 FAILED | "
        f"Expected: Kê đơn thuốc thành công. | "
        f"Actual: {prescription_message}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=7,
        description=(
            f"Doctor tạo và lưu đơn thuốc với thuốc '{selected_drug}' thành công"
        )
    )

    # ============================================================
    # Step 8:
    # Doctor đăng xuất và Patient đăng nhập lại.
    # ============================================================

    logout_current_user( driver )

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    report_step(
        test_case_id=test_case_id,
        step_number=8,
        description=(
            "Đăng xuất Doctor và đăng nhập lại Patient thành công"
        )
    )

    # ============================================================
    # Step 9:
    # Patient mở trang Thông báo và kiểm tra notification
    # sau khi Doctor tạo đơn thuốc.
    # ============================================================

    notification_page = NotificationPage( driver )

    notification_page.open_page()

    notification_page_title = ( notification_page .get_page_title() )

    assert (
        notification_page_title
        == "Thông báo của tôi"
    ), (
        "TC-NOTIFICATION-006 | STEP 9 FAILED | "
        f"Expected: Thông báo của tôi | "
        f"Actual: {notification_page_title}"
    )

    notification = (
        notification_page
        .get_latest_notification_by_type_and_keyword(
            test_data["notification_type"],
            test_data["expected_keyword"]
        )
    )

    assert (
        notification is not None
    ), (
        "TC-NOTIFICATION-006 | STEP 9 FAILED | "
        "Không tìm thấy notification sau khi Doctor kê đơn thuốc."
    )

    notification_type = ( notification_page .get_notification_type( notification ) )

    notification_content = ( notification_page .get_notification_content( notification ) )

    notification_time = ( notification_page .get_notification_time( notification ) )

    assert (
        notification_type
        == test_data["notification_type"]
    ), (
        "TC-NOTIFICATION-006 | STEP 9 FAILED | "
        f"Expected type: {test_data['notification_type']} | "
        f"Actual: {notification_type}"
    )

    normalized_expected = ( notification_page.normalize_text( test_data["expected_keyword"] ) )

    normalized_content = ( notification_page.normalize_text( notification_content ) )

    assert (
        normalized_expected
        in normalized_content
    ), (
        "TC-NOTIFICATION-006 | STEP 9 FAILED | "
        f"Expected keyword: {test_data['expected_keyword']} | "
        f"Actual content: {notification_content}"
    )

    assert (
        notification_time.strip()
        != ""
    ), (
        "TC-NOTIFICATION-006 | STEP 9 FAILED | "
        "Notification không hiển thị thời gian."
    )

    try:
        datetime.strptime( notification_time, test_data["time_format"] )

    except ValueError as exc:
        pytest.fail(
            "TC-NOTIFICATION-006 | STEP 9 FAILED | "
            f"Thời gian '{notification_time}' không đúng format "
            f"'{test_data['time_format']}'. Error: {exc}"
        )

    report_step(
        test_case_id=test_case_id,
        step_number=9,
        description=(
            "Patient nhận notification đơn thuốc đúng loại, "
            "đúng nội dung và đúng định dạng thời gian"
        )
    )


def test_tc_notification_007_patient_receives_notification_after_doctor_adds_test_result(
        driver):
    """
    TC-NOTIFICATION-007:
    Kiểm tra Patient nhận được thông báo đúng
    sau khi Doctor thêm và lưu kết quả xét nghiệm
    vào hồ sơ bệnh án của Patient.
    """

    test_case_id = "TC-NOTIFICATION-007"

    test_data = get_test_data_csv( NOTIFICATION_TEST_DATA_CSV, test_case_id )

    # ============================================================
    # Step 1:
    # Chuẩn bị Patient có hồ sơ bệnh án đã được Doctor tạo.
    # Flow:
    # - Patient đặt lịch.
    # - Admin xác nhận.
    # - Doctor khám bệnh.
    # - Doctor nhập Chẩn đoán và Hướng điều trị.
    # - Doctor lưu hồ sơ bệnh án.
    # ============================================================

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    doctor_id = int( test_data["doctor_id"] )

    appointment_api = AppointmentApi()

    # ------------------------------------------------------------
    # Chuẩn bị slot.
    # Nếu hết slot thì tự tạo schedule test.
    # ------------------------------------------------------------
    booking_slot = get_or_create_booking_slot(
        doctor_id=doctor_id,
        test_data=test_data,
        schedule_note="SELENIUM-TC-NOTIFICATION-007"
    )

    booking_date = ( booking_slot["booking_date"] )

    booking_time = ( booking_slot["booking_time"] )

    unique_time = str( int(time.time()) )

    note = ( test_data["note_prefix"] + unique_time )

    doctor_page = DoctorPage( driver )

    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage( driver )

    booking_page.enter_date( booking_date )

    booking_page.enter_time( booking_time )

    actual_booking_time = ( booking_page.get_time_value() )

    assert (
        actual_booking_time
        == booking_time
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        f"Expected booking time: {booking_time} | "
        f"Actual: {actual_booking_time}"
    )

    booking_page.enter_notes( note )

    booking_page.click_booking_button()

    booking_message = ( booking_page.get_message() )

    assert (
        "Đặt lịch thành công"
        in booking_message
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        f"Không đặt được lịch. Actual: {booking_message}"
    )

    appointment = ( appointment_api .find_appointment_by_note( doctor_id=doctor_id, note=note ) )

    appointment_id = ( appointment["appointmentId"] )

    assert (
        appointment.get("status")
        == "pending"
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        "Appointment sau khi tạo không ở trạng thái pending."
    )

    # Admin xác nhận lịch.
    logout_current_user( driver )

    login_account( driver, test_data["admin_username"], test_data["admin_password"] )

    admin_page = AdminAppointmentPage( driver )

    admin_page.open_page()

    assert (
        admin_page.get_appointment_id_by_note(
            note
        )
        == str(appointment_id)
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        f"Không tìm thấy appointment #{appointment_id} trên Admin."
    )

    assert (
        admin_page.get_status_by_note(
            note
        )
        == "Chờ xác nhận"
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        "Appointment không ở trạng thái Chờ xác nhận."
    )

    assert (
        admin_page.is_confirm_button_present(
            note
        )
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        "Không tìm thấy nút Xác nhận."
    )

    admin_page.click_confirm( note )

    confirm_message = ( admin_page .get_confirm_success_message() )

    assert (
        confirm_message
        == "Xác nhận lịch hẹn thành công."
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        f"Actual confirm message: {confirm_message}"
    )

    admin_page.open_page()

    confirmed_status = ( admin_page.get_status_by_note( note ) )

    assert (
        confirmed_status
        == "Đã xác nhận"
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        f"Expected: Đã xác nhận | Actual: {confirmed_status}"
    )

    # Doctor tạo hồ sơ bệnh án.
    logout_current_user( driver )

    login_account( driver, test_data["doctor_username"], test_data["doctor_password"] )

    doctor_appointment_page = DoctorAppointmentPage( driver )

    doctor_appointment_page.open_page()

    assert (
        doctor_appointment_page
        .get_note_by_id(
            appointment_id
        )
        == note
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        "Doctor không thấy đúng appointment vừa tạo."
    )

    assert (
        doctor_appointment_page
        .get_status_by_id(
            appointment_id
        )
        == "Đã xác nhận"
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        "Appointment của Doctor chưa ở trạng thái Đã xác nhận."
    )

    assert (
        doctor_appointment_page
        .is_examine_button_present(
            appointment_id
        )
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        "Không tìm thấy nút Khám bệnh."
    )

    doctor_appointment_page.click_examine( appointment_id )

    examination_page = DoctorExaminationPage( driver )

    assert (
        examination_page.get_page_title()
        == "Khám bệnh"
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        "Không mở đúng trang Khám bệnh."
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        f"URL không chứa appointmentId={appointment_id}."
    )

    assert (
        examination_page
        .is_create_record_form_present()
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        "Không tìm thấy form tạo hồ sơ bệnh án."
    )

    diagnosis = ( test_data["diagnosis_prefix"] + unique_time )

    treatment = ( test_data["treatment_prefix"] + unique_time )

    examination_page.enter_diagnosis( diagnosis )

    examination_page.enter_treatment( treatment )

    examination_page.click_save_medical_record()

    medical_record_page = MedicalRecordPage( driver )

    assert (
        medical_record_page
        .get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        "Không mở đúng trang Chi tiết hồ sơ bệnh án."
    )

    actual_diagnosis = ( medical_record_page .get_diagnosis_information() )

    assert (
        diagnosis
        in actual_diagnosis
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        "Diagnosis vừa nhập chưa được lưu đúng."
    )

    actual_treatment = ( medical_record_page .get_treatment_information() )

    assert (
        treatment
        in actual_treatment
    ), (
        "TC-NOTIFICATION-007 | STEP 1 FAILED | "
        "Treatment vừa nhập chưa được lưu đúng."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description=(
            f"Chuẩn bị appointment #{appointment_id}, "
            "Admin xác nhận và Doctor tạo hồ sơ bệnh án thành công"
        )
    )

    # ============================================================
    # Step 2:
    # Xác nhận Doctor đang đăng nhập và đang truy cập hồ sơ.
    # ============================================================

    assert (
        medical_record_page
        .is_medical_record_information_present()
    ), (
        "TC-NOTIFICATION-007 | STEP 2 FAILED | "
        "Không xác nhận được Doctor đang truy cập hồ sơ bệnh án."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description=(
            "Doctor đang đăng nhập và truy cập được hồ sơ bệnh án"
        )
    )

    # ============================================================
    # Step 3:
    # Mở Chi tiết hồ sơ bệnh án của Patient.
    # ============================================================

    medical_record_page.open_page( appointment_id )

    record_page_title = ( medical_record_page .get_page_title() )

    assert (
        record_page_title
        == "Chi tiết hồ sơ bệnh án"
    ), (
        "TC-NOTIFICATION-007 | STEP 3 FAILED | "
        f"Expected: Chi tiết hồ sơ bệnh án | "
        f"Actual: {record_page_title}"
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        "TC-NOTIFICATION-007 | STEP 3 FAILED | "
        f"URL không chứa appointmentId={appointment_id}."
    )

    assert (
        diagnosis
        in medical_record_page
        .get_diagnosis_information()
    ), (
        "TC-NOTIFICATION-007 | STEP 3 FAILED | "
        "Không hiển thị đúng diagnosis đã lưu."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            f"Mở hồ sơ bệnh án của appointment "
            f"#{appointment_id} thành công"
        )
    )

    # ============================================================
    # Step 4:
    # Chuyển đến phần Xét nghiệm.
    # ============================================================

    test_result_page = TestResultPage( driver )

    test_result_page.open_test_result_tab()

    assert (
        test_result_page
        .is_test_result_form_present()
    ), (
        "TC-NOTIFICATION-007 | STEP 4 FAILED | "
        "Không tìm thấy form nhập kết quả xét nghiệm."
    )

    report_step( test_case_id=test_case_id, step_number=4, description="Mở phần Xét nghiệm thành công" )

    # ============================================================
    # Step 5:
    # Nhập kết quả xét nghiệm hợp lệ.
    # ============================================================

    test_name = ( test_data["test_name_prefix"] + unique_time )

    test_result = ( test_data["test_result_prefix"] + unique_time )

    test_result_page.enter_test_name( test_name )

    test_result_page.enter_test_result( test_result )

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            f"Nhập xét nghiệm '{test_name}' "
            "và kết quả hợp lệ"
        )
    )

    # ============================================================
    # Step 6:
    # Lưu kết quả xét nghiệm.
    # ============================================================

    test_result_page.click_save_test_result()

    save_message = ( test_result_page .get_success_message() )

    assert (
        save_message
        == "Thêm kết quả xét nghiệm thành công."
    ), (
        "TC-NOTIFICATION-007 | STEP 6 FAILED | "
        f"Expected: Thêm kết quả xét nghiệm thành công. | "
        f"Actual: {save_message}"
    )

    assert (
        test_result_page
        .has_test_result(
            test_name,
            test_result
        )
    ), (
        "TC-NOTIFICATION-007 | STEP 6 FAILED | "
        f"Không tìm thấy kết quả xét nghiệm '{test_name}' "
        "sau khi lưu."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            f"Lưu kết quả xét nghiệm '{test_name}' thành công"
        )
    )

    # ============================================================
    # Step 7:
    # Đăng xuất Doctor và đăng nhập lại Patient.
    # ============================================================

    logout_current_user( driver )

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    report_step(
        test_case_id=test_case_id,
        step_number=7,
        description=(
            "Đăng xuất Doctor và đăng nhập lại Patient thành công"
        )
    )

    # ============================================================
    # Step 8:
    # Patient mở trang Thông báo.
    # ============================================================

    notification_page = NotificationPage( driver )

    notification_page.open_page()

    notification_page_title = ( notification_page .get_page_title() )

    assert (
        notification_page_title
        == "Thông báo của tôi"
    ), (
        "TC-NOTIFICATION-007 | STEP 8 FAILED | "
        f"Expected: Thông báo của tôi | "
        f"Actual: {notification_page_title}"
    )

    report_step( test_case_id=test_case_id, step_number=8, description="Patient mở trang Thông báo thành công" )

    # ============================================================
    # Step 9:
    # Tìm notification mới phát sinh liên quan
    # đến kết quả xét nghiệm vừa được lưu.
    # ============================================================

    notification = (
        notification_page
        .get_latest_notification_by_type_and_keyword(
            test_data["notification_type"],
            test_name
        )
    )

    assert (
        notification is not None
    ), (
        "TC-NOTIFICATION-007 | STEP 9 FAILED | "
        f"Không tìm thấy notification cho xét nghiệm '{test_name}'."
    )

    notification_type = ( notification_page .get_notification_type( notification ) )

    notification_content = ( notification_page .get_notification_content( notification ) )

    notification_time = ( notification_page .get_notification_time( notification ) )

    assert (
        notification_type
        == test_data["notification_type"]
    ), (
        "TC-NOTIFICATION-007 | STEP 9 FAILED | "
        f"Expected type: {test_data['notification_type']} | "
        f"Actual: {notification_type}"
    )

    normalized_test_name = ( notification_page .normalize_text( test_name ) )

    normalized_content = ( notification_page .normalize_text( notification_content ) )

    assert (
        normalized_test_name
        in normalized_content
    ), (
        "TC-NOTIFICATION-007 | STEP 9 FAILED | "
        f"Notification không chứa tên xét nghiệm '{test_name}'. "
        f"Actual: {notification_content}"
    )

    normalized_expected = ( notification_page .normalize_text( test_data["expected_keyword"] ) )

    assert (
        normalized_expected
        in normalized_content
    ), (
        "TC-NOTIFICATION-007 | STEP 9 FAILED | "
        f"Expected keyword: {test_data['expected_keyword']} | "
        f"Actual: {notification_content}"
    )

    assert (
        notification_time.strip()
        != ""
    ), (
        "TC-NOTIFICATION-007 | STEP 9 FAILED | "
        "Notification không hiển thị thời gian."
    )

    try:
        datetime.strptime( notification_time, test_data["time_format"] )

    except ValueError as exc:
        pytest.fail(
            "TC-NOTIFICATION-007 | STEP 9 FAILED | "
            f"Thời gian '{notification_time}' không đúng format "
            f"'{test_data['time_format']}'. Error: {exc}"
        )

    report_step(
        test_case_id=test_case_id,
        step_number=9,
        description=(
            f"Patient nhận notification cho xét nghiệm "
            f"'{test_name}' đúng loại, nội dung và thời gian"
        )
    )


def test_tc_notification_008_patient_receives_new_notification_when_doctor_creates_another_prescription(
        driver):
    """
    TC-NOTIFICATION-008:

    Kiểm tra Patient nhận được một notification [Đơn thuốc] mới
    khi Doctor kê thêm một đơn thuốc mới cho Patient
    đã có đơn thuốc trước đó.

    Đồng thời kiểm tra notification mới không ghi đè
    hoặc bị nhầm với notification của đơn thuốc cũ.
    """

    test_case_id = "TC-NOTIFICATION-008"

    test_data = get_test_data_csv( NOTIFICATION_TEST_DATA_CSV, test_case_id )

    # ============================================================
    # Step 1:
    # Chuẩn bị Patient đã có một đơn thuốc được lưu trước đó.
    # - Patient đặt lịch.
    # - Admin xác nhận.
    # - Doctor khám.
    # - Doctor tạo hồ sơ bệnh án.
    # - Doctor kê đơn thuốc thứ nhất.
    # ============================================================

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    doctor_id = int( test_data["doctor_id"] )

    appointment_api = AppointmentApi()

    # ------------------------------------------------------------
    # Chuẩn bị slot.
    # Nếu hết slot thì tự tạo schedule test.
    # ------------------------------------------------------------

    booking_slot = get_or_create_booking_slot(
        doctor_id=doctor_id,
        test_data=test_data,
        schedule_note="SELENIUM-TC-NOTIFICATION-008"
    )

    booking_date = booking_slot[ "booking_date" ]

    booking_time = booking_slot[ "booking_time" ]

    unique_time = str( int(time.time()) )

    note = ( test_data["note_prefix"] + unique_time )

    doctor_page = DoctorPage( driver )

    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage( driver )

    booking_page.enter_date( booking_date )

    booking_page.enter_time( booking_time )

    actual_booking_time = ( booking_page.get_time_value() )

    assert (
        actual_booking_time
        == booking_time
    ), (
        "TC-NOTIFICATION-008 | STEP 1 FAILED | "
        f"Expected booking time: {booking_time} | "
        f"Actual: {actual_booking_time}"
    )

    booking_page.enter_notes( note )

    booking_page.click_booking_button()

    booking_message = ( booking_page.get_message() )

    assert (
        "Đặt lịch thành công"
        in booking_message
    ), (
        "TC-NOTIFICATION-008 | STEP 1 FAILED | "
        f"Không đặt được lịch. Actual: {booking_message}"
    )

    appointment = ( appointment_api .find_appointment_by_note( doctor_id=doctor_id, note=note ) )

    appointment_id = ( appointment["appointmentId"] )

    assert (
        appointment.get("status")
        == "pending"
    ), (
        "TC-NOTIFICATION-008 | STEP 1 FAILED | "
        "Appointment sau khi tạo không ở trạng thái pending."
    )

    # Admin xác nhận.
    logout_current_user( driver )

    login_account( driver, test_data["admin_username"], test_data["admin_password"] )

    admin_page = AdminAppointmentPage( driver )

    admin_page.open_page()

    assert (
        admin_page
        .get_appointment_id_by_note(
            note
        )
        == str(appointment_id)
    ), (
        "TC-NOTIFICATION-008 | STEP 1 FAILED | "
        f"Không tìm thấy appointment #{appointment_id}."
    )

    assert (
        admin_page
        .get_status_by_note(
            note
        )
        == "Chờ xác nhận"
    ), (
        "TC-NOTIFICATION-008 | STEP 1 FAILED | "
        "Appointment không ở trạng thái Chờ xác nhận."
    )

    admin_page.click_confirm( note )

    confirm_message = ( admin_page .get_confirm_success_message() )

    assert (
        confirm_message
        == "Xác nhận lịch hẹn thành công."
    ), (
        "TC-NOTIFICATION-008 | STEP 1 FAILED | "
        f"Actual confirm message: {confirm_message}"
    )

    admin_page.open_page()

    assert (
        admin_page
        .get_status_by_note(
            note
        )
        == "Đã xác nhận"
    ), (
        "TC-NOTIFICATION-008 | STEP 1 FAILED | "
        "Appointment chưa chuyển sang Đã xác nhận."
    )

    # Doctor tạo hồ sơ bệnh án.
    logout_current_user( driver )

    login_account( driver, test_data["doctor_username"], test_data["doctor_password"] )

    doctor_appointment_page = DoctorAppointmentPage( driver )

    doctor_appointment_page.open_page()

    assert (
        doctor_appointment_page
        .get_note_by_id(
            appointment_id
        )
        == note
    ), (
        "TC-NOTIFICATION-008 | STEP 1 FAILED | "
        "Doctor không thấy đúng appointment."
    )

    assert (
        doctor_appointment_page
        .get_status_by_id(
            appointment_id
        )
        == "Đã xác nhận"
    ), (
        "TC-NOTIFICATION-008 | STEP 1 FAILED | "
        "Appointment phía Doctor chưa Đã xác nhận."
    )

    assert (
        doctor_appointment_page
        .is_examine_button_present(
            appointment_id
        )
    ), (
        "TC-NOTIFICATION-008 | STEP 1 FAILED | "
        "Không tìm thấy nút Khám bệnh."
    )

    doctor_appointment_page.click_examine( appointment_id )

    examination_page = DoctorExaminationPage( driver )

    assert (
        examination_page.get_page_title()
        == "Khám bệnh"
    ), (
        "TC-NOTIFICATION-008 | STEP 1 FAILED | "
        "Không mở đúng trang Khám bệnh."
    )

    diagnosis = ( test_data["diagnosis_prefix"] + unique_time )

    treatment = ( test_data["treatment_prefix"] + unique_time )

    examination_page.enter_diagnosis( diagnosis )

    examination_page.enter_treatment( treatment )

    examination_page.click_save_medical_record()

    medical_record_page = MedicalRecordPage( driver )

    assert (
        medical_record_page
        .get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    ), (
        "TC-NOTIFICATION-008 | STEP 1 FAILED | "
        "Không mở đúng trang Chi tiết hồ sơ bệnh án."
    )

    # Doctor kê đơn thuốc thứ nhất.
    prescription_page = PrescriptionPage( driver )

    prescription_page.open_prescription_tab()

    assert (
        prescription_page
        .is_prescription_form_present()
    ), (
        "TC-NOTIFICATION-008 | STEP 1 FAILED | "
        "Không tìm thấy form kê đơn thuốc."
    )

    prescription_page.select_drug_by_index( test_data["drug_option_index"] )

    prescription_page.enter_quantity( test_data["prescription_quantity"] )

    first_dosage = ( "FIRST-" + test_data["prescription_dosage"] + "-" + unique_time )

    prescription_page.enter_dosage( first_dosage )

    prescription_page.click_add_to_prescription()

    assert (
        prescription_page
        .get_prescription_item_count()
        == 1
    ), (
        "TC-NOTIFICATION-008 | STEP 1 FAILED | "
        "Đơn thuốc thứ nhất không có đúng 1 thuốc."
    )

    prescription_page.click_save_prescription()

    first_prescription_message = ( prescription_page .get_prescription_success_message() )

    assert (
        first_prescription_message
        == "Kê đơn thuốc thành công."
    ), (
        "TC-NOTIFICATION-008 | STEP 1 FAILED | "
        f"Không lưu được đơn thuốc thứ nhất. "
        f"Actual: {first_prescription_message}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description=(
            f"Chuẩn bị appointment #{appointment_id}, "
            "hồ sơ bệnh án và đơn thuốc thứ nhất thành công"
        )
    )

    # ============================================================
    # Step 2:
    # Patient ghi nhận notification của đơn thuốc thứ nhất.
    # ============================================================

    logout_current_user( driver )

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    notification_page = NotificationPage( driver )

    notification_page.open_page()

    assert (
        notification_page
        .get_page_title()
        == "Thông báo của tôi"
    ), (
        "TC-NOTIFICATION-008 | STEP 2 FAILED | "
        "Không mở đúng trang Thông báo."
    )

    first_notification = (
        notification_page
        .get_latest_notification_by_type_and_keyword(
            test_data["notification_type"],
            test_data["expected_keyword"]
        )
    )

    assert (
        first_notification is not None
    ), (
        "TC-NOTIFICATION-008 | STEP 2 FAILED | "
        "Không tìm thấy notification của đơn thuốc thứ nhất."
    )

    first_notification_content = ( notification_page .get_notification_content( first_notification ) )

    first_notification_time = ( notification_page .get_notification_time( first_notification ) )

    assert (
        first_notification_time.strip()
        != ""
    ), (
        "TC-NOTIFICATION-008 | STEP 2 FAILED | "
        "Notification đơn thuốc thứ nhất không có thời gian."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description=(
            "Ghi nhận notification của đơn thuốc thứ nhất thành công"
        )
    )

    # ============================================================
    # Step 3:
    # Đăng nhập lại bằng Doctor.
    # ============================================================

    logout_current_user( driver )

    login_account( driver, test_data["doctor_username"], test_data["doctor_password"] )

    report_step( test_case_id=test_case_id, step_number=3, description="Đăng nhập lại Doctor thành công" )

    # ============================================================
    # Step 4:
    # Doctor mở phần Đơn thuốc của hồ sơ.
    # ============================================================

    medical_record_page = MedicalRecordPage( driver )

    medical_record_page.open_page( appointment_id )

    assert (
        medical_record_page
        .get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    ), (
        "TC-NOTIFICATION-008 | STEP 4 FAILED | "
        "Không mở đúng hồ sơ bệnh án."
    )

    prescription_page = PrescriptionPage( driver )

    prescription_page.open_prescription_tab()

    assert (
        prescription_page
        .is_prescription_form_present()
    ), (
        "TC-NOTIFICATION-008 | STEP 4 FAILED | "
        "Không tìm thấy form kê đơn thuốc."
    )

    report_step( test_case_id=test_case_id, step_number=4, description="Doctor mở phần Đơn thuốc thành công" )

    # ============================================================
    # Step 5:
    # Kê thêm đơn thuốc mới với dữ liệu khác.
    # ============================================================

    selected_drug = ( prescription_page .select_drug_by_index( test_data["drug_option_index"] ) )

    assert ( selected_drug != "" ), ( "TC-NOTIFICATION-008 | STEP 5 FAILED | " "Không chọn được thuốc." )

    second_quantity = ( int( test_data["prescription_quantity"] ) + 1 )

    second_dosage = ( "SECOND-" + test_data["prescription_dosage"] + "-" + unique_time )

    prescription_page.enter_quantity( second_quantity )

    prescription_page.enter_dosage( second_dosage )

    prescription_page.click_add_to_prescription()

    assert (
        prescription_page
        .get_prescription_item_count()
        == 1
    ), (
        "TC-NOTIFICATION-008 | STEP 5 FAILED | "
        "Đơn thuốc thứ hai không có đúng 1 thuốc."
    )

    report_step( test_case_id=test_case_id, step_number=5, description=( "Nhập dữ liệu cho đơn thuốc thứ hai thành công" ) )

    # ============================================================
    # Step 6:
    # Lưu đơn thuốc mới.
    # ============================================================

    prescription_page.click_save_prescription()

    second_prescription_message = ( prescription_page .get_prescription_success_message() )

    assert (
        second_prescription_message
        == "Kê đơn thuốc thành công."
    ), (
        "TC-NOTIFICATION-008 | STEP 6 FAILED | "
        f"Không lưu được đơn thuốc thứ hai. "
        f"Actual: {second_prescription_message}"
    )

    report_step( test_case_id=test_case_id, step_number=6, description="Lưu đơn thuốc thứ hai thành công" )

    # ============================================================
    # Step 7:
    # Đăng xuất Doctor và đăng nhập lại Patient.
    # ============================================================

    logout_current_user( driver )

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    report_step(
        test_case_id=test_case_id,
        step_number=7,
        description=(
            "Đăng xuất Doctor và đăng nhập lại Patient thành công"
        )
    )

    # ============================================================
    # Step 8:
    # Patient mở trang Thông báo.
    # ============================================================

    notification_page = NotificationPage( driver )

    notification_page.open_page()

    assert (
        notification_page
        .get_page_title()
        == "Thông báo của tôi"
    ), (
        "TC-NOTIFICATION-008 | STEP 8 FAILED | "
        "Không mở đúng trang Thông báo."
    )

    report_step( test_case_id=test_case_id, step_number=8, description="Patient mở trang Thông báo thành công" )

    # ============================================================
    # Step 9:
    # Tìm và kiểm tra notification mới
    # của đơn thuốc thứ hai.
    # ============================================================

    second_notification = (
        notification_page
        .get_latest_notification_by_type_and_keyword(
            test_data["notification_type"],
            test_data["expected_keyword"]
        )
    )

    assert (
        second_notification is not None
    ), (
        "TC-NOTIFICATION-008 | STEP 9 FAILED | "
        "Không tìm thấy notification của đơn thuốc thứ hai."
    )

    second_notification_type = ( notification_page .get_notification_type( second_notification ) )

    second_notification_content = ( notification_page .get_notification_content( second_notification ) )

    second_notification_time = ( notification_page .get_notification_time( second_notification ) )

    assert (
        second_notification_type
        == test_data["notification_type"]
    ), (
        "TC-NOTIFICATION-008 | STEP 9 FAILED | "
        f"Expected type: {test_data['notification_type']} | "
        f"Actual: {second_notification_type}"
    )

    normalized_expected = ( notification_page .normalize_text( test_data["expected_keyword"] ) )

    normalized_second_content = ( notification_page .normalize_text( second_notification_content ) )

    assert (
        normalized_expected
        in normalized_second_content
    ), (
        "TC-NOTIFICATION-008 | STEP 9 FAILED | "
        f"Expected keyword: {test_data['expected_keyword']} | "
        f"Actual: {second_notification_content}"
    )

    assert (
        second_notification_content
        != first_notification_content
    ), (
        "TC-NOTIFICATION-008 | STEP 9 FAILED | "
        "Notification của đơn thuốc mới bị trùng "
        "với notification của đơn thuốc cũ."
    )

    assert (
        second_notification_time.strip()
        != ""
    ), (
        "TC-NOTIFICATION-008 | STEP 9 FAILED | "
        "Notification mới không có thời gian."
    )

    try:
        datetime.strptime( second_notification_time, test_data["time_format"] )

    except ValueError as exc:
        pytest.fail(
            "TC-NOTIFICATION-008 | STEP 9 FAILED | "
            f"Thời gian '{second_notification_time}' không đúng format "
            f"'{test_data['time_format']}'. Error: {exc}"
        )

    assert (
        first_notification_time.strip()
        != ""
    ), (
        "TC-NOTIFICATION-008 | STEP 9 FAILED | "
        "Notification cũ bị mất thời gian hiển thị."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=9,
        description=(
            "Patient nhận notification mới của đơn thuốc thứ hai, "
            "không trùng notification cũ và đúng định dạng thời gian"
        )
    )


def test_tc_notification_009_patient_receives_new_notification_after_doctor_updates_existing_medical_record(
        driver):
    """
    TC-NOTIFICATION-009:

    Kiểm tra Patient nhận được notification mới
    sau khi Doctor chỉnh sửa Chẩn đoán và Hướng điều trị
    của một hồ sơ bệnh án đã tồn tại.
    """

    test_case_id = "TC-NOTIFICATION-009"

    test_data = get_test_data_csv( NOTIFICATION_TEST_DATA_CSV, test_case_id )

    # ============================================================
    # Step 1:
    # Chuẩn bị Patient đã có hồ sơ bệnh án.
    # - Patient đặt lịch.
    # - Admin xác nhận.
    # - Doctor tạo hồ sơ bệnh án ban đầu.
    # - Patient ghi nhận số notification trước khi update.
    # ============================================================

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    doctor_id = int( test_data["doctor_id"] )

    appointment_api = AppointmentApi()

    # ------------------------------------------------------------
    # Chuẩn bị slot.
    # Nếu hết slot thì tự tạo schedule test.
    # ------------------------------------------------------------

    booking_slot = get_or_create_booking_slot(
        doctor_id=doctor_id,
        test_data=test_data,
        schedule_note="SELENIUM-TC-NOTIFICATION-009"
    )

    booking_date = ( booking_slot["booking_date"] )

    booking_time = ( booking_slot["booking_time"] )

    unique_time = str( int(time.time()) )

    note = ( test_data["note_prefix"] + unique_time )

    doctor_page = DoctorPage( driver )

    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage( driver )

    booking_page.enter_date( booking_date )

    booking_page.enter_time( booking_time )

    actual_booking_time = ( booking_page.get_time_value() )

    assert (
        actual_booking_time
        == booking_time
    ), (
        "TC-NOTIFICATION-009 | STEP 1 FAILED | "
        f"Expected booking time: {booking_time} | "
        f"Actual: {actual_booking_time}"
    )

    booking_page.enter_notes( note )

    booking_page.click_booking_button()

    booking_message = ( booking_page.get_message() )

    assert (
        "Đặt lịch thành công"
        in booking_message
    ), (
        "TC-NOTIFICATION-009 | STEP 1 FAILED | "
        f"Không đặt được lịch. Actual: {booking_message}"
    )

    appointment = ( appointment_api .find_appointment_by_note( doctor_id=doctor_id, note=note ) )

    appointment_id = ( appointment["appointmentId"] )

    assert (
        appointment.get("status")
        == "pending"
    ), (
        "TC-NOTIFICATION-009 | STEP 1 FAILED | "
        "Appointment sau khi tạo không ở trạng thái pending."
    )

    # Admin xác nhận lịch.
    logout_current_user( driver )

    login_account( driver, test_data["admin_username"], test_data["admin_password"] )

    admin_page = AdminAppointmentPage( driver )

    admin_page.open_page()

    assert (
        admin_page
        .get_appointment_id_by_note(
            note
        )
        == str(appointment_id)
    ), (
        "TC-NOTIFICATION-009 | STEP 1 FAILED | "
        f"Không tìm thấy appointment #{appointment_id}."
    )

    assert (
        admin_page
        .get_status_by_note(
            note
        )
        == "Chờ xác nhận"
    ), (
        "TC-NOTIFICATION-009 | STEP 1 FAILED | "
        "Appointment không ở trạng thái Chờ xác nhận."
    )

    admin_page.click_confirm( note )

    confirm_message = ( admin_page .get_confirm_success_message() )

    assert (
        confirm_message
        == "Xác nhận lịch hẹn thành công."
    ), (
        "TC-NOTIFICATION-009 | STEP 1 FAILED | "
        f"Actual confirm message: {confirm_message}"
    )

    admin_page.open_page()

    assert (
        admin_page
        .get_status_by_note(
            note
        )
        == "Đã xác nhận"
    ), (
        "TC-NOTIFICATION-009 | STEP 1 FAILED | "
        "Appointment chưa chuyển sang Đã xác nhận."
    )

    # Doctor tạo hồ sơ bệnh án ban đầu.
    logout_current_user( driver )

    login_account( driver, test_data["doctor_username"], test_data["doctor_password"] )

    doctor_appointment_page = DoctorAppointmentPage( driver )

    doctor_appointment_page.open_page()

    assert (
        doctor_appointment_page
        .get_note_by_id(
            appointment_id
        )
        == note
    ), (
        "TC-NOTIFICATION-009 | STEP 1 FAILED | "
        "Doctor không thấy đúng appointment."
    )

    assert (
        doctor_appointment_page
        .get_status_by_id(
            appointment_id
        )
        == "Đã xác nhận"
    ), (
        "TC-NOTIFICATION-009 | STEP 1 FAILED | "
        "Appointment phía Doctor chưa ở trạng thái Đã xác nhận."
    )

    assert (
        doctor_appointment_page
        .is_examine_button_present(
            appointment_id
        )
    ), (
        "TC-NOTIFICATION-009 | STEP 1 FAILED | "
        "Không tìm thấy nút Khám bệnh."
    )

    doctor_appointment_page.click_examine( appointment_id )

    examination_page = DoctorExaminationPage( driver )

    assert (
        examination_page.get_page_title()
        == "Khám bệnh"
    ), (
        "TC-NOTIFICATION-009 | STEP 1 FAILED | "
        "Không mở đúng trang Khám bệnh."
    )

    original_diagnosis = ( test_data["diagnosis_prefix"] + "ORIGINAL-" + unique_time )

    original_treatment = ( test_data["treatment_prefix"] + "ORIGINAL-" + unique_time )

    examination_page.enter_diagnosis( original_diagnosis )

    examination_page.enter_treatment( original_treatment )

    examination_page.click_save_medical_record()

    medical_record_page = MedicalRecordPage( driver )

    assert (
        medical_record_page
        .get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    ), (
        "TC-NOTIFICATION-009 | STEP 1 FAILED | "
        "Không mở đúng trang Chi tiết hồ sơ bệnh án."
    )

    assert (
        original_diagnosis
        in medical_record_page
        .get_diagnosis_information()
    ), (
        "TC-NOTIFICATION-009 | STEP 1 FAILED | "
        "Diagnosis ban đầu chưa được lưu đúng."
    )

    assert (
        original_treatment
        in medical_record_page
        .get_treatment_information()
    ), (
        "TC-NOTIFICATION-009 | STEP 1 FAILED | "
        "Treatment ban đầu chưa được lưu đúng."
    )

    # Patient ghi nhận số notification trước khi update.
    logout_current_user( driver )

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    notification_page = NotificationPage( driver )

    notification_page.open_page()

    notifications_before_update = ( notification_page .get_all_notification_contents() )

    notification_count_before = len( notifications_before_update )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description=(
            f"Chuẩn bị appointment #{appointment_id}, "
            "hồ sơ bệnh án ban đầu và ghi nhận "
            f"{notification_count_before} notification trước khi cập nhật"
        )
    )

    # ============================================================
    # Step 2:
    # Đăng nhập Doctor phụ trách.
    # ============================================================

    logout_current_user( driver )

    login_account( driver, test_data["doctor_username"], test_data["doctor_password"] )

    report_step( test_case_id=test_case_id, step_number=2, description="Đăng nhập Doctor phụ trách thành công" )

    # ============================================================
    # Step 3:
    # Mở hồ sơ khám của Patient.
    # ============================================================

    medical_record_page = MedicalRecordPage( driver )

    medical_record_page.open_page( appointment_id )

    record_page_title = ( medical_record_page .get_page_title() )

    assert (
        record_page_title
        == "Chi tiết hồ sơ bệnh án"
    ), (
        "TC-NOTIFICATION-009 | STEP 3 FAILED | "
        f"Expected: Chi tiết hồ sơ bệnh án | "
        f"Actual: {record_page_title}"
    )

    assert (
        original_diagnosis
        in medical_record_page
        .get_diagnosis_information()
    ), (
        "TC-NOTIFICATION-009 | STEP 3 FAILED | "
        "Không hiển thị đúng diagnosis ban đầu."
    )

    assert (
        original_treatment
        in medical_record_page
        .get_treatment_information()
    ), (
        "TC-NOTIFICATION-009 | STEP 3 FAILED | "
        "Không hiển thị đúng treatment ban đầu."
    )

    assert (
        medical_record_page
        .is_edit_button_present()
    ), (
        "TC-NOTIFICATION-009 | STEP 3 FAILED | "
        "Không tìm thấy nút Chỉnh sửa."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            f"Doctor mở hồ sơ của appointment "
            f"#{appointment_id} thành công"
        )
    )

    # ============================================================
    # Step 4:
    # Chỉnh sửa Chẩn đoán và Hướng điều trị.
    # ============================================================

    medical_record_page.click_edit_button()

    assert (
        medical_record_page
        .is_edit_form_present()
    ), (
        "TC-NOTIFICATION-009 | STEP 4 FAILED | "
        "Không tìm thấy form chỉnh sửa hồ sơ."
    )

    diagnosis_input_before = ( medical_record_page .get_diagnosis_input_value() )

    assert (
        diagnosis_input_before
        == original_diagnosis
    ), (
        "TC-NOTIFICATION-009 | STEP 4 FAILED | "
        f"Expected diagnosis cũ: {original_diagnosis} | "
        f"Actual: {diagnosis_input_before}"
    )

    treatment_input_before = ( medical_record_page .get_treatment_input_value() )

    assert (
        treatment_input_before
        == original_treatment
    ), (
        "TC-NOTIFICATION-009 | STEP 4 FAILED | "
        f"Expected treatment cũ: {original_treatment} | "
        f"Actual: {treatment_input_before}"
    )

    updated_diagnosis = ( test_data["diagnosis_prefix"] + "UPDATED-" + unique_time )

    updated_treatment = ( test_data["treatment_prefix"] + "UPDATED-" + unique_time )

    medical_record_page.enter_diagnosis( updated_diagnosis )

    medical_record_page.enter_treatment( updated_treatment )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            "Doctor chỉnh sửa Chẩn đoán và Hướng điều trị thành công"
        )
    )

    # ============================================================
    # Step 5:
    # Lưu thông tin đã cập nhật.
    # ============================================================

    medical_record_page.click_save_changes()

    update_message = ( medical_record_page .get_update_success_message() )

    assert (
        update_message
        == "Cập nhật hồ sơ bệnh án thành công."
    ), (
        "TC-NOTIFICATION-009 | STEP 5 FAILED | "
        f"Expected: Cập nhật hồ sơ bệnh án thành công. | "
        f"Actual: {update_message}"
    )

    actual_updated_diagnosis = ( medical_record_page .get_diagnosis_information() )

    assert (
        updated_diagnosis
        in actual_updated_diagnosis
    ), (
        "TC-NOTIFICATION-009 | STEP 5 FAILED | "
        "Diagnosis mới chưa được cập nhật đúng."
    )

    actual_updated_treatment = ( medical_record_page .get_treatment_information() )

    assert (
        updated_treatment
        in actual_updated_treatment
    ), (
        "TC-NOTIFICATION-009 | STEP 5 FAILED | "
        "Treatment mới chưa được cập nhật đúng."
    )

    assert (
        original_diagnosis
        not in actual_updated_diagnosis
    ), (
        "TC-NOTIFICATION-009 | STEP 5 FAILED | "
        "Diagnosis cũ vẫn còn hiển thị sau khi cập nhật."
    )

    assert (
        original_treatment
        not in actual_updated_treatment
    ), (
        "TC-NOTIFICATION-009 | STEP 5 FAILED | "
        "Treatment cũ vẫn còn hiển thị sau khi cập nhật."
    )

    report_step( test_case_id=test_case_id, step_number=5, description="Cập nhật hồ sơ bệnh án thành công" )

    # ============================================================
    # Step 6:
    # Đăng xuất Doctor và đăng nhập Patient.
    # ============================================================

    logout_current_user( driver )

    login_account( driver, test_data["patient_username"], test_data["patient_password"] )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            "Đăng xuất Doctor và đăng nhập lại Patient thành công"
        )
    )

    # ============================================================
    # Step 7:
    # Mở trang Thông báo.
    # ============================================================

    notification_page = NotificationPage( driver )

    notification_page.open_page()

    notification_page_title = ( notification_page .get_page_title() )

    assert (
        notification_page_title
        == "Thông báo của tôi"
    ), (
        "TC-NOTIFICATION-009 | STEP 7 FAILED | "
        f"Expected: Thông báo của tôi | "
        f"Actual: {notification_page_title}"
    )

    report_step( test_case_id=test_case_id, step_number=7, description="Patient mở trang Thông báo thành công" )

    # ============================================================
    # Step 8:
    # Kiểm tra có notification mới sau khi Doctor cập nhật hồ sơ.
    # ============================================================

    notifications_after_update = ( notification_page .get_all_notification_contents() )

    notification_count_after = len( notifications_after_update )

    # ------------------------------------------------------------
    # Known Bug:
    # Hiện tại hệ thống chưa phát sinh notification mới
    # sau khi Doctor cập nhật Chẩn đoán/Hướng điều trị.
    # ------------------------------------------------------------

    if (
        notification_count_after
        <= notification_count_before
    ):
        report_step(
            test_case_id=test_case_id,
            step_number=8,
            description=(
                "Không phát sinh notification mới sau khi "
                "Doctor cập nhật hồ sơ bệnh án"
            ),
            status="XFAIL",
            detail=(
                f"Before: {notification_count_before} | "
                f"After: {notification_count_after} | "
                "Known bug của hệ thống"
            )
        )

        pytest.xfail(
            "KNOWN BUG - TC-NOTIFICATION-009 | STEP 8 | "
            f"Trước khi cập nhật có {notification_count_before} notification, "
            f"sau khi cập nhật có {notification_count_after}. "
            "Hồ sơ bệnh án cập nhật thành công nhưng "
            "Patient không nhận được notification mới."
        )

    assert (
        notification_count_after
        > notification_count_before
    ), (
        "TC-NOTIFICATION-009 | STEP 8 FAILED | "
        f"Expected số notification > {notification_count_before} | "
        f"Actual: {notification_count_after}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=8,
        description=(
            "Patient nhận thêm notification mới "
            "sau khi Doctor cập nhật hồ sơ bệnh án"
        )
    )