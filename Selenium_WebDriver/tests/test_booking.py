from pages.LoginPage import LoginPage
from pages.BookingPage import BookingPage
from pages.DoctorPage import DoctorPage
from api.AppointmentApi import AppointmentApi
import time
from datetime import datetime, timedelta
from utils.test_reporter import report_step
from utils.data_reader import (
    get_test_data_csv,
    BOOKING_TEST_DATA_CSV,
)
from api.MedicalRecordApi import MedicalRecordApi
from api.DoctorScheduleApi import DoctorScheduleApi
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
def get_test_date(days_after=30):
    test_date = datetime.now() + timedelta(days=days_after)

    return test_date.strftime("%d/%m/%Y")

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

def get_or_create_booking_slot(
        doctor_id,
        test_data,
        schedule_note
):
    """
    Tìm slot đặt lịch còn trống.
    Nếu không còn slot thì tự tạo một ca làm việc test
    trong tương lai rồi tìm lại slot.
    """

    medical_record_api = MedicalRecordApi()

    try:
        return medical_record_api.find_available_booking_slot(
            doctor_id
        )

    except AssertionError:
        doctor_schedule_api = DoctorScheduleApi()

        # Booking CSV cần có tài khoản Admin
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


def old_tc_booking_001_booking_success(driver):
    """
    TC-BOOKING-001:
    Đặt lịch thành công với ngày và giờ hợp lệ.
    """

    test_case_id = "TC-BOOKING-001"

    # ============================================================
    # Đọc dữ liệu test từ CSV
    # ============================================================

    test_data = get_test_data_csv(
        BOOKING_TEST_DATA_CSV,
        test_case_id
    )

    doctor_id = int(
        test_data["doctor_id"]
    )

    appointment_api = AppointmentApi()

    # Tìm slot còn trống.
    # Nếu hết slot thì helper sẽ tự tạo schedule test mới.
    booking_slot = get_or_create_booking_slot(
        doctor_id=doctor_id,
        test_data=test_data,
        schedule_note=(
            test_data["note_prefix"]
            + "SCHEDULE"
        )
    )

    booking_date = booking_slot[
        "booking_date"
    ]

    booking_time = booking_slot[
        "booking_time"
    ]

    # ============================================================
    # Step 1:
    # Đăng nhập bằng tài khoản Patient hợp lệ.
    # ============================================================

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    assert driver.current_url == "http://localhost:3000/", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Patient đăng nhập không thành công. "
        "Expected URL: http://localhost:3000/ | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description=(
            "Đăng nhập bằng tài khoản Patient "
            "hợp lệ thành công"
        )
    )

    # ============================================================
    # Step 2:
    # Mở trang Bác sĩ và chọn bác sĩ cần đặt lịch.
    # ============================================================

    booking_page = (
        open_tran_binh_booking_page(driver)
    )

    assert driver.current_url == BOOKING_URL, (
        f"{test_case_id} | STEP 2 FAILED | "
        "Không chuyển đến trang đặt lịch của bác sĩ. "
        f"Expected URL: {BOOKING_URL} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description=(
            "Mở trang Bác sĩ và chọn bác sĩ "
            "Tran Binh thành công"
        )
    )

    # ============================================================
    # Step 3:
    # Kiểm tra trang Đặt lịch hiển thị đầy đủ thông tin.
    # ============================================================

    assert booking_page.find(
        *booking_page.DATE_INPUT
    ).is_displayed(), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Không hiển thị trường Ngày khám."
    )

    assert booking_page.find(
        *booking_page.TIME_INPUT
    ).is_displayed(), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Không hiển thị trường Giờ khám."
    )

    assert booking_page.find(
        *booking_page.NOTES_INPUT
    ).is_displayed(), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Không hiển thị trường Ghi chú."
    )

    assert booking_page.find(
        *booking_page.BOOKING_BUTTON
    ).is_displayed(), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Không hiển thị nút Đặt lịch."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            "Trang Đặt lịch hiển thị đầy đủ "
            "Ngày khám, Giờ khám, Ghi chú "
            "và nút Đặt lịch"
        )
    )

    # ============================================================
    # Step 4:
    # Chọn ngày và giờ hợp lệ còn trống.
    # ============================================================

    booking_page.enter_date(
        booking_date
    )

    booking_page.enter_time(
        booking_time
    )

    actual_time = (
        booking_page.get_time_value()
    )

    assert actual_time == booking_time, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected time: {booking_time} | "
        f"Actual: {actual_time}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            f"Chọn ngày {booking_date} "
            f"và giờ {booking_time} thành công"
        )
    )

    # ============================================================
    # Step 5:
    # Nhập ghi chú hợp lệ và nhấn Đặt lịch.
    # ============================================================

    note = (
        test_data["note_prefix"]
        + str(int(time.time()))
    )

    booking_page.enter_notes(
        note
    )

    booking_page.click_booking_button()

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            "Nhập ghi chú hợp lệ "
            "và nhấn Đặt lịch"
        )
    )

    # ============================================================
    # Step 6:
    # Kiểm tra thông báo và lịch hẹn vừa tạo.
    # ============================================================

    message = (
        booking_page.get_message()
    )

    expected_message = (
        test_data[
            "expected_success_message"
        ]
    )

    assert expected_message in message, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected message chứa: "
        f"{expected_message} | "
        f"Actual: {message}"
    )

    appointment = (
        appointment_api.find_appointment_by_note(
            doctor_id=doctor_id,
            note=note
        )
    )

    assert appointment is not None, (
        f"{test_case_id} | STEP 6 FAILED | "
        "Không tìm thấy lịch hẹn vừa tạo. "
        f"Expected note: {note} | "
        "Actual: Không tìm thấy appointment"
    )

    actual_status = (
        appointment.get("status")
    )

    assert actual_status == "pending", (
        f"{test_case_id} | STEP 6 FAILED | "
        "Trạng thái lịch hẹn không đúng. "
        "Expected: pending | "
        f"Actual: {actual_status}"
    )

    appointment_id = (
        appointment.get("appointmentId")
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            "Đặt lịch thành công và lịch hẹn "
            "được tạo với trạng thái pending"
        ),
        detail=(
            f"Appointment ID: "
            f"{appointment_id} | "
            f"Status: {actual_status}"
        )
    )

    # ============================================================
    # CLEANUP
    # Hủy dữ liệu test vừa tạo để lần chạy sau không bị ảnh hưởng.
    # ============================================================

    if appointment_id:
        appointment_api.cancel_appointment(
            appointment_id
        )

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


