from datetime import date, timedelta

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


def cleanup_schedule(api, data, work_date, shift, token):
    api.delete_matching_schedule(
        doctor_name=data["doctor_name"],
        work_date=work_date,
        shift=shift,
        token=token
    )


# ============================================================
# TC-DS-ADMIN-001
# ============================================================

def test_tc_ds_admin_001_display_add_schedule_form(driver):
    """
    TC-DS-ADMIN-001:
    Kiểm tra form Thêm lịch làm việc hiển thị đầy đủ
    thông tin cần thiết.
    """

    test_case_id = "TC-DS-ADMIN-001"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra form Thêm lịch làm việc "
        "hiển thị đầy đủ thông tin cần thiết"
    )

    data = load_case(test_case_id)
    page = DoctorScheduleAdminPage(driver)

    expected_shift_options = data["shift_options"].split("|")
    expected_status_options = data["status_options"].split("|")

    # Step 1 + 2
    login_and_open(
        driver,
        data,
        page,
        test_case_id
    )

    # Step 3
    actual_form_title = page.get_form_title()

    assert actual_form_title == data["form_title"], (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: {data['form_title']} | "
        f"Actual: {actual_form_title}"
    )

    report_step(
        test_case_id,
        3,
        "Form Thêm lịch làm việc được hiển thị"
    )

    # Step 4
    page.open_doctor_dropdown()
    doctor_options = page.get_doctor_options()

    assert doctor_options, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Danh sách Bác sĩ không có dữ liệu"
    )

    assert doctor_options[0] == data["doctor_default"], (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected default: {data['doctor_default']} | "
        f"Actual: {doctor_options[0]}"
    )

    assert len(doctor_options) > 1, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Có ít nhất một bác sĩ | "
        f"Actual: {doctor_options}"
    )

    report_step(
        test_case_id,
        4,
        "Mở danh sách Bác sĩ và kiểm tra các lựa chọn được hiển thị",
        detail=f"Options={doctor_options}"
    )

    # Step 5
    page.open_shift_dropdown()
    shift_options = page.get_shift_options()

    assert shift_options == expected_shift_options, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: {expected_shift_options} | "
        f"Actual: {shift_options}"
    )

    report_step(
        test_case_id,
        5,
        "Mở danh sách Ca làm việc và kiểm tra đầy đủ các lựa chọn",
        detail=f"Options={shift_options}"
    )

    # Step 6
    page.open_status_dropdown()
    status_options = page.get_status_options()

    assert status_options == expected_status_options, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: {expected_status_options} | "
        f"Actual: {status_options}"
    )

    report_step(
        test_case_id,
        6,
        "Mở danh sách Trạng thái và kiểm tra các lựa chọn được hiển thị",
        detail=f"Options={status_options}"
    )

    # Step 7
    fields = {
        "doctor": page.is_doctor_select_displayed(),
        "work_date": page.is_work_date_input_displayed(),
        "shift": page.is_shift_select_displayed(),
        "status": page.is_status_select_displayed(),
        "note": page.is_note_input_displayed(),
        "add_button": page.is_add_button_displayed(),
    }

    missing_fields = [
        name
        for name, displayed in fields.items()
        if not displayed
    ]

    assert not missing_fields, (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Missing fields: {missing_fields}"
    )

    actual_doctor = page.get_selected_doctor_text()
    actual_date = page.get_work_date_value()
    actual_shift = page.get_selected_shift_text()
    actual_status = page.get_selected_status_text()
    actual_note = page.get_note_value()

    assert actual_doctor == data["doctor_default"]
    assert actual_date == data["work_date_default"]
    assert actual_shift == data["shift_default"]
    assert actual_status == data["status_default"]
    assert actual_note == data["note_default"]

    report_step(
        test_case_id,
        7,
        "Các trường và giá trị mặc định trên form hiển thị đúng",
        detail=(
            f"Doctor={actual_doctor} | "
            f"Date='{actual_date}' | "
            f"Shift={actual_shift} | "
            f"Status={actual_status} | "
            f"Note='{actual_note}'"
        )
    )


# ============================================================
# TC-DS-ADMIN-002
# ============================================================

