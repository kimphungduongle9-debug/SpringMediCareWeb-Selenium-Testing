from datetime import datetime, timedelta

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
def test_tc_booking_005_day_without_schedule(driver):
    """
    TC-BOOKING-005:
    Kiểm tra Patient không thể đặt lịch
    vào ngày bác sĩ không có lịch làm việc.
    """

    test_case_id = "TC-BOOKING-005"
    test_data = get_test_data_csv(BOOKING_TEST_DATA_CSV, test_case_id)

    # Tìm một ngày tương lai không có lịch làm việc.
    no_schedule_date = (
        datetime.now() + timedelta(days=60)
    ).strftime("%d/%m/%Y")

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

    # Step 3 - Chọn ngày bác sĩ không có lịch làm việc
    booking_page.enter_date(no_schedule_date)

    report_step(
        test_case_id, 3,
        f"Chọn ngày bác sĩ không có lịch làm việc: {no_schedule_date}"
    )

    # Step 4 - Kiểm tra trạng thái thời gian
    actual_message = booking_page.get_no_schedule_message()
    expected_message = test_data["expected_no_schedule_message"]

    assert actual_message == expected_message, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: {expected_message} | Actual: {actual_message}"
    )

    report_step(
        test_case_id, 4,
        "Hệ thống xác định bác sĩ không có lịch làm việc trong ngày đã chọn",
        detail=actual_message
    )

    # Step 5 - Kiểm tra không cho phép đặt lịch
    disabled = booking_page.is_booking_button_disabled()

    assert disabled is True, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: disabled=True | Actual: {disabled}"
    )

    report_step(
        test_case_id, 5,
        "Hệ thống không cho phép thực hiện Đặt lịch"
    )

    # Step 6 - Xác nhận lịch hẹn không được tạo
    final_message = booking_page.get_no_schedule_message()

    assert final_message == expected_message, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: {expected_message} | Actual: {final_message}"
    )

    assert booking_page.is_booking_button_disabled(), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Nút Đặt lịch vẫn được enable"
    )

    report_step(
        test_case_id, 6,
        "Không tạo lịch hẹn vào ngày bác sĩ không làm việc",
        detail=final_message
    )

def test_tc_booking_006_outside_working_hours(driver):
    """
    TC-BOOKING-006:
    Kiểm tra Patient không thể đặt lịch
    vào giờ nằm ngoài ca làm việc của bác sĩ.
    """

    test_case_id = "TC-BOOKING-006"
    test_data = get_test_data_csv(
        BOOKING_TEST_DATA_CSV,
        test_case_id
    )

    doctor_id = int(test_data["doctor_id"])

    # Step 1 - Đăng nhập Patient
    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    assert driver.current_url == "http://localhost:3000/", (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected URL: http://localhost:3000/ | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản Patient hợp lệ thành công"
    )

    # Step 2 - Mở trang Đặt lịch
    booking_page = open_tran_binh_booking_page(driver)

    assert driver.current_url == BOOKING_URL, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected URL: {BOOKING_URL} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        2,
        "Mở trang Đặt lịch của bác sĩ Tran Binh thành công"
    )

    # Step 3 - Chọn ngày bác sĩ có lịch làm việc
    try:
        booking_slot = get_or_create_booking_slot(
            doctor_id=doctor_id,
            test_data=test_data,
            schedule_note=test_data["note_prefix"] + "SCHEDULE"
        )

        booking_date = booking_slot["booking_date"]

    except Exception as exc:
        raise AssertionError(
            f"{test_case_id} | STEP 3 FAILED | "
            "Không thể tìm hoặc chuẩn bị ngày bác sĩ có lịch làm việc. "
            f"Actual: {exc}"
        ) from exc

    booking_page.enter_date(booking_date)

    report_step(
        test_case_id,
        3,
        f"Chọn ngày bác sĩ có lịch làm việc: {booking_date}"
    )

    # Step 4 - Nhập giờ ngoài ca làm việc
    outside_time = "12:00"

    booking_page.enter_time(outside_time)

    actual_time = booking_page.get_time_value()

    assert actual_time == outside_time, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected time: {outside_time} | "
        f"Actual time: {actual_time}"
    )

    report_step(
        test_case_id,
        4,
        f"Nhập giờ {outside_time} nằm ngoài ca làm việc của bác sĩ"
    )

    # Step 5 - Thực hiện đặt lịch
    booking_page.click_booking_button()

    report_step(
        test_case_id,
        5,
        "Nhấn nút Đặt lịch"
    )

    # Step 6 - Kiểm tra hệ thống từ chối
    message = booking_page.get_message()
    expected_message = test_data["expected_outside_hours_message"]

    assert expected_message in message, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: {expected_message} | "
        f"Actual: {message}"
    )

    report_step(
        test_case_id,
        6,
        "Hệ thống từ chối đặt lịch vào giờ ngoài ca làm việc",
        detail=f"Expected: {expected_message} | Actual: {message}"
    )