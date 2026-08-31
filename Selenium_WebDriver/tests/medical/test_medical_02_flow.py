from pages.LoginPage import LoginPage
from pages.DoctorAppointmentPage import DoctorAppointmentPage
from pages.DoctorExaminationPage import DoctorExaminationPage
from pages.MedicalRecordPage import MedicalRecordPage

from api.MedicalRecordApi import MedicalRecordApi

from utils.test_reporter import report_step
from utils.data_reader import (
    get_test_data_csv,
    MEDICAL_TEST_DATA_CSV,
)

from selenium.webdriver.support.ui import WebDriverWait


# ============================================================
# COMMON HELPERS
# ============================================================

def login_account(driver, username, password):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        username,
        password
    )

    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == "http://localhost:3000/"
    )

    assert driver.current_url == "http://localhost:3000/", (
        "LOGIN FAILED | "
        "Expected: http://localhost:3000/ | "
        f"Actual: {driver.current_url}"
    )


# ============================================================
# TC-MEDICAL-004
# ============================================================

def test_tc_medical_004_prevent_duplicate_medical_record(driver):
    """
    TC-MEDICAL-004:
    Kiểm tra hệ thống không cho phép bác sĩ tạo thêm
    hồ sơ bệnh án cho lịch hẹn đã hoàn thành
    và đã có hồ sơ bệnh án.
    """

    test_case_id = "TC-MEDICAL-004"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra không cho phép tạo thêm hồ sơ bệnh án "
        "cho lịch đã hoàn thành"
    )

    test_data = get_test_data_csv(
        MEDICAL_TEST_DATA_CSV,
        test_case_id
    )

    patient_id = int(
        test_data["patient_id"]
    )

    doctor_id = int(
        test_data["doctor_id"]
    )

    note = test_data["note"]
    diagnosis = test_data["diagnosis"]
    treatment = test_data["treatment"]

    medical_record_api = MedicalRecordApi()

    # ============================================================
    # STEP 1:
    # Chuẩn bị lịch Đã hoàn thành
    # và đã có hồ sơ bệnh án.
    # ============================================================

    try:
        appointment_id = (
            medical_record_api
            .prepare_completed_medical_record(
                patient_id=patient_id,
                doctor_id=doctor_id,
                notes=note,
                diagnosis=diagnosis,
                treatment=treatment
            )
        )

    except AssertionError as error:
        raise AssertionError(
            f"{test_case_id} | STEP 1 FAILED | "
            "Không thể chuẩn bị lịch Đã hoàn thành "
            "và hồ sơ bệnh án. "
            f"Actual: {error}"
        ) from error

    medical_record_api.assert_appointment_status(
        doctor_id=doctor_id,
        appointment_id=appointment_id,
        expected_status="completed"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description=(
            f"Chuẩn bị appointment #{appointment_id} "
            "ở trạng thái Đã hoàn thành "
            "và đã có hồ sơ bệnh án"
        )
    )

    # ============================================================
    # STEP 2:
    # Đăng nhập bằng bác sĩ phụ trách.
    # ============================================================

    login_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description=(
            "Đăng nhập bằng tài khoản "
            "bác sĩ phụ trách thành công"
        )
    )

    # ============================================================
    # STEP 3:
    # Mở trang Lịch hẹn bệnh nhân
    # và tìm đúng lịch đã chuẩn bị.
    # ============================================================

    appointment_page = DoctorAppointmentPage(
        driver
    )

    appointment_page.open_page()

    actual_note = (
        appointment_page
        .get_note_by_id(
            appointment_id
        )
    )

    assert actual_note == note, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected note: {note} | "
        f"Actual: {actual_note}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            "Mở trang Lịch hẹn bệnh nhân "
            f"và tìm đúng appointment #{appointment_id}"
        )
    )

    # ============================================================
    # STEP 4:
    # Kiểm tra lịch ở trạng thái Đã hoàn thành,
    # có nút Xem hồ sơ và không còn nút Khám bệnh.
    # ============================================================

    actual_status = (
        appointment_page
        .get_status_by_id(
            appointment_id
        )
    )

    assert actual_status == "Đã hoàn thành", (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected status: Đã hoàn thành | "
        f"Actual: {actual_status}"
    )

    assert (
        appointment_page
        .is_view_medical_record_button_present_by_id(
            appointment_id
        )
    ), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Có nút Xem hồ sơ | "
        "Actual: Không tìm thấy nút Xem hồ sơ."
    )

    assert not (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    ), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Không còn nút Khám bệnh | "
        "Actual: Nút Khám bệnh vẫn hiển thị."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            f"Appointment #{appointment_id} "
            "ở trạng thái Đã hoàn thành, "
            "có nút Xem hồ sơ và "
            "không còn nút Khám bệnh"
        )
    )

    # ============================================================
    # STEP 5:
    # Nhấn Xem hồ sơ và kiểm tra
    # hồ sơ hiện có được hiển thị đúng.
    # ============================================================

    appointment_page.click_view_medical_record(
        note
    )

    medical_record_page = MedicalRecordPage(
        driver
    )

    actual_title = (
        medical_record_page
        .get_page_title()
    )

    assert (
        actual_title
        == "Chi tiết hồ sơ bệnh án"
    ), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected page title: "
        "Chi tiết hồ sơ bệnh án | "
        f"Actual: {actual_title}"
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected URL chứa appointmentId="
        f"{appointment_id} | "
        f"Actual URL: {driver.current_url}"
    )

    actual_diagnosis = (
        medical_record_page
        .get_diagnosis_information()
    )

    actual_treatment = (
        medical_record_page
        .get_treatment_information()
    )

    assert diagnosis in actual_diagnosis, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected diagnosis chứa: {diagnosis} | "
        f"Actual: {actual_diagnosis}"
    )

    assert treatment in actual_treatment, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected treatment chứa: {treatment} | "
        f"Actual: {actual_treatment}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            "Nhấn Xem hồ sơ và hồ sơ hiện có "
            "hiển thị đúng Chẩn đoán "
            "và Hướng điều trị"
        )
    )

    # ============================================================
    # STEP 6:
    # Truy cập trực tiếp trang Khám bệnh
    # bằng appointmentId của lịch đã hoàn thành.
    # ============================================================

    examination_page = DoctorExaminationPage(
        driver
    )

    examination_page.open_page(
        appointment_id
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            "Truy cập trực tiếp trang Khám bệnh "
            f"với appointmentId={appointment_id}"
        )
    )

    # ============================================================
    # STEP 7:
    # Kiểm tra hệ thống chặn thao tác khám bệnh
    # và không hiển thị form tạo hồ sơ mới.
    # ============================================================

    invalid_message = (
        examination_page
        .get_invalid_appointment_message()
    )

    assert invalid_message.strip() != "", (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected: Có thông báo chặn truy cập | "
        "Actual: Không tìm thấy thông báo."
    )

    assert not (
        examination_page
        .is_create_record_form_present()
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected: Không hiển thị form "
        "tạo hồ sơ bệnh án | "
        "Actual: Form vẫn đang hiển thị."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=7,
        description=(
            "Hệ thống chặn thao tác Khám bệnh "
            "và không hiển thị form "
            "tạo hồ sơ bệnh án mới"
        )
    )

    # ============================================================
    # STEP 8:
    # Mở lại hồ sơ và kiểm tra
    # dữ liệu cũ không thay đổi.
    # ============================================================

    medical_record_page.open_page(
        appointment_id
    )

    final_diagnosis = (
        medical_record_page
        .get_diagnosis_information()
    )

    final_treatment = (
        medical_record_page
        .get_treatment_information()
    )

    assert diagnosis in final_diagnosis, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected diagnosis chứa: {diagnosis} | "
        f"Actual: {final_diagnosis}"
    )

    assert treatment in final_treatment, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected treatment chứa: {treatment} | "
        f"Actual: {final_treatment}"
    )

    medical_record_api.assert_appointment_status(
        doctor_id=doctor_id,
        appointment_id=appointment_id,
        expected_status="completed"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=8,
        description=(
            f"Hồ sơ appointment #{appointment_id} "
            "không thay đổi và lịch vẫn "
            "ở trạng thái Đã hoàn thành"
        )
    )