def test_tc_ds_admin_002_add_valid_schedule(driver):
    """
    TC-DS-ADMIN-002:
    Kiểm tra Admin thêm lịch làm việc cho bác sĩ
    với dữ liệu hợp lệ.
    """

    test_case_id = "TC-DS-ADMIN-002"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra Admin thêm lịch làm việc "
        "cho bác sĩ với dữ liệu hợp lệ"
    )

    data = load_case(test_case_id)
    page = DoctorScheduleAdminPage(driver)
    api = DoctorScheduleApi()

    target_date, date_display, date_api = get_target_date(data)
    token = get_admin_token(api, data)

    cleanup_schedule(
        api,
        data,
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
        "Chọn bác sĩ trên form",
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
        "Chọn ngày làm việc cho lịch mới",
        detail=actual_date
    )

    # Step 5
    page.select_shift(data["shift_form"])

    actual_shift = page.get_selected_shift_text()

    assert actual_shift == data["shift_form"], (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: {data['shift_form']} | "
        f"Actual: {actual_shift}"
    )

    report_step(
        test_case_id,
        5,
        "Chọn Ca sáng",
        detail=actual_shift
    )

    # Step 6
    page.select_status(data["status_form"])

    actual_status = page.get_selected_status_text()

    assert actual_status == data["status_form"], (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: {data['status_form']} | "
        f"Actual: {actual_status}"
    )

    report_step(
        test_case_id,
        6,
        "Chọn trạng thái Có lịch làm việc",
        detail=actual_status
    )

    # Step 7
    page.enter_note(data["note"])

    actual_note = page.get_note_value()

    assert actual_note == data["note"], (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected: {data['note']} | "
        f"Actual: {actual_note}"
    )

    report_step(
        test_case_id,
        7,
        "Nhập ghi chú cho lịch",
        detail=actual_note
    )

    # Step 8
    page.click_add_button()

    report_step(
        test_case_id,
        8,
        "Nhấn Thêm lịch"
    )

    # Step 9
    try:
        message = page.get_message()

        assert message == data["success_message"], (
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected: {data['success_message']} | "
            f"Actual: {message}"
        )

        schedule_exists = page.is_schedule_present_in_list(
            doctor_name=data["doctor_name"],
            work_date=date_display,
            shift_name=data["shift_name"],
            status=data["status_display"],
            note=data["note"]
        )

        assert schedule_exists, (
            f"{test_case_id} | STEP 9 FAILED | "
            "Không tìm thấy lịch vừa tạo"
        )

        report_step(
            test_case_id,
            9,
            "Kiểm tra thông báo và lịch vừa tạo trong Danh sách lịch làm việc",
            detail=(
                f"Message={message} | "
                f"Doctor={data['doctor_name']} | "
                f"Date={date_display} | "
                f"Shift={data['shift_name']} | "
                f"Status={data['status_display']} | "
                f"Note={data['note']}"
            )
        )

    finally:
        cleanup_schedule(
            api,
            data,
            date_api,
            "morning",
            token
        )


# ============================================================
# TC-DS-ADMIN-003
# ============================================================

