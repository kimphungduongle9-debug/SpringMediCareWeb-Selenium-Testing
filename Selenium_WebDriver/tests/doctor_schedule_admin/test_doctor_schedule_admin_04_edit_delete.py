from datetime import date, timedelta

from api.DoctorScheduleApi import DoctorScheduleApi
from pages.DoctorScheduleAdminPage import DoctorScheduleAdminPage
from tests.helpers.auth_helper import login_user
from utils.data_reader import (
    DOCTOR_SCHEDULE_ADMIN_TEST_DATA_CSV,
    get_test_data_csv,
)
from utils.test_reporter import report_step


# ============================================================
# TC-DS-ADMIN-018
# ============================================================

def test_tc_ds_admin_018_update_existing_schedule(driver):
    """
    TC-DS-ADMIN-018:
    Kiểm tra Admin cập nhật thông tin
    của một lịch làm việc đã tồn tại.
    """

    test_case_id = "TC-DS-ADMIN-018"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra Admin cập nhật thông tin "
        "của một lịch làm việc đã tồn tại"
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

    updated_note = "Đã cập nhật lịch"

    # SETUP
    api.delete_matching_schedule(
        data["doctor_name"],
        date_api,
        "morning",
        token
    )

    api.create_schedule(
        doctor_name=data["doctor_name"],
        work_date=date_api,
        shift="morning",
        start_time="07:00:00",
        end_time="11:30:00",
        status="available",
        note=data["note"],
        token=token
    )

    schedule = api.find_schedule(
        data["doctor_name"],
        date_api,
        "morning"
    )

    assert schedule is not None, (
        f"{test_case_id} | SETUP FAILED | "
        "Không tạo được lịch chuẩn bị cho testcase"
    )

    schedule_id = schedule["scheduleId"]

    # Step 1: Đăng nhập Admin
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

    # Step 2: Mở trang
    page.open_page()

    assert page.get_page_title() == data["page_title"], (
        f"{test_case_id} | STEP 2 FAILED | "
        "Không mở đúng trang Quản lý lịch làm việc bác sĩ"
    )

    report_step(
        test_case_id,
        2,
        "Mở trang Quản lý lịch làm việc bác sĩ"
    )

    # Step 3: Chọn lịch và nhấn Sửa
    page.scroll_to_schedule_list()

    edit_opened = page.click_edit_schedule_by_id(
        schedule_id
    )

    assert edit_opened, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Không tìm thấy lịch ID={schedule_id}"
    )

    report_step(
        test_case_id,
        3,
        "Chọn lịch đã tồn tại và nhấn Sửa",
        detail=f"ScheduleId={schedule_id}"
    )

    # Step 4: Kiểm tra dữ liệu cũ trên form
    actual_doctor = page.get_selected_doctor_text()
    actual_date = page.get_work_date_value()
    actual_shift = page.get_selected_shift_text()
    actual_status = page.get_selected_status_text()
    actual_note = page.get_note_value()

    assert page.get_update_form_title() == "Cập nhật lịch làm việc"
    assert actual_doctor == data["doctor_name"]
    assert actual_date == date_display
    assert actual_shift == data["shift_form"]
    assert actual_status == data["status_form"]
    assert actual_note == data["note"]

    report_step(
        test_case_id,
        4,
        "Kiểm tra form hiển thị đúng dữ liệu của lịch cần sửa",
        detail=(
            f"Doctor={actual_doctor} | "
            f"Date={actual_date} | "
            f"Shift={actual_shift} | "
            f"Status={actual_status} | "
            f"Note={actual_note}"
        )
    )

    # Step 5: Thay đổi trạng thái và ghi chú
    page.select_status(
        data["status_form_2"]
    )

    page.enter_note(
        updated_note
    )

    assert (
        page.get_selected_status_text()
        == data["status_form_2"]
    )

    assert page.get_note_value() == updated_note

    report_step(
        test_case_id,
        5,
        "Thay đổi Trạng thái và Ghi chú",
        detail=(
            f"Status={data['status_form_2']} | "
            f"Note={updated_note}"
        )
    )

    # Step 6: Nhấn Cập nhật
    page.click_update_button()

    message = page.get_message()

    assert message == "Cập nhật lịch làm việc thành công!", (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: Cập nhật lịch làm việc thành công! | "
        f"Actual: {message}"
    )

    report_step(
        test_case_id,
        6,
        "Cập nhật lịch làm việc thành công",
        detail=message
    )

    # Step 7: Kiểm tra kết quả sau cập nhật
    try:
        page.scroll_to_schedule_list()

        updated_schedule = (
            page.is_schedule_present_in_list(
                doctor_name=data["doctor_name"],
                work_date=date_display,
                shift_name=data["shift_name"],
                status=data["status_display_2"],
                note=updated_note
            )
        )

        count = api.count_matching_schedules(
            data["doctor_name"],
            date_api,
            "morning"
        )

        assert updated_schedule, (
            f"{test_case_id} | STEP 7 FAILED | "
            "Không tìm thấy dữ liệu đã cập nhật "
            "trong Danh sách lịch làm việc"
        )

        assert count == 1, (
            f"{test_case_id} | STEP 7 FAILED | "
            f"Expected ScheduleCount=1 | "
            f"Actual={count}"
        )

        report_step(
            test_case_id,
            7,
            "Kiểm tra lịch hiển thị đúng dữ liệu mới "
            "và không tạo thêm bản ghi",
            detail=(
                f"Status={data['status_display_2']} | "
                f"Note={updated_note} | "
                f"ScheduleCount={count}"
            )
        )

    finally:
        api.delete_matching_schedule(
            data["doctor_name"],
            date_api,
            "morning",
            token
        )

