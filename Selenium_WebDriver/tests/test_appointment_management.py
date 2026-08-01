import time
import pytest
from pages.LoginPage import LoginPage
from pages.AdminAppointmentPage import AdminAppointmentPage

from pages.DoctorAppointmentPage import DoctorAppointmentPage
from pages.DoctorExaminationPage import DoctorExaminationPage
from pages.MedicalRecordPage import MedicalRecordPage
from pages.BookingPage import BookingPage
from pages.DoctorPage import DoctorPage

ADMIN_USERNAME = "admin_system"
ADMIN_PASSWORD = "Abc@123"
DOCTOR_USERNAME = "doctor_minh"
DOCTOR_PASSWORD = "Abc@123"
OTHER_DOCTOR_USERNAME = "doctor_binh"
OTHER_DOCTOR_PASSWORD = "Abc@123"
PATIENT_USERNAME = "patient_an"
PATIENT_PASSWORD = "Abc@123"

BOOKING_URL = (
    "http://localhost:3000/"
    "booking?doctorId=1"
)
HOME_URL = "http://localhost:3000/"


def login_admin(driver):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )

    time.sleep(2)

    assert driver.current_url == HOME_URL

def login_doctor(driver):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        DOCTOR_USERNAME,
        DOCTOR_PASSWORD
    )

    time.sleep(2)

    assert driver.current_url == HOME_URL

def login_other_doctor(driver):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        OTHER_DOCTOR_USERNAME,
        OTHER_DOCTOR_PASSWORD
    )

    time.sleep(2)

    assert driver.current_url == HOME_URL
def login_patient(driver):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        PATIENT_USERNAME,
        PATIENT_PASSWORD
    )

    time.sleep(2)

    assert driver.current_url == HOME_URL


def logout_current_user(driver):
    login_page = LoginPage(driver)

    login_page.logout()

    time.sleep(2)

    assert (
        driver.current_url
        == "http://localhost:3000/login"
    )


def open_tran_binh_booking_page(driver):
    doctor_page = DoctorPage(driver)

    doctor_page.open_page()

    time.sleep(2)

    doctor_page.book_tran_binh()

    assert driver.current_url == BOOKING_URL

    return BookingPage(driver)

def test_admin_confirms_pending_appointment(
        driver,
        appointment_tc2_data):
    """
    TC-APPOINTMENT-002:
    Admin xác nhận thành công
    lịch hẹn đang chờ xác nhận.
    """

    login_admin(driver)

    appointment_page = AdminAppointmentPage(
        driver
    )

    appointment_page.open_page()

    assert (
        appointment_page.get_page_title()
        == "Quản lý lịch hẹn"
    )

    note = appointment_tc2_data["note"]

    assert (
        appointment_page
        .get_appointment_id_by_note(note)
        == str(
            appointment_tc2_data[
                "appointment_id"
            ]
        )
    )

    assert (
        appointment_page
        .get_patient_name_by_note(note)
        == appointment_tc2_data[
            "patient_name"
        ]
    )

    assert (
        appointment_page
        .get_doctor_name_by_note(note)
        == appointment_tc2_data[
            "doctor_name"
        ]
    )

    assert (
        appointment_page
        .get_appointment_time_by_note(note)
        == appointment_tc2_data[
            "appointment_time"
        ]
    )

    assert (
        appointment_page
        .get_status_by_note(note)
        == "Chờ xác nhận"
    )

    assert (
        appointment_page
        .is_confirm_button_present(note)
    )

    assert (
        appointment_page
        .is_cancel_button_present(note)
    )

    appointment_page.click_confirm(note)

    assert (
        appointment_page
        .get_confirm_success_message()
        == "Xác nhận lịch hẹn thành công."
    )

    # Tải lại danh sách sau khi xác nhận
    appointment_page.open_page()

    assert (
        appointment_page
        .get_status_by_note(note)
        == "Đã xác nhận"
    )

    assert not (
        appointment_page
        .is_confirm_button_present(note)
    )

    assert not (
        appointment_page
        .is_cancel_button_present(note)
    )

    # Thông tin lịch không bị thay đổi
    assert (
        appointment_page
        .get_appointment_id_by_note(note)
        == str(
            appointment_tc2_data[
                "appointment_id"
            ]
        )
    )

    assert (
        appointment_page
        .get_patient_name_by_note(note)
        == appointment_tc2_data[
            "patient_name"
        ]
    )

    assert (
        appointment_page
        .get_doctor_name_by_note(note)
        == appointment_tc2_data[
            "doctor_name"
        ]
    )

    assert (
        appointment_page
        .get_appointment_time_by_note(note)
        == appointment_tc2_data[
            "appointment_time"
        ]
    )

