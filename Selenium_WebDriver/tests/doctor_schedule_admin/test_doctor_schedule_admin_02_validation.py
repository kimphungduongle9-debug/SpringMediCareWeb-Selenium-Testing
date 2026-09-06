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


def load_case(test_case_id):
    return get_test_data_csv(
        DOCTOR_SCHEDULE_ADMIN_TEST_DATA_CSV,
        test_case_id
    )


def get_target_date(data):
    target_date = date.today() + timedelta(
        days=int(data["date_offset_days"])
    )

    return (
        target_date,
        target_date.strftime("%d/%m/%Y"),
        target_date.strftime("%Y-%m-%d"),
    )


def login_and_open(driver, data, page, test_case_id):
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


def get_admin_token(api, data):
    return api.get_token(
        data["username"],
        data["password"]
    )


def cleanup_schedule(
        api,
        doctor_name,
        work_date,
        shift,
        token
):
    api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    )


# ============================================================
# TC-DS-ADMIN-007
# ============================================================

def test_tc_ds_admin_007_reject_past_work_date(driver):
    """
    TC-DS-ADMIN-007:
    Kiểm tra hệ thống không cho phép Admin
    tạo lịch làm việc cho ngày đã qua.
    """

    test_case_id = "TC-DS-ADMIN-007"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra hệ thống không cho phép Admin "
        "tạo lịch làm việc cho ngày đã qua"
    )

    data = load_case(test_case_id)
    page = DoctorScheduleAdminPage(driver)
    api = DoctorScheduleApi()

    target_date, date_display, date_api = get_target_date(data)
    token = get_admin_token(api, data)

    cleanup_schedule(
        api,
        data["doctor_name"],
        date_api,
        "morning",
        token
    )

    # Step 1 + 2
    login_and_open(
        driver,
        data,
        page,
        test_case_id
    )

    # Step 3
    page.select_doctor(data["doctor_name"])

    actual_doctor = page.get_selected_doctor_text()

    assert actual_doctor == data["doctor_name"], (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: {data['doctor_name']} | "
        f"Actual: {actual_doctor}"
    )

    report_step(
        test_case_id,
        3,
        "Chọn một bác sĩ",
        detail=actual_doctor
    )

    # Step 4
    page.select_work_date(target_date)

    actual_date = page.get_work_date_value()

    assert actual_date == date_display, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: {date_display} | "
        f"Actual: {actual_date}"
    )

    report_step(
        test_case_id,
        4,
        "Chọn một ngày trước ngày hiện tại",
        detail=actual_date
    )

    # Step 5
    page.select_shift(data["shift_form"])
    page.select_status(data["status_form"])

    actual_shift = page.get_selected_shift_text()
    actual_status = page.get_selected_status_text()

    assert actual_shift == data["shift_form"]
    assert actual_status == data["status_form"]

    report_step(
        test_case_id,
        5,
        "Chọn ca và trạng thái hợp lệ",
        detail=(
            f"Shift={actual_shift} | "
            f"Status={actual_status}"
        )
    )

    # Step 6
    page.click_add_button()

    report_step(
        test_case_id,
        6,
        "Nhấn Thêm lịch"
    )

    # Step 7
    actual_message = page.get_message()

    created_schedule = api.find_schedule(
        data["doctor_name"],
        date_api,
        "morning"
    )

    schedule_created = created_schedule is not None

    if schedule_created:
        cleanup_schedule(
            api,
            data["doctor_name"],
            date_api,
            "morning",
            token
        )

    actual_result = (
        f"Message='{actual_message}' | "
        f"ScheduleCreated={schedule_created}"
    )

    if (
        actual_message == "Thêm lịch làm việc thành công!"
        or schedule_created
    ):
        report_step(
            test_case_id,
            7,
            "Hệ thống chưa từ chối lịch có ngày làm việc đã qua",
            status="XFAIL",
            detail=actual_result
        )

        pytest.xfail(
            f"KNOWN BUG - {test_case_id} | STEP 7 | "
            "Expected: Không tạo lịch cho ngày đã qua | "
            f"Actual: {actual_result}"
        )

    assert not schedule_created, (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Actual: {actual_result}"
    )

    report_step(
        test_case_id,
        7,
        "Hệ thống từ chối ngày đã qua và không tạo lịch mới",
        detail=actual_result
    )


# ============================================================
# TC-DS-ADMIN-008
# ============================================================