# ============================================================
# TC-DS-ADMIN-019
# ============================================================

def test_tc_ds_admin_019_cancel_edit_schedule(driver):
    """
    TC-DS-ADMIN-019:
    Kiểm tra chức năng Hủy sửa không làm thay đổi
    dữ liệu lịch làm việc đã tồn tại.
    """

    test_case_id = "TC-DS-ADMIN-019"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra chức năng Hủy sửa không làm thay đổi dữ liệu lịch"
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

    changed_note = "Dữ liệu thay đổi nhưng không lưu"

    # SETUP
    api.delete_matching_schedule(
        data["doctor_name"],
        date_api,
        "morning",
        token
    )

    api.create_schedule(
        doctor_name=data["doctor_name"],
        work_date=date_api,
        shift="morning",
        start_time="07:00:00",
        end_time="11:30:00",
        status="available",
        note=data["note"],
        token=token
    )

    schedule = api.find_schedule(
        data["doctor_name"],
        date_api,
        "morning"
    )

    assert schedule is not None, (
        f"{test_case_id} | SETUP FAILED | "
        "Không tạo được lịch chuẩn bị cho testcase"
    )

    schedule_id = schedule["scheduleId"]

    # Step 1: Đăng nhập Admin
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

    # Step 2: Mở trang quản lý lịch
    page.open_page()

    report_step(
        test_case_id,
        2,
        "Mở trang Quản lý lịch làm việc bác sĩ"
    )

    # Step 3: Mở lịch cần sửa
    page.scroll_to_schedule_list()

    assert page.click_edit_schedule_by_id(
        schedule_id
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Không tìm thấy ScheduleId={schedule_id}"
    )

    assert page.get_update_form_title() == "Cập nhật lịch làm việc"

    report_step(
        test_case_id,
        3,
        "Chọn lịch đã tồn tại và nhấn Sửa",
        detail=f"ScheduleId={schedule_id}"
    )

    # Step 4: Kiểm tra dữ liệu ban đầu
    actual_status = page.get_selected_status_text()
    actual_note = page.get_note_value()

    assert actual_status == data["status_form"]
    assert actual_note == data["note"]

    report_step(
        test_case_id,
        4,
        "Kiểm tra dữ liệu ban đầu trên form Cập nhật",
        detail=(
            f"Status={actual_status} | "
            f"Note={actual_note}"
        )
    )

    # Step 5: Thay đổi dữ liệu nhưng chưa lưu
    page.select_status(
        data["status_form_2"]
    )

    page.enter_note(
        changed_note
    )

    assert (
        page.get_selected_status_text()
        == data["status_form_2"]
    )

    assert page.get_note_value() == changed_note

    report_step(
        test_case_id,
        5,
        "Thay đổi Trạng thái và Ghi chú nhưng chưa cập nhật",
        detail=(
            f"Status={data['status_form_2']} | "
            f"Note={changed_note}"
        )
    )

    # Step 6: Nhấn Hủy sửa
    page.click_cancel_edit_button()

    assert page.get_form_title() == "Thêm lịch làm việc", (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: Form trở về Thêm lịch làm việc"
    )

    report_step(
        test_case_id,
        6,
        "Nhấn Hủy sửa và trở về form Thêm lịch làm việc"
    )

    # Step 7: Kiểm tra dữ liệu cũ không thay đổi
    try:
        page.scroll_to_schedule_list()

        original_schedule = (
            page.is_schedule_present_in_list(
                doctor_name=data["doctor_name"],
                work_date=date_display,
                shift_name=data["shift_name"],
                status=data["status_display"],
                note=data["note"]
            )
        )

        schedule_after_cancel = api.find_schedule(
            data["doctor_name"],
            date_api,
            "morning"
        )

        assert original_schedule, (
            f"{test_case_id} | STEP 7 FAILED | "
            "Dữ liệu gốc không còn hiển thị trong danh sách"
        )

        assert schedule_after_cancel is not None, (
            f"{test_case_id} | STEP 7 FAILED | "
            "Không tìm thấy lịch sau khi Hủy sửa"
        )

        assert schedule_after_cancel.get("status") == "available", (
            f"{test_case_id} | STEP 7 FAILED | "
            "Status đã bị thay đổi dù chưa bấm Cập nhật"
        )

        assert schedule_after_cancel.get("note") == data["note"], (
            f"{test_case_id} | STEP 7 FAILED | "
            "Ghi chú đã bị thay đổi dù đã Hủy sửa"
        )

        report_step(
            test_case_id,
            7,
            "Kiểm tra lịch vẫn giữ nguyên dữ liệu trước khi chỉnh sửa",
            detail=(
                f"Status={data['status_display']} | "
                f"Note={data['note']}"
            )
        )

    finally:
        api.delete_matching_schedule(
            data["doctor_name"],
            date_api,
            "morning",
            token
        )

