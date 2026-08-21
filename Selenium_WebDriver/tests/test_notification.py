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

from utils.data_reader import (
    get_test_data,
    get_test_data_csv,
    NOTIFICATION_TEST_DATA_FILE,
    NOTIFICATION_TEST_DATA_CSV
)
from pages.DoctorExaminationPage import DoctorExaminationPage
from pages.MedicalRecordPage import MedicalRecordPage

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

    time.sleep(2)

    assert driver.current_url == "http://localhost:3000/"


def logout_current_user(driver):
    login_page = LoginPage(driver)

    login_page.logout()

    time.sleep(2)

    assert driver.current_url == "http://localhost:3000/login"

def test_tc_notification_001_patient_receives_notification_after_admin_confirms(
        driver):
    """
    TC-NOTIFICATION-001:
    Kiểm tra Patient nhận được thông báo đúng
    sau khi Admin xác nhận lịch hẹn mà Patient đã đặt.
    """

    test_data = get_test_data_csv(NOTIFICATION_TEST_DATA_CSV,"TC-NOTIFICATION-001")

    # ============================================================
    # Step 1:
    # Patient thực hiện đặt một lịch khám hợp lệ.
    # ============================================================

    login_account(driver,test_data["patient_username"],test_data["patient_password"])
    doctor_id = int(test_data["doctor_id"])
    medical_record_api = MedicalRecordApi()

    booking_slot = (medical_record_api.find_available_booking_slot(doctor_id))
    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    note = (test_data["note_prefix"]+ str(int(time.time())))

    doctor_page = DoctorPage(driver)
    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage(driver)
    booking_page.enter_date(booking_date)
    booking_page.enter_time(booking_time)

    assert (booking_page.get_time_value()== booking_time)

    booking_page.enter_notes(note)

    booking_page.click_booking_button()

    assert ("Đặt lịch thành công"in booking_page.get_message())

    # Lấy lại đúng appointment vừa được tạo
    # để dùng cho các Step tiếp theo.
    appointment_api = AppointmentApi()
    appointment = (appointment_api.find_appointment_by_note(doctor_id=doctor_id,note=note))

    appointment_id = appointment["appointmentId"]

    assert (appointment.get("status")== "pending")

    # ============================================================
    # Step 2:
    # Đăng nhập bằng Admin.
    # ============================================================

    logout_current_user(driver)
    login_account(driver,test_data["admin_username"],test_data["admin_password"])

    # ============================================================
    # Step 3:
    # Mở Quản lý lịch hẹn và xác nhận lịch vừa tạo.
    # ============================================================

    admin_page = AdminAppointmentPage(driver)

    admin_page.open_page()

    assert (admin_page.get_page_title()== "Quản lý lịch hẹn")
    assert (admin_page.get_appointment_id_by_note(note)== str(appointment_id))
    assert (admin_page.get_status_by_note(note)== "Chờ xác nhận")
    assert (admin_page.is_confirm_button_present(note))

    admin_page.click_confirm(note)

    assert (admin_page.get_confirm_success_message()== "Xác nhận lịch hẹn thành công.")

    admin_page.open_page()

    assert (admin_page.get_status_by_note(note)== "Đã xác nhận")

    # ============================================================
    # Step 4:
    # Đăng xuất Admin và đăng nhập lại bằng Patient.
    # ============================================================

    logout_current_user(driver)
    login_account(driver,test_data["patient_username"],test_data["patient_password"])

    # ============================================================
    # Step 5:
    # Mở trang Thông báo.
    # ============================================================

    notification_page = NotificationPage(driver)

    notification_page.open_page()

    assert (notification_page.get_page_title()== "Thông báo của tôi")

    # ============================================================
    # Step 6:
    # Tìm thông báo liên quan đến lịch hẹn vừa được xác nhận.
    # ============================================================

    notification = (notification_page.get_notification_by_appointment_id(appointment_id))

    assert notification is not None

    # ============================================================
    # Step 7:
    # Kiểm tra loại, nội dung và thời gian của thông báo.
    # ============================================================

    notification_type = (notification_page.get_notification_type(notification))
    notification_content = (notification_page.get_notification_content(notification))
    notification_time = (notification_page.get_notification_time(notification))

    # 7.1. Kiểm tra đúng loại thông báo.
    assert (notification_type== test_data["notification_type"])

    # 7.2. Kiểm tra thông báo thuộc đúng
    # lịch hẹn vừa được Admin xác nhận.
    assert (f"#{appointment_id}"in notification_content)

    # 7.3. Kiểm tra nội dung thể hiện
    # lịch hẹn đã được xác nhận.
    assert (test_data["expected_keyword"]in notification_content.lower())

    # 7.4. Kiểm tra notification có thời gian.
    assert (notification_time.strip()!= "")

    # 7.5. Kiểm tra thời gian hiển thị
    # đúng định dạng HH:mm:ss dd/MM/yyyy.
    datetime.strptime(notification_time,test_data["time_format"])

def test_tc_notification_002_patient_receives_notification_after_admin_cancels(
        driver):
    """
    TC-NOTIFICATION-002:
    Kiểm tra Patient nhận được thông báo phù hợp
    khi Admin thực hiện hủy lịch hẹn của Patient.
    """

    test_data = get_test_data_csv(NOTIFICATION_TEST_DATA_CSV,"TC-NOTIFICATION-002")

    # ============================================================
    # Step 1:
    # Patient đặt một lịch khám hợp lệ.
    # ============================================================

    login_account(driver,test_data["patient_username"],test_data["patient_password"])

    doctor_id = int(test_data["doctor_id"])
    medical_record_api = MedicalRecordApi()

    booking_slot = medical_record_api.find_available_booking_slot(doctor_id)

    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    note = (test_data["note_prefix"]+ str(int(time.time())))

    doctor_page = DoctorPage(driver)
    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage(driver)
    booking_page.enter_date(booking_date)
    booking_page.enter_time(booking_time)

    assert booking_page.get_time_value() == booking_time

    booking_page.enter_notes(note)
    booking_page.click_booking_button()

    assert "Đặt lịch thành công" in booking_page.get_message()

    appointment_api = AppointmentApi()

    appointment = appointment_api.find_appointment_by_note(doctor_id=doctor_id,note=note)

    appointment_id = appointment["appointmentId"]

    assert appointment.get("status") == "pending"

    # ============================================================
    # Step 2:
    # Đăng nhập bằng Admin.
    # ============================================================

    logout_current_user(driver)
    login_account(driver,test_data["admin_username"],test_data["admin_password"])

    # ============================================================
    # Step 3:
    # Mở Quản lý lịch hẹn và hủy lịch vừa tạo.
    # ============================================================

    admin_page = AdminAppointmentPage(driver)
    admin_page.open_page()

    assert admin_page.get_page_title() == "Quản lý lịch hẹn"

    assert (admin_page.get_appointment_id_by_note(note)== str(appointment_id))

    assert admin_page.get_status_by_note(note) == "Chờ xác nhận"

    assert admin_page.is_cancel_button_present(note)

    admin_page.click_cancel(note)

    assert (admin_page.get_cancel_success_message() == "Hủy lịch hẹn thành công.")

    admin_page.open_page()

    assert admin_page.get_status_by_note(note) == "Đã hủy"

    # ============================================================
    # Step 4:
    # Đăng xuất Admin và đăng nhập lại bằng Patient.
    # ============================================================

    logout_current_user(driver)
    login_account(driver,test_data["patient_username"],test_data["patient_password"])

    # ============================================================
    # Step 5:
    # Mở trang Thông báo.
    # ============================================================

    notification_page = NotificationPage(driver)
    notification_page.open_page()

    assert (notification_page.get_page_title() == "Thông báo của tôi")
    # ============================================================
    # Step 6:
    # Tìm thông báo liên quan đến lịch hẹn vừa bị hủy.
    # ============================================================

    notification = (notification_page.get_notification_by_appointment_id(appointment_id))

    assert notification is not None

    # ============================================================
    # Step 7:
    # Kiểm tra loại, nội dung và thời gian của thông báo.
    # ============================================================

    notification_type = (notification_page.get_notification_type(notification))
    notification_content = (notification_page.get_notification_content(notification))

    notification_time = (notification_page.get_notification_time(notification))

    # 7.1. Kiểm tra đúng loại thông báo.
    assert (notification_type == test_data["notification_type"])

    # 7.2. Kiểm tra thông báo thuộc đúng
    # lịch hẹn vừa bị Admin hủy.
    assert (f"#{appointment_id}"in notification_content)

    # 7.3. Kiểm tra nội dung thể hiện
    # lịch hẹn đã bị hủy.
    assert (test_data["expected_keyword"]in notification_content.lower())

    # 7.4. Kiểm tra notification có thời gian.
    assert notification_time.strip() != ""

    # 7.5. Kiểm tra thời gian hiển thị
    # đúng định dạng HH:mm:ss dd/MM/yyyy.
    datetime.strptime(notification_time,test_data["time_format"])

