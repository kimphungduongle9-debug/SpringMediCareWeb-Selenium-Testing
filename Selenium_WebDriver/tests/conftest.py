import sys
import time
import re
from pathlib import Path
import inspect
import pytest
from selenium import webdriver

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import các module của project SAU KHI đã thêm PROJECT_ROOT vào sys.path.
from api.AppointmentApi import AppointmentApi
from api.MedicalRecordApi import MedicalRecordApi
from utils.test_reporter import (
    generate_word_report,
    reset_test_report,
    save_test_result,
    report_failed_step,
)
@pytest.fixture
def driver():
    browser = webdriver.Chrome()

    browser.maximize_window()
    browser.implicitly_wait(3)

    yield browser

    browser.quit()


@pytest.fixture
def booking_test_data():
    appointment_api = AppointmentApi()

    doctor_id = 1
    booking_date = "11/04/2026"
    patient_ids = [1, 2]

    test_times = [
        "09:00",
        "09:30",
        "14:00",
        "15:30",
        "15:31"
    ]

    # Dọn dữ liệu cũ trước khi chạy test
    for booking_time in test_times:
        appointment_api.cancel_matching_appointments(
            doctor_id=doctor_id,
            booking_date=booking_date,
            booking_time=booking_time,
            patient_ids=patient_ids
        )

    yield appointment_api

    # Dọn dữ liệu vừa tạo sau khi test kết thúc
    for booking_time in test_times:
        appointment_api.cancel_matching_appointments(
            doctor_id=doctor_id,
            booking_date=booking_date,
            booking_time=booking_time,
            patient_ids=patient_ids
        )

@pytest.fixture
def medical_record_tc7_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc7_data(
        patient_id=7,
        doctor_id=3
    )

    yield appointment_id

@pytest.fixture
def medical_record_tc5_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc5_data(
        patient_id=7,
        doctor_id=3
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-MEDICAL-005",
        "patient_name": "Duong Le Kim Phung",
        "doctor_name": "Ly Minh",
        "diagnosis": "Đau lưng do ngồi lâu",
        "treatment": (
            "Nghỉ ngơi và hạn chế vận động mạnh"
        )
    }

@pytest.fixture
def medical_record_tc6_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc6_data(
        patient_id=7,
        doctor_id=3
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-MEDICAL-006"
    }

@pytest.fixture
def medical_record_tc9_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc9_data(
        patient_id=7,
        doctor_id=3
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-MEDICAL-009"
    }

@pytest.fixture
def medical_record_tc1_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc1_data(
        patient_id=7,
        doctor_id=3
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-MEDICAL-001",
        "diagnosis": (
            "Đau đầu nhẹ do thiếu ngủ"
        ),
        "treatment": (
            "Nghỉ ngơi và uống đủ nước"
        )
    }

@pytest.fixture
def medical_record_tc2_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc2_data(
        patient_id=7,
        doctor_id=3
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-MEDICAL-002",
        "treatment": (
            "Nghỉ ngơi và uống thuốc theo hướng dẫn"
        )
    }

@pytest.fixture
def medical_record_tc3_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc3_data(
        patient_id=7,
        doctor_id=3
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-MEDICAL-003",
        "diagnosis": (
            "Đau vai do vận động sai tư thế"
        )
    }

@pytest.fixture
def medical_record_tc4_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc4_data(
        patient_id=7,
        doctor_id=3
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-MEDICAL-004"
    }

@pytest.fixture
def medical_record_tc8_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc8_data(
        patient_id=7,
        doctor_id=3
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-MEDICAL-008"
    }

@pytest.fixture
def appointment_tc2_data():
    appointment_api = AppointmentApi()
    medical_record_api = MedicalRecordApi()

    patient_id = 7
    doctor_id = 3

    booking_slot = (
        medical_record_api
        .find_available_booking_slot(
            doctor_id
        )
    )

    note = (
        "SELENIUM-TC-APPOINTMENT-002-"
        + str(int(time.time()))
    )

    appointment = appointment_api.create_appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        booking_date=booking_slot["booking_date"],
        booking_time=booking_slot["booking_time"],
        notes=note
    )

    appointment_id = appointment["appointmentId"]

    yield {
        "appointment_id": appointment_id,
        "note": note,
        "patient_name": "Duong Le Kim Phung",
        "doctor_name": "Ly Minh",
        "appointment_time": (
            booking_slot["booking_time"]
            + " "
            + booking_slot["booking_date"]
        )
    }