def test_admin_cancels_pending_appointment(
        driver,
        appointment_tc3_data):
    """
    TC-APPOINTMENT-003:
    Admin hủy thành công
    lịch hẹn đang chờ xác nhận.
    """

    login_admin(driver)

    appointment_page = AdminAppointmentPage(
        driver
    )

    appointment_page.open_page()

    note = appointment_tc3_data["note"]

    appointment_id_before = (
        appointment_page
        .get_appointment_id_by_note(note)
    )

    patient_name_before = (
        appointment_page
        .get_patient_name_by_note(note)
    )

    doctor_name_before = (
        appointment_page
        .get_doctor_name_by_note(note)
    )

    appointment_time_before = (
        appointment_page
        .get_appointment_time_by_note(note)
    )

    assert (
        appointment_id_before
        == str(
            appointment_tc3_data[
                "appointment_id"
            ]
        )
    )

    assert (
        patient_name_before
        == appointment_tc3_data[
            "patient_name"
        ]
    )

    assert (
        doctor_name_before
        == appointment_tc3_data[
            "doctor_name"
        ]
    )

    assert (
        appointment_time_before
        == appointment_tc3_data[
            "appointment_time"
        ]
    )

    assert (
        appointment_page
        .get_status_by_note(note)
        == "Chờ xác nhận"
    )

    assert (
        appointment_page
        .is_confirm_button_present(note)
    )

    assert (
        appointment_page
        .is_cancel_button_present(note)
    )

    appointment_page.click_cancel(note)

    # Đồng ý trên hộp thoại xác nhận
    alert = driver.switch_to.alert

    assert alert.text == (
        "Bạn chắc chắn muốn hủy "
        "lịch hẹn này không?"
    )

    alert.accept()

    assert (
        appointment_page
        .get_cancel_success_message()
        == "Hủy lịch hẹn thành công."
    )

    appointment_page.open_page()

    assert (
        appointment_page
        .get_status_by_note(note)
        == "Đã hủy"
    )

    assert not (
        appointment_page
        .is_confirm_button_present(note)
    )

    assert not (
        appointment_page
        .is_cancel_button_present(note)
    )

    # Thông tin lịch không bị thay đổi
    assert (
        appointment_page
        .get_appointment_id_by_note(note)
        == appointment_id_before
    )

    assert (
        appointment_page
        .get_patient_name_by_note(note)
        == patient_name_before
    )

    assert (
        appointment_page
        .get_doctor_name_by_note(note)
        == doctor_name_before
    )

    assert (
        appointment_page
        .get_appointment_time_by_note(note)
        == appointment_time_before
    )