def test_tc_ds_admin_008_reject_duplicate_schedule(driver):
    """
    TC-DS-ADMIN-008:
    Kiểm tra hệ thống không cho phép tạo lịch trùng
    cho cùng bác sĩ, ngày và ca.
    """

    test_case_id = "TC-DS-ADMIN-008"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra hệ thống không cho phép tạo lịch trùng "
        "cho cùng bác sĩ, ngày và ca"
    )

    data = load_case(test_case_id)
    page = DoctorScheduleAdminPage(driver)
    api = DoctorScheduleApi()

    target_date, date_display, date_api = get_target_date(data)
    token = get_admin_token(api, data)

    cleanup_schedule(
        api,
        data["doctor_name"],
        date_api,
        "morning",
        token
    )

    # Step 1 + 2
    login_and_open(
        driver,
        data,
        page,
        test_case_id
    )

    # Step 3
    page.select_doctor(data["doctor_name"])

    actual_doctor = page.get_selected_doctor_text()

    assert actual_doctor == data["doctor_name"]

    report_step(
        test_case_id,
        3,
        "Chọn một bác sĩ",
        detail=actual_doctor
    )

    # Step 4
    page.select_work_date(target_date)
    page.select_shift(data["shift_form"])

    actual_date = page.get_work_date_value()
    actual_shift = page.get_selected_shift_text()

    assert actual_date == date_display
    assert actual_shift == data["shift_form"]

    report_step(
        test_case_id,
        4,
        "Chọn ngày và ca chưa có lịch",
        detail=(
            f"Date={actual_date} | "
            f"Shift={actual_shift}"
        )
    )

    # Step 5
    page.select_status(data["status_form"])
    page.enter_note(data["note"])

    actual_status = page.get_selected_status_text()
    actual_note = page.get_note_value()

    assert actual_status == data["status_form"]
    assert actual_note == data["note"]

    report_step(
        test_case_id,
        5,
        "Chọn trạng thái và nhập ghi chú",
        detail=(
            f"Status={actual_status} | "
            f"Note={actual_note}"
        )
    )

    # Step 6
    page.click_add_button()

    first_message = page.get_message()

    first_count = api.count_matching_schedules(
        data["doctor_name"],
        date_api,
        "morning"
    )

    assert first_message == data["success_message"]
    assert first_count == 1

    report_step(
        test_case_id,
        6,
        "Thêm lịch lần đầu thành công",
        detail=(
            f"Message={first_message} | "
            f"ScheduleCount={first_count}"
        )
    )

    # Step 7
    page.select_doctor(data["doctor_name"])
    page.select_work_date(target_date)
    page.select_shift(data["shift_form"])

    actual_doctor = page.get_selected_doctor_text()
    actual_date = page.get_work_date_value()
    actual_shift = page.get_selected_shift_text()

    assert actual_doctor == data["doctor_name"]
    assert actual_date == date_display
    assert actual_shift == data["shift_form"]

    report_step(
        test_case_id,
        7,
        "Nhập lại cùng bác sĩ, cùng ngày và cùng ca",
        detail=(
            f"Doctor={actual_doctor} | "
            f"Date={actual_date} | "
            f"Shift={actual_shift}"
        )
    )

    # Step 8
    page.click_add_button()
    page.scroll_to_top()

    report_step(
        test_case_id,
        8,
        "Nhấn Thêm lịch lần nữa"
    )

    # Step 9
    try:
        duplicate_message = page.get_message()

        final_count = api.count_matching_schedules(
            data["doctor_name"],
            date_api,
            "morning"
        )

        assert duplicate_message == data["error_message"], (
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected: {data['error_message']} | "
            f"Actual: {duplicate_message}"
        )

        assert final_count == 1, (
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected ScheduleCount=1 | Actual={final_count}"
        )

        assert page.is_message_displayed()

        report_step(
            test_case_id,
            9,
            "Kiểm tra hệ thống không tạo lịch trùng "
            "và chỉ giữ một bản ghi",
            detail=(
                f"Message={duplicate_message} | "
                f"ScheduleCount={final_count}"
            )
        )

    finally:
        cleanup_schedule(
            api,
            data["doctor_name"],
            date_api,
            "morning",
            token
        )


# ============================================================
# TC-DS-ADMIN-009
# ============================================================