def test_booking_without_notes(driver, booking_test_data):
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

def test_booking_duplicate_time(driver, booking_test_data):
    """
    TC-BOOKING-007:
    Đặt lịch trùng đúng giờ đã có người đặt.
    """

    # Chuẩn bị dữ liệu:
    # patient_an đã đặt lịch bác sĩ Trần Bình lúc 14:00
    booking_test_data.create_appointment(
        patient_id=1,
        doctor_id=1,
        booking_date="11/04/2026",
        booking_time="14:00",
        notes="Dữ liệu chuẩn bị cho TC-BOOKING-007"
    )

    # patient_chi thử đặt trùng giờ
    login_second_patient(driver)

    booking_page = open_tran_binh_booking_page(driver)

    booking_page.enter_date("11/04/2026")

    booking_page.enter_time("14:00")

    assert booking_page.get_time_value() == "14:00"

    booking_page.click_booking_button()

    message = booking_page.get_message()

    assert "Khung giờ này đã có người đặt" in message

def test_booking_within_thirty_minutes(
        driver,
        booking_test_data):
    """
    TC-BOOKING-008:
    Đặt lịch cách lịch đã có dưới 30 phút.
    """

    # Chuẩn bị dữ liệu:
    # patient_an đã đặt lịch lúc 15:30
    booking_test_data.create_appointment(
        patient_id=1,
        doctor_id=1,
        booking_date="11/04/2026",
        booking_time="15:30",
        notes="Dữ liệu chuẩn bị cho TC-BOOKING-008"
    )

    # patient_chi thử đặt lúc 15:31
    login_second_patient(driver)

    booking_page = open_tran_binh_booking_page(driver)

    booking_page.enter_date("11/04/2026")

    booking_page.enter_time("15:31")

    assert booking_page.get_time_value() == "15:31"

    booking_page.click_booking_button()

    message = booking_page.get_message()

    assert "30 phút" in message