def test_doctor_cannot_examine_pending_appointment_by_url(
        driver,
        appointment_tc5_data):
    """
    TC-APPOINTMENT-005:
    Bác sĩ không được khám lịch hẹn
    chưa được Admin xác nhận.
    """

    login_doctor(driver)

    appointment_id = (
        appointment_tc5_data[
            "appointment_id"
        ]
    )

    note = appointment_tc5_data["note"]

    # Kiểm tra lịch vẫn đang chờ xác nhận
    appointment_page = DoctorAppointmentPage(
        driver
    )

    appointment_page.open_page()

    assert (
        appointment_page.get_status_by_note(note)
        == "Chờ xác nhận"
    )

    assert not (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    )

    # Thử nhập trực tiếp URL trang khám
    examination_page = DoctorExaminationPage(
        driver
    )

    examination_page.open_page(
        appointment_id
    )

    assert (
        examination_page
        .get_invalid_appointment_message()
        == (
            "Lịch hẹn chưa được xác nhận "
            "hoặc đã bị hủy."
        )
    )

    assert not (
        examination_page
        .is_appointment_information_present()
    )

    assert not (
        examination_page
        .is_create_record_form_present()
    )

    # Kiểm tra trạng thái lịch không bị thay đổi
    appointment_page.open_page()

    assert (
        appointment_page.get_status_by_note(note)
        == "Chờ xác nhận"
    )

def test_owner_doctor_can_open_confirmed_appointment(
        driver,
        appointment_tc6_data):
    """
    TC-APPOINTMENT-006:
    Đúng bác sĩ được mở chức năng khám bệnh
    khi lịch đã được Admin xác nhận.
    """

    login_doctor(driver)

    appointment_page = DoctorAppointmentPage(
        driver
    )

    appointment_page.open_page()

    appointment_id = (
        appointment_tc6_data[
            "appointment_id"
        ]
    )

    note = appointment_tc6_data["note"]

    assert (
        appointment_page.get_status_by_note(note)
        == "Đã xác nhận"
    )

    assert (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    )

    appointment_page.click_examine(
        appointment_id
    )

    examination_page = DoctorExaminationPage(
        driver
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
        examination_page.get_patient_name()
        == appointment_tc6_data[
            "patient_name"
        ]
    )

    assert note in (
        examination_page
        .get_appointment_note()
    )

    assert "Đã xác nhận" in (
        examination_page
        .get_appointment_status()
    )

    assert (
        examination_page
        .is_appointment_information_present()
    )

    assert (
        examination_page
        .is_create_record_form_present()
    )

    # Chưa lưu hồ sơ nên trạng thái vẫn được giữ nguyên
    appointment_page.open_page()

    assert (
        appointment_page.get_status_by_note(note)
        == "Đã xác nhận"
    )

    assert (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    )

def test_other_doctor_cannot_examine_confirmed_appointment(
        driver,
        appointment_tc7_data):
    """
    TC-APPOINTMENT-007:
    Bác sĩ khác không được khám lịch hẹn
    đã xác nhận nhưng không thuộc mình.
    """

    login_other_doctor(driver)

    appointment_id = (
        appointment_tc7_data[
            "appointment_id"
        ]
    )

    note = appointment_tc7_data["note"]

    appointment_page = DoctorAppointmentPage(
        driver
    )

    appointment_page.open_page()

    # Lịch của doctor_minh không xuất hiện
    # trong danh sách doctor_binh
    assert not (
        appointment_page
        .is_appointment_present_by_note(note)
    )

    # Thử truy cập trực tiếp trang khám
    examination_page = DoctorExaminationPage(
        driver
    )

    examination_page.open_page(
        appointment_id
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    )

    assert (
        examination_page
        .get_access_denied_message()
        == "Bạn không có quyền khám lịch hẹn này."
    )

    assert not (
        examination_page
        .is_appointment_information_present()
    )

    assert not (
        examination_page
        .is_create_record_form_present()
    )