# ============================================================
# TC-DS-ADMIN-020
# ============================================================

def test_tc_ds_admin_020_delete_existing_schedule(driver):
    """
    TC-DS-ADMIN-020:
    Kiểm tra Admin xóa một lịch làm việc
    đã tồn tại của bác sĩ.
    """

    test_case_id = "TC-DS-ADMIN-020"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra Admin xóa một lịch làm việc đã tồn tại"
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
        data["doctor_name"],
        date_api,
        "morning",
        token
    )

    api.create_schedule(
        doctor_name=data["doctor_name"],
        work_date=date_api,
        shift="morning",
        start_time="07:00:00",
        end_time="11:30:00",
        status="available",
        note=data["note"],
        token=token
    )

    schedule = api.find_schedule(
        data["doctor_name"],
        date_api,
        "morning"
    )

    assert schedule is not None, (
        f"{test_case_id} | SETUP FAILED | "
        "Không tạo được lịch chuẩn bị cho testcase"
    )

    schedule_id = schedule["scheduleId"]

    # Step 1: Đăng nhập
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

    # Step 2: Mở trang
    page.open_page()

    report_step(
        test_case_id,
        2,
        "Mở trang Quản lý lịch làm việc bác sĩ"
    )

    # Step 3: Xác định lịch cần xóa
    page.scroll_to_schedule_list()

    assert page.is_schedule_present_in_list(
        doctor_name=data["doctor_name"],
        work_date=date_display,
        shift_name=data["shift_name"],
        status=data["status_display"],
        note=data["note"]
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Không tìm thấy lịch cần xóa"
    )

    report_step(
        test_case_id,
        3,
        "Xác định lịch cần xóa trong Danh sách lịch làm việc",
        detail=f"ScheduleId={schedule_id}"
    )

    # Step 4: Nhấn Xóa
    assert page.click_delete_schedule_by_id(
        schedule_id
    ), (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Không tìm thấy nút Xóa của ScheduleId={schedule_id}"
    )

    report_step(
        test_case_id,
        4,
        "Nhấn Xóa lịch làm việc"
    )

    # Step 5: Kiểm tra hộp thoại xác nhận
    alert = driver.switch_to.alert

    assert (
        alert.text
        == "Bạn chắc chắn muốn xóa lịch này không?"
    ), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Nội dung hộp thoại xác nhận không đúng | "
        f"Actual: {alert.text}"
    )

    report_step(
        test_case_id,
        5,
        "Kiểm tra hộp thoại xác nhận xóa",
        detail=alert.text
    )

    # Step 6: Xác nhận xóa
    alert.accept()

    message = page.get_message()

    assert message == "Xóa lịch làm việc thành công!", (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: Xóa lịch làm việc thành công! | "
        f"Actual: {message}"
    )

    report_step(
        test_case_id,
        6,
        "Xác nhận xóa lịch thành công",
        detail=message
    )

    # Step 7: Kiểm tra lịch đã bị xóa
    page.scroll_to_schedule_list()

    schedule_in_list = (
        page.is_schedule_present_in_list(
            doctor_name=data["doctor_name"],
            work_date=date_display,
            shift_name=data["shift_name"],
            status=data["status_display"],
            note=data["note"]
        )
    )

    schedule_in_api = api.find_schedule(
        data["doctor_name"],
        date_api,
        "morning"
    )

    assert not schedule_in_list, (
        f"{test_case_id} | STEP 7 FAILED | "
        "Lịch vẫn còn hiển thị trong danh sách"
    )

    assert schedule_in_api is None, (
        f"{test_case_id} | STEP 7 FAILED | "
        "Lịch vẫn còn tồn tại trong API"
    )

    report_step(
        test_case_id,
        7,
        "Kiểm tra lịch đã bị xóa khỏi hệ thống",
        detail=(
            f"ScheduleInList={schedule_in_list} | "
            f"ScheduleInApi={schedule_in_api}"
        )
    )