from datetime import date, timedelta

import pytest

from api.DoctorScheduleApi import DoctorScheduleApi
from pages.DoctorScheduleAdminPage import DoctorScheduleAdminPage
from tests.helpers.auth_helper import login_user
from utils.data_reader import (
    DOCTOR_SCHEDULE_ADMIN_TEST_DATA_CSV,
    get_test_data_csv,
)
from utils.test_reporter import report_step


# ============================================================
# TC-DS-ADMIN-012
# ============================================================

def test_tc_ds_admin_012_prevent_multiple_schedules_on_rapid_click(driver):
    """
    TC-DS-ADMIN-012:
    Kiểm tra hệ thống không tạo nhiều lịch
    khi Admin nhấn nút Thêm lịch liên tục.
    """

    test_case_id = "TC-DS-ADMIN-012"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra hệ thống không tạo nhiều lịch "
        "khi Admin nhấn nút Thêm lịch liên tục"
    )

    data = get_test_data_csv(
        DOCTOR_SCHEDULE_ADMIN_TEST_DATA_CSV,
        test_case_id
    )

    page = DoctorScheduleAdminPage(driver)
    api = DoctorScheduleApi()

    target_date = (
        date.today()
        + timedelta(days=int(data["date_offset_days"]))
    )

    date_display = target_date.strftime("%d/%m/%Y")
    date_api = target_date.strftime("%Y-%m-%d")

    token = api.get_token(
        data["username"],
        data["password"]
    )

    # SETUP
    api.delete_matching_schedule(
        doctor_name=data["doctor_name"],
        work_date=date_api,
        shift="morning",
        token=token
    )

    # Step 1
    login_user(
        driver,
        data["username"],
        data["password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập với vai trò Admin thành công"
    )

    # Step 2
    page.open_page()

    assert page.get_page_title() == data["page_title"], (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected: {data['page_title']} | "
        f"Actual: {page.get_page_title()}"
    )

    report_step(
        test_case_id,
        2,
        "Mở trang Quản lý lịch làm việc bác sĩ"
    )

    # Step 3
    page.select_doctor(data["doctor_name"])
    page.select_work_date(target_date)
    page.select_shift(data["shift_form"])
    page.select_status(data["status_form"])
    page.enter_note(data["note"])

    actual_doctor = page.get_selected_doctor_text()
    actual_date = page.get_work_date_value()
    actual_shift = page.get_selected_shift_text()
    actual_status = page.get_selected_status_text()
    actual_note = page.get_note_value()

    assert actual_doctor == data["doctor_name"]
    assert actual_date == date_display
    assert actual_shift == data["shift_form"]
    assert actual_status == data["status_form"]
    assert actual_note == data["note"]

    report_step(
        test_case_id,
        3,
        "Nhập thông tin hợp lệ cho một lịch chưa tồn tại",
        detail=(
            f"Doctor={actual_doctor} | "
            f"Date={actual_date} | "
            f"Shift={actual_shift} | "
            f"Status={actual_status} | "
            f"Note={actual_note}"
        )
    )

    # Step 4
    page.click_add_button_multiple_times(
        click_count=3
    )

    report_step(
        test_case_id,
        4,
        "Nhấn nút Thêm lịch 3 lần liên tục"
    )
    # Step 5
    try:
        actual_message = page.get_message()

        page.scroll_to_schedule_list()

        schedule_count = api.count_matching_schedules(
            doctor_name=data["doctor_name"],
            work_date=date_api,
            shift="morning"
        )

        schedule_in_list = page.is_schedule_present_in_list(
            doctor_name=data["doctor_name"],
            work_date=date_display,
            shift_name=data["shift_name"],
            status=data["status_display"],
            note=data["note"]
        )

        assert schedule_count == 1, (
            f"{test_case_id} | STEP 5 FAILED | "
            "Expected: Chỉ tạo đúng 1 lịch khi Admin "
            "nhấn nút Thêm lịch liên tục | "
            f"Actual count: {schedule_count}"
        )

        assert schedule_in_list, (
            f"{test_case_id} | STEP 5 FAILED | "
            "Không tìm thấy lịch vừa tạo "
            "trong Danh sách lịch làm việc"
        )

        report_step(
            test_case_id,
            5,
            "Kiểm tra hệ thống chỉ tạo một lịch làm việc",
            detail=(
                f"Message='{actual_message}' | "
                f"ScheduleCount={schedule_count} | "
                f"ScheduleInList={schedule_in_list}"
            )
        )

    finally:
        while True:
            deleted = api.delete_matching_schedule(
                doctor_name=data["doctor_name"],
                work_date=date_api,
                shift="morning",
                token=token
            )

            if not deleted:
                break

# ============================================================
# TC-DS-ADMIN-013
# ============================================================

def test_tc_ds_admin_013_reset_form_after_success(driver):
    """
    TC-DS-ADMIN-013:
    Kiểm tra form trở về trạng thái mặc định
    sau khi thêm lịch thành công.
    """

    test_case_id = "TC-DS-ADMIN-013"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra form trở về trạng thái mặc định "
        "sau khi thêm lịch thành công"
    )

    data = get_test_data_csv(
        DOCTOR_SCHEDULE_ADMIN_TEST_DATA_CSV,
        test_case_id
    )

    page = DoctorScheduleAdminPage(driver)
    api = DoctorScheduleApi()

    target_date = (
        date.today()
        + timedelta(days=int(data["date_offset_days"]))
    )

    date_display = target_date.strftime("%d/%m/%Y")
    date_api = target_date.strftime("%Y-%m-%d")

    token = api.get_token(
        data["username"],
        data["password"]
    )

    # SETUP
    api.delete_matching_schedule(
        doctor_name=data["doctor_name"],
        work_date=date_api,
        shift="afternoon",
        token=token
    )

    # Step 1
    login_user(
        driver,
        data["username"],
        data["password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập với vai trò Admin thành công"
    )

    # Step 2
    page.open_page()

    assert page.get_page_title() == data["page_title"]

    report_step(
        test_case_id,
        2,
        "Mở trang Quản lý lịch làm việc bác sĩ"
    )

    # Step 3
    page.select_doctor(data["doctor_name"])
    page.select_work_date(target_date)
    page.select_shift(data["shift_form"])
    page.select_status(data["status_form"])
    page.enter_note(data["note"])

    actual_doctor = page.get_selected_doctor_text()
    actual_date = page.get_work_date_value()
    actual_shift = page.get_selected_shift_text()
    actual_status = page.get_selected_status_text()
    actual_note = page.get_note_value()

    assert actual_doctor == data["doctor_name"]
    assert actual_date == date_display
    assert actual_shift == data["shift_form"]
    assert actual_status == data["status_form"]
    assert actual_note == data["note"]

    report_step(
        test_case_id,
        3,
        "Nhập dữ liệu hợp lệ cho một lịch chưa tồn tại",
        detail=(
            f"Doctor={actual_doctor} | "
            f"Date={actual_date} | "
            f"Shift={actual_shift} | "
            f"Status={actual_status} | "
            f"Note={actual_note}"
        )
    )

    # Step 4
    page.click_add_button()

    message = page.get_message()

    assert message == data["success_message"], (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: {data['success_message']} | "
        f"Actual: {message}"
    )

    report_step(
        test_case_id,
        4,
        "Thêm lịch thành công",
        detail=message
    )

    # Step 5
    try:
        doctor_default = page.get_selected_doctor_text()
        date_default = page.get_work_date_value()
        shift_default = page.get_selected_shift_text()
        status_default = page.get_selected_status_text()
        note_default = page.get_note_value()

        assert doctor_default == data["doctor_default"]
        assert date_default == ""
        assert shift_default == data["shift_default"]
        assert status_default == data["status_default"]
        assert note_default == ""
        assert page.is_add_button_displayed()

        report_step(
            test_case_id,
            5,
            "Kiểm tra form trở về trạng thái mặc định",
            detail=(
                f"Doctor={doctor_default} | "
                f"Date='{date_default}' | "
                f"Shift={shift_default} | "
                f"Status={status_default} | "
                f"Note='{note_default}'"
            )
        )

    finally:
        api.delete_matching_schedule(
            doctor_name=data["doctor_name"],
            work_date=date_api,
            shift="afternoon",
            token=token
        )


# ============================================================
# TC-DS-ADMIN-014
# ============================================================

def test_tc_ds_admin_014_filter_schedule_by_doctor(driver):
    """
    TC-DS-ADMIN-014:
    Kiểm tra Admin lọc lịch làm việc theo bác sĩ.
    """

    test_case_id = "TC-DS-ADMIN-014"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra Admin lọc lịch làm việc theo bác sĩ"
    )

    data = get_test_data_csv(
        DOCTOR_SCHEDULE_ADMIN_TEST_DATA_CSV,
        test_case_id
    )

    page = DoctorScheduleAdminPage(driver)

    # Step 1
    login_user(
        driver,
        data["username"],
        data["password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập với vai trò Admin thành công"
    )

    # Step 2
    page.open_page()

    actual_title = page.get_page_title()

    assert actual_title == data["page_title"], (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected: {data['page_title']} | "
        f"Actual: {actual_title}"
    )

    report_step(
        test_case_id,
        2,
        "Mở trang Quản lý lịch làm việc bác sĩ"
    )

    # Step 3
    page.select_filter_doctor(
        data["doctor_name"]
    )

    actual_doctor = (
        page.get_selected_filter_doctor_text()
    )

    assert actual_doctor == data["doctor_name"], (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: {data['doctor_name']} | "
        f"Actual: {actual_doctor}"
    )

    report_step(
        test_case_id,
        3,
        "Chọn bác sĩ tại bộ lọc",
        detail=actual_doctor
    )

    # Step 4
    page.scroll_to_week_view()

    displayed_doctors = (
        page.get_week_view_doctor_names()
    )

    assert displayed_doctors, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Không có lịch nào hiển thị trong bảng tuần"
    )

    unexpected_doctors = [
        doctor
        for doctor in displayed_doctors
        if doctor != data["doctor_name"]
    ]

    assert not unexpected_doctors, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: Chỉ hiển thị {data['doctor_name']} | "
        f"Actual: {displayed_doctors}"
    )

    report_step(
        test_case_id,
        4,
        "Bảng tuần chỉ hiển thị lịch của bác sĩ đã chọn",
        detail=f"DisplayedDoctors={displayed_doctors}"
    )


