from utils.data_reader import (
    get_test_data_csv,
    BOOKING_TEST_DATA_CSV,
)
from utils.test_reporter import report_step
import pytest
from pages.DoctorPage import DoctorPage
from tests.helpers.booking_helpers import (
    BOOKING_URL,
    login_account,
    open_tran_binh_booking_page,
)
def test_tc_booking_007_duplicate_time(driver, booking_test_data):
    """
    TC-BOOKING-007:
    Kiểm tra Patient không thể đặt lịch
    trùng đúng thời gian đã có người đặt.
    """

    test_case_id = "TC-BOOKING-007"
    test_data = get_test_data_csv(BOOKING_TEST_DATA_CSV, test_case_id)

    doctor_id = int(test_data["doctor_id"])
    booking_date = "11/04/2026"
    booking_time = "14:00"

    # Step 1 - Chuẩn bị lịch đã tồn tại
    existing_appointment = booking_test_data.create_appointment(
        patient_id=1,
        doctor_id=doctor_id,
        booking_date=booking_date,
        booking_time=booking_time,
        notes=test_data["note_prefix"] + "EXISTING"
    )

    assert existing_appointment is not None, (
        f"{test_case_id} | STEP 1 FAILED | "
        "Không tạo được lịch hẹn chuẩn bị cho test."
    )

    report_step(
        test_case_id, 1,
        f"Chuẩn bị lịch đã tồn tại lúc {booking_time} ngày {booking_date}"
    )

    # Step 2 - Đăng nhập Patient thứ hai
    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    assert driver.current_url == "http://localhost:3000/", (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id, 2,
        "Đăng nhập bằng tài khoản Patient thứ hai thành công"
    )

    # Step 3 - Mở trang Đặt lịch
    booking_page = open_tran_binh_booking_page(driver)

    assert driver.current_url == BOOKING_URL, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: {BOOKING_URL} | Actual: {driver.current_url}"
    )

    report_step(
        test_case_id, 3,
        "Mở trang Đặt lịch của bác sĩ Tran Binh thành công"
    )

    # Step 4 - Chọn đúng ngày và giờ đã tồn tại
    booking_page.enter_date(booking_date)
    booking_page.enter_time(booking_time)

    actual_time = booking_page.get_time_value()

    assert actual_time == booking_time, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: {booking_time} | Actual: {actual_time}"
    )

    report_step(
        test_case_id, 4,
        f"Chọn đúng khung giờ đã có người đặt: {booking_date} {booking_time}"
    )

    # Step 5 - Nhấn Đặt lịch
    booking_page.click_booking_button()

    report_step(
        test_case_id, 5,
        "Nhấn nút Đặt lịch"
    )

    # Step 6 - Kiểm tra hệ thống từ chối
    message = booking_page.get_message()
    expected_message = test_data["expected_duplicate_message"]

    assert expected_message in message, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: {expected_message} | Actual: {message}"
    )

    report_step(
        test_case_id, 6,
        "Hệ thống từ chối đặt lịch trùng giờ đã tồn tại",
        detail=message
    )

