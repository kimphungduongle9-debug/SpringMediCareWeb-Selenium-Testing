from datetime import datetime, timedelta

from pages.DoctorWorkSchedulePage import DoctorWorkSchedulePage

from utils.data_reader import get_test_data_csv, WORK_SCHEDULE_TEST_DATA_CSV
from utils.test_reporter import report_step

from tests.helpers.work_schedule_helpers import login_doctor


def report_test_case_start(test_case_id, description):
    print()
    print("=" * 100)
    print(f"{test_case_id} | {description}")
    print("=" * 100)


# ============================================================
# TC-WORKSCHEDULE-001
# ============================================================

def test_tc_workschedule_001(driver):
    test_case_id = "TC-WORKSCHEDULE-001"
    description = (
        "Kiểm tra Doctor xem được đúng thông tin cá nhân "
        "và lịch làm việc của mình trong tuần được hiển thị."
    )

    report_test_case_start(test_case_id, description)

    test_data = get_test_data_csv(
        WORK_SCHEDULE_TEST_DATA_CSV,
        test_case_id
    )

    # Step 1: Đăng nhập bằng tài khoản Doctor có lịch làm việc
    login_doctor(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản Doctor thành công"
    )

    # Step 2: Mở trang Lịch làm việc của tôi
    schedule_page = DoctorWorkSchedulePage(driver)
    schedule_page.open_page()

    actual_title = schedule_page.get_page_title()
    expected_title = test_data["expected_page_title"]

    assert actual_title == expected_title, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected: {expected_title} | Actual: {actual_title}"
    )

    report_step(
        test_case_id,
        2,
        "Mở trang Lịch làm việc của tôi thành công"
    )

    # Step 3: Kiểm tra tên Doctor và chuyên khoa
    doctor_name = schedule_page.get_doctor_name()
    specialty = schedule_page.get_specialty()

    assert doctor_name.strip() != "", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Tên Doctor không rỗng | Actual: rỗng"
    )

    assert specialty.strip() != "", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Chuyên khoa không rỗng | Actual: rỗng"
    )

    report_step(
        test_case_id,
        3,
        f"Hiển thị Doctor {doctor_name} - Chuyên khoa {specialty}"
    )

    # Step 4: Kiểm tra khoảng thời gian và 7 ngày của tuần
    week_range = schedule_page.get_week_range()
    dates = schedule_page.get_week_header_dates()

    assert week_range.strip() != "", (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Có khoảng thời gian tuần | Actual: rỗng"
    )

    assert len(dates) == 7, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: 7 ngày | Actual: {len(dates)} ngày"
    )

    parsed_dates = [
        datetime.strptime(date, "%d/%m/%Y")
        for date in dates
    ]

    for index in range(1, len(parsed_dates)):
        expected_date = parsed_dates[index - 1] + timedelta(days=1)

        assert parsed_dates[index] == expected_date, (
            f"{test_case_id} | STEP 4 FAILED | "
            f"Expected ngày tiếp theo: {expected_date.strftime('%d/%m/%Y')} | "
            f"Actual: {parsed_dates[index].strftime('%d/%m/%Y')}"
        )

    report_step(
        test_case_id,
        4,
        f"Tuần hiển thị đúng 7 ngày liên tiếp: {week_range}"
    )

    # Step 5: Kiểm tra các ca Sáng, Chiều, Tối
    shifts = schedule_page.get_week_shift_rows()

    assert len(shifts) == 3, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: 3 ca làm việc | Actual: {len(shifts)}"
    )

    assert test_data["expected_shift_morning"] in shifts[0], (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: {test_data['expected_shift_morning']} | Actual: {shifts[0]}"
    )

    assert test_data["expected_shift_afternoon"] in shifts[1], (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: {test_data['expected_shift_afternoon']} | Actual: {shifts[1]}"
    )

    assert test_data["expected_shift_evening"] in shifts[2], (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: {test_data['expected_shift_evening']} | Actual: {shifts[2]}"
    )

    report_step(
        test_case_id,
        5,
        "Bảng lịch hiển thị đầy đủ Ca sáng, Ca chiều và Ca tối"
    )

    # Step 6: Kiểm tra lịch thuộc đúng Doctor và các ô trống
    doctor_names = schedule_page.get_week_doctor_names()
    empty_count = schedule_page.get_empty_cell_count()

    assert all(name == doctor_name for name in doctor_names), (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: Chỉ hiển thị Doctor {doctor_name} | "
        f"Actual Doctor trong bảng: {doctor_names}"
    )

    assert empty_count >= 0, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: Số ô Trống hợp lệ | Actual: {empty_count}"
    )

    report_step(
        test_case_id,
        6,
        f"Các lịch thuộc đúng Doctor {doctor_name}; số ô Trống: {empty_count}"
    )


# ============================================================
# TC-WORKSCHEDULE-002
# ============================================================