# ============================================================
# TC-DS-ADMIN-015
# ============================================================

def test_tc_ds_admin_015_clear_doctor_filter(driver):
    """
    TC-DS-ADMIN-015:
    Kiểm tra Admin hiển thị lại lịch của tất cả bác sĩ
    sau khi bỏ điều kiện lọc.
    """

    test_case_id = "TC-DS-ADMIN-015"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra hiển thị lại lịch của tất cả bác sĩ "
        "sau khi bỏ điều kiện lọc"
    )

    data = get_test_data_csv(
        DOCTOR_SCHEDULE_ADMIN_TEST_DATA_CSV,
        test_case_id
    )

    page = DoctorScheduleAdminPage(driver)

    # Step 1
    login_user(
        driver,
        data["username"],
        data["password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập với vai trò Admin thành công"
    )

    # Step 2
    page.open_page()

    report_step(
        test_case_id,
        2,
        "Mở trang Quản lý lịch làm việc bác sĩ"
    )

    # Step 3
    page.select_filter_doctor(
        data["doctor_name"]
    )

    filtered_doctors = (
        page.get_week_view_doctor_names()
    )

    assert filtered_doctors, (
        f"{test_case_id} | STEP 3 FAILED | "
        "Không có lịch hiển thị sau khi lọc"
    )

    assert all(
        doctor == data["doctor_name"]
        for doctor in filtered_doctors
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: Chỉ có {data['doctor_name']} | "
        f"Actual: {filtered_doctors}"
    )

    report_step(
        test_case_id,
        3,
        "Lọc lịch theo một bác sĩ",
        detail=f"DisplayedDoctors={filtered_doctors}"
    )

    # Step 4
    page.select_filter_doctor(
        "Tất cả bác sĩ"
    )

    selected_filter = (
        page.get_selected_filter_doctor_text()
    )

    assert selected_filter == "Tất cả bác sĩ", (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: Tất cả bác sĩ | "
        f"Actual: {selected_filter}"
    )

    report_step(
        test_case_id,
        4,
        "Bỏ điều kiện lọc và chọn lại Tất cả bác sĩ"
    )

    # Step 5
    page.scroll_to_week_view()

    all_doctors = (
        page.get_week_view_doctor_names()
    )

    unique_doctors = set(all_doctors)

    assert all_doctors, (
        f"{test_case_id} | STEP 5 FAILED | "
        "Bảng tuần không có dữ liệu"
    )

    assert len(unique_doctors) > 1, (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Hiển thị lịch của nhiều bác sĩ | "
        f"Actual: {all_doctors}"
    )

    report_step(
        test_case_id,
        5,
        "Hiển thị lại lịch của tất cả bác sĩ",
        detail=f"DisplayedDoctors={sorted(unique_doctors)}"
    )


# ============================================================
# TC-DS-ADMIN-016
# ============================================================

def test_tc_ds_admin_016_previous_week(driver):
    """
    TC-DS-ADMIN-016:
    Kiểm tra Admin chuyển sang tuần trước
    để xem lịch làm việc.
    """

    test_case_id = "TC-DS-ADMIN-016"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra Admin chuyển sang tuần trước "
        "để xem lịch làm việc"
    )

    data = get_test_data_csv(
        DOCTOR_SCHEDULE_ADMIN_TEST_DATA_CSV,
        test_case_id
    )

    page = DoctorScheduleAdminPage(driver)

    # Step 1
    login_user(
        driver,
        data["username"],
        data["password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập với vai trò Admin thành công"
    )

    # Step 2
    page.open_page()

    report_step(
        test_case_id,
        2,
        "Mở trang Quản lý lịch làm việc bác sĩ"
    )

    # Step 3
    current_range = page.get_week_range_text()

    report_step(
        test_case_id,
        3,
        "Ghi nhận khoảng thời gian của tuần hiện tại",
        detail=current_range
    )

    # Step 4
    page.click_previous_week()

    previous_range = page.get_week_range_text()

    assert previous_range != current_range, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Current={current_range} | "
        f"Previous={previous_range}"
    )

    report_step(
        test_case_id,
        4,
        "Chuyển sang tuần trước thành công",
        detail=f"{current_range} -> {previous_range}"
    )


