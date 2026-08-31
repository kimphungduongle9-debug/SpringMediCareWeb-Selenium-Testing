import time

from pages.LoginPage import LoginPage
from pages.MedicalRecordPage import MedicalRecordPage

from api.MedicalRecordApi import MedicalRecordApi

from utils.test_reporter import report_step
from utils.data_reader import (
    get_test_data_csv,
    MEDICAL_TEST_DATA_CSV,
)

from tests.helpers.medical_helpers import (
    prepare_completed_medical_record,
)

from selenium.webdriver.support.ui import WebDriverWait


HOME_URL = "http://localhost:3000/"


# ============================================================
# COMMON HELPER
# ============================================================

def login_account(driver, username, password):
    login_page = LoginPage(driver)

    login_page.open_page()
    login_page.login(username, password)

    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == HOME_URL
    )

    assert driver.current_url == HOME_URL, (
        "LOGIN FAILED | "
        f"Expected: {HOME_URL} | "
        f"Actual: {driver.current_url}"
    )


# ============================================================
# TC-MEDICAL-009
# ============================================================

def test_tc_medical_009_cancel_update_keeps_old_data(driver):
    """
    TC-MEDICAL-009:
    Kiểm tra thao tác Hủy cập nhật không làm thay đổi
    dữ liệu hồ sơ bệnh án đã lưu.
    """

    test_case_id = "TC-MEDICAL-009"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra Hủy cập nhật không làm thay đổi "
        "dữ liệu hồ sơ bệnh án đã lưu"
    )

    test_data = get_test_data_csv(
        MEDICAL_TEST_DATA_CSV,
        test_case_id
    )

    patient_id = int(test_data["patient_id"])
    doctor_id = int(test_data["doctor_id"])

    note = test_data["note"]
    patient_name = test_data["patient_name"]
    doctor_name = test_data["doctor_name"]

    setup_diagnosis = test_data["diagnosis"]
    setup_treatment = test_data["treatment"]

    medical_record_api = MedicalRecordApi()

    # ============================================================
    # STEP 1
    # Chuẩn bị hồ sơ bệnh án
    # và ghi nhận dữ liệu hiện tại.
    # ============================================================

    appointment_id = prepare_completed_medical_record(
        medical_record_api=medical_record_api,
        patient_id=patient_id,
        doctor_id=doctor_id,
        note=note,
        diagnosis=setup_diagnosis,
        treatment=setup_treatment,
        test_data=test_data,
        test_case_id=test_case_id
    )

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
            "ở trạng thái Đã hoàn thành và đã có hồ sơ bệnh án"
        )
    )

    # ============================================================
    # STEP 2
    # Đăng nhập bác sĩ phụ trách và mở hồ sơ.
    # ============================================================

    login_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    medical_record_page = MedicalRecordPage(driver)

    medical_record_page.open_page(
        appointment_id
    )

    assert (
        medical_record_page.get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    ), (
        f"{test_case_id} | STEP 2 FAILED | "
        "Không mở được trang Chi tiết hồ sơ bệnh án."
    )

    original_patient = (
        medical_record_page.get_patient_name()
    )

    original_doctor = (
        medical_record_page.get_doctor_information()
    )

    original_diagnosis_text = (
        medical_record_page.get_diagnosis_information()
    )

    original_treatment_text = (
        medical_record_page.get_treatment_information()
    )

    assert original_patient == patient_name, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected patient: {patient_name} | "
        f"Actual: {original_patient}"
    )

    assert doctor_name in original_doctor, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected doctor chứa: {doctor_name} | "
        f"Actual: {original_doctor}"
    )

    original_diagnosis = (
        original_diagnosis_text
        .replace("Chẩn đoán:", "", 1)
        .strip()
    )

    original_treatment = (
        original_treatment_text
        .replace("Hướng điều trị:", "", 1)
        .strip()
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description=(
            f"Đăng nhập bác sĩ phụ trách và mở hồ sơ "
            f"appointment #{appointment_id} thành công"
        )
    )

    # ============================================================
    # STEP 3
    # Nhấn Cập nhật hồ sơ.
    # ============================================================

    assert (
        medical_record_page.is_edit_button_present()
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Có nút Cập nhật hồ sơ | "
        "Actual: Không tìm thấy nút."
    )

    medical_record_page.click_edit_button()

    assert (
        medical_record_page.is_edit_form_present()
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Form cập nhật hiển thị | "
        "Actual: Không tìm thấy form."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            "Nhấn Cập nhật hồ sơ và mở form chỉnh sửa thành công"
        )
    )

    # ============================================================
    # STEP 4
    # Kiểm tra form preload đúng dữ liệu hiện tại.
    # ============================================================

    diagnosis_input_before = (
        medical_record_page
        .get_diagnosis_input_value()
    )

    treatment_input_before = (
        medical_record_page
        .get_treatment_input_value()
    )

    assert diagnosis_input_before == original_diagnosis, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected diagnosis preload: {original_diagnosis} | "
        f"Actual: {diagnosis_input_before}"
    )

    assert treatment_input_before == original_treatment, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected treatment preload: {original_treatment} | "
        f"Actual: {treatment_input_before}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            "Form cập nhật hiển thị đúng "
            "Chẩn đoán và Hướng điều trị hiện tại"
        )
    )

    # ============================================================
    # STEP 5
    # Thay đổi Chẩn đoán và Hướng điều trị
    # bằng dữ liệu mới.
    # ============================================================

    unique_time = str(int(time.time()))

    new_diagnosis = (
        "Chẩn đoán tạm TC-MEDICAL-009 "
        + unique_time
    )

    new_treatment = (
        "Hướng điều trị tạm TC-MEDICAL-009 "
        + unique_time
    )

    medical_record_page.enter_diagnosis(
        new_diagnosis
    )

    medical_record_page.enter_treatment(
        new_treatment
    )

    assert (
        medical_record_page.get_diagnosis_input_value()
        == new_diagnosis
    ), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Diagnosis input không nhận dữ liệu mới."
    )

    assert (
        medical_record_page.get_treatment_input_value()
        == new_treatment
    ), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Treatment input không nhận dữ liệu mới."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            "Thay đổi Chẩn đoán và Hướng điều trị "
            "bằng dữ liệu tạm mới"
        )
    )

    # ============================================================
    # STEP 6
    # Nhấn Hủy.
    # ============================================================

    medical_record_page.click_cancel_edit()

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            "Nhấn Hủy cập nhật hồ sơ"
        )
    )

    # ============================================================
    # STEP 7
    # Kiểm tra form đóng
    # và dữ liệu mới không được lưu.
    # ============================================================

    assert not (
        medical_record_page.is_edit_form_present()
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected: Form cập nhật đã đóng | "
        "Actual: Form vẫn đang hiển thị."
    )

    current_diagnosis = (
        medical_record_page.get_diagnosis_information()
    )

    current_treatment = (
        medical_record_page.get_treatment_information()
    )

    assert new_diagnosis not in current_diagnosis, (
        f"{test_case_id} | STEP 7 FAILED | "
        "Diagnosis tạm vẫn xuất hiện sau khi Hủy."
    )

    assert new_treatment not in current_treatment, (
        f"{test_case_id} | STEP 7 FAILED | "
        "Treatment tạm vẫn xuất hiện sau khi Hủy."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=7,
        description=(
            "Form cập nhật được đóng và dữ liệu tạm mới "
            "không được lưu"
        )
    )

    # ============================================================
    # STEP 8
    # Mở lại hồ sơ và kiểm tra
    # dữ liệu ban đầu vẫn giữ nguyên.
    # ============================================================

    medical_record_page.open_page(
        appointment_id
    )

    final_diagnosis = (
        medical_record_page.get_diagnosis_information()
    )

    final_treatment = (
        medical_record_page.get_treatment_information()
    )

    assert final_diagnosis == original_diagnosis_text, (
        f"{test_case_id} | STEP 8 FAILED | "
        "Diagnosis ban đầu bị thay đổi. "
        f"Before: {original_diagnosis_text} | "
        f"After: {final_diagnosis}"
    )

    assert final_treatment == original_treatment_text, (
        f"{test_case_id} | STEP 8 FAILED | "
        "Treatment ban đầu bị thay đổi. "
        f"Before: {original_treatment_text} | "
        f"After: {final_treatment}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=8,
        description=(
            "Mở lại hồ sơ và xác nhận Chẩn đoán, "
            "Hướng điều trị ban đầu vẫn được giữ nguyên"
        )
    )

    # ============================================================
    # STEP 9
    # Kiểm tra hồ sơ vẫn thuộc đúng lịch hẹn,
    # bệnh nhân, bác sĩ và lịch vẫn Completed.
    # ============================================================

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected appointmentId={appointment_id} | "
        f"Actual URL: {driver.current_url}"
    )

    final_patient = (
        medical_record_page.get_patient_name()
    )

    final_doctor = (
        medical_record_page.get_doctor_information()
    )

    assert final_patient == original_patient, (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected patient: {original_patient} | "
        f"Actual: {final_patient}"
    )

    assert final_doctor == original_doctor, (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected doctor: {original_doctor} | "
        f"Actual: {final_doctor}"
    )

    medical_record_api.assert_appointment_status(
        doctor_id=doctor_id,
        appointment_id=appointment_id,
        expected_status="completed"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=9,
        description=(
            f"Hồ sơ vẫn thuộc appointment #{appointment_id}, "
            f"bệnh nhân {patient_name}, bác sĩ {doctor_name} "
            "và lịch vẫn ở trạng thái Đã hoàn thành"
        )
    )