import time

from api.AppointmentApi import AppointmentApi

from utils.data_reader import (
    get_test_data_csv,
    BOOKING_TEST_DATA_CSV,
)

from utils.test_reporter import report_step

from tests.helpers.booking_helpers import (
    BOOKING_URL,
    login_account,
    open_tran_binh_booking_page,
    get_or_create_booking_slot,
)

def test_tc_booking_010_ci_booking_success(driver):
    """
    TC-BOOKING-010:
    Kiểm tra lại luồng đặt lịch thành công với ngày và giờ hợp lệ
    để xác minh test case mới được thực thi trên Local và GitHub Actions.
    """

    test_case_id = "TC-BOOKING-010"

    # Đọc dữ liệu test của TC-BOOKING-010
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

    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    # ============================================================
    # STEP 1:
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
    # STEP 2:
    # Mở trang Bác sĩ và chọn bác sĩ cần đặt lịch.
    # ============================================================

    booking_page = open_tran_binh_booking_page(driver)

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
    # STEP 3:
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
    # STEP 4:
    # Chọn ngày và giờ hợp lệ còn trống.
    # ============================================================

    booking_page.enter_date(booking_date)
    booking_page.enter_time(booking_time)

    actual_time = booking_page.get_time_value()

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
    # STEP 5:
    # Nhập ghi chú hợp lệ và nhấn Đặt lịch.
    # ============================================================

    note = (
        test_data["note_prefix"]
        + str(int(time.time()))
    )

    booking_page.enter_notes(note)
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
    # STEP 6:
    # Kiểm tra thông báo và lịch hẹn vừa tạo.
    # ============================================================

    message = booking_page.get_message()

    expected_message = test_data[
        "expected_success_message"
    ]

    assert expected_message in message, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected message chứa: {expected_message} | "
        f"Actual: {message}"
    )

    appointment = appointment_api.find_appointment_by_note(
        doctor_id=doctor_id,
        note=note
    )

    assert appointment is not None, (
        f"{test_case_id} | STEP 6 FAILED | "
        "Không tìm thấy lịch hẹn vừa tạo. "
        f"Expected note: {note} | "
        "Actual: Không tìm thấy appointment"
    )

    actual_status = appointment.get("status")

    assert actual_status == "pending", (
        f"{test_case_id} | STEP 6 FAILED | "
        "Trạng thái lịch hẹn không đúng. "
        "Expected: pending | "
        f"Actual: {actual_status}"
    )

    appointment_id = appointment.get("appointmentId")

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            "Đặt lịch thành công và lịch hẹn "
            "được tạo với trạng thái pending"
        ),
        detail=(
            f"Appointment ID: {appointment_id} | "
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