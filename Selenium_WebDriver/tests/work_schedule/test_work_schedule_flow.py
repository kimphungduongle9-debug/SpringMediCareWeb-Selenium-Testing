from pages.DoctorWorkSchedulePage import DoctorWorkSchedulePage

from utils.data_reader import get_test_data_csv, WORK_SCHEDULE_TEST_DATA_CSV
from utils.test_reporter import report_step

from tests.helpers.work_schedule_helpers import (
    login_doctor,
    logout_current_user,
)


def report_test_case_start(test_case_id, description):
    print()
    print("=" * 100)
    print(f"{test_case_id} | {description}")
    print("=" * 100)


# ============================================================
# TC-WORKSCHEDULE-004
# ============================================================

def test_tc_workschedule_004(driver):
    test_case_id = "TC-WORKSCHEDULE-004"
    description = (
        "Kiểm tra thông tin lịch làm việc trong bảng Lịch làm việc theo tuần "
        "khớp với dữ liệu trong Danh sách lịch làm việc của Doctor."
    )

    report_test_case_start(test_case_id, description)

    test_data = get_test_data_csv(
        WORK_SCHEDULE_TEST_DATA_CSV,
        test_case_id
    )

    # Step 1: Đăng nhập bằng Doctor có lịch làm việc
    login_doctor(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản Doctor có lịch làm việc thành công"
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

    # Step 3: Ghi nhận các lịch trong một tuần có dữ liệu
    week_range = schedule_page.get_week_range()

    if not schedule_page.has_schedule_in_week():
        for _ in range(4):
            schedule_page.click_previous_week()

            if schedule_page.has_schedule_in_week():
                break

    assert schedule_page.has_schedule_in_week(), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Tìm thấy ít nhất một tuần có lịch làm việc | "
        "Actual: Không có lịch trong tuần hiện tại và 4 tuần trước"
    )

    week_range = schedule_page.get_week_range()
    week_records = schedule_page.get_week_schedule_records()

    assert len(week_records) > 0, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: Có ít nhất 1 lịch trong tuần {week_range} | "
        f"Actual: {len(week_records)} lịch"
    )

    report_step(
        test_case_id,
        3,
        f"Ghi nhận {len(week_records)} lịch trong tuần {week_range}"
    )

    # Step 4: Mở khu vực Danh sách lịch làm việc
    schedule_page.scroll_to_schedule_list()

    report_step(
        test_case_id,
        4,
        "Mở khu vực Danh sách lịch làm việc phía dưới"
    )

    # Step 5: Ghi nhận dữ liệu trong danh sách
    list_records = schedule_page.get_schedule_list_records()

    assert len(list_records) > 0, (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Có dữ liệu trong Danh sách lịch làm việc | Actual: 0 lịch"
    )

    report_step(
        test_case_id,
        5,
        f"Ghi nhận {len(list_records)} lịch trong Danh sách lịch làm việc"
    )

    # Step 6: Đối chiếu Doctor, ngày, ca và thời gian
    def normalize_record(record):
        return {
            "doctor": record["doctor"].strip(),
            "date": record["date"].strip(),
            "shift": record["shift"].strip(),
            "start": record["start"].strip(),
            "end": record["end"].strip(),
        }

    normalized_week = [
        normalize_record(record)
        for record in week_records
    ]

    normalized_list = [
        normalize_record(record)
        for record in list_records
    ]

    missing_records = [
        record
        for record in normalized_week
        if record not in normalized_list
    ]

    assert not missing_records, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: Mọi lịch trong bảng tuần đều có trong danh sách | "
        f"Actual thiếu: {missing_records}"
    )

    report_step(
        test_case_id,
        6,
        "Doctor, ngày, ca và thời gian khớp giữa bảng tuần và danh sách"
    )


# ============================================================
# TC-WORKSCHEDULE-005
# ============================================================

