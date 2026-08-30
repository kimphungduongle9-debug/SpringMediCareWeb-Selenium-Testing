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
def test_tc_booking_001_booking_success(driver):
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

def test_tc_booking_002_without_date(driver):
    """
    TC-BOOKING-002:
    Kiểm tra Patient không thể đặt lịch
    khi chưa chọn ngày khám.
    """

    test_case_id = "TC-BOOKING-002"
    test_data = get_test_data_csv(BOOKING_TEST_DATA_CSV, test_case_id)

    # Step 1 - Đăng nhập Patient
    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    assert driver.current_url == "http://localhost:3000/", (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id, 1,
        "Đăng nhập bằng tài khoản Patient hợp lệ thành công"
    )

    # Step 2 - Mở trang Đặt lịch
    booking_page = open_tran_binh_booking_page(driver)

    assert driver.current_url == BOOKING_URL, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected: {BOOKING_URL} | Actual: {driver.current_url}"
    )

    report_step(
        test_case_id, 2,
        "Mở trang Đặt lịch của bác sĩ Tran Binh thành công"
    )

    # Step 3 - Để trống Ngày khám
    date_value = booking_page.find(
        *booking_page.DATE_INPUT
    ).get_attribute("value")

    assert not date_value, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: Ngày khám để trống | Actual: {date_value}"
    )

    report_step(
        test_case_id, 3,
        "Để trống trường Ngày khám"
    )

    # Step 4 - Kiểm tra validation ngày
    actual_warning = booking_page.get_warning_message()
    expected_warning = test_data["expected_no_date_message"]

    assert actual_warning == expected_warning, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: {expected_warning} | Actual: {actual_warning}"
    )

    report_step(
        test_case_id, 4,
        "Hệ thống nhận biết trường Ngày khám chưa được chọn",
        detail=actual_warning
    )

    # Step 5 - Không cho phép đặt lịch
    disabled = booking_page.is_booking_button_disabled()

    assert disabled is True, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: disabled=True | Actual: {disabled}"
    )

    report_step(
        test_case_id, 5,
        "Hệ thống không cho phép thực hiện Đặt lịch khi chưa chọn ngày"
    )

    # Step 6 - Xác nhận validation cuối cùng
    final_warning = booking_page.get_warning_message()

    assert final_warning == expected_warning, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: {expected_warning} | Actual: {final_warning}"
    )

    assert booking_page.is_booking_button_disabled(), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Nút Đặt lịch không bị disable"
    )

    report_step(
        test_case_id, 6,
        "Hiển thị đúng validation và không cho phép tạo lịch hẹn",
        detail=final_warning
    )

def test_tc_booking_003_without_time(driver):
    """
    TC-BOOKING-003:
    Không thể đặt lịch khi chưa chọn giờ khám.
    """

    test_case_id = "TC-BOOKING-003"

    test_data = get_test_data_csv(
        BOOKING_TEST_DATA_CSV,
        test_case_id
    )

    doctor_id = int(
        test_data["doctor_id"]
    )

    booking_slot = get_or_create_booking_slot(
        doctor_id=doctor_id,
        test_data=test_data,
        schedule_note=(
            test_data["note_prefix"]
            + "SCHEDULE"
        )
    )

    booking_date = booking_slot["booking_date"]

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
        "Expected: đăng nhập Patient thành công | "
        f"Actual URL: {driver.current_url}"
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
    # Mở trang Đặt lịch của bác sĩ cần đặt.
    # ============================================================

    booking_page = open_tran_binh_booking_page(driver)

    assert driver.current_url == BOOKING_URL, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected URL: {BOOKING_URL} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description=(
            "Mở trang Đặt lịch của bác sĩ "
            "Tran Binh thành công"
        )
    )

    # ============================================================
    # STEP 3:
    # Chọn một ngày bác sĩ có lịch làm việc.
    # ============================================================

    booking_page.enter_date(
        booking_date
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            f"Chọn ngày bác sĩ có lịch làm việc: "
            f"{booking_date}"
        )
    )

    # ============================================================
    # STEP 4:
    # Để trống giờ khám.
    # ============================================================

    actual_time = booking_page.get_time_value()

    assert not actual_time, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Giờ khám để trống | "
        f"Actual: {actual_time}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description="Để trống trường Giờ khám"
    )

    # ============================================================
    # STEP 5:
    # Kiểm tra hệ thống không cho phép đặt lịch.
    # ============================================================

    disabled = booking_page.is_booking_button_disabled()

    assert disabled is True, (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: nút Đặt lịch bị disable | "
        f"Actual: disabled={disabled}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            "Hệ thống không cho phép thực hiện "
            "Đặt lịch khi chưa chọn giờ"
        )
    )

    # ============================================================
    # STEP 6:
    # Kiểm tra validation và xác nhận không tạo lịch hẹn.
    # ============================================================

    actual_warning = (
        booking_page.get_time_warning_message()
    )

    expected_warning = (
        test_data["expected_no_time_message"]
    )

    assert actual_warning == expected_warning, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: {expected_warning} | "
        f"Actual: {actual_warning}"
    )

    assert booking_page.is_booking_button_disabled(), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: không cho phép tạo lịch | "
        "Actual: nút Đặt lịch đang được enable"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            "Hiển thị đúng validation và "
            "không cho phép tạo lịch hẹn"
        ),
        detail=actual_warning
    )
def test_tc_booking_004_without_note(driver):
    """
    TC-BOOKING-004:
    Kiểm tra Patient vẫn đặt lịch thành công
    khi không nhập ghi chú.
    """

    test_case_id = "TC-BOOKING-004"
    test_data = get_test_data_csv(BOOKING_TEST_DATA_CSV, test_case_id)

    doctor_id = int(test_data["doctor_id"])

    booking_slot = get_or_create_booking_slot(
        doctor_id=doctor_id,
        test_data=test_data,
        schedule_note=test_data["note_prefix"] + "SCHEDULE"
    )

    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    # Step 1 - Đăng nhập Patient
    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    assert driver.current_url == "http://localhost:3000/", (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected: đăng nhập Patient thành công | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description="Đăng nhập bằng tài khoản Patient hợp lệ thành công"
    )

    # Step 2 - Mở trang Đặt lịch
    booking_page = open_tran_binh_booking_page(driver)

    assert driver.current_url == BOOKING_URL, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected URL: {BOOKING_URL} | Actual: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description="Mở trang Đặt lịch của bác sĩ Tran Binh thành công"
    )

    # Step 3 - Chọn ngày và giờ hợp lệ
    booking_page.enter_date(booking_date)
    booking_page.enter_time(booking_time)

    actual_time = booking_page.get_time_value()

    assert actual_time == booking_time, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected time: {booking_time} | Actual: {actual_time}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=f"Chọn ngày {booking_date} và giờ {booking_time} hợp lệ"
    )

    # Step 4 - Để trống Ghi chú
    note_value = booking_page.find(
        *booking_page.NOTES_INPUT
    ).get_attribute("value")

    assert not note_value, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: Ghi chú để trống | Actual: {note_value}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description="Để trống trường Ghi chú"
    )

    # Step 5 - Nhấn Đặt lịch
    booking_page.click_booking_button()

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description="Nhấn nút Đặt lịch"
    )

    # Step 6 - Kiểm tra kết quả
    message = booking_page.get_message()
    expected_message = test_data["expected_success_message"]

    assert expected_message in message, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: {expected_message} | Actual: {message}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description="Đặt lịch thành công mặc dù không nhập Ghi chú",
        detail=message
    )