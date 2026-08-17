import time
from pages.LoginPage import LoginPage
from pages.DoctorPage import DoctorPage
from pages.BookingPage import BookingPage
from pages.AdminAppointmentPage import AdminAppointmentPage
from pages.NotificationPage import NotificationPage
from datetime import datetime
from api.AppointmentApi import AppointmentApi
from api.MedicalRecordApi import MedicalRecordApi

# ============================================================
# TEST ACCOUNTS
# ============================================================

PATIENT_USERNAME = "patient_an"
PATIENT_PASSWORD = "Abc@123"

ADMIN_USERNAME = "admin_system"
ADMIN_PASSWORD = "Abc@123"

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

    # ============================================================
    # Step 1:
    # Patient thực hiện đặt một lịch khám hợp lệ.
    # ============================================================

    login_account(driver,PATIENT_USERNAME,PATIENT_PASSWORD)
    doctor_id = 1
    medical_record_api = MedicalRecordApi()

    booking_slot = (medical_record_api.find_available_booking_slot(doctor_id))
    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    note = ("SELENIUM-TC-NOTIFICATION-001-"+ str(int(time.time())))

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
    login_account(driver,ADMIN_USERNAME,ADMIN_PASSWORD)

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
    login_account(driver,PATIENT_USERNAME,PATIENT_PASSWORD)

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
    assert (notification_type== "[Lịch hẹn]")

    # 7.2. Kiểm tra thông báo thuộc đúng
    # lịch hẹn vừa được Admin xác nhận.
    assert (f"#{appointment_id}"in notification_content)

    # 7.3. Kiểm tra nội dung thể hiện
    # lịch hẹn đã được xác nhận.
    assert ("da duoc xac nhan"in notification_content.lower())

    # 7.4. Kiểm tra notification có thời gian.
    assert (notification_time.strip()!= "")

    # 7.5. Kiểm tra thời gian hiển thị
    # đúng định dạng HH:mm:ss dd/MM/yyyy.
    datetime.strptime(notification_time,"%H:%M:%S %d/%m/%Y")