def test_tc_workschedule_005(driver):
    test_case_id = "TC-WORKSCHEDULE-005"
    description = (
        "Kiểm tra mỗi Doctor chỉ xem được lịch làm việc thuộc tài khoản của mình "
        "và không bị hiển thị lịch của Doctor khác."
    )

    report_test_case_start(test_case_id, description)

    test_data = get_test_data_csv(
        WORK_SCHEDULE_TEST_DATA_CSV,
        test_case_id
    )

    # Step 1: Đăng nhập bằng Doctor A
    login_doctor(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng Doctor A thành công"
    )

    # Step 2: Ghi nhận thông tin và lịch của Doctor A
    schedule_page = DoctorWorkSchedulePage(driver)
    schedule_page.open_page()

    doctor_a_name = schedule_page.get_doctor_name()
    doctor_a_specialty = schedule_page.get_specialty()
    doctor_a_week_records = schedule_page.get_week_schedule_records()

    schedule_page.scroll_to_schedule_list()
    doctor_a_list_records = schedule_page.get_schedule_list_records()

    assert doctor_a_name.strip() != "", (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected: Có tên Doctor A | Actual: rỗng"
    )

    assert doctor_a_specialty.strip() != "", (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected: Có chuyên khoa Doctor A | Actual: rỗng"
    )

    assert all(
        record["doctor"] == doctor_a_name
        for record in doctor_a_week_records
    ), (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected: Bảng tuần chỉ có {doctor_a_name} | "
        f"Actual: {doctor_a_week_records}"
    )

    assert all(
        record["doctor"] == doctor_a_name
        for record in doctor_a_list_records
    ), (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected: Danh sách chỉ có {doctor_a_name} | "
        f"Actual: {doctor_a_list_records}"
    )

    report_step(
        test_case_id,
        2,
        f"Ghi nhận Doctor A: {doctor_a_name} - {doctor_a_specialty}"
    )

    # Step 3: Đăng xuất Doctor A
    logout_current_user(driver)

    report_step(
        test_case_id,
        3,
        "Đăng xuất Doctor A thành công"
    )

    # Step 4: Đăng nhập bằng Doctor B
    login_doctor(
        driver,
        test_data["other_doctor_username"],
        test_data["other_doctor_password"]
    )

    report_step(
        test_case_id,
        4,
        "Đăng nhập bằng Doctor B thành công"
    )

    # Step 5: Ghi nhận thông tin và lịch của Doctor B
    schedule_page = DoctorWorkSchedulePage(driver)
    schedule_page.open_page()

    doctor_b_name = schedule_page.get_doctor_name()
    doctor_b_specialty = schedule_page.get_specialty()
    doctor_b_week_records = schedule_page.get_week_schedule_records()

    schedule_page.scroll_to_schedule_list()
    doctor_b_list_records = schedule_page.get_schedule_list_records()

    assert doctor_b_name.strip() != "", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Có tên Doctor B | Actual: rỗng"
    )

    assert doctor_b_specialty.strip() != "", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Có chuyên khoa Doctor B | Actual: rỗng"
    )

    assert doctor_b_name != doctor_a_name, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: Doctor B khác Doctor A ({doctor_a_name}) | "
        f"Actual: {doctor_b_name}"
    )

    report_step(
        test_case_id,
        5,
        f"Ghi nhận Doctor B: {doctor_b_name} - {doctor_b_specialty}"
    )

    # Step 6: Kiểm tra Doctor B chỉ thấy lịch của mình
    assert all(
        record["doctor"] == doctor_b_name
        for record in doctor_b_week_records
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: Bảng tuần chỉ có {doctor_b_name} | "
        f"Actual: {doctor_b_week_records}"
    )

    assert all(
        record["doctor"] == doctor_b_name
        for record in doctor_b_list_records
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: Danh sách chỉ có {doctor_b_name} | "
        f"Actual: {doctor_b_list_records}"
    )

    report_step(
        test_case_id,
        6,
        f"Doctor B chỉ thấy lịch làm việc của {doctor_b_name}"
    )

    # Step 7: Đối chiếu dữ liệu A và B, bảo đảm không bị lẫn
    doctor_b_week_names = [
        record["doctor"]
        for record in doctor_b_week_records
    ]

    doctor_b_list_names = [
        record["doctor"]
        for record in doctor_b_list_records
    ]

    assert doctor_a_name not in doctor_b_week_names, (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected: Không có Doctor A ({doctor_a_name}) trong bảng của Doctor B | "
        f"Actual: {doctor_b_week_names}"
    )

    assert doctor_a_name not in doctor_b_list_names, (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected: Không có Doctor A ({doctor_a_name}) trong danh sách của Doctor B | "
        f"Actual: {doctor_b_list_names}"
    )

    report_step(
        test_case_id,
        7,
        f"Dữ liệu Doctor A ({doctor_a_name}) và Doctor B ({doctor_b_name}) được phân tách đúng"
    )