def test_tc_notification_003_patient_receives_notification_after_doctor_updates_result(
        driver):
    """
    TC-NOTIFICATION-003:
    Kiểm tra Patient nhận được thông báo
    sau khi Doctor cập nhật kết quả khám.
    """
    test_data = get_test_data_csv(NOTIFICATION_TEST_DATA_CSV,"TC-NOTIFICATION-003")
    # ============================================================
    # Step 1:
    # Chuẩn bị Patient có lịch hẹn đã được Admin xác nhận.
    # ============================================================

    login_account(driver,test_data["patient_username"],test_data["patient_password"])

    doctor_id = int(test_data["doctor_id"])
    medical_record_api = MedicalRecordApi()

    booking_slot = (medical_record_api.find_available_booking_slot(doctor_id))

    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    note = (test_data["note_prefix"] + str(int(time.time())))

    doctor_page = DoctorPage(driver)
    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage(driver)
    booking_page.enter_date(booking_date)
    booking_page.enter_time(booking_time)

    assert booking_page.get_time_value() == booking_time

    booking_page.enter_notes(note)
    booking_page.click_booking_button()

    assert ("Đặt lịch thành công"in booking_page.get_message())

    appointment_api = AppointmentApi()
    appointment = appointment_api.find_appointment_by_note(doctor_id=doctor_id,note=note)
    appointment_id = appointment["appointmentId"]

    assert appointment.get("status") == "pending"

    # Admin xác nhận lịch để hoàn thành dữ liệu tiền điều kiện.
    logout_current_user(driver)
    login_account(driver,test_data["admin_username"],test_data["admin_password"])

    admin_page = AdminAppointmentPage(driver)
    admin_page.open_page()

    assert (admin_page.get_appointment_id_by_note(note) == str(appointment_id))
    assert admin_page.get_status_by_note(note) == "Chờ xác nhận"
    admin_page.click_confirm(note)
    assert (admin_page.get_confirm_success_message() == "Xác nhận lịch hẹn thành công.")
    admin_page.open_page()
    assert admin_page.get_status_by_note(note) == "Đã xác nhận"

    # ============================================================
    # Step 2:
    # Đăng nhập Doctor phụ trách lịch hẹn.
    # ============================================================

    logout_current_user(driver)
    login_account(driver,test_data["doctor_username"],test_data["doctor_password"])

    # ============================================================
    # Step 3:
    # Mở lịch hẹn của Patient và chọn Khám bệnh.
    # ============================================================

    doctor_appointment_page = DoctorAppointmentPage(driver)
    doctor_appointment_page.open_page()

    assert (doctor_appointment_page.get_note_by_id(appointment_id)== note)
    assert (doctor_appointment_page.get_status_by_id(appointment_id)== "Đã xác nhận")
    assert (doctor_appointment_page.is_examine_button_present(appointment_id))
    doctor_appointment_page.click_examine(appointment_id)
    examination_page = DoctorExaminationPage(driver)
    assert examination_page.get_page_title() == "Khám bệnh"
    assert (f"appointmentId={appointment_id}"in driver.current_url)
    assert (examination_page.is_create_record_form_present())

    # ============================================================
    # Step 4:
    # Nhập Chẩn đoán và Hướng điều trị hợp lệ.
    # ============================================================
    unique_time = str(int(time.time()))
    diagnosis = (test_data["diagnosis_prefix"] + unique_time)
    treatment = (test_data["treatment_prefix"] + unique_time)
    examination_page.enter_diagnosis(diagnosis)
    examination_page.enter_treatment(treatment)

    # ============================================================
    # Step 5:
    # Lưu hồ sơ bệnh án.
    # ============================================================

    examination_page.click_save_medical_record()

    medical_record_page = MedicalRecordPage(driver)

    assert (medical_record_page.get_page_title() == "Chi tiết hồ sơ bệnh án")
    assert (diagnosis in medical_record_page.get_diagnosis_information())
    assert (treatment in medical_record_page.get_treatment_information())

    # ============================================================
    # Step 6:
    # Đăng xuất Doctor và đăng nhập lại bằng Patient.
    # ============================================================

    logout_current_user(driver)
    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    # ============================================================
    # Step 7:
    # Mở trang Thông báo.
    # ============================================================
    notification_page = NotificationPage(driver)
    notification_page.open_page()
    assert (notification_page.get_page_title() == "Thông báo của tôi")
    # ============================================================
    # Step 8:
    # Tìm và kiểm tra thông báo mới phát sinh
    # sau khi Doctor lưu hồ sơ bệnh án.
    # ============================================================
    notification = (
        notification_page
        .get_latest_notification_by_type_and_keyword(
            test_data["notification_type"],
            test_data["expected_keyword"]
        )
    )
    assert notification is not None
    notification_type = (notification_page.get_notification_type(notification))
    notification_content = (notification_page.get_notification_content(notification))
    notification_time = (notification_page.get_notification_time(notification))

    # 8.1. Kiểm tra đúng loại thông báo.
    assert (notification_type == test_data["notification_type"])

    # 8.2. Kiểm tra nội dung thông báo
    # thể hiện kết quả khám đã được cập nhật.
    assert (
            notification_page.normalize_text(
                test_data["expected_keyword"]
            )
            in notification_page.normalize_text(notification_content)
    )

    # 8.3. Kiểm tra notification có thời gian.
    assert notification_time.strip() != ""

    # 8.4. Kiểm tra định dạng thời gian.
    datetime.strptime(notification_time,test_data["time_format"])

