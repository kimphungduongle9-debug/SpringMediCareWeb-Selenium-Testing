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


# ============================================================
# COMMON HELPER
# ============================================================

def login_account(driver, username, password):
    login_page = LoginPage(driver)

    login_page.open_page()
    login_page.login(username, password)

    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == "http://localhost:3000/"
    )

    assert driver.current_url == "http://localhost:3000/", (
        "LOGIN FAILED | "
        "Expected: http://localhost:3000/ | "
        f"Actual: {driver.current_url}"
    )


# ============================================================
# TC-MEDICAL-006
# ============================================================

def test_tc_medical_006_update_medical_record(driver):
    """
    TC-MEDICAL-006:
    Kiểm tra bác sĩ có thể cập nhật thành công
    hồ sơ bệnh án thuộc lịch hẹn của mình.
    """

    test_case_id = "TC-MEDICAL-006"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra bác sĩ cập nhật thành công "
        "hồ sơ bệnh án thuộc lịch hẹn của mình"
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
    # Chuẩn bị lịch Completed, đã có hồ sơ
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
            "ở trạng thái Đã hoàn thành, đã có hồ sơ "
            "và ghi nhận dữ liệu hiện tại"
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

    actual_title = (
        medical_record_page.get_page_title()
    )

    assert actual_title == "Chi tiết hồ sơ bệnh án", (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected title: Chi tiết hồ sơ bệnh án | "
        f"Actual: {actual_title}"
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected URL chứa appointmentId={appointment_id} | "
        f"Actual URL: {driver.current_url}"
    )

    actual_diagnosis_before = (
        medical_record_page
        .get_diagnosis_information()
    )

    actual_treatment_before = (
        medical_record_page
        .get_treatment_information()
    )

    assert actual_diagnosis_before.strip() != "", (
        f"{test_case_id} | STEP 2 FAILED | "
        "Hồ sơ hiện tại không có Chẩn đoán."
    )

    assert actual_treatment_before.strip() != "", (
        f"{test_case_id} | STEP 2 FAILED | "
        "Hồ sơ hiện tại không có Hướng điều trị."
    )

    # Ghi nhận dữ liệu thực tế hiện tại làm baseline cho TC006.
    original_diagnosis = (
        actual_diagnosis_before
        .replace("Chẩn đoán:", "", 1)
        .strip()
    )

    original_treatment = (
        actual_treatment_before
        .replace("Hướng điều trị:", "", 1)
        .strip()
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description=(
            "Đăng nhập bằng bác sĩ phụ trách "
            f"và mở hồ sơ appointment #{appointment_id} thành công"
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
        "Expected: Form cập nhật được hiển thị | "
        "Actual: Không tìm thấy form."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            "Nhấn Cập nhật hồ sơ và mở form cập nhật thành công"
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
    # Thay đổi Chẩn đoán và Hướng điều trị.
    # ============================================================

    unique_time = str(int(time.time()))

    new_diagnosis = (
        "Chẩn đoán cập nhật TC-MEDICAL-006 "
        + unique_time
    )

    new_treatment = (
        "Hướng điều trị cập nhật TC-MEDICAL-006 "
        + unique_time
    )

    medical_record_page.enter_diagnosis(
        new_diagnosis
    )

    medical_record_page.enter_treatment(
        new_treatment
    )

    actual_diagnosis_input = (
        medical_record_page
        .get_diagnosis_input_value()
    )

    actual_treatment_input = (
        medical_record_page
        .get_treatment_input_value()
    )

    assert actual_diagnosis_input == new_diagnosis, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected diagnosis input: {new_diagnosis} | "
        f"Actual: {actual_diagnosis_input}"
    )

    assert actual_treatment_input == new_treatment, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected treatment input: {new_treatment} | "
        f"Actual: {actual_treatment_input}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            "Thay đổi Chẩn đoán và Hướng điều trị "
            "bằng dữ liệu mới"
        )
    )

    # ============================================================
    # STEP 6
    # Nhấn Lưu cập nhật.
    # ============================================================

    medical_record_page.click_save_changes()

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description="Nhấn Lưu cập nhật"
    )

    # ============================================================
    # STEP 7
    # Kiểm tra thông báo cập nhật thành công.
    # ============================================================

    update_message = (
        medical_record_page
        .get_update_success_message()
    )

    assert (
        update_message
        == "Cập nhật hồ sơ bệnh án thành công."
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected: Cập nhật hồ sơ bệnh án thành công. | "
        f"Actual: {update_message}"
    )

    assert not (
        medical_record_page.is_edit_form_present()
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected: Form cập nhật đóng sau khi lưu | "
        "Actual: Form vẫn đang hiển thị."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=7,
        description=(
            "Hệ thống hiển thị thông báo "
            "Cập nhật hồ sơ bệnh án thành công"
        )
    )

    # ============================================================
    # STEP 8
    # Mở lại hồ sơ và kiểm tra dữ liệu mới.
    # ============================================================

    medical_record_page.open_page(
        appointment_id
    )

    updated_diagnosis = (
        medical_record_page
        .get_diagnosis_information()
    )

    updated_treatment = (
        medical_record_page
        .get_treatment_information()
    )

    assert new_diagnosis in updated_diagnosis, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected diagnosis mới: {new_diagnosis} | "
        f"Actual: {updated_diagnosis}"
    )

    assert new_treatment in updated_treatment, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected treatment mới: {new_treatment} | "
        f"Actual: {updated_treatment}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=8,
        description=(
            "Mở lại hồ sơ và xác nhận "
            "Chẩn đoán, Hướng điều trị đã được cập nhật"
        )
    )

    # ============================================================
    # STEP 9
    # Kiểm tra hồ sơ vẫn thuộc cùng appointment,
    # patient và doctor.
    # ============================================================

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected appointmentId={appointment_id} | "
        f"Actual URL: {driver.current_url}"
    )

    actual_patient = (
        medical_record_page
        .get_patient_name()
    )

    actual_doctor = (
        medical_record_page
        .get_doctor_information()
    )

    assert actual_patient == patient_name, (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected patient: {patient_name} | "
        f"Actual: {actual_patient}"
    )

    assert doctor_name in actual_doctor, (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected doctor chứa: {doctor_name} | "
        f"Actual: {actual_doctor}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=9,
        description=(
            f"Hồ sơ vẫn thuộc appointment #{appointment_id}, "
            f"bệnh nhân {patient_name} và bác sĩ {doctor_name}"
        )
    )

    # ============================================================
    # STEP 10
    # Kiểm tra cập nhật hồ sơ hiện tại,
    # không tạo thêm hồ sơ mới
    # và appointment vẫn Completed.
    # ============================================================

    # Cùng appointmentId vẫn mở được đúng hồ sơ vừa cập nhật.
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

    assert new_diagnosis in final_diagnosis, (
        f"{test_case_id} | STEP 10 FAILED | "
        "Expected: Hồ sơ hiện tại chứa diagnosis mới | "
        f"Actual: {final_diagnosis}"
    )

    assert new_treatment in final_treatment, (
        f"{test_case_id} | STEP 10 FAILED | "
        "Expected: Hồ sơ hiện tại chứa treatment mới | "
        f"Actual: {final_treatment}"
    )

    medical_record_api.assert_appointment_status(
        doctor_id=doctor_id,
        appointment_id=appointment_id,
        expected_status="completed"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=10,
        description=(
            "Hệ thống giữ nguyên hồ sơ của appointment "
            f"#{appointment_id}, dữ liệu đã được cập nhật "
            "và lịch vẫn ở trạng thái Đã hoàn thành"
        )
    )