def test_tc_ds_admin_009_allow_multiple_shifts_same_day(driver):
    """
    TC-DS-ADMIN-009:
    Kiểm tra một bác sĩ có thể được xếp
    nhiều ca khác nhau trong cùng ngày.
    """

    test_case_id = "TC-DS-ADMIN-009"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra một bác sĩ có thể được xếp "
        "nhiều ca khác nhau trong cùng ngày"
    )

    data = load_case(test_case_id)
    page = DoctorScheduleAdminPage(driver)
    api = DoctorScheduleApi()

    target_date, date_display, date_api = get_target_date(data)
    token = get_admin_token(api, data)

    cleanup_schedule(
        api,
        data["doctor_name"],
        date_api,
        "morning",
        token
    )

    cleanup_schedule(
        api,
        data["doctor_name"],
        date_api,
        "afternoon",
        token
    )

    api.create_schedule(
        doctor_name=data["doctor_name"],
        work_date=date_api,
        shift="morning",
        start_time="07:00:00",
        end_time="11:30:00",
        status="available",
        note="Ca sáng có sẵn",
        token=token
    )

    # Step 1 + 2
    login_and_open(
        driver,
        data,
        page,
        test_case_id
    )

    # Step 3
    morning_in_list = page.is_schedule_present_in_list(
        doctor_name=data["doctor_name"],
        work_date=date_display,
        shift_name="Ca sáng",
        status="Có lịch",
        note="Ca sáng có sẵn"
    )

    assert morning_in_list, (
        f"{test_case_id} | STEP 3 FAILED | "
        "Không tìm thấy lịch Ca sáng đã chuẩn bị"
    )

    report_step(
        test_case_id,
        3,
        "Xác nhận bác sĩ đã có lịch ở một ca trong ngày",
        detail=(
            f"Doctor={data['doctor_name']} | "
            f"Date={date_display} | Shift=Ca sáng"
        )
    )

    # Step 4
    page.select_doctor(data["doctor_name"])
    page.select_work_date(target_date)

    actual_doctor = page.get_selected_doctor_text()
    actual_date = page.get_work_date_value()

    assert actual_doctor == data["doctor_name"]
    assert actual_date == date_display

    report_step(
        test_case_id,
        4,
        "Chọn cùng bác sĩ và cùng ngày",
        detail=(
            f"Doctor={actual_doctor} | "
            f"Date={actual_date}"
        )
    )

    # Step 5
    page.select_shift(data["shift_form"])

    actual_shift = page.get_selected_shift_text()

    assert actual_shift == data["shift_form"]

    report_step(
        test_case_id,
        5,
        "Chọn một ca khác với ca đã có",
        detail=actual_shift
    )

    # Step 6
    page.enter_note(data["note"])
    page.click_add_button()

    message = page.get_message()

    assert message == data["success_message"], (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: {data['success_message']} | "
        f"Actual: {message}"
    )

    report_step(
        test_case_id,
        6,
        "Thêm ca làm việc thứ hai thành công",
        detail=message
    )

    # Step 7
    try:
        page.scroll_to_schedule_list()

        morning_in_list = page.is_schedule_present_in_list(
            doctor_name=data["doctor_name"],
            work_date=date_display,
            shift_name="Ca sáng",
            status="Có lịch",
            note="Ca sáng có sẵn"
        )

        afternoon_in_list = page.is_schedule_present_in_list(
            doctor_name=data["doctor_name"],
            work_date=date_display,
            shift_name=data["shift_name"],
            status=data["status_display"],
            note=data["note"]
        )

        morning_count = api.count_matching_schedules(
            data["doctor_name"],
            date_api,
            "morning"
        )

        afternoon_count = api.count_matching_schedules(
            data["doctor_name"],
            date_api,
            "afternoon"
        )

        assert morning_in_list, (
            f"{test_case_id} | STEP 7 FAILED | "
            "Không tìm thấy Ca sáng"
        )

        assert afternoon_in_list, (
            f"{test_case_id} | STEP 7 FAILED | "
            "Không tìm thấy Ca chiều"
        )

        assert morning_count == 1
        assert afternoon_count == 1

        report_step(
            test_case_id,
            7,
            "Kiểm tra ca mới được thêm và ca trước vẫn được giữ nguyên",
            detail=(
                "List: Morning=True, Afternoon=True | "
                f"MorningCount={morning_count} | "
                f"AfternoonCount={afternoon_count}"
            )
        )

    finally:
        cleanup_schedule(
            api,
            data["doctor_name"],
            date_api,
            "morning",
            token
        )

        cleanup_schedule(
            api,
            data["doctor_name"],
            date_api,
            "afternoon",
            token
        )


# ============================================================
# TC-DS-ADMIN-010
# ============================================================

