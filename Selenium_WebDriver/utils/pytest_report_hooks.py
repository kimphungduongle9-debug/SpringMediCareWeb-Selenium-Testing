import inspect
import re
import time
from pathlib import Path

import pytest
from utils.test_reporter import (
    generate_word_report,
    generate_overall_report,
    register_test_case,
    reset_test_report,
    save_test_result,
    report_failed_step,
    report_step,
)

# ============================================================
# NOTIFICATION TEST REPORT
# Ghi nhận kết quả TC-NOTIFICATION và tự xuất báo cáo Word.
# ============================================================
_notification_tests_collected = False
_booking_tests_collected = False
_appointment_tests_collected = False
_my_appointment_tests_collected = False
_work_schedule_tests_collected = False
_doctor_tests_collected = False
_specialty_tests_collected = False
_stat_tests_collected = False
_drug_category_tests_collected = False
_medical_tests_collected = False
_login_tests_collected = False
_register_tests_collected = False
_doctor_schedule_admin_tests_collected = False
_medical_history_tests_collected = False

FEATURE_NAMES = {
    "NOTIFICATION": "THÔNG BÁO",
    "BOOKING": "ĐẶT LỊCH",
    "APPOINTMENT": "QUẢN LÝ LỊCH HẸN",
    "MYAPPOINTMENT": "LỊCH HẸN CỦA TÔI",
    "WORKSCHEDULE": "LỊCH LÀM VIỆC CỦA BÁC SĨ",
    "DOCTOR": "BÁC SĨ",
    "SPECIALTY": "CHUYÊN KHOA",
    "STAT": "THỐNG KÊ",
    "DRUG-CATEGORY": "QUẢN LÝ KHO DƯỢC PHẨM",
    "MEDICAL": "HỒ SƠ BỆNH ÁN",
    "MEDICALHISTORY": "LỊCH SỬ KHÁM BỆNH",
    "LOGIN": "ĐĂNG NHẬP",
    "REGISTER": "ĐĂNG KÝ",
    "DS-ADMIN": "QUẢN LÝ LỊCH LÀM VIỆC BÁC SĨ - ADMIN",
}