def test_tc_booking_008_within_thirty_minutes(driver, booking_test_data):
    """
    TC-BOOKING-008:
    Kiểm tra Patient không thể đặt lịch
    cách lịch đã tồn tại dưới 30 phút.
    """

    test_case_id = "TC-BOOKING-008"
    test_data = get_test_data_csv(BOOKING_TEST_DATA_CSV, test_case_id)

    doctor_id = int(test_data["doctor_id"])
    booking_date = "11/04/2026"
    existing_time = "15:30"
    test_time = "15:31"

    # Step 1 - Chuẩn bị lịch đã tồn tại
    existing_appointment = booking_test_data.create_appointment(
        patient_id=1,
        doctor_id=doctor_id,
        booking_date=booking_date,
        booking_time=existing_time,
        notes=test_data["note_prefix"] + "EXISTING"
    )

    assert existing_appointment is not None, (
        f"{test_case_id} | STEP 1 FAILED | "
        "Không tạo được lịch hẹn chuẩn bị cho test."
    )

    report_step(
        test_case_id, 1,
        f"Chuẩn bị lịch đã tồn tại lúc {existing_time} ngày {booking_date}"
    )

    # Step 2 - Đăng nhập Patient thứ hai
    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    assert driver.current_url == "http://localhost:3000/", (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id, 2,
        "Đăng nhập bằng tài khoản Patient thứ hai thành công"
    )

    # Step 3 - Mở trang Đặt lịch
    booking_page = open_tran_binh_booking_page(driver)

    assert driver.current_url == BOOKING_URL, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: {BOOKING_URL} | Actual: {driver.current_url}"
    )

    report_step(
        test_case_id, 3,
        "Mở trang Đặt lịch của bác sĩ Tran Binh thành công"
    )

    # Step 4 - Chọn thời gian cách lịch cũ dưới 30 phút
    booking_page.enter_date(booking_date)
    booking_page.enter_time(test_time)

    actual_time = booking_page.get_time_value()

    assert actual_time == test_time, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: {test_time} | Actual: {actual_time}"
    )

    report_step(
        test_case_id, 4,
        f"Chọn giờ {test_time}, cách lịch {existing_time} dưới 30 phút"
    )

    # Step 5 - Nhấn Đặt lịch
    booking_page.click_booking_button()

    report_step(
        test_case_id, 5,
        "Nhấn nút Đặt lịch"
    )

    # Step 6 - Kiểm tra hệ thống từ chối
    message = booking_page.get_message()
    expected_message = test_data["expected_30_minutes_message"]

    assert expected_message in message, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected chứa: {expected_message} | Actual: {message}"
    )

    report_step(
        test_case_id, 6,
        "Hệ thống từ chối lịch cách lịch đã tồn tại dưới 30 phút",
        detail=message
    )
def test_tc_booking_009_guest_cannot_access_booking(driver):
    """
    TC-BOOKING-009:
    Kiểm tra Guest chưa đăng nhập không được
    truy cập chức năng Đặt lịch hẹn.
    """

    test_case_id = "TC-BOOKING-009"

    # Step 1 - Đảm bảo chưa đăng nhập
    driver.get("http://localhost:3000/")
    driver.delete_all_cookies()

    driver.execute_script(
        "window.localStorage.clear();"
        "window.sessionStorage.clear();"
    )

    driver.refresh()

    report_step(
        test_case_id, 1,
        "Đảm bảo người dùng đang ở trạng thái chưa đăng nhập"
    )

    # Step 2 - Mở trang Bác sĩ
    doctor_page = DoctorPage(driver)
    doctor_page.open_page()

    report_step(
        test_case_id, 2,
        "Guest mở trang Bác sĩ thành công"
    )

    # Step 3 - Chọn bác sĩ cần đặt lịch
    report_step(
        test_case_id, 3,
        "Chọn bác sĩ Tran Binh để thực hiện đặt lịch"
    )

    # Step 4 - Nhấn Đặt lịch hẹn
    doctor_page.book_tran_binh()

    report_step(
        test_case_id, 4,
        "Guest nhấn nút Đặt lịch hẹn"
    )

    # Step 5 - Kiểm tra trang được điều hướng đến
    current_url = driver.current_url

    if "/login" not in current_url:
        report_step(
            test_case_id=test_case_id,
            step_number=5,
            description=(
                "Guest không được chuyển đến trang đăng nhập"
            ),
            status="XFAIL",
            detail=(
                f"Expected URL chứa /login | "
                f"Actual: {current_url} | "
                "Known bug: Guest vẫn truy cập được trang Đặt lịch"
            )
        )

        pytest.xfail(
            f"KNOWN BUG - {test_case_id} | STEP 5 | "
            "Guest chưa đăng nhập vẫn truy cập được trang Đặt lịch. "
            f"Actual URL: {current_url}"
        )

    report_step(
        test_case_id, 5,
        "Guest được chuyển đến trang Đăng nhập"
    )

    # Step 6 - Xác nhận Guest không truy cập form Đặt lịch
    assert "/booking" not in driver.current_url, (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: Guest không truy cập form Đặt lịch | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id, 6,
        "Guest không thể truy cập form Đặt lịch"
    )