# ============================================================
# TC-DS-ADMIN-017
# ============================================================

def test_tc_ds_admin_017_next_week(driver):
    """
    TC-DS-ADMIN-017:
    Kiểm tra Admin chuyển sang tuần sau
    để xem lịch làm việc.
    """

    test_case_id = "TC-DS-ADMIN-017"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra Admin chuyển sang tuần sau "
        "để xem lịch làm việc"
    )

    data = get_test_data_csv(
        DOCTOR_SCHEDULE_ADMIN_TEST_DATA_CSV,
        test_case_id
    )

    page = DoctorScheduleAdminPage(driver)

    # Step 1
    login_user(
        driver,
        data["username"],
        data["password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập với vai trò Admin thành công"
    )

    # Step 2
    page.open_page()

    report_step(
        test_case_id,
        2,
        "Mở trang Quản lý lịch làm việc bác sĩ"
    )

    # Step 3
    current_range = page.get_week_range_text()

    report_step(
        test_case_id,
        3,
        "Ghi nhận khoảng thời gian của tuần hiện tại",
        detail=current_range
    )

    # Step 4
    page.click_next_week()

    next_range = page.get_week_range_text()

    assert next_range != current_range, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Current={current_range} | "
        f"Next={next_range}"
    )

    report_step(
        test_case_id,
        4,
        "Chuyển sang tuần sau thành công",
        detail=f"{current_range} -> {next_range}"
    )