def get_failed_step_from_traceback(call):
    """
    Xác định Step bị lỗi từ traceback.

    Ưu tiên:
    1. Đọc trực tiếp STEP N FAILED trong assertion.
    2. Nếu lỗi xảy ra trong helper/POM thì quay về dòng test
       và tìm comment '# Step N:' gần nhất.

    Nhờ vậy không cần sửa lại toàn bộ 9 Notification Test Case.
    """

    if call.excinfo is None:
        return None

    # --------------------------------------------------------
    # Cách 1:
    # Assertion hiện tại đã có dạng:
    # TC-NOTIFICATION-001 | STEP 6 FAILED | ...
    # --------------------------------------------------------

    error_text = str(call.excinfo.value)

    match = re.search(
        r"STEP\s+(\d+)\s+FAILED",
        error_text,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    # --------------------------------------------------------
    # Cách 2:
    # Nếu lỗi nằm trong helper như login_account(),
    # tìm dòng gọi helper trong test_notification.py
    # rồi dò ngược lên comment '# Step N:'.
    # --------------------------------------------------------

    try:
        traceback_entries = list(call.excinfo.traceback)

        for entry in reversed(traceback_entries):

            try:
                file_path = Path(str(entry.path))
            except Exception:
                continue

            file_name = file_path.name
            is_supported_test = (
                    file_name.startswith("test_notification")
                    or file_name.startswith("test_booking")
                    or file_name.startswith("test_appointment")
                    or file_name.startswith("test_my_appointment")
                    or file_name.startswith("test_work_schedule")
                    or file_name.startswith("test_doctor")
                    or file_name.startswith("test_specialty")
                    or file_name.startswith("test_stat")
                    or file_name.startswith("test_drug_category")
                    or file_name.startswith("test_medical")
                    or file_name.startswith("test_login")
                    or file_name.startswith("test_register")
            )
            if not is_supported_test:
                continue

            source_lines = file_path.read_text(
                encoding="utf-8"
            ).splitlines()

            line_index = int(entry.lineno)

            if line_index >= len(source_lines):
                line_index = len(source_lines) - 1

            for index in range(line_index, -1, -1):

                step_match = re.search(
                    r"#\s*Step\s+(\d+)\b",
                    source_lines[index],
                    re.IGNORECASE
                )

                if step_match:
                    return int(step_match.group(1))

    except Exception:
        pass

    return None


def get_failure_detail(call):
    """
    Lấy lý do lỗi thực tế để đưa vào terminal và Word report.
    """

    if call.excinfo is None:
        return "Không xác định được nguyên nhân lỗi."

    detail = str(call.excinfo.value).strip()

    if not detail:
        return "Không xác định được nguyên nhân lỗi."

    # Không để report Word bị nhồi lỗi quá dài.
    if len(detail) > 1500:
        detail = detail[:1500] + "..."

    return detail


def capture_failure_screenshot(
        item,
        test_case_id,
        step_number=None
):
    """
    Tự động chụp browser khi Notification Test Case FAIL.

    File được lưu tại:
    reports/screenshots/
    """

    browser = item.funcargs.get("driver")

    if browser is None:
        return ""

    screenshot_directory = Path(
        "reports/screenshots"
    )

    screenshot_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = time.strftime(
        "%Y%m%d_%H%M%S"
    )

    if step_number is None:
        file_name = (
            f"{test_case_id}_FAILED_{timestamp}.png"
        )
    else:
        file_name = (
            f"{test_case_id}_STEP_{step_number}_"
            f"FAILED_{timestamp}.png"
        )

    screenshot_path = (
        screenshot_directory / file_name
    )

    try:
        browser.save_screenshot(
            str(screenshot_path)
        )

        print(
            f"\nSCREENSHOT SAVED | "
            f"{screenshot_path}"
        )

        return str(screenshot_path)

    except Exception as error:

        print(
            "\nSCREENSHOT ERROR | "
            f"{error}"
        )

        return ""

def get_test_case_id(item):
    """
    Lấy mã Test Case từ tên hàm pytest.

    Ví dụ:
    test_tc_notification_001_...
    -> TC-NOTIFICATION-001

    test_tc_booking_001_...
    -> TC-BOOKING-001
    """

    match = re.search(
        r"test_tc_([a-z_]+)_(\d{3})",
        item.name,
        re.IGNORECASE
    )

    if match is None:
        return None

    module_name = match.group(1).upper().replace("_", "-")
    test_number = match.group(2)

    return f"TC-{module_name}-{test_number}"

def get_feature_name(test_case_id):
    """
    Xác định chức năng từ mã Test Case.
    """

    if test_case_id is None:
        return "KHÁC"

    without_prefix = test_case_id.replace(
        "TC-",
        "",
        1
    )

    module_code = re.sub(
        r"-\d{3}$",
        "",
        without_prefix
    )

    return FEATURE_NAMES.get(
        module_code,
        module_code
    )

def pytest_sessionstart(session):
    """Xóa dữ liệu report cũ trước mỗi lần pytest bắt đầu."""
    global _notification_tests_collected
    global _booking_tests_collected
    global _appointment_tests_collected
    global _my_appointment_tests_collected
    global _work_schedule_tests_collected
    global _doctor_tests_collected
    global _specialty_tests_collected
    global _stat_tests_collected
    global _drug_category_tests_collected
    global _medical_tests_collected
    global _login_tests_collected
    global _register_tests_collected
    global _doctor_schedule_admin_tests_collected
    global _medical_history_tests_collected

    _notification_tests_collected = False
    _booking_tests_collected = False
    _appointment_tests_collected = False
    _my_appointment_tests_collected = False
    _work_schedule_tests_collected = False
    _doctor_tests_collected = False
    _specialty_tests_collected = False
    _stat_tests_collected = False
    _drug_category_tests_collected = False
    _medical_tests_collected = False
    _login_tests_collected = False
    _register_tests_collected = False
    _doctor_schedule_admin_tests_collected = False
    _medical_history_tests_collected = False

    reset_test_report()

def pytest_collection_modifyitems(session, config, items):
    """Xác định session hiện tại đang chạy module test nào."""
    global _notification_tests_collected
    global _booking_tests_collected
    global _appointment_tests_collected
    global _my_appointment_tests_collected
    global _work_schedule_tests_collected
    global _doctor_tests_collected
    global _specialty_tests_collected
    global _stat_tests_collected
    global _drug_category_tests_collected
    global _medical_tests_collected
    global _login_tests_collected
    global _register_tests_collected
    global _doctor_schedule_admin_tests_collected
    global _medical_history_tests_collected

    _notification_tests_collected = any(
        "test_tc_notification_" in item.name
        for item in items
    )

    _booking_tests_collected = any(
        "test_tc_booking_" in item.name
        for item in items
    )

    _appointment_tests_collected = any(
        "test_tc_appointment_" in item.name
        for item in items
    )

    _my_appointment_tests_collected = any(
        "test_tc_myappointment_" in item.name
        for item in items
    )
    _work_schedule_tests_collected = any(
        "test_tc_workschedule_" in item.name
        for item in items
    )
    _doctor_tests_collected = any(
        "test_tc_doctor_" in item.name
        for item in items
    )
    _specialty_tests_collected = any(
        "test_tc_specialty_" in item.name
        for item in items
    )
    _stat_tests_collected = any(
        "test_tc_stat_" in item.name
        for item in items
    )
    _drug_category_tests_collected = any(
        "test_tc_drug_category_" in item.name
        for item in items
    )
    _medical_tests_collected = any(
        "test_tc_medical_" in item.name
        for item in items
    )
    _login_tests_collected = any(
        "test_tc_login_" in item.name
        for item in items
    )
    _register_tests_collected = any(
        "test_tc_register_" in item.name
        for item in items
    )
    _doctor_schedule_admin_tests_collected = any(
        "test_tc_ds_admin_" in item.name
        for item in items
    )
    _medical_history_tests_collected = any(
        "test_tc_medicalhistory_" in item.name
        for item in items
    )

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Ghi kết quả Notification Test Case.

    Khi FAIL:
    - xác định Test Case,
    - xác định Step,
    - ghi Step FAIL,
    - ghi nguyên nhân,
    - chụp screenshot,
    - ghi duration.

    PASSED  : Test chạy thành công.
    FAILED  : Test thất bại.
    XFAILED : Known bug / expected failure.
    SKIPPED : Test bị bỏ qua.
    """

    outcome = yield
    report = outcome.get_result()

    test_case_id = get_test_case_id(
        item
    )

    if test_case_id is None:
        return

    # ========================================================
    # SETUP / TEARDOWN FAILED
    # ========================================================

    if (
        report.when in ("setup", "teardown")
        and report.failed
    ):

        detail = get_failure_detail(call)

        screenshot = capture_failure_screenshot(
            item=item,
            test_case_id=test_case_id
        )

        save_test_result(
            test_case_id=test_case_id,
            status="FAILED",
            detail=(
                f"Lỗi tại giai đoạn {report.when}. "
                f"{detail}"
            ),
            duration=report.duration,
            screenshot=screenshot
        )

        return

    # Kết quả chính chỉ xử lý ở phase call
    if report.when != "call":
        return

    # ========================================================
    # XFAIL
    # ========================================================

    if (
            report.skipped
            and hasattr(report, "wasxfail")
    ):

        detail = get_failure_detail(call)

        step_number = (
            get_failed_step_from_traceback(call)
        )

        if step_number is not None:
            report_step(
                test_case_id=test_case_id,
                step_number=step_number,
                description=(
                    "Known bug - Step không đạt Expected Result"
                ),
                status="XFAIL",
                detail=detail
            )

        save_test_result(
            test_case_id=test_case_id,
            status="XFAILED",
            detail=(
                f"{report.wasxfail} | "
                f"{detail}"
            ),
            duration=report.duration
        )

        return
    # ========================================================
    # FAILED
    # ========================================================

    if report.failed:

        detail = get_failure_detail(call)

        step_number = (
            get_failed_step_from_traceback(call)
        )

        # ----------------------------------------------------
        # Ghi FAIL cho đúng Step
        # ----------------------------------------------------

        if step_number is not None:

            report_failed_step(
                test_case_id=test_case_id,
                step_number=step_number,
                detail=detail
            )

        else:

            print(
                f"\n{test_case_id} | "
                "STEP UNKNOWN | FAIL | "
                f"{detail}"
            )

        # ----------------------------------------------------
        # Screenshot ngay tại thời điểm fail
        # ----------------------------------------------------

        screenshot = capture_failure_screenshot(
            item=item,
            test_case_id=test_case_id,
            step_number=step_number
        )

        # ----------------------------------------------------
        # Kết quả cuối Test Case
        # ----------------------------------------------------

        save_test_result(
            test_case_id=test_case_id,
            status="FAILED",
            detail=detail,
            duration=report.duration,
            screenshot=screenshot
        )

        return

    # ========================================================
    # SKIPPED
    # ========================================================

    if report.skipped:

        save_test_result(
            test_case_id=test_case_id,
            status="SKIPPED",
            detail="Test Case bị bỏ qua.",
            duration=report.duration
        )

        return

    # ========================================================
    # PASSED
    # ========================================================

    if report.passed:

        save_test_result(
            test_case_id=test_case_id,
            status="PASSED",
            duration=report.duration
        )
def pytest_sessionfinish(session, exitstatus):
    """
    Sau khi pytest kết thúc,
    tự động xuất Word report theo module đã chạy.

    Mỗi report riêng chỉ chứa Test Case
    thuộc đúng chức năng của report đó.

    Cuối cùng xuất Overall Test Report
    chứa toàn bộ Test Case của session.
    """

    if session.config.option.collectonly:
        return

    # ========================================================
    # NOTIFICATION
    # ========================================================

    if _notification_tests_collected:
        generate_word_report(
            "reports/Notification_Test_Report.docx",
            "THÔNG BÁO",
            "TC-NOTIFICATION-"
        )

    # ========================================================
    # BOOKING
    # ========================================================

    if _booking_tests_collected:
        generate_word_report(
            "reports/Booking_Test_Report.docx",
            "ĐẶT LỊCH",
            "TC-BOOKING-"
        )

    # ========================================================
    # APPOINTMENT
    # ========================================================

    if _appointment_tests_collected:
        generate_word_report(
            "reports/Appointment_Test_Report.docx",
            "QUẢN LÝ LỊCH HẸN",
            "TC-APPOINTMENT-"
        )

    # ========================================================
    # MY APPOINTMENT
    # ========================================================

    if _my_appointment_tests_collected:
        generate_word_report(
            "reports/MyAppointment_Test_Report.docx",
            "LỊCH HẸN CỦA TÔI",
            "TC-MYAPPOINTMENT-"
        )

    # ========================================================
    # WORK SCHEDULE
    # ========================================================

    if _work_schedule_tests_collected:
        generate_word_report(
            "reports/WorkSchedule_Test_Report.docx",
            "LỊCH LÀM VIỆC CỦA BÁC SĨ",
            "TC-WORKSCHEDULE-"
        )

    # ========================================================
    # DOCTOR
    # ========================================================

    if _doctor_tests_collected:
        generate_word_report(
            "reports/Doctor_Test_Report.docx",
            "BÁC SĨ",
            "TC-DOCTOR-"
        )

    # ========================================================
    # SPECIALTY
    # ========================================================

    if _specialty_tests_collected:
        generate_word_report(
            "reports/Specialty_Test_Report.docx",
            "CHUYÊN KHOA",
            "TC-SPECIALTY-"
        )

    # ========================================================
    # STAT
    # ========================================================

    if _stat_tests_collected:
        generate_word_report(
            "reports/Stat_Test_Report.docx",
            "THỐNG KÊ",
            "TC-STAT-"
        )

    # ========================================================
    # DRUG CATEGORY
    # ========================================================

    if _drug_category_tests_collected:
        generate_word_report(
            "reports/Drug_Category_Test_Report.docx",
            "QUẢN LÝ KHO DƯỢC PHẨM",
            "TC-DRUG-CATEGORY-"
        )

    # ========================================================
    # MEDICAL
    # ========================================================

    if _medical_tests_collected:
        generate_word_report(
            "reports/Medical_Test_Report.docx",
            "HỒ SƠ BỆNH ÁN",
            "TC-MEDICAL-"
        )

    # ========================================================
    # LOGIN
    # ========================================================

    if _login_tests_collected:
        generate_word_report(
            "reports/Login_Test_Report.docx",
            "ĐĂNG NHẬP",
            "TC-LOGIN-"
        )

    # ========================================================
    # REGISTER
    # ========================================================

    if _register_tests_collected:
        generate_word_report(
            "reports/Register_Test_Report.docx",
            "ĐĂNG KÝ",
            "TC-REGISTER-"
        )

    # ========================================================
    # DOCTOR SCHEDULE ADMIN
    # ========================================================

    if _doctor_schedule_admin_tests_collected:
        generate_word_report(
            "reports/Doctor_Schedule_Admin_Test_Report.docx",
            "QUẢN LÝ LỊCH LÀM VIỆC BÁC SĨ - ADMIN",
            "TC-DS-ADMIN-"
        )

    # ========================================================
    # MEDICAL HISTORY
    # ========================================================

    if _medical_history_tests_collected:
        generate_word_report(
            "reports/Medical_History_Test_Report.docx",
            "LỊCH SỬ KHÁM BỆNH",
            "TC-MEDICALHISTORY-"
        )

    # ========================================================
    # OVERALL TEST REPORT
    # ========================================================

    generate_overall_report(
        "reports/Overall_Test_Report.docx"
    )
def pytest_runtest_setup(item):
    """
    Hiển thị mã Test Case và mô tả
    trước khi bắt đầu thực thi từng test.
    """
    is_notification = "test_tc_notification_" in item.name
    is_booking = "test_tc_booking_" in item.name
    is_appointment = "test_tc_appointment_" in item.name
    is_doctor = "test_tc_doctor_" in item.name
    is_specialty = "test_tc_specialty_" in item.name
    is_stat = "test_tc_stat_" in item.name
    is_drug_category = ("test_tc_drug_category_" in item.name)
    is_medical = "test_tc_medical_" in item.name
    is_login = "test_tc_login_" in item.name
    is_register = "test_tc_register_" in item.name
    is_doctor_schedule_admin = ("test_tc_ds_admin_" in item.name)
    is_medical_history = ("test_tc_medicalhistory_" in item.name)
    is_my_appointment = "test_tc_myappointment_" in item.name
    is_work_schedule = "test_tc_workschedule_" in item.name

    if not (
            is_notification
            or is_booking
            or is_appointment
            or is_doctor
            or is_specialty
            or is_stat
            or is_drug_category
            or is_medical
            or is_login
            or is_register
            or is_doctor_schedule_admin
            or is_medical_history
            or is_my_appointment
            or is_work_schedule
    ):
        return

    description = inspect.getdoc(item.obj)

    test_case_id = get_test_case_id(
        item
    )

    if test_case_id is not None:
        register_test_case(
            test_case_id=test_case_id,
            feature_name=get_feature_name(
                test_case_id
            ),
            description=description or ""
        )

    print("\n")
    print("=" * 80)
    print("TEST CASE DESCRIPTION")
    print("=" * 80)

    if description:
        print(description)
    else:
        print("Không có mô tả Test Case.")

    print("=" * 80)