def test_tc_ds_admin_010_allow_different_doctors_same_shift(driver):
    """
    TC-DS-ADMIN-010:
    Kiểm tra nhiều bác sĩ có thể được xếp
    cùng ngày và cùng ca.
    """

    test_case_id = "TC-DS-ADMIN-010"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra nhiều bác sĩ có thể được xếp "
        "cùng ngày và cùng ca"
    )

    data = load_case(test_case_id)
    page = DoctorScheduleAdminPage(driver)
    api = DoctorScheduleApi()

    doctor_1 = data["doctor_name"]
    doctor_2 = data["doctor_name_2"]

    target_date, date_display, date_api = get_target_date(data)
    token = get_admin_token(api, data)

    cleanup_schedule(
        api,
        doctor_1,
        date_api,
        "morning",
        token
    )

    cleanup_schedule(
        api,
        doctor_2,
        date_api,
        "morning",
        token
    )

    # Step 1 + 2
    login_and_open(
        driver,
        data,
        page,
        test_case_id
    )

    # Step 3
    page.select_doctor(doctor_1)

    actual_doctor = page.get_selected_doctor_text()

    assert actual_doctor == doctor_1

    report_step(
        test_case_id,
        3,
        "Chọn bác sĩ thứ nhất",
        detail=actual_doctor
    )

    # Step 4
    page.select_work_date(target_date)
    page.select_shift(data["shift_form"])
    page.select_status(data["status_form"])
    page.enter_note(data["note"])
    page.click_add_button()

    first_message = page.get_message()

    first_count = api.count_matching_schedules(
        doctor_1,
        date_api,
        "morning"
    )

    assert first_message == data["success_message"]
    assert first_count == 1

    report_step(
        test_case_id,
        4,
        "Thêm lịch cho bác sĩ thứ nhất với ngày và ca hợp lệ",
        detail=(
            f"Doctor={doctor_1} | "
            f"Date={date_display} | "
            f"Shift={data['shift_name']} | "
            f"ScheduleCount={first_count}"
        )
    )

    # Step 5
    page.select_doctor(doctor_2)

    actual_doctor = page.get_selected_doctor_text()

    assert actual_doctor == doctor_2

    report_step(
        test_case_id,
        5,
        "Chọn bác sĩ thứ hai",
        detail=actual_doctor
    )

    # Step 6
    page.select_work_date(target_date)
    page.select_shift(data["shift_form"])

    actual_date = page.get_work_date_value()
    actual_shift = page.get_selected_shift_text()

    assert actual_date == date_display
    assert actual_shift == data["shift_form"]

    report_step(
        test_case_id,
        6,
        "Chọn cùng ngày và cùng ca với bác sĩ thứ nhất",
        detail=(
            f"Date={actual_date} | "
            f"Shift={actual_shift}"
        )
    )

    # Step 7
    page.select_status(data["status_form"])
    page.enter_note(data["note"])
    page.click_add_button()

    second_message = page.get_message()

    assert second_message == data["success_message"]

    report_step(
        test_case_id,
        7,
        "Thêm lịch cho bác sĩ thứ hai",
        detail=second_message
    )

    # Step 8
    try:
        page.scroll_to_schedule_list()

        doctor_1_in_list = page.is_schedule_present_in_list(
            doctor_name=doctor_1,
            work_date=date_display,
            shift_name=data["shift_name"],
            status=data["status_display"],
            note=data["note"]
        )

        doctor_2_in_list = page.is_schedule_present_in_list(
            doctor_name=doctor_2,
            work_date=date_display,
            shift_name=data["shift_name"],
            status=data["status_display"],
            note=data["note"]
        )

        doctor_1_count = api.count_matching_schedules(
            doctor_1,
            date_api,
            "morning"
        )

        doctor_2_count = api.count_matching_schedules(
            doctor_2,
            date_api,
            "morning"
        )

        assert doctor_1_in_list
        assert doctor_2_in_list
        assert doctor_1_count == 1
        assert doctor_2_count == 1

        report_step(
            test_case_id,
            8,
            "Kiểm tra hai bác sĩ đều có lịch độc lập "
            "trong cùng ngày và cùng ca",
            detail=(
                f"{doctor_1}=True, Count={doctor_1_count} | "
                f"{doctor_2}=True, Count={doctor_2_count} | "
                f"Date={date_display} | "
                f"Shift={data['shift_name']}"
            )
        )

    finally:
        cleanup_schedule(
            api,
            doctor_1,
            date_api,
            "morning",
            token
        )

        cleanup_schedule(
            api,
            doctor_2,
            date_api,
            "morning",
            token
        )


# ============================================================
# TC-DS-ADMIN-011
# ============================================================