@pytest.fixture
def appointment_tc3_data():
    appointment_api = AppointmentApi()
    medical_record_api = MedicalRecordApi()

    patient_id = 7
    doctor_id = 3

    booking_slot = (
        medical_record_api
        .find_available_booking_slot(
            doctor_id
        )
    )

    note = (
        "SELENIUM-TC-APPOINTMENT-003-"
        + str(int(time.time()))
    )

    appointment = appointment_api.create_appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        booking_date=booking_slot["booking_date"],
        booking_time=booking_slot["booking_time"],
        notes=note
    )

    appointment_id = appointment[
        "appointmentId"
    ]

    yield {
        "appointment_id": appointment_id,
        "note": note,
        "patient_name": "Duong Le Kim Phung",
        "doctor_name": "Ly Minh",
        "appointment_time": (
            booking_slot["booking_time"]
            + " "
            + booking_slot["booking_date"]
        )
    }

    appointments = (
        appointment_api
        .get_appointments_by_doctor(
            doctor_id
        )
    )

    for item in appointments:
        if (
            item.get("appointmentId")
            == appointment_id
            and item.get("status")
            != "cancelled"
        ):
            appointment_api.cancel_appointment(
                appointment_id
            )
            break

@pytest.fixture
def appointment_tc5_data():
    appointment_api = AppointmentApi()
    medical_record_api = MedicalRecordApi()

    patient_id = 7
    doctor_id = 3
    note = "SELENIUM-TC-APPOINTMENT-005"

    appointment = None

    appointments = (
        appointment_api
        .get_appointments_by_doctor(
            doctor_id
        )
    )

    for item in appointments:
        if (
            item.get("notes") == note
            and item.get("status") == "pending"
        ):
            appointment = item
            break

    if appointment is None:
        booking_slot = (
            medical_record_api
            .find_available_booking_slot(
                doctor_id
            )
        )
        appointment = (
            appointment_api.create_appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                booking_date=booking_slot[
                    "booking_date"
                ],
                booking_time=booking_slot[
                    "booking_time"
                ],
                notes=note
            )
        )
    yield {
        "appointment_id": appointment[
            "appointmentId"
        ],
        "note": note
    }

@pytest.fixture
def appointment_tc6_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = (
        medical_record_api
        .prepare_confirmed_appointment(
            patient_id=7,
            doctor_id=3,
            notes="SELENIUM-TC-APPOINTMENT-006"
        )
    )
    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-APPOINTMENT-006",
        "patient_name": "Duong Le Kim Phung"
    }
@pytest.fixture
def appointment_tc7_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = (
        medical_record_api
        .prepare_confirmed_appointment(
            patient_id=7,
            doctor_id=3,
            notes="SELENIUM-TC-APPOINTMENT-007"
        )
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-APPOINTMENT-007"
    }

@pytest.fixture
def appointment_tc8_data():
    appointment_api = AppointmentApi()
    medical_record_api = MedicalRecordApi()

    patient_id = 7
    doctor_id = 3
    note = "SELENIUM-TC-APPOINTMENT-008"

    appointment = None

    appointments = (
        appointment_api
        .get_appointments_by_doctor(
            doctor_id
        )
    )

    # Dùng lại lịch TC8 đã hủy nếu có
    for item in appointments:
        if (
            item.get("notes") == note
            and item.get("status") == "cancelled"
        ):
            appointment = item
            break

    # Chưa có thì tạo lịch mới rồi hủy
    if appointment is None:
        booking_slot = (
            medical_record_api
            .find_available_booking_slot(
                doctor_id
            )
        )

        appointment = (
            appointment_api.create_appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                booking_date=booking_slot[
                    "booking_date"
                ],
                booking_time=booking_slot[
                    "booking_time"
                ],
                notes=note
            )
        )

        appointment_api.cancel_appointment(
            appointment["appointmentId"]
        )

    yield {
        "appointment_id": appointment[
            "appointmentId"
        ],
        "note": note
    }

@pytest.fixture
def appointment_tc9_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = (
        medical_record_api
        .prepare_confirmed_appointment(
            patient_id=7,
            doctor_id=3,
            notes="SELENIUM-TC-APPOINTMENT-009"
        )
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-APPOINTMENT-009",
        "patient_name": "Duong Le Kim Phung",
        "doctor_name": "Ly Minh",
        "diagnosis": (
            "Đau cổ do ngồi sai tư thế"
        ),
        "treatment": (
            "Nghỉ ngơi và tập vận động nhẹ"
        )
    }