def test_tc_workschedule_002(driver):
    test_case_id = "TC-WORKSCHEDULE-002"
    description = (
        "Kiểm tra chức năng Tuần trước hiển thị đúng lịch làm việc "
        "của Doctor trong tuần liền trước."
    )

    report_test_case_start(test_case_id, description)

    test_data = get_test_data_csv(
        WORK_SCHEDULE_TEST_DATA_CSV,
        test_case_id
    )

    # Step 1: Đăng nhập bằng Doctor
    login_doctor(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản Doctor thành công"
    )

    # Step 2: Mở trang và ghi nhận tuần hiện tại
    schedule_page = DoctorWorkSchedulePage(driver)
    schedule_page.open_page()

    week_before = schedule_page.get_week_range()
    dates_before = schedule_page.get_week_header_dates()

    assert len(dates_before) == 7, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected: 7 ngày | Actual: {len(dates_before)}"
    )

    report_step(
        test_case_id,
        2,
        f"Ghi nhận tuần đang hiển thị: {week_before}"
    )

    # Step 3: Nhấn Tuần trước
    schedule_page.click_previous_week()

    dates_after = schedule_page.get_week_header_dates()

    assert len(dates_after) == 7, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: 7 ngày sau khi chuyển tuần | Actual: {len(dates_after)}"
    )

    report_step(
        test_case_id,
        3,
        "Nhấn Tuần trước thành công"
    )

    # Step 4: Kiểm tra khoảng thời gian và ngày sau khi chuyển tuần
    week_after = schedule_page.get_week_range()

    first_date_before = datetime.strptime(
        dates_before[0],
        "%d/%m/%Y"
    )

    first_date_after = datetime.strptime(
        dates_after[0],
        "%d/%m/%Y"
    )

    expected_date = first_date_before - timedelta(days=7)

    assert first_date_after == expected_date, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: {expected_date.strftime('%d/%m/%Y')} | "
        f"Actual: {first_date_after.strftime('%d/%m/%Y')}"
    )

    assert week_after != week_before, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: Khoảng tuần thay đổi | Actual vẫn là: {week_after}"
    )

    report_step(
        test_case_id,
        4,
        f"Tuần được chuyển đúng từ {week_before} sang {week_after}"
    )

    # Step 5: Kiểm tra dữ liệu lịch thuộc tuần vừa chọn
    week_records = schedule_page.get_week_schedule_records()

    selected_dates = {
        datetime.strptime(date, "%d/%m/%Y").date()
        for date in dates_after
    }

    invalid_records = [
        record
        for record in week_records
        if datetime.strptime(record["date"], "%d/%m/%Y").date()
           not in selected_dates
    ]

    assert not invalid_records, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: Chỉ có lịch thuộc tuần đã chọn | "
        f"Actual record sai tuần: {invalid_records}"
    )

    assert not invalid_records, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: Chỉ có lịch thuộc tuần đã chọn | "
        f"Actual record sai tuần: {invalid_records}"
    )

    report_step(
        test_case_id,
        5,
        f"Dữ liệu lịch thuộc đúng tuần vừa chọn, tổng số lịch: {len(week_records)}"
    )


# ============================================================
# TC-WORKSCHEDULE-003
# ============================================================

def test_tc_workschedule_003(driver):
    test_case_id = "TC-WORKSCHEDULE-003"
    description = (
        "Kiểm tra chức năng Tuần sau hiển thị đúng lịch làm việc "
        "của Doctor trong tuần kế tiếp."
    )

    report_test_case_start(test_case_id, description)

    test_data = get_test_data_csv(
        WORK_SCHEDULE_TEST_DATA_CSV,
        test_case_id
    )

    # Step 1: Đăng nhập bằng Doctor
    login_doctor(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản Doctor thành công"
    )

    # Step 2: Mở trang và ghi nhận tuần hiện tại
    schedule_page = DoctorWorkSchedulePage(driver)
    schedule_page.open_page()

    week_before = schedule_page.get_week_range()
    dates_before = schedule_page.get_week_header_dates()

    assert len(dates_before) == 7, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected: 7 ngày | Actual: {len(dates_before)}"
    )

    report_step(
        test_case_id,
        2,
        f"Ghi nhận tuần đang hiển thị: {week_before}"
    )

    # Step 3: Nhấn Tuần sau
    schedule_page.click_next_week()

    dates_after = schedule_page.get_week_header_dates()

    assert len(dates_after) == 7, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: 7 ngày sau khi chuyển tuần | Actual: {len(dates_after)}"
    )

    report_step(
        test_case_id,
        3,
        "Nhấn Tuần sau thành công"
    )

    # Step 4: Kiểm tra khoảng thời gian và ngày sau khi chuyển tuần
    week_after = schedule_page.get_week_range()

    first_date_before = datetime.strptime(
        dates_before[0],
        "%d/%m/%Y"
    )

    first_date_after = datetime.strptime(
        dates_after[0],
        "%d/%m/%Y"
    )

    expected_date = first_date_before + timedelta(days=7)

    assert first_date_after == expected_date, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: {expected_date.strftime('%d/%m/%Y')} | "
        f"Actual: {first_date_after.strftime('%d/%m/%Y')}"
    )

    assert week_after != week_before, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: Khoảng tuần thay đổi | Actual vẫn là: {week_after}"
    )

    report_step(
        test_case_id,
        4,
        f"Tuần được chuyển đúng từ {week_before} sang {week_after}"
    )
    # Step 5: Kiểm tra dữ liệu lịch thuộc tuần vừa chọn
    week_records = schedule_page.get_week_schedule_records()

    selected_dates = {
        datetime.strptime(date, "%d/%m/%Y").date()
        for date in dates_after
    }

    invalid_records = [
        record
        for record in week_records
        if datetime.strptime(record["date"], "%d/%m/%Y").date()
           not in selected_dates
    ]

    assert not invalid_records, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: Chỉ có lịch thuộc tuần đã chọn | "
        f"Actual record sai tuần: {invalid_records}"
    )

    report_step(
        test_case_id,
        5,
        f"Dữ liệu lịch thuộc đúng tuần vừa chọn, tổng số lịch: {len(week_records)}"
    )