def test_doctor_cannot_examine_cancelled_appointment(
        driver,
        appointment_tc8_data):
    """
    TC-APPOINTMENT-008:
    Bác sĩ không được khám bệnh
    đối với lịch đã bị Admin hủy.
    """

    login_doctor(driver)

    appointment_id = (
        appointment_tc8_data[
            "appointment_id"
        ]
    )

    note = appointment_tc8_data["note"]

    appointment_page = DoctorAppointmentPage(
        driver
    )

    appointment_page.open_page()

    # Lịch đã hủy vẫn xuất hiện
    # trong danh sách của đúng bác sĩ
    assert (
        appointment_page
        .is_appointment_present_by_note(note)
    )

    assert (
        appointment_page
        .get_status_by_note(note)
        == "Đã hủy"
    )

    # Lịch đã hủy không có nút Khám bệnh
    assert not (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    )

    # Thử nhập trực tiếp URL trang khám
    examination_page = DoctorExaminationPage(
        driver
    )

    examination_page.open_page(
        appointment_id
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    )

    assert (
        examination_page
        .get_invalid_appointment_message()
        == (
            "Lịch hẹn chưa được xác nhận "
            "hoặc đã bị hủy."
        )
    )

    assert not (
        examination_page
        .is_appointment_information_present()
    )

    assert not (
        examination_page
        .is_create_record_form_present()
    )

    # Trạng thái lịch vẫn không thay đổi
    appointment_page.open_page()

    assert (
        appointment_page
        .get_status_by_note(note)
        == "Đã hủy"
    )
def test_doctor_completes_confirmed_appointment(
        driver,
        appointment_tc9_data):
    """
    TC-APPOINTMENT-009:
    Bác sĩ lưu hồ sơ bệnh án và
    hoàn thành lịch đã xác nhận.
    """

    login_doctor(driver)

    appointment_page = DoctorAppointmentPage(
        driver
    )

    appointment_page.open_page()

    appointment_id = (
        appointment_tc9_data[
            "appointment_id"
        ]
    )

    assert (
        appointment_page.get_status_by_id(
            appointment_id
        )
        == "Đã xác nhận"
    )

    assert (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    )

    appointment_page.click_examine(
        appointment_id
    )

    examination_page = DoctorExaminationPage(
        driver
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    )

    assert (
        examination_page
        .is_create_record_form_present()
    )

    examination_page.enter_diagnosis(
        appointment_tc9_data[
            "diagnosis"
        ]
    )

    examination_page.enter_treatment(
        appointment_tc9_data[
            "treatment"
        ]
    )

    examination_page.click_save_medical_record()

    medical_record_page = MedicalRecordPage(
        driver
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
        medical_record_page.get_patient_name()
        == appointment_tc9_data[
            "patient_name"
        ]
    )

    assert appointment_tc9_data[
        "doctor_name"
    ] in medical_record_page.get_doctor_information()

    assert appointment_tc9_data[
        "diagnosis"
    ] in medical_record_page.get_diagnosis_information()

    assert appointment_tc9_data[
        "treatment"
    ] in medical_record_page.get_treatment_information()

    # Quay lại danh sách lịch của bác sĩ
    appointment_page.open_page()

    assert (
        appointment_page.get_status_by_id(
            appointment_id
        )
        == "Đã hoàn thành"
    )

    assert not (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    )

    assert (
        appointment_page
        .is_view_medical_record_button_present_by_id(
            appointment_id
        )
    )

