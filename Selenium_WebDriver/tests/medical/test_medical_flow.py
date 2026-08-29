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

def test_tc_medical_004_prevent_duplicate_medical_record(driver):
    """
    TC-MEDICAL-004:
    Kiểm tra không thể tạo hồ sơ bệnh án thứ hai
    cho một lịch hẹn đã hoàn thành và đã có hồ sơ.
    """

    test_case_id = "TC-MEDICAL-004"

    test_data = get_test_data_csv(
        MEDICAL_TEST_DATA_CSV,
        test_case_id
    )

    patient_id = int(test_data["patient_id"])
    doctor_id = int(test_data["doctor_id"])

    note = test_data["note"]
    diagnosis = test_data["diagnosis"]
    treatment = test_data["treatment"]

    medical_record_api = MedicalRecordApi()

    # ============================================================
    # Step 1:
    # Chuẩn bị lịch Đã hoàn thành và đã có hồ sơ bệnh án;
    # ghi nhận appointmentId và nội dung hồ sơ hiện tại.
    # ============================================================

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

    medical_record_api.assert_appointment_status(
        doctor_id=doctor_id,
        appointment_id=appointment_id,
        expected_status="completed"
    )
    original_diagnosis = diagnosis
    original_treatment = treatment

    assert original_diagnosis != "", (
        "TC-MEDICAL-004 | STEP 1 FAILED | "
        "Chẩn đoán ban đầu trong CSV đang trống."
    )

    assert original_treatment != "", (
        "TC-MEDICAL-004 | STEP 1 FAILED | "
        "Hướng điều trị ban đầu trong CSV đang trống."
    )
    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description=(
            f"Chuẩn bị appointment #{appointment_id} "
            "đã hoàn thành và đã có hồ sơ bệnh án"
        )
    )

    # ============================================================
    # Step 2:
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
            "Đăng nhập bằng tài khoản bác sĩ phụ trách thành công"
        )
    )

    # ============================================================
    # Step 3:
    # Mở Lịch hẹn bệnh nhân, tìm đúng lịch và mở Xem hồ sơ.
    # ============================================================

    appointment_page = DoctorAppointmentPage(driver)

    appointment_page.open_page()

    actual_note = (
        appointment_page
        .get_note_by_id(
            appointment_id
        )
    )

    assert actual_note == note, (
        "TC-MEDICAL-004 | STEP 3 FAILED | "
        f"Expected note: {note} | "
        f"Actual: {actual_note}"
    )

    actual_status = (
        appointment_page
        .get_status_by_id(
            appointment_id
        )
    )

    assert actual_status == "Đã hoàn thành", (
        "TC-MEDICAL-004 | STEP 3 FAILED | "
        "Expected: Đã hoàn thành | "
        f"Actual: {actual_status}"
    )

    assert (
        appointment_page
        .is_view_medical_record_button_present_by_id(
            appointment_id
        )
    ), (
        "TC-MEDICAL-004 | STEP 3 FAILED | "
        "Không tìm thấy nút Xem hồ sơ."
    )

    appointment_page.click_view_medical_record(
        note
    )

    medical_record_page = MedicalRecordPage(driver)

    assert (
        medical_record_page.get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    ), (
        "TC-MEDICAL-004 | STEP 3 FAILED | "
        "Không mở đúng trang Chi tiết hồ sơ bệnh án."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            f"Tìm đúng appointment #{appointment_id} "
            "và mở Xem hồ sơ thành công"
        )
    )

    # ============================================================
    # Step 4:
    # Kiểm tra hồ sơ hiện tại được hiển thị đúng.
    # ============================================================

    actual_diagnosis = (
        medical_record_page
        .get_diagnosis_information()
    )

    actual_treatment = (
        medical_record_page
        .get_treatment_information()
    )

    assert original_diagnosis in actual_diagnosis, (
        "TC-MEDICAL-004 | STEP 4 FAILED | "
        f"Expected diagnosis chứa: {original_diagnosis} | "
        f"Actual: {actual_diagnosis}"
    )

    assert original_treatment in actual_treatment, (
        "TC-MEDICAL-004 | STEP 4 FAILED | "
        f"Expected treatment chứa: {original_treatment} | "
        f"Actual: {actual_treatment}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            "Hồ sơ hiện tại hiển thị đúng Chẩn đoán "
            "và Hướng điều trị đã lưu"
        )
    )

    # ============================================================
    # Step 5:
    # Truy cập trực tiếp trang Khám bệnh
    # bằng appointmentId của lịch đã hoàn thành.
    # ============================================================

    examination_page = DoctorExaminationPage(driver)

    examination_page.open_page(
        appointment_id
    )

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            f"Truy cập trực tiếp trang Khám bệnh "
            f"với appointmentId={appointment_id}"
        )
    )

    # ============================================================
    # Step 6:
    # Kiểm tra hệ thống chặn tạo hồ sơ bệnh án mới.
    # ============================================================

    invalid_message = (
        examination_page
        .get_invalid_appointment_message()
    )

    assert invalid_message.strip() != "", (
        "TC-MEDICAL-004 | STEP 6 FAILED | "
        "Không có thông báo chặn truy cập."
    )

    assert not (
        examination_page
        .is_create_record_form_present()
    ), (
        "TC-MEDICAL-004 | STEP 6 FAILED | "
        "Form tạo hồ sơ bệnh án vẫn được hiển thị."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            "Hệ thống chặn tạo hồ sơ bệnh án thứ hai "
            "cho lịch đã hoàn thành"
        )
    )

    # ============================================================
    # Step 7:
    # Mở lại hồ sơ và xác nhận dữ liệu cũ không thay đổi,
    # lịch vẫn ở trạng thái Đã hoàn thành.
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

    assert original_diagnosis in final_diagnosis, (
        "TC-MEDICAL-004 | STEP 7 FAILED | "
        "Chẩn đoán cũ đã bị thay đổi."
    )

    assert original_treatment in final_treatment, (
        "TC-MEDICAL-004 | STEP 7 FAILED | "
        "Hướng điều trị cũ đã bị thay đổi."
    )

    medical_record_api.assert_appointment_status(
        doctor_id=doctor_id,
        appointment_id=appointment_id,
        expected_status="completed"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=7,
        description=(
            f"Hồ sơ appointment #{appointment_id} không thay đổi "
            "và lịch vẫn ở trạng thái Đã hoàn thành"
        )
    )