def test_tc_ds_admin_003_add_unavailable_schedule(driver):
    """
    TC-DS-ADMIN-003:
    Kiểm tra Admin thêm lịch cho bác sĩ
    với trạng thái Không làm việc.
    """

    test_case_id = "TC-DS-ADMIN-003"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra Admin thêm lịch cho bác sĩ "
        "với trạng thái Không làm việc"
    )

    data = load_case(test_case_id)
    page = DoctorScheduleAdminPage(driver)
    api = DoctorScheduleApi()

    target_date, date_display, date_api = get_target_date(data)
    token = get_admin_token(api, data)

    cleanup_schedule(
        api,
        data,
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
        "Chọn bác sĩ trên form",
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

    actual_status = page.get_selected_status_text()

    assert actual_status == data["status_form"]

    report_step(
        test_case_id,
        5,
        "Chọn trạng thái Không làm việc",
        detail=actual_status
    )

    # Step 6
    page.enter_note(data["note"])

    actual_note = page.get_note_value()

    assert actual_note == data["note"]

    report_step(
        test_case_id,
        6,
        "Nhập ghi chú cho lịch",
        detail=actual_note
    )

    # Step 7
    page.click_add_button()

    report_step(
        test_case_id,
        7,
        "Nhấn Thêm lịch"
    )

    # Step 8
    try:
        message = page.get_message()

        assert message == data["success_message"], (
            f"{test_case_id} | STEP 8 FAILED | "
            f"Expected: {data['success_message']} | "
            f"Actual: {message}"
        )

        schedule_exists = page.is_schedule_present_in_list(
            doctor_name=data["doctor_name"],
            work_date=date_display,
            shift_name=data["shift_name"],
            status=data["status_display"],
            note=data["note"]
        )

        assert schedule_exists, (
            f"{test_case_id} | STEP 8 FAILED | "
            "Không tìm thấy lịch Không làm việc vừa tạo"
        )

        report_step(
            test_case_id,
            8,
            "Kiểm tra thông báo và lịch vừa tạo trong Danh sách lịch làm việc",
            detail=(
                f"Message={message} | "
                f"Doctor={data['doctor_name']} | "
                f"Date={date_display} | "
                f"Shift={data['shift_name']} | "
                f"Status={data['status_display']} | "
                f"Note={data['note']}"
            )
        )

    finally:
        cleanup_schedule(
            api,
            data,
            date_api,
            "morning",
            token
        )


# ============================================================
# TC-DS-ADMIN-004
# ============================================================

def test_tc_ds_admin_004_add_schedule_without_note(driver):
    """
    TC-DS-ADMIN-004:
    Kiểm tra Admin có thể thêm lịch
    khi để trống trường Ghi chú.
    """

    test_case_id = "TC-DS-ADMIN-004"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra Admin có thể thêm lịch "
        "khi để trống trường Ghi chú"
    )

    data = load_case(test_case_id)
    page = DoctorScheduleAdminPage(driver)
    api = DoctorScheduleApi()

    target_date, date_display, date_api = get_target_date(data)
    token = get_admin_token(api, data)

    cleanup_schedule(
        api,
        data,
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
        3,
        "Chọn bác sĩ, ngày làm việc và ca chưa có lịch",
        detail=(
            f"Doctor={actual_doctor} | "
            f"Date={actual_date} | "
            f"Shift={actual_shift}"
        )
    )

    # Step 4
    page.select_status(data["status_form"])

    actual_status = page.get_selected_status_text()

    assert actual_status == data["status_form"]

    report_step(
        test_case_id,
        4,
        "Chọn trạng thái Có lịch làm việc",
        detail=actual_status
    )

    # Step 5
    actual_note = page.get_note_value()

    assert actual_note == "", (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: Ghi chú trống | Actual: '{actual_note}'"
    )

    report_step(
        test_case_id,
        5,
        "Để trống trường Ghi chú"
    )

    # Step 6
    page.click_add_button()

    report_step(
        test_case_id,
        6,
        "Nhấn Thêm lịch"
    )

    # Step 7
    try:
        message = page.get_message()

        assert message == data["success_message"]

        schedule_exists = page.is_schedule_present_in_list(
            doctor_name=data["doctor_name"],
            work_date=date_display,
            shift_name=data["shift_name"],
            status=data["status_display"],
            note=""
        )

        assert schedule_exists, (
            f"{test_case_id} | STEP 7 FAILED | "
            "Không tìm thấy lịch có Ghi chú trống"
        )

        report_step(
            test_case_id,
            7,
            "Kiểm tra lịch vừa tạo trong Danh sách lịch làm việc",
            detail=(
                f"Message={message} | "
                f"Doctor={data['doctor_name']} | "
                f"Date={date_display} | "
                f"Shift={data['shift_name']} | "
                f"Status={data['status_display']} | "
                "Note=''"
            )
        )

    finally:
        cleanup_schedule(
            api,
            data,
            date_api,
            "morning",
            token
        )


# ============================================================
# TC-DS-ADMIN-005
# ============================================================