@pytest.fixture
def appointment_tc1_data():
    appointment_api = AppointmentApi()
    medical_record_api = MedicalRecordApi()

    doctor_id = 1

    booking_slot = (
        medical_record_api
        .find_available_booking_slot(
            doctor_id
        )
    )

    note = (
        "SELENIUM-TC-APPOINTMENT-001-"
        + str(int(time.time()))
    )

    yield {
        "appointment_api": appointment_api,
        "doctor_id": doctor_id,
        "booking_date": booking_slot[
            "booking_date"
        ],
        "booking_time": booking_slot[
            "booking_time"
        ],
        "note": note
    }
@pytest.fixture
def appointment_tc4_data():
    appointment_api = AppointmentApi()
    medical_record_api = MedicalRecordApi()

    patient_id = 7
    doctor_id = 3
    note = "SELENIUM-TC-APPOINTMENT-004"

    appointment = None

    appointments = (
        appointment_api
        .get_appointments_by_doctor(
            doctor_id
        )
    )

    # Dùng lại lịch TC4 đang chờ xác nhận
    for item in appointments:
        if (
            item.get("notes") == note
            and item.get("status") == "pending"
        ):
            appointment = item
            break

    # Chưa có thì tạo lịch mới
    if appointment is None:
        booking_slot = (
            medical_record_api
            .find_available_booking_slot(
                doctor_id
            )
        )

        appointment = (
            appointment_api
            .create_appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                booking_date=booking_slot[
                    "booking_date"
                ],
                booking_time=booking_slot[
                    "booking_time"
                ],
                notes=note
            )
        )

    yield {
        "appointment_id": appointment[
            "appointmentId"
        ],
        "note": note,
        "patient_name": "Duong Le Kim Phung"
    }

# ============================================================
# NOTIFICATION TEST REPORT
# Ghi nhận kết quả TC-NOTIFICATION và tự xuất báo cáo Word.
# ============================================================

_notification_tests_collected = False

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

            if file_path.name != "test_notification.py":
                continue

            source_lines = file_path.read_text(
                encoding="utf-8"
            ).splitlines()

            line_index = int(entry.lineno)

            if line_index >= len(source_lines):
                line_index = len(source_lines) - 1

            for index in range(line_index, -1, -1):

                step_match = re.search(
                    r"#\s*Step\s+(\d+)\s*:",
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

def get_notification_test_case_id(item):
    """
    Lấy mã Test Case từ tên hàm pytest.

    Ví dụ:
    test_tc_notification_001_patient_receives_notification_after_admin_confirms
    -> TC-NOTIFICATION-001
    """
    match = re.search(r"test_tc_notification_(\d{3})", item.name)

    if match is None:
        return None

    return f"TC-NOTIFICATION-{match.group(1)}"


def pytest_sessionstart(session):
    """Xóa dữ liệu report cũ trước mỗi lần pytest bắt đầu."""
    global _notification_tests_collected
    _notification_tests_collected = False
    reset_test_report()


def pytest_collection_modifyitems(session, config, items):
    """Đánh dấu session hiện tại có chạy Notification test hay không."""
    global _notification_tests_collected

    _notification_tests_collected = any(
        get_notification_test_case_id(item) is not None
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

    test_case_id = get_notification_test_case_id(
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

        save_test_result(
            test_case_id=test_case_id,
            status="XFAILED",
            detail=str(report.wasxfail),
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
    Sau khi pytest kết thúc, chỉ xuất Word khi session có Notification TC.

    --collect-only không xuất report vì test chưa được thực thi.
    """
    if not _notification_tests_collected:
        return

    if session.config.option.collectonly:
        return

    generate_word_report(
        "reports/Notification_Test_Report.docx"
    )
def pytest_runtest_setup(item):
    """
    Hiển thị mã Test Case và mô tả
    trước khi bắt đầu thực thi từng test.
    """

    # Chỉ áp dụng cho Notification Test Case
    if "test_tc_notification_" not in item.name:
        return

    description = inspect.getdoc(item.obj)

    print("\n")
    print("=" * 80)
    print("TEST CASE DESCRIPTION")
    print("=" * 80)

    if description:
        print(description)
    else:
        print("Không có mô tả Test Case.")

    print("=" * 80)