def test_patient_books_and_admin_sees_pending_appointment(
        driver,
        appointment_tc1_data):
    """
    TC-APPOINTMENT-001:
    Bệnh nhân đặt lịch thành công.
    Admin thấy đúng lịch mới ở trạng thái
    Chờ xác nhận.
    """

    # 1. Bệnh nhân đăng nhập và mở trang đặt lịch
    login_patient(driver)

    booking_page = (
        open_tran_binh_booking_page(driver)
    )

    booking_date = (
        appointment_tc1_data[
            "booking_date"
        ]
    )

    booking_time = (
        appointment_tc1_data[
            "booking_time"
        ]
    )

    note = appointment_tc1_data["note"]

    # 2. Bệnh nhân nhập thông tin đặt lịch
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

    # 3. Bệnh nhân nhấn Đặt lịch
    booking_page.click_booking_button()

    assert (
        "Đặt lịch thành công"
        in booking_page.get_message()
    )

    # 4. Lấy đúng lịch vừa được tạo
    time.sleep(1)

    appointment_api = (
        appointment_tc1_data[
            "appointment_api"
        ]
    )

    appointment = (
        appointment_api
        .find_appointment_by_note(
            doctor_id=appointment_tc1_data[
                "doctor_id"
            ],
            note=note
        )
    )

    appointment_id = appointment[
        "appointmentId"
    ]

    assert (
        appointment.get("status")
        == "pending"
    )

    expected_appointment_time = (
        appointment_api
        .parse_appointment_date(
            appointment[
                "appointmentDate"
            ]
        )
        .strftime("%H:%M %d/%m/%Y")
    )

    # 5. Bệnh nhân đăng xuất
    logout_current_user(driver)

    # 6. Admin đăng nhập
    login_admin(driver)

    admin_page = AdminAppointmentPage(
        driver
    )

    admin_page.open_page()

    assert (
        admin_page.get_page_title()
        == "Quản lý lịch hẹn"
    )

    # 7. Admin thấy đúng thông tin lịch mới
    assert (
        admin_page
        .get_appointment_id_by_note(note)
        == str(appointment_id)
    )

    assert (
        admin_page
        .get_patient_name_by_note(note)
        == "Nguyen An"
    )

    assert (
        admin_page
        .get_doctor_name_by_note(note)
        == "Tran Binh"
    )

    assert (
        admin_page
        .get_appointment_time_by_note(note)
        == expected_appointment_time
    )

    assert (
        admin_page.get_status_by_note(note)
        == "Chờ xác nhận"
    )

    # 8. Lịch chờ xác nhận có đủ thao tác
    assert (
        admin_page
        .is_confirm_button_present(note)
    )

    assert (
        admin_page
        .is_cancel_button_present(note)
    )

@pytest.mark.xfail(
    reason=(
        "Known bug: bác sĩ chưa thể xem hồ sơ "
        "bệnh nhân khi lịch đang chờ xác nhận."
    ),
    strict=True
)
def test_doctor_can_view_patient_profile_while_appointment_pending(
        driver,
        appointment_tc4_data):
    """
    TC-APPOINTMENT-004:
    Bác sĩ được xem hồ sơ bệnh nhân
    khi lịch còn chờ xác nhận,
    nhưng không được khám bệnh.
    """

    login_doctor(driver)

    appointment_id = (
        appointment_tc4_data[
            "appointment_id"
        ]
    )

    note = appointment_tc4_data["note"]

    appointment_page = DoctorAppointmentPage(
        driver
    )

    appointment_page.open_page()

    # Đúng lịch hẹn của bác sĩ
    assert (
        appointment_page
        .get_note_by_id(appointment_id)
        == note
    )

    assert (
        appointment_page
        .get_patient_name_by_note(note)
        == appointment_tc4_data[
            "patient_name"
        ]
    )

    # Lịch vẫn đang chờ Admin xác nhận
    assert (
        appointment_page
        .get_status_by_id(
            appointment_id
        )
        == "Chờ xác nhận"
    )

    # Không được hiển thị nút Khám bệnh
    assert not (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    )

    # Theo yêu cầu phải có nút xem hồ sơ
    assert (
        appointment_page
        .is_patient_profile_button_present(
            appointment_id
        )
    ), (
        "BUG: Lịch đang chờ xác nhận nhưng "
        "bác sĩ không có nút xem hồ sơ "
        "hoặc lịch sử khám của bệnh nhân."
    )

    # Bác sĩ cũng không được mở trang khám
    # bằng cách nhập URL trực tiếp
    examination_page = DoctorExaminationPage(
        driver
    )

    examination_page.open_page(
        appointment_id
    )

    assert (
        examination_page
        .get_invalid_appointment_message()
        == (
            "Lịch hẹn chưa được xác nhận "
            "hoặc đã bị hủy."
        )
    )

    assert not (
        examination_page
        .is_appointment_information_present()
    )

    assert not (
        examination_page
        .is_create_record_form_present()
    )