def test_tc_ds_admin_005_require_doctor(driver):
    """
    TC-DS-ADMIN-005:
    Kiểm tra hệ thống xử lý khi Admin không chọn bác sĩ.
    """

    test_case_id = "TC-DS-ADMIN-005"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra hệ thống xử lý khi Admin không chọn bác sĩ"
    )

    data = load_case(test_case_id)
    page = DoctorScheduleAdminPage(driver)

    target_date, date_display, _ = get_target_date(data)

    # Step 1 + 2
    login_and_open(
        driver,
        data,
        page,
        test_case_id
    )

    # Step 3
    actual_doctor = page.get_selected_doctor_text()

    assert actual_doctor == data["doctor_default"], (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: {data['doctor_default']} | "
        f"Actual: {actual_doctor}"
    )

    report_step(
        test_case_id,
        3,
        "Giữ trường Bác sĩ ở giá trị -- Chọn bác sĩ --",
        detail=actual_doctor
    )

    # Step 4
    page.select_work_date(target_date)

    actual_date = page.get_work_date_value()

    assert actual_date == date_display

    report_step(
        test_case_id,
        4,
        "Chọn ngày làm việc hợp lệ",
        detail=actual_date
    )

    # Step 5
    actual_shift = page.get_selected_shift_text()
    actual_status = page.get_selected_status_text()

    assert actual_shift == data["shift_default"]
    assert actual_status == data["status_default"]

    report_step(
        test_case_id,
        5,
        "Giữ nguyên ca và trạng thái mặc định",
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
    actual_doctor_after = page.get_selected_doctor_text()

    assert actual_doctor_after == data["doctor_default"], (
        f"{test_case_id} | STEP 7 FAILED | "
        "Trường Bác sĩ không giữ trạng thái chưa chọn"
    )

    schedule_exists = page.is_schedule_present_in_list(
        doctor_name="",
        work_date=date_display,
        shift_name=data["shift_name"],
        status=data["status_display"],
        note=""
    )

    assert not schedule_exists, (
        f"{test_case_id} | STEP 7 FAILED | "
        "Hệ thống đã tạo lịch dù chưa chọn bác sĩ"
    )

    report_step(
        test_case_id,
        7,
        "Kiểm tra phản hồi tại trường Bác sĩ và Danh sách lịch làm việc",
        detail=(
            f"Doctor={actual_doctor_after} | "
            "ScheduleCreated=False"
        )
    )


# ============================================================
# TC-DS-ADMIN-006
# ============================================================

def test_tc_ds_admin_006_require_work_date(driver):
    """
    TC-DS-ADMIN-006:
    Kiểm tra hệ thống xử lý khi Admin
    không chọn ngày làm việc.
    """

    test_case_id = "TC-DS-ADMIN-006"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra hệ thống xử lý khi Admin "
        "không chọn ngày làm việc"
    )

    data = load_case(test_case_id)
    page = DoctorScheduleAdminPage(driver)

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
    actual_date = page.get_work_date_value()

    assert actual_date == ""

    report_step(
        test_case_id,
        4,
        "Để trống trường Ngày làm việc",
        detail="WorkDate=''"
    )

    # Step 5
    actual_shift = page.get_selected_shift_text()
    actual_status = page.get_selected_status_text()

    assert actual_shift == data["shift_default"]
    assert actual_status == data["status_default"]

    report_step(
        test_case_id,
        5,
        "Giữ nguyên ca và trạng thái mặc định",
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
    validation_message = (
        page.get_work_date_validation_message()
    )

    assert validation_message, (
        f"{test_case_id} | STEP 7 FAILED | "
        "Không có validation message cho Ngày làm việc"
    )

    actual_date_after = page.get_work_date_value()
    actual_doctor_after = page.get_selected_doctor_text()

    assert actual_date_after == ""
    assert actual_doctor_after == data["doctor_name"]

    report_step(
        test_case_id,
        7,
        "Kiểm tra thông báo bắt buộc tại trường "
        "Ngày làm việc và xác nhận không tạo lịch",
        detail=(
            f"Validation='{validation_message}' | "
            "WorkDate='' | "
            f"Doctor={actual_doctor_after} | "
            "ScheduleCreated=False"
        )
    )