def test_tc_ds_admin_011_reject_conflicting_status_same_shift(driver):
    """
    TC-DS-ADMIN-011:
    Kiểm tra không cho phép tạo hai lịch có trạng thái
    khác nhau cho cùng bác sĩ, ngày và ca.
    """

    test_case_id = "TC-DS-ADMIN-011"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra không cho phép tạo hai lịch có trạng thái "
        "khác nhau cho cùng bác sĩ, ngày và ca"
    )

    data = load_case(test_case_id)
    page = DoctorScheduleAdminPage(driver)
    api = DoctorScheduleApi()

    target_date, date_display, date_api = get_target_date(data)
    token = get_admin_token(api, data)

    cleanup_schedule(
        api,
        data["doctor_name"],
        date_api,
        "morning",
        token
    )

    # Step 1 + 2
    login_and_open(
        driver,
        data,
        page,
        test_case_id
    )

    # Step 3
    page.select_doctor(data["doctor_name"])

    actual_doctor = page.get_selected_doctor_text()

    assert actual_doctor == data["doctor_name"]

    report_step(
        test_case_id,
        3,
        "Chọn một bác sĩ",
        detail=actual_doctor
    )

    # Step 4
    page.select_work_date(target_date)
    page.select_shift(data["shift_form"])

    actual_date = page.get_work_date_value()
    actual_shift = page.get_selected_shift_text()

    assert actual_date == date_display
    assert actual_shift == data["shift_form"]

    report_step(
        test_case_id,
        4,
        "Chọn ngày và ca chưa có lịch",
        detail=(
            f"Date={actual_date} | "
            f"Shift={actual_shift}"
        )
    )

    # Step 5
    page.select_status(data["status_form"])
    page.enter_note(data["note"])
    page.click_add_button()

    first_message = page.get_message()

    first_count = api.count_matching_schedules(
        data["doctor_name"],
        date_api,
        "morning"
    )

    assert first_message == data["success_message"]
    assert first_count == 1

    report_step(
        test_case_id,
        5,
        "Thêm lịch với trạng thái Có lịch làm việc",
        detail=(
            f"Message={first_message} | "
            f"ScheduleCount={first_count}"
        )
    )

    # Step 6
    page.select_doctor(data["doctor_name"])
    page.select_work_date(target_date)
    page.select_shift(data["shift_form"])

    actual_doctor = page.get_selected_doctor_text()
    actual_date = page.get_work_date_value()
    actual_shift = page.get_selected_shift_text()

    assert actual_doctor == data["doctor_name"]
    assert actual_date == date_display
    assert actual_shift == data["shift_form"]

    report_step(
        test_case_id,
        6,
        "Chọn lại cùng bác sĩ, cùng ngày và cùng ca",
        detail=(
            f"Doctor={actual_doctor} | "
            f"Date={actual_date} | "
            f"Shift={actual_shift}"
        )
    )

    # Step 7
    page.select_status(data["status_form_2"])

    actual_status = page.get_selected_status_text()

    assert actual_status == data["status_form_2"]

    report_step(
        test_case_id,
        7,
        "Chọn trạng thái Không làm việc",
        detail=actual_status
    )

    # Step 8
    page.click_add_button()
    page.scroll_to_top()

    report_step(
        test_case_id,
        8,
        "Nhấn Thêm lịch lần nữa"
    )

    # Step 9
    try:
        duplicate_message = page.get_message()

        final_count = api.count_matching_schedules(
            data["doctor_name"],
            date_api,
            "morning"
        )

        assert duplicate_message == data["error_message"], (
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected: {data['error_message']} | "
            f"Actual: {duplicate_message}"
        )

        assert final_count == 1, (
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected ScheduleCount=1 | Actual={final_count}"
        )

        page.scroll_to_schedule_list()

        original_exists = page.is_schedule_present_in_list(
            doctor_name=data["doctor_name"],
            work_date=date_display,
            shift_name=data["shift_name"],
            status=data["status_display"],
            note=data["note"]
        )

        assert original_exists, (
            f"{test_case_id} | STEP 9 FAILED | "
            "Lịch ban đầu không còn được giữ nguyên"
        )

        report_step(
            test_case_id,
            9,
            "Kiểm tra hệ thống không tạo lịch "
            "có trạng thái xung đột",
            detail=(
                f"Message={duplicate_message} | "
                f"ScheduleCount={final_count} | "
                "OriginalSchedule=True"
            )
        )

    finally:
        cleanup_schedule(
            api,
            data["doctor_name"],
            date_api,
            "morning",
            token
        )