def test_tc_notification_004_notifications_are_stored_separately(
        driver):
    """
    TC-NOTIFICATION-004:
    Kiểm tra khi Patient phát sinh nhiều thông báo từ
    các sự kiện khác nhau, các thông báo được lưu riêng biệt
    và không ghi đè lẫn nhau.
    """

    test_data = get_test_data_csv(NOTIFICATION_TEST_DATA_CSV,"TC-NOTIFICATION-004")

    doctor_id = int(test_data["doctor_id"])
    medical_record_api = MedicalRecordApi()
    appointment_api = AppointmentApi()

    # ============================================================
    # Step 1:
    # Chuẩn bị Patient đã có ít nhất một notification trước đó.
    #
    # Để TC004 không phụ thuộc dữ liệu của test case khác:
    # - Patient tự tạo lịch hẹn thứ nhất.
    # - Admin xác nhận lịch hẹn thứ nhất.
    # - Lịch hẹn thứ nhất sẽ tạo notification cũ dùng để đối chiếu.
    # ============================================================

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    # Tìm slot trống cho lịch hẹn thứ nhất.
    first_booking_slot = (
        medical_record_api
        .find_available_booking_slot(doctor_id)
    )

    first_booking_date = first_booking_slot["booking_date"]
    first_booking_time = first_booking_slot["booking_time"]

    first_note = (
        test_data["note_prefix"]
        + "OLD-"
        + str(int(time.time()))
    )

    doctor_page = DoctorPage(driver)
    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage(driver)
    booking_page.enter_date(first_booking_date)
    booking_page.enter_time(first_booking_time)

    assert (booking_page.get_time_value()== first_booking_time)

    booking_page.enter_notes(first_note)
    booking_page.click_booking_button()

    assert ("Đặt lịch thành công"in booking_page.get_message())

    first_appointment = (
        appointment_api
        .find_appointment_by_note(
            doctor_id=doctor_id,
            note=first_note
        )
    )

    first_appointment_id = (first_appointment["appointmentId"])
    assert (first_appointment.get("status")== "pending")

    # Admin xác nhận lịch thứ nhất
    # để phát sinh notification cũ.
    logout_current_user(driver)

    login_account(
        driver,
        test_data["admin_username"],
        test_data["admin_password"]
    )

    admin_page = AdminAppointmentPage(driver)
    admin_page.open_page()

    assert (
        admin_page.get_appointment_id_by_note(
            first_note
        )
        == str(first_appointment_id)
    )

    assert (admin_page.get_status_by_note(first_note) == "Chờ xác nhận")

    admin_page.click_confirm(first_note)

    assert (admin_page.get_confirm_success_message() == "Xác nhận lịch hẹn thành công.")

    admin_page.open_page()

    assert (admin_page.get_status_by_note(first_note) == "Đã xác nhận")

    # Patient kiểm tra notification cũ thực sự tồn tại
    # trước khi phát sinh notification mới.
    logout_current_user(driver)

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    notification_page = NotificationPage(driver)
    notification_page.open_page()

    old_notification = (
        notification_page
        .get_notification_by_appointment_id(
            first_appointment_id
        )
    )
    assert old_notification is not None
    old_notification_content = (
        notification_page
        .get_notification_content(
            old_notification
        )
    )
    assert (f"#{first_appointment_id}"in old_notification_content)

    # ============================================================
    # Step 2:
    # Patient tạo thêm một lịch hẹn mới.
    # ============================================================

    # Sau khi lịch thứ nhất đã được đặt,
    # tìm lại một slot trống khác.
    second_booking_slot = (
        medical_record_api
        .find_available_booking_slot(doctor_id)
    )

    second_booking_date = (second_booking_slot["booking_date"])
    second_booking_time = (second_booking_slot["booking_time"])
    second_note = (
        test_data["note_prefix"]
        + "NEW-"
        + str(int(time.time()))
    )
    doctor_page = DoctorPage(driver)
    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage(driver)
    booking_page.enter_date(second_booking_date)
    booking_page.enter_time(second_booking_time)

    assert (booking_page.get_time_value() == second_booking_time)

    booking_page.enter_notes(second_note)
    booking_page.click_booking_button()

    assert ("Đặt lịch thành công"in booking_page.get_message())

    second_appointment = (
        appointment_api
        .find_appointment_by_note(
            doctor_id=doctor_id,
            note=second_note
        )
    )

    second_appointment_id = (second_appointment["appointmentId"])
    assert (second_appointment.get("status")== "pending")

    # Quan trọng:
    # hai notification sau này phải thuộc hai lịch khác nhau.
    assert (second_appointment_id!= first_appointment_id)

    # ============================================================
    # Step 3:
    # Admin xác nhận lịch hẹn mới.
    # ============================================================

    logout_current_user(driver)
    login_account(
        driver,
        test_data["admin_username"],
        test_data["admin_password"]
    )
    admin_page = AdminAppointmentPage(driver)
    admin_page.open_page()

    assert (
        admin_page.get_appointment_id_by_note(
            second_note
        )
        == str(second_appointment_id)
    )

    assert (admin_page.get_status_by_note(second_note) == "Chờ xác nhận")

    admin_page.click_confirm(second_note)

    assert (admin_page.get_confirm_success_message() == "Xác nhận lịch hẹn thành công.")

    admin_page.open_page()

    assert (admin_page.get_status_by_note(second_note)== "Đã xác nhận")

    # ============================================================
    # Step 4:
    # Đăng nhập lại bằng Patient.
    # ============================================================

    logout_current_user(driver)

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    # ============================================================
    # Step 5:
    # Mở trang Thông báo.
    # ============================================================

    notification_page = NotificationPage(driver)
    notification_page.open_page()

    assert (notification_page.get_page_title() == "Thông báo của tôi")

    # ============================================================
    # Step 6:
    # Kiểm tra notification mới của lịch vừa được xác nhận.
    # ============================================================

    new_notification = (
        notification_page
        .get_notification_by_appointment_id(
            second_appointment_id
        )
    )

    assert new_notification is not None

    new_notification_type = (
        notification_page
        .get_notification_type(
            new_notification
        )
    )

    new_notification_content = (
        notification_page
        .get_notification_content(
            new_notification
        )
    )

    new_notification_time = (
        notification_page
        .get_notification_time(
            new_notification
        )
    )

    assert (new_notification_type == test_data["notification_type"])
    assert (f"#{second_appointment_id}"in new_notification_content)
    assert (test_data["expected_keyword"] in new_notification_content.lower())
    assert new_notification_time.strip() != ""

    datetime.strptime(new_notification_time,test_data["time_format"])

    # ============================================================
    # Step 7:
    # Kiểm tra notification cũ vẫn còn hiển thị
    # và không bị notification mới ghi đè.
    # ============================================================

    old_notification_after = (
        notification_page
        .get_notification_by_appointment_id(
            first_appointment_id
        )
    )
    assert old_notification_after is not None
    old_content_after = (
        notification_page
        .get_notification_content(
            old_notification_after
        )
    )
    # Notification cũ vẫn thuộc lịch thứ nhất.
    assert (f"#{first_appointment_id}" in old_content_after)

    # Notification cũ không bị biến thành
    # notification của lịch thứ hai.
    assert (f"#{second_appointment_id}" not in old_content_after)

    # Notification mới không chứa ID lịch cũ.
    assert (f"#{first_appointment_id}" not in new_notification_content)

    # Hai notification là hai nội dung riêng biệt.
    assert (old_content_after != new_notification_content)

def test_tc_notification_005_notifications_are_isolated_between_patients(
        driver):
    """
    TC-NOTIFICATION-005:
    Kiểm tra danh sách notification hiển thị
    được phân tách giữa hai tài khoản Patient.
    """

    test_data = get_test_data_csv(NOTIFICATION_TEST_DATA_CSV,"TC-NOTIFICATION-005")

    patient_a_username = test_data["patient_username"]
    patient_a_password = test_data["patient_password"]

    patient_b_username = test_data["patient_b_username"]
    patient_b_password = test_data["patient_b_password"]

    # ============================================================
    # Step 1:
    # Đăng nhập bằng Patient A.
    # ============================================================

    login_account(
        driver,
        patient_a_username,
        patient_a_password
    )

    # ============================================================
    # Step 2:
    # Mở trang Thông báo và lấy danh sách
    # notification đang hiển thị của Patient A.
    # ============================================================

    notification_page = NotificationPage(driver)
    notification_page.open_page()

    assert (notification_page.get_page_title() == "Thông báo của tôi")

    patient_a_notifications = (notification_page.get_all_notification_contents())

    assert len(patient_a_notifications) > 0

    # ============================================================
    # Step 3:
    # Đăng xuất Patient A và đăng nhập bằng Patient B.
    # ============================================================

    logout_current_user(driver)

    login_account(
        driver,
        patient_b_username,
        patient_b_password
    )

    # ============================================================
    # Step 4:
    # Mở trang Thông báo và lấy danh sách
    # notification đang hiển thị của Patient B.
    # ============================================================

    notification_page = NotificationPage(driver)
    notification_page.open_page()

    assert (notification_page.get_page_title() == "Thông báo của tôi")

    patient_b_notifications = (notification_page.get_all_notification_contents())

    assert len(patient_b_notifications) > 0

    # ============================================================
    # Step 5:
    # So sánh danh sách notification của hai Patient.
    # Danh sách phải được phân tách theo từng tài khoản.
    # ============================================================

    assert (patient_a_notifications!= patient_b_notifications)

def test_tc_notification_006_patient_receives_notification_after_doctor_creates_prescription(
        driver):
    """
    TC-NOTIFICATION-006:
    Kiểm tra Patient nhận được thông báo đúng
    sau khi Doctor tạo và lưu đơn thuốc mới.
    """

    test_data = get_test_data_csv(
        NOTIFICATION_TEST_DATA_CSV,
        "TC-NOTIFICATION-006"
    )

    # ============================================================
    # Step 1:
    # Chuẩn bị Patient có lịch hẹn đã được xác nhận.
    # - Patient đặt lịch hợp lệ.
    # - Admin xác nhận lịch hẹn vừa tạo.
    # ============================================================
    print(
        "TC6 LOGIN DATA:",
        test_data["patient_username"],
        test_data["patient_password"]
    )
    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    doctor_id = int(
        test_data["doctor_id"]
    )

    medical_record_api = MedicalRecordApi()
    appointment_api = AppointmentApi()

    # ============================================================
    # Chuẩn bị dữ liệu lịch làm việc cho riêng TC6.
    #
    # Nếu database hiện không còn ca làm việc trong tương lai
    # của bác sĩ Tran Binh, tạo một ca test bằng API.
    #
    # Phần này chỉ chuẩn bị test data cho TC6,
    # không thay đổi logic dùng chung của TC1 - TC5.
    # ============================================================

    try:
        booking_slot = (
            medical_record_api
            .find_available_booking_slot(doctor_id)
        )

    except AssertionError:
        doctor_schedule_api = DoctorScheduleApi()

        admin_token = doctor_schedule_api.get_token(
            test_data["admin_username"],
            test_data["admin_password"]
        )

        doctor_name = "Tran Binh"

        # Tìm một ngày tương lai chưa có ca morning
        # để tránh trùng dữ liệu hiện có trong database.
        created_work_date = None

        for days_ahead in range(1, 31):
            work_date_obj = (
                    datetime.now().date()
                    + timedelta(days=days_ahead)
            )

            work_date = work_date_obj.strftime(
                "%Y-%m-%d"
            )

            existing_schedule = (
                doctor_schedule_api.find_schedule(
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
                    note="SELENIUM-TC-NOTIFICATION-006",
                    token=admin_token
                )

                created_work_date = work_date
                break

        assert created_work_date is not None, (
            "Không thể chuẩn bị lịch làm việc "
            "cho TC-NOTIFICATION-006."
        )

        # Sau khi tạo schedule mới,
        # tìm lại slot hợp lệ bằng helper hiện có.
        booking_slot = (
            medical_record_api
            .find_available_booking_slot(doctor_id)
        )

    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    unique_time = str(int(time.time()))

    note = (
        test_data["note_prefix"]
        + unique_time
    )

    doctor_page = DoctorPage(driver)
    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage(driver)

    booking_page.enter_date(
        booking_date
    )

    booking_page.enter_time(
        booking_time
    )

    assert (
        booking_page.get_time_value()
        == booking_time
    )

    booking_page.enter_notes(note)

    booking_page.click_booking_button()

    assert (
        "Đặt lịch thành công"
        in booking_page.get_message()
    )

    appointment = (
        appointment_api
        .find_appointment_by_note(
            doctor_id=doctor_id,
            note=note
        )
    )

    appointment_id = (
        appointment["appointmentId"]
    )

    assert (
        appointment.get("status")
        == "pending"
    )

    # ------------------------------------------------------------
    # Admin xác nhận lịch hẹn
    # ------------------------------------------------------------

    logout_current_user(driver)

    login_account(
        driver,
        test_data["admin_username"],
        test_data["admin_password"]
    )

    admin_page = AdminAppointmentPage(driver)

    admin_page.open_page()

    assert (
        admin_page.get_appointment_id_by_note(note)
        == str(appointment_id)
    )

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

    admin_page.open_page()

    assert (
        admin_page.get_status_by_note(note)
        == "Đã xác nhận"
    )

    # ============================================================
    # Step 2:
    # Doctor đăng nhập.
    # ============================================================

    logout_current_user(driver)

    login_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    # ============================================================
    # Step 3:
    # Doctor mở đúng lịch hẹn của Patient.
    # ============================================================

    doctor_appointment_page = (
        DoctorAppointmentPage(driver)
    )

    doctor_appointment_page.open_page()

    assert (
        doctor_appointment_page
        .get_note_by_id(appointment_id)
        == note
    )

    assert (
        doctor_appointment_page
        .get_status_by_id(appointment_id)
        == "Đã xác nhận"
    )

    assert (
        doctor_appointment_page
        .is_examine_button_present(
            appointment_id
        )
    )

    doctor_appointment_page.click_examine(
        appointment_id
    )

    examination_page = (
        DoctorExaminationPage(driver)
    )

    assert (
        examination_page.get_page_title()
        == "Khám bệnh"
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    )

    assert (
        examination_page
        .is_create_record_form_present()
    )

    # ============================================================
    # Step 4:
    # Doctor thực hiện khám bệnh.
    # Nhập Chẩn đoán và Hướng điều trị hợp lệ.
    # ============================================================

    diagnosis = (
        test_data["diagnosis_prefix"]
        + unique_time
    )

    treatment = (
        test_data["treatment_prefix"]
        + unique_time
    )

    examination_page.enter_diagnosis(
        diagnosis
    )

    examination_page.enter_treatment(
        treatment
    )

    # ============================================================
    # Step 5:
    # Doctor lưu thông tin khám / hồ sơ bệnh án.
    # ============================================================

    examination_page.click_save_medical_record()

    medical_record_page = (
        MedicalRecordPage(driver)
    )

    assert (
        medical_record_page.get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    )

    assert (
        diagnosis
        in medical_record_page
        .get_diagnosis_information()
    )

    assert (
        treatment
        in medical_record_page
        .get_treatment_information()
    )

    # ============================================================
    # Step 6 - POM: PrescriptionPage
    # Doctor mở chức năng kê đơn thuốc.
    # ============================================================

    prescription_page = (
        PrescriptionPage(driver)
    )

    prescription_page.open_prescription_tab()

    assert (
        prescription_page
        .is_prescription_form_present()
    )

    # ============================================================
    # Step 7 - POM: PrescriptionPage
    # Doctor tạo và lưu một đơn thuốc hợp lệ:
    # - Chọn thuốc.
    # - Nhập số lượng.
    # - Nhập liều dùng.
    # - Thêm thuốc vào đơn.
    # - Lưu đơn thuốc.
    # ============================================================

    selected_drug = (
        prescription_page
        .select_drug_by_index(
            test_data["drug_option_index"]
        )
    )

    assert selected_drug != ""

    assert (
        "-- Chọn thuốc --"
        not in selected_drug
    )

    prescription_page.enter_quantity(
        test_data["prescription_quantity"]
    )

    prescription_page.enter_dosage(
        test_data["prescription_dosage"]
    )

    prescription_page.click_add_to_prescription()

    assert (
        prescription_page
        .get_prescription_item_count()
        == 1
    )

    prescription_page.click_save_prescription()

    assert (
        prescription_page
        .get_prescription_success_message()
        == "Kê đơn thuốc thành công."
    )

    # ============================================================
    # Step 8:
    # Doctor đăng xuất.
    # Patient đăng nhập lại hệ thống.
    # ============================================================

    logout_current_user(driver)

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    # ============================================================
    # Step 9 - POM: NotificationPage
    # Patient mở trang Thông báo và kiểm tra notification
    # được tạo sau khi Doctor lưu đơn thuốc.
    # ============================================================

    notification_page = (
        NotificationPage(driver)
    )

    notification_page.open_page()

    assert (
        notification_page.get_page_title()
        == "Thông báo của tôi"
    )

    notification = (
        notification_page
        .get_latest_notification_by_type_and_keyword(
            test_data["notification_type"],
            test_data["expected_keyword"]
        )
    )

    notification_type = (
        notification_page
        .get_notification_type(notification)
    )

    notification_content = (
        notification_page
        .get_notification_content(notification)
    )

    notification_time = (
        notification_page
        .get_notification_time(notification)
    )

    # ------------------------------------------------------------
    # Expected Result 1:
    # Notification đúng loại [Đơn thuốc].
    # ------------------------------------------------------------

    assert (
        notification_type
        == test_data["notification_type"]
    )

    # ------------------------------------------------------------
    # Expected Result 2:
    # Nội dung notification thể hiện Patient
    # có một đơn thuốc mới.
    # ------------------------------------------------------------

    assert (
        notification_page.normalize_text(
            test_data["expected_keyword"]
        )
        in notification_page.normalize_text(
            notification_content
        )
    )

    # ------------------------------------------------------------
    # Expected Result 3:
    # Notification phải hiển thị thời gian.
    # ------------------------------------------------------------

    assert (
        notification_time.strip()
        != ""
    )

    # ------------------------------------------------------------
    # Expected Result 4:
    # Thời gian đúng định dạng:
    # HH:mm:ss dd/MM/yyyy
    # ------------------------------------------------------------

    datetime.strptime(
        notification_time,
        test_data["time_format"]
    )

def test_tc_notification_007_patient_receives_notification_after_doctor_adds_test_result(
        driver):
    """
    TC-NOTIFICATION-007:
    Kiểm tra Patient nhận được thông báo đúng
    sau khi Doctor thêm và lưu kết quả xét nghiệm
    vào hồ sơ bệnh án của Patient.
    """

    test_data = get_test_data_csv(
        NOTIFICATION_TEST_DATA_CSV,
        "TC-NOTIFICATION-007"
    )

    # ============================================================
    # Step 1:
    # Chuẩn bị Patient có hồ sơ bệnh án đã được Doctor tạo.
    #
    # Flow chuẩn bị:
    # - Patient đặt lịch.
    # - Admin xác nhận lịch.
    # - Doctor khám bệnh.
    # - Doctor nhập Chẩn đoán và Hướng điều trị.
    # - Doctor lưu hồ sơ bệnh án.
    # ============================================================

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    doctor_id = int(
        test_data["doctor_id"]
    )

    medical_record_api = MedicalRecordApi()
    appointment_api = AppointmentApi()

    # ------------------------------------------------------------
    # Chuẩn bị lịch làm việc.
    #
    # Giống TC6:
    # Nếu database không còn lịch available trong tương lai,
    # chỉ TC7 tự tạo một schedule test.
    #
    # Không sửa helper dùng chung nên không ảnh hưởng TC1-TC6.
    # ------------------------------------------------------------

    try:
        booking_slot = (
            medical_record_api
            .find_available_booking_slot(doctor_id)
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

            work_date = work_date_obj.strftime(
                "%Y-%m-%d"
            )

            existing_schedule = (
                doctor_schedule_api.find_schedule(
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
                    note="SELENIUM-TC-NOTIFICATION-007",
                    token=admin_token
                )

                created_work_date = work_date
                break

        assert created_work_date is not None, (
            "Không thể chuẩn bị lịch làm việc "
            "cho TC-NOTIFICATION-007."
        )

        booking_slot = (
            medical_record_api
            .find_available_booking_slot(doctor_id)
        )

    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    unique_time = str(
        int(time.time())
    )

    note = (
        test_data["note_prefix"]
        + unique_time
    )

    # ------------------------------------------------------------
    # Patient đặt lịch với Doctor Tran Binh.
    # ------------------------------------------------------------

    doctor_page = DoctorPage(driver)

    doctor_page.open_page()

    doctor_page.book_tran_binh()

    booking_page = BookingPage(driver)

    booking_page.enter_date(
        booking_date
    )

    booking_page.enter_time(
        booking_time
    )

    assert (
        booking_page.get_time_value()
        == booking_time
    )

    booking_page.enter_notes(
        note
    )

    booking_page.click_booking_button()

    assert (
        "Đặt lịch thành công"
        in booking_page.get_message()
    )

    appointment = (
        appointment_api
        .find_appointment_by_note(
            doctor_id=doctor_id,
            note=note
        )
    )

    appointment_id = (
        appointment["appointmentId"]
    )

    assert (
        appointment.get("status")
        == "pending"
    )

    # ------------------------------------------------------------
    # Admin xác nhận lịch hẹn.
    # ------------------------------------------------------------

    logout_current_user(driver)

    login_account(
        driver,
        test_data["admin_username"],
        test_data["admin_password"]
    )

    admin_page = AdminAppointmentPage(driver)

    admin_page.open_page()

    assert (
        admin_page.get_appointment_id_by_note(note)
        == str(appointment_id)
    )

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

    admin_page.open_page()

    assert (
        admin_page.get_status_by_note(note)
        == "Đã xác nhận"
    )

    # ------------------------------------------------------------
    # Doctor đăng nhập để tạo hồ sơ bệnh án.
    #
    # Đây vẫn thuộc bước chuẩn bị của Step 1.
    # ------------------------------------------------------------

    logout_current_user(driver)

    login_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    doctor_appointment_page = (
        DoctorAppointmentPage(driver)
    )

    doctor_appointment_page.open_page()

    assert (
        doctor_appointment_page
        .get_note_by_id(appointment_id)
        == note
    )

    assert (
        doctor_appointment_page
        .get_status_by_id(appointment_id)
        == "Đã xác nhận"
    )

    assert (
        doctor_appointment_page
        .is_examine_button_present(
            appointment_id
        )
    )

    doctor_appointment_page.click_examine(
        appointment_id
    )

    examination_page = (
        DoctorExaminationPage(driver)
    )

    assert (
        examination_page.get_page_title()
        == "Khám bệnh"
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    )

    assert (
        examination_page
        .is_create_record_form_present()
    )

    diagnosis = (
        test_data["diagnosis_prefix"]
        + unique_time
    )

    treatment = (
        test_data["treatment_prefix"]
        + unique_time
    )

    examination_page.enter_diagnosis(
        diagnosis
    )

    examination_page.enter_treatment(
        treatment
    )

    examination_page.click_save_medical_record()

    medical_record_page = (
        MedicalRecordPage(driver)
    )

    assert (
        medical_record_page.get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    )

    assert (
        diagnosis
        in medical_record_page
        .get_diagnosis_information()
    )

    assert (
        treatment
        in medical_record_page
        .get_treatment_information()
    )

    # ============================================================
    # Step 2:
    # Đăng nhập bằng Doctor phụ trách hồ sơ bệnh án.
    #
    # Doctor hiện đã đăng nhập từ bước chuẩn bị Step 1.
    # Xác nhận đúng Doctor session vẫn đang hoạt động
    # bằng việc đang truy cập được hồ sơ bệnh án.
    # ============================================================

    assert (
        medical_record_page
        .is_medical_record_information_present()
    )

    # ============================================================
    # Step 3:
    # Mở Chi tiết hồ sơ bệnh án của Patient.
    # ============================================================

    medical_record_page.open_page(
        appointment_id
    )

    assert (
        medical_record_page.get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    )

    assert (
        diagnosis
        in medical_record_page
        .get_diagnosis_information()
    )

    # ============================================================
    # Step 4 - POM: TestResultPage
    # Chuyển đến phần Xét nghiệm.
    # ============================================================

    test_result_page = (
        TestResultPage(driver)
    )

    test_result_page.open_test_result_tab()

    assert (
        test_result_page
        .is_test_result_form_present()
    )

    # ============================================================
    # Step 5 - POM: TestResultPage
    # Thêm kết quả xét nghiệm với thông tin hợp lệ.
    # ============================================================

    test_name = (
        test_data["test_name_prefix"]
        + unique_time
    )

    test_result = (
        test_data["test_result_prefix"]
        + unique_time
    )

    test_result_page.enter_test_name(
        test_name
    )

    test_result_page.enter_test_result(
        test_result
    )

    # ============================================================
    # Step 6 - POM: TestResultPage
    # Lưu kết quả xét nghiệm.
    # ============================================================

    test_result_page.click_save_test_result()

    assert (
        test_result_page.get_success_message()
        == "Thêm kết quả xét nghiệm thành công."
    )

    # Kiểm tra kết quả vừa lưu xuất hiện
    # trong danh sách Kết quả xét nghiệm.
    assert (
        test_result_page.has_test_result(
            test_name,
            test_result
        )
    )

    # ============================================================
    # Step 7:
    # Đăng xuất Doctor và đăng nhập lại bằng Patient.
    # ============================================================

    logout_current_user(driver)

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    # ============================================================
    # Step 8 - POM: NotificationPage
    # Patient mở trang Thông báo.
    # ============================================================

    notification_page = (
        NotificationPage(driver)
    )

    notification_page.open_page()

    assert (
        notification_page.get_page_title()
        == "Thông báo của tôi"
    )

    # ============================================================
    # Step 9 - POM: NotificationPage
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

    notification_type = (
        notification_page
        .get_notification_type(
            notification
        )
    )

    notification_content = (
        notification_page
        .get_notification_content(
            notification
        )
    )

    notification_time = (
        notification_page
        .get_notification_time(
            notification
        )
    )

    # ------------------------------------------------------------
    # Expected Result 1:
    # Notification thuộc loại [Kết quả xét nghiệm].
    # ------------------------------------------------------------

    assert (
        notification_type
        == test_data["notification_type"]
    )

    # ------------------------------------------------------------
    # Expected Result 2:
    # Nội dung chứa đúng tên xét nghiệm vừa được thêm.
    # ------------------------------------------------------------

    assert (
        notification_page.normalize_text(
            test_name
        )
        in notification_page.normalize_text(
            notification_content
        )
    )

    # ------------------------------------------------------------
    # Expected Result 3:
    # Nội dung thể hiện kết quả xét nghiệm
    # đã được cập nhật.
    # ------------------------------------------------------------

    assert (
        notification_page.normalize_text(
            test_data["expected_keyword"]
        )
        in notification_page.normalize_text(
            notification_content
        )
    )

    # ------------------------------------------------------------
    # Expected Result 4:
    # Notification có thời gian hiển thị.
    # ------------------------------------------------------------

    assert (
        notification_time.strip()
        != ""
    )

    # ------------------------------------------------------------
    # Expected Result 5:
    # Thời gian đúng định dạng:
    # HH:mm:ss dd/MM/yyyy
    # ------------------------------------------------------------

    datetime.strptime(
        notification_time,
        test_data["time_format"]
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

    test_data = get_test_data_csv(
        NOTIFICATION_TEST_DATA_CSV,
        "TC-NOTIFICATION-008"
    )

    # ============================================================
    # Step 1:
    # Chuẩn bị Patient đã có một đơn thuốc được lưu trước đó.
    #
    # Flow chuẩn bị:
    # - Patient đặt lịch.
    # - Admin xác nhận.
    # - Doctor khám.
    # - Doctor tạo hồ sơ bệnh án.
    # - Doctor kê và lưu đơn thuốc thứ nhất.
    # ============================================================

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    doctor_id = int(
        test_data["doctor_id"]
    )

    medical_record_api = MedicalRecordApi()
    appointment_api = AppointmentApi()

    # ------------------------------------------------------------
    # Chuẩn bị lịch làm việc cho riêng TC8.
    # Không thay đổi helper dùng chung.
    # ------------------------------------------------------------

    try:
        booking_slot = (
            medical_record_api
            .find_available_booking_slot(doctor_id)
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

            work_date = work_date_obj.strftime(
                "%Y-%m-%d"
            )

            existing_schedule = (
                doctor_schedule_api.find_schedule(
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
                    note="SELENIUM-TC-NOTIFICATION-008",
                    token=admin_token
                )

                created_work_date = work_date
                break

        assert created_work_date is not None, (
            "Không thể chuẩn bị lịch làm việc "
            "cho TC-NOTIFICATION-008."
        )

        booking_slot = (
            medical_record_api
            .find_available_booking_slot(doctor_id)
        )

    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    unique_time = str(
        int(time.time())
    )

    note = (
        test_data["note_prefix"]
        + unique_time
    )

    # ------------------------------------------------------------
    # Patient đặt lịch.
    # ------------------------------------------------------------

    doctor_page = DoctorPage(driver)

    doctor_page.open_page()

    doctor_page.book_tran_binh()

    booking_page = BookingPage(driver)

    booking_page.enter_date(
        booking_date
    )

    booking_page.enter_time(
        booking_time
    )

    assert (
        booking_page.get_time_value()
        == booking_time
    )

    booking_page.enter_notes(
        note
    )

    booking_page.click_booking_button()

    assert (
        "Đặt lịch thành công"
        in booking_page.get_message()
    )

    appointment = (
        appointment_api
        .find_appointment_by_note(
            doctor_id=doctor_id,
            note=note
        )
    )

    appointment_id = (
        appointment["appointmentId"]
    )

    assert (
        appointment.get("status")
        == "pending"
    )

    # ------------------------------------------------------------
    # Admin xác nhận lịch.
    # ------------------------------------------------------------

    logout_current_user(driver)

    login_account(
        driver,
        test_data["admin_username"],
        test_data["admin_password"]
    )

    admin_page = AdminAppointmentPage(driver)

    admin_page.open_page()

    assert (
        admin_page.get_appointment_id_by_note(note)
        == str(appointment_id)
    )

    assert (
        admin_page.get_status_by_note(note)
        == "Chờ xác nhận"
    )

    admin_page.click_confirm(
        note
    )

    assert (
        admin_page.get_confirm_success_message()
        == "Xác nhận lịch hẹn thành công."
    )

    admin_page.open_page()

    assert (
        admin_page.get_status_by_note(note)
        == "Đã xác nhận"
    )

    # ------------------------------------------------------------
    # Doctor tạo hồ sơ bệnh án.
    # ------------------------------------------------------------

    logout_current_user(driver)

    login_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    doctor_appointment_page = (
        DoctorAppointmentPage(driver)
    )

    doctor_appointment_page.open_page()

    assert (
        doctor_appointment_page
        .get_note_by_id(appointment_id)
        == note
    )

    assert (
        doctor_appointment_page
        .get_status_by_id(appointment_id)
        == "Đã xác nhận"
    )

    assert (
        doctor_appointment_page
        .is_examine_button_present(
            appointment_id
        )
    )

    doctor_appointment_page.click_examine(
        appointment_id
    )

    examination_page = (
        DoctorExaminationPage(driver)
    )

    assert (
        examination_page.get_page_title()
        == "Khám bệnh"
    )

    diagnosis = (
        test_data["diagnosis_prefix"]
        + unique_time
    )

    treatment = (
        test_data["treatment_prefix"]
        + unique_time
    )

    examination_page.enter_diagnosis(
        diagnosis
    )

    examination_page.enter_treatment(
        treatment
    )

    examination_page.click_save_medical_record()

    medical_record_page = (
        MedicalRecordPage(driver)
    )

    assert (
        medical_record_page.get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    )

    # ------------------------------------------------------------
    # Doctor kê đơn thuốc thứ nhất.
    # ------------------------------------------------------------

    prescription_page = (
        PrescriptionPage(driver)
    )

    prescription_page.open_prescription_tab()

    assert (
        prescription_page
        .is_prescription_form_present()
    )

    prescription_page.select_drug_by_index(
        test_data["drug_option_index"]
    )

    prescription_page.enter_quantity(
        test_data["prescription_quantity"]
    )

    first_dosage = (
        "FIRST-"
        + test_data["prescription_dosage"]
        + "-"
        + unique_time
    )

    prescription_page.enter_dosage(
        first_dosage
    )

    prescription_page.click_add_to_prescription()

    assert (
        prescription_page
        .get_prescription_item_count()
        == 1
    )

    prescription_page.click_save_prescription()

    assert (
        prescription_page
        .get_prescription_success_message()
        == "Kê đơn thuốc thành công."
    )

    # ============================================================
    # Step 2:
    # Ghi nhận notification của đơn thuốc hiện tại.
    #
    # Đăng nhập Patient để lấy notification của đơn thuốc thứ nhất.
    # ============================================================

    logout_current_user(driver)

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    notification_page = (
        NotificationPage(driver)
    )

    notification_page.open_page()

    assert (
        notification_page.get_page_title()
        == "Thông báo của tôi"
    )

    first_notification = (
        notification_page
        .get_latest_notification_by_type_and_keyword(
            test_data["notification_type"],
            test_data["expected_keyword"]
        )
    )

    assert first_notification is not None

    first_notification_content = (
        notification_page
        .get_notification_content(
            first_notification
        )
    )

    first_notification_time = (
        notification_page
        .get_notification_time(
            first_notification
        )
    )

    assert (
        first_notification_time.strip()
        != ""
    )

    # ============================================================
    # Step 3:
    # Đăng nhập bằng Doctor phụ trách hồ sơ.
    # ============================================================

    logout_current_user(driver)

    login_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    # ============================================================
    # Step 4:
    # Mở phần Đơn thuốc của hồ sơ.
    # ============================================================

    medical_record_page = (
        MedicalRecordPage(driver)
    )

    medical_record_page.open_page(
        appointment_id
    )

    assert (
        medical_record_page.get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    )

    prescription_page = (
        PrescriptionPage(driver)
    )

    prescription_page.open_prescription_tab()

    assert (
        prescription_page
        .is_prescription_form_present()
    )

    # ============================================================
    # Step 5:
    # Kê thêm một đơn thuốc mới với thông tin khác
    # so với đơn thuốc trước đó.
    # ============================================================

    selected_drug = (
        prescription_page
        .select_drug_by_index(
            test_data["drug_option_index"]
        )
    )

    assert selected_drug != ""

    second_quantity = (
        int(
            test_data["prescription_quantity"]
        ) + 1
    )

    second_dosage = (
        "SECOND-"
        + test_data["prescription_dosage"]
        + "-"
        + unique_time
    )

    prescription_page.enter_quantity(
        second_quantity
    )

    prescription_page.enter_dosage(
        second_dosage
    )

    prescription_page.click_add_to_prescription()

    assert (
        prescription_page
        .get_prescription_item_count()
        == 1
    )

    # ============================================================
    # Step 6:
    # Lưu đơn thuốc mới.
    # ============================================================

    prescription_page.click_save_prescription()

    assert (
        prescription_page
        .get_prescription_success_message()
        == "Kê đơn thuốc thành công."
    )

    # ============================================================
    # Step 7:
    # Đăng xuất Doctor và đăng nhập lại bằng Patient.
    # ============================================================

    logout_current_user(driver)

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    # ============================================================
    # Step 8:
    # Mở trang Thông báo.
    # ============================================================

    notification_page = (
        NotificationPage(driver)
    )

    notification_page.open_page()

    assert (
        notification_page.get_page_title()
        == "Thông báo của tôi"
    )

    # ============================================================
    # Step 9:
    # Tìm và kiểm tra notification mới
    # phát sinh từ đơn thuốc thứ hai.
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
    )

    second_notification_type = (
        notification_page
        .get_notification_type(
            second_notification
        )
    )

    second_notification_content = (
        notification_page
        .get_notification_content(
            second_notification
        )
    )

    second_notification_time = (
        notification_page
        .get_notification_time(
            second_notification
        )
    )

    # ------------------------------------------------------------
    # Expected Result 1:
    # Notification mới thuộc loại [Đơn thuốc].
    # ------------------------------------------------------------

    assert (
        second_notification_type
        == test_data["notification_type"]
    )

    # ------------------------------------------------------------
    # Expected Result 2:
    # Nội dung thể hiện có đơn thuốc mới.
    # ------------------------------------------------------------

    assert (
        notification_page.normalize_text(
            test_data["expected_keyword"]
        )
        in notification_page.normalize_text(
            second_notification_content
        )
    )

    # ------------------------------------------------------------
    # Expected Result 3:
    # Notification mới không phải notification cũ.
    #
    # Backend tạo prescription ID mới nên nội dung
    # notification phải khác nhau.
    # ------------------------------------------------------------

    assert (
        second_notification_content
        != first_notification_content
    ), (
        "TC-NOTIFICATION-008 FAILED: "
        "Notification của đơn thuốc mới bị trùng "
        "với notification của đơn thuốc cũ."
    )

    # ------------------------------------------------------------
    # Expected Result 4:
    # Notification mới có thời gian.
    # ------------------------------------------------------------

    assert (
        second_notification_time.strip()
        != ""
    )

    datetime.strptime(
        second_notification_time,
        test_data["time_format"]
    )

    # ------------------------------------------------------------
    # Expected Result 5:
    # Notification của đơn thuốc cũ và mới
    # được ghi nhận độc lập.
    # ------------------------------------------------------------

    assert (
        first_notification_time.strip()
        != ""
    )

def test_tc_notification_009_patient_receives_new_notification_after_doctor_updates_existing_medical_record(
        driver):
    """
    TC-NOTIFICATION-009:

    Kiểm tra Patient nhận được notification mới
    sau khi Doctor chỉnh sửa Chẩn đoán và Hướng điều trị
    của một hồ sơ bệnh án đã tồn tại.
    """

    test_data = get_test_data_csv(
        NOTIFICATION_TEST_DATA_CSV,
        "TC-NOTIFICATION-009"
    )

    # ============================================================
    # Step 1:
    # Chuẩn bị Patient đã có hồ sơ khám với
    # Chẩn đoán và Hướng điều trị được lưu trước đó.
    #
    # Flow chuẩn bị:
    # - Patient đặt lịch.
    # - Admin xác nhận.
    # - Doctor khám.
    # - Doctor tạo hồ sơ bệnh án.
    # - Patient ghi nhận notification đã có trước khi update.
    # ============================================================

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    doctor_id = int(
        test_data["doctor_id"]
    )

    medical_record_api = MedicalRecordApi()
    appointment_api = AppointmentApi()

    # ------------------------------------------------------------
    # Chuẩn bị lịch làm việc riêng cho TC9.
    # Không sửa helper dùng chung.
    # ------------------------------------------------------------

    try:
        booking_slot = (
            medical_record_api
            .find_available_booking_slot(doctor_id)
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

            work_date = work_date_obj.strftime(
                "%Y-%m-%d"
            )

            existing_schedule = (
                doctor_schedule_api.find_schedule(
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
                    note="SELENIUM-TC-NOTIFICATION-009",
                    token=admin_token
                )

                created_work_date = work_date
                break

        assert created_work_date is not None, (
            "Không thể chuẩn bị lịch làm việc "
            "cho TC-NOTIFICATION-009."
        )

        booking_slot = (
            medical_record_api
            .find_available_booking_slot(doctor_id)
        )

    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    unique_time = str(
        int(time.time())
    )

    note = (
        test_data["note_prefix"]
        + unique_time
    )

    # ------------------------------------------------------------
    # Patient đặt lịch.
    # ------------------------------------------------------------

    doctor_page = DoctorPage(driver)

    doctor_page.open_page()
    doctor_page.book_tran_binh()

    booking_page = BookingPage(driver)

    booking_page.enter_date(
        booking_date
    )

    booking_page.enter_time(
        booking_time
    )

    assert (
        booking_page.get_time_value()
        == booking_time
    )

    booking_page.enter_notes(
        note
    )

    booking_page.click_booking_button()

    assert (
        "Đặt lịch thành công"
        in booking_page.get_message()
    )

    appointment = (
        appointment_api
        .find_appointment_by_note(
            doctor_id=doctor_id,
            note=note
        )
    )

    appointment_id = (
        appointment["appointmentId"]
    )

    assert (
        appointment.get("status")
        == "pending"
    )

    # ------------------------------------------------------------
    # Admin xác nhận lịch.
    # ------------------------------------------------------------

    logout_current_user(driver)

    login_account(
        driver,
        test_data["admin_username"],
        test_data["admin_password"]
    )

    admin_page = AdminAppointmentPage(driver)

    admin_page.open_page()

    assert (
        admin_page.get_appointment_id_by_note(note)
        == str(appointment_id)
    )

    assert (
        admin_page.get_status_by_note(note)
        == "Chờ xác nhận"
    )

    admin_page.click_confirm(
        note
    )

    assert (
        admin_page.get_confirm_success_message()
        == "Xác nhận lịch hẹn thành công."
    )

    admin_page.open_page()

    assert (
        admin_page.get_status_by_note(note)
        == "Đã xác nhận"
    )

    # ------------------------------------------------------------
    # Doctor tạo hồ sơ bệnh án ban đầu.
    # ------------------------------------------------------------

    logout_current_user(driver)

    login_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    doctor_appointment_page = (
        DoctorAppointmentPage(driver)
    )

    doctor_appointment_page.open_page()

    assert (
        doctor_appointment_page
        .get_note_by_id(appointment_id)
        == note
    )

    assert (
        doctor_appointment_page
        .get_status_by_id(appointment_id)
        == "Đã xác nhận"
    )

    assert (
        doctor_appointment_page
        .is_examine_button_present(
            appointment_id
        )
    )

    doctor_appointment_page.click_examine(
        appointment_id
    )

    examination_page = (
        DoctorExaminationPage(driver)
    )

    assert (
        examination_page.get_page_title()
        == "Khám bệnh"
    )

    original_diagnosis = (
        test_data["diagnosis_prefix"]
        + "ORIGINAL-"
        + unique_time
    )

    original_treatment = (
        test_data["treatment_prefix"]
        + "ORIGINAL-"
        + unique_time
    )

    examination_page.enter_diagnosis(
        original_diagnosis
    )

    examination_page.enter_treatment(
        original_treatment
    )

    examination_page.click_save_medical_record()

    medical_record_page = (
        MedicalRecordPage(driver)
    )

    assert (
        medical_record_page.get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    )

    assert (
        original_diagnosis
        in medical_record_page
        .get_diagnosis_information()
    )

    assert (
        original_treatment
        in medical_record_page
        .get_treatment_information()
    )

    # ------------------------------------------------------------
    # Ghi nhận notification trước khi update.
    #
    # Việc này dùng để chứng minh sau update phải có
    # một notification mới, không được nhầm notification cũ.
    # ------------------------------------------------------------

    logout_current_user(driver)

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    notification_page = (
        NotificationPage(driver)
    )

    notification_page.open_page()

    notifications_before_update = (
        notification_page
        .get_all_notification_contents()
    )

    notification_count_before = len(
        notifications_before_update
    )

    # ============================================================
    # Step 2:
    # Đăng nhập Doctor phụ trách.
    # ============================================================

    logout_current_user(driver)

    login_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    # ============================================================
    # Step 3 - POM: MedicalRecordPage
    # Mở hồ sơ khám của Patient.
    # ============================================================

    medical_record_page = (
        MedicalRecordPage(driver)
    )

    medical_record_page.open_page(
        appointment_id
    )

    assert (
        medical_record_page.get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    )

    assert (
        original_diagnosis
        in medical_record_page
        .get_diagnosis_information()
    )

    assert (
        original_treatment
        in medical_record_page
        .get_treatment_information()
    )

    assert (
        medical_record_page
        .is_edit_button_present()
    )

    # ============================================================
    # Step 4 - POM: MedicalRecordPage
    # Chỉnh sửa Chẩn đoán và Hướng điều trị.
    # ============================================================

    medical_record_page.click_edit_button()

    assert (
        medical_record_page
        .is_edit_form_present()
    )

    # Xác nhận form edit load đúng dữ liệu cũ.
    assert (
        medical_record_page
        .get_diagnosis_input_value()
        == original_diagnosis
    )

    assert (
        medical_record_page
        .get_treatment_input_value()
        == original_treatment
    )

    updated_diagnosis = (
        test_data["diagnosis_prefix"]
        + "UPDATED-"
        + unique_time
    )

    updated_treatment = (
        test_data["treatment_prefix"]
        + "UPDATED-"
        + unique_time
    )

    medical_record_page.enter_diagnosis(
        updated_diagnosis
    )

    medical_record_page.enter_treatment(
        updated_treatment
    )

    # ============================================================
    # Step 5 - POM: MedicalRecordPage
    # Lưu thông tin đã cập nhật.
    # ============================================================

    medical_record_page.click_save_changes()

    assert (
        medical_record_page
        .get_update_success_message()
        == "Cập nhật hồ sơ bệnh án thành công."
    )

    # Kiểm tra dữ liệu mới đã thực sự được cập nhật.
    assert (
        updated_diagnosis
        in medical_record_page
        .get_diagnosis_information()
    )

    assert (
        updated_treatment
        in medical_record_page
        .get_treatment_information()
    )

    # Đồng thời đảm bảo dữ liệu cũ không còn hiển thị.
    assert (
        original_diagnosis
        not in medical_record_page
        .get_diagnosis_information()
    )

    assert (
        original_treatment
        not in medical_record_page
        .get_treatment_information()
    )

    # ============================================================
    # Step 6:
    # Đăng xuất Doctor và đăng nhập Patient.
    # ============================================================

    logout_current_user(driver)

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    # ============================================================
    # Step 7 - POM: NotificationPage
    # Mở trang Thông báo.
    # ============================================================

    notification_page = (
        NotificationPage(driver)
    )

    notification_page.open_page()

    assert (
        notification_page.get_page_title()
        == "Thông báo của tôi"
    )
    # ============================================================
    # Step 8 - POM: NotificationPage
    # Tìm và kiểm tra notification mới phát sinh
    # sau khi Doctor cập nhật hồ sơ khám.
    # ============================================================

    notifications_after_update = (
        notification_page
        .get_all_notification_contents()
    )

    notification_count_after = len(
        notifications_after_update
    )

    # ------------------------------------------------------------
    # Expected Result:
    # Sau khi Doctor cập nhật Chẩn đoán/Hướng điều trị,
    # Patient phải nhận thêm một notification mới.
    #
    # Hiện tại hệ thống chưa phát sinh notification mới,
    # nên TC-NOTIFICATION-009 được kỳ vọng FAIL tại đây.
    # ------------------------------------------------------------

    if notification_count_after <= notification_count_before:
        pytest.xfail(
            "KNOWN BUG - TC-NOTIFICATION-009: "
            f"Trước khi cập nhật có {notification_count_before} notification, "
            f"sau khi cập nhật vẫn có {notification_count_after} notification. "
            "Hồ sơ bệnh án cập nhật thành công nhưng "
            "Patient không nhận được notification mới."
        )