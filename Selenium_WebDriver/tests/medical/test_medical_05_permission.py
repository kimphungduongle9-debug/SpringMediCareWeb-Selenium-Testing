from pages.LoginPage import LoginPage
from pages.DoctorAppointmentPage import DoctorAppointmentPage
from pages.MedicalRecordPage import MedicalRecordPage

from api.MedicalRecordApi import MedicalRecordApi

from utils.test_reporter import report_step
from utils.data_reader import (
    get_test_data_csv,
    MEDICAL_TEST_DATA_CSV,
)

from tests.helpers.medical_helpers import (
    prepare_completed_medical_record,
    logout_current_user,
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
# TC-MEDICAL-007
# ============================================================

def test_tc_medical_007_other_doctor_cannot_view_record(driver):
    """
    TC-MEDICAL-007:
    Kiểm tra bác sĩ khác không thể xem hồ sơ bệnh án
    không thuộc lịch hẹn của mình.
    """

    test_case_id = "TC-MEDICAL-007"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra bác sĩ khác không thể xem hồ sơ bệnh án "
        "không thuộc lịch hẹn của mình"
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
    # Chuẩn bị hồ sơ thuộc Doctor A
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

    # Login Doctor A để ghi nhận dữ liệu thật hiện tại.
    login_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    owner_record_page = MedicalRecordPage(driver)

    owner_record_page.open_page(
        appointment_id
    )

    assert (
        owner_record_page.get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    ), (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected: Doctor A mở được hồ sơ bệnh án | "
        f"Actual URL: {driver.current_url}"
    )

    original_patient = (
        owner_record_page.get_patient_name()
    )

    original_doctor = (
        owner_record_page.get_doctor_information()
    )

    original_diagnosis = (
        owner_record_page.get_diagnosis_information()
    )

    original_treatment = (
        owner_record_page.get_treatment_information()
    )

    assert original_patient == patient_name, (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected patient: {patient_name} | "
        f"Actual: {original_patient}"
    )

    assert doctor_name in original_doctor, (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected doctor chứa: {doctor_name} | "
        f"Actual: {original_doctor}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description=(
            f"Chuẩn bị appointment #{appointment_id} "
            f"đã hoàn thành và có hồ sơ thuộc Doctor A "
            f"({doctor_name})"
        )
    )

    # ============================================================
    # STEP 2
    # Đăng xuất Doctor A và đăng nhập Doctor B.
    # ============================================================

    logout_current_user(driver)

    login_account(
        driver,
        test_data["other_doctor_username"],
        test_data["other_doctor_password"]
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description=(
            "Đăng xuất Doctor A và đăng nhập "
            "Doctor B thành công"
        )
    )

    # ============================================================
    # STEP 3
    # Doctor B mở trang Lịch hẹn bệnh nhân.
    # ============================================================

    appointment_page = DoctorAppointmentPage(driver)

    appointment_page.open_page()

    assert "/doctor-appointments" in driver.current_url, (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected URL chứa /doctor-appointments | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            "Doctor B mở trang Lịch hẹn bệnh nhân thành công"
        )
    )

    # ============================================================
    # STEP 4
    # Kiểm tra appointment của Doctor A
    # không xuất hiện trong danh sách Doctor B.
    # ============================================================

    try:
        visible_note = (
            appointment_page
            .get_note_by_id(appointment_id)
        )
    except Exception:
        visible_note = None

    assert visible_note is None, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: Appointment #{appointment_id} "
        "không xuất hiện trong danh sách Doctor B | "
        f"Actual: Tìm thấy note '{visible_note}'."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            f"Appointment #{appointment_id} của Doctor A "
            "không xuất hiện trong danh sách Doctor B"
        )
    )

    # ============================================================
    # STEP 5
    # Doctor B truy cập trực tiếp URL hồ sơ Doctor A.
    # ============================================================

    medical_record_page = MedicalRecordPage(driver)

    medical_record_page.open_page(
        appointment_id
    )

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            "Doctor B truy cập trực tiếp URL hồ sơ "
            f"appointment #{appointment_id}"
        )
    )

    # ============================================================
    # STEP 6
    # Hệ thống phải chặn Doctor B
    # và không hiển thị dữ liệu hồ sơ.
    # ============================================================

    access_denied_message = (
        medical_record_page
        .get_access_denied_message()
    )

    expected_message = (
        "Bạn không có quyền xem hồ sơ bệnh án này."
    )

    assert access_denied_message == expected_message, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: {expected_message} | "
        f"Actual: {access_denied_message}"
    )

    assert not (
        medical_record_page
        .is_medical_record_information_present()
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: Không hiển thị thông tin hồ sơ | "
        "Actual: Doctor B vẫn thấy thông tin hồ sơ."
    )

    assert not (
        medical_record_page
        .is_edit_button_present()
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: Không có nút Cập nhật | "
        "Actual: Doctor B vẫn thấy nút Cập nhật."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            "Hệ thống từ chối quyền truy cập của Doctor B, "
            "không hiển thị dữ liệu và nút Cập nhật"
        )
    )

    # ============================================================
    # STEP 7
    # Đăng xuất Doctor B và đăng nhập lại Doctor A.
    # ============================================================

    logout_current_user(driver)

    login_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    report_step(
        test_case_id=test_case_id,
        step_number=7,
        description=(
            "Đăng xuất Doctor B và đăng nhập lại "
            "Doctor A thành công"
        )
    )

    # ============================================================
    # STEP 8
    # Doctor A mở lại hồ sơ.
    # Dữ liệu phải không thay đổi
    # và appointment vẫn Completed.
    # ============================================================

    owner_record_page = MedicalRecordPage(driver)

    owner_record_page.open_page(
        appointment_id
    )

    final_patient = (
        owner_record_page.get_patient_name()
    )

    final_doctor = (
        owner_record_page.get_doctor_information()
    )

    final_diagnosis = (
        owner_record_page.get_diagnosis_information()
    )

    final_treatment = (
        owner_record_page.get_treatment_information()
    )

    assert final_patient == original_patient, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected patient: {original_patient} | "
        f"Actual: {final_patient}"
    )

    assert final_doctor == original_doctor, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected doctor: {original_doctor} | "
        f"Actual: {final_doctor}"
    )

    assert final_diagnosis == original_diagnosis, (
        f"{test_case_id} | STEP 8 FAILED | "
        "Diagnosis bị thay đổi sau khi Doctor B truy cập. "
        f"Before: {original_diagnosis} | "
        f"After: {final_diagnosis}"
    )

    assert final_treatment == original_treatment, (
        f"{test_case_id} | STEP 8 FAILED | "
        "Treatment bị thay đổi sau khi Doctor B truy cập. "
        f"Before: {original_treatment} | "
        f"After: {final_treatment}"
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
            f"Doctor A mở lại hồ sơ appointment #{appointment_id}; "
            "dữ liệu không thay đổi và lịch vẫn "
            "ở trạng thái Đã hoàn thành"
        )
    )

# ============================================================
# TC-MEDICAL-008
# ============================================================

def test_tc_medical_008_other_doctor_cannot_update_record(driver):
    """
    TC-MEDICAL-008:
    Kiểm tra bác sĩ khác không thể cập nhật hồ sơ bệnh án
    không thuộc lịch hẹn của mình.
    """

    test_case_id = "TC-MEDICAL-008"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra bác sĩ khác không thể cập nhật hồ sơ bệnh án "
        "không thuộc lịch hẹn của mình"
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
    # Chuẩn bị hồ sơ thuộc Doctor A
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

    # Login Doctor A để ghi nhận baseline thật.
    login_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    owner_record_page = MedicalRecordPage(driver)

    owner_record_page.open_page(
        appointment_id
    )

    assert (
        owner_record_page.get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    ), (
        f"{test_case_id} | STEP 1 FAILED | "
        "Doctor A không mở được hồ sơ đã chuẩn bị."
    )

    original_patient = (
        owner_record_page.get_patient_name()
    )

    original_doctor = (
        owner_record_page.get_doctor_information()
    )

    original_diagnosis = (
        owner_record_page.get_diagnosis_information()
    )

    original_treatment = (
        owner_record_page.get_treatment_information()
    )

    assert original_patient == patient_name, (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected patient: {patient_name} | "
        f"Actual: {original_patient}"
    )

    assert doctor_name in original_doctor, (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected doctor chứa: {doctor_name} | "
        f"Actual: {original_doctor}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description=(
            f"Chuẩn bị appointment #{appointment_id} "
            f"đã hoàn thành, có hồ sơ thuộc Doctor A "
            f"({doctor_name}) và ghi nhận dữ liệu hiện tại"
        )
    )

    # ============================================================
    # STEP 2
    # Đăng nhập Doctor B.
    # ============================================================

    logout_current_user(driver)

    login_account(
        driver,
        test_data["other_doctor_username"],
        test_data["other_doctor_password"]
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description=(
            "Đăng xuất Doctor A và đăng nhập Doctor B thành công"
        )
    )

    # ============================================================
    # STEP 3
    # Doctor B truy cập trực tiếp URL hồ sơ Doctor A.
    # ============================================================

    medical_record_page = MedicalRecordPage(driver)

    medical_record_page.open_page(
        appointment_id
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            "Doctor B truy cập trực tiếp URL hồ sơ "
            f"appointment #{appointment_id}"
        )
    )

    # ============================================================
    # STEP 4
    # Kiểm tra hệ thống chặn truy cập
    # và Doctor B không thể sử dụng chức năng Cập nhật.
    # ============================================================

    access_denied_message = (
        medical_record_page
        .get_access_denied_message()
    )

    expected_message = (
        "Bạn không có quyền xem hồ sơ bệnh án này."
    )

    assert access_denied_message == expected_message, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: {expected_message} | "
        f"Actual: {access_denied_message}"
    )

    assert not (
        medical_record_page
        .is_medical_record_information_present()
    ), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Không hiển thị nội dung hồ sơ | "
        "Actual: Doctor B vẫn xem được nội dung hồ sơ."
    )

    assert not (
        medical_record_page
        .is_edit_button_present()
    ), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Doctor B không có nút Cập nhật | "
        "Actual: Nút Cập nhật vẫn hiển thị."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            "Hệ thống chặn Doctor B và không cho phép "
            "sử dụng chức năng Cập nhật hồ sơ"
        )
    )

    # ============================================================
    # STEP 5
    # Đăng xuất Doctor B và đăng nhập lại Doctor A.
    # ============================================================

    logout_current_user(driver)

    login_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            "Đăng xuất Doctor B và đăng nhập lại Doctor A thành công"
        )
    )

    # ============================================================
    # STEP 6
    # Mở lại hồ sơ đã chuẩn bị.
    # ============================================================

    owner_record_page = MedicalRecordPage(driver)

    owner_record_page.open_page(
        appointment_id
    )

    assert (
        owner_record_page.get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Doctor A không mở lại được hồ sơ."
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected URL chứa appointmentId={appointment_id} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            f"Doctor A mở lại hồ sơ appointment "
            f"#{appointment_id} thành công"
        )
    )

    # ============================================================
    # STEP 7
    # Kiểm tra Chẩn đoán và Hướng điều trị
    # không bị thay đổi.
    # ============================================================

    final_diagnosis = (
        owner_record_page
        .get_diagnosis_information()
    )

    final_treatment = (
        owner_record_page
        .get_treatment_information()
    )

    assert final_diagnosis == original_diagnosis, (
        f"{test_case_id} | STEP 7 FAILED | "
        "Chẩn đoán bị thay đổi trái phép. "
        f"Before: {original_diagnosis} | "
        f"After: {final_diagnosis}"
    )

    assert final_treatment == original_treatment, (
        f"{test_case_id} | STEP 7 FAILED | "
        "Hướng điều trị bị thay đổi trái phép. "
        f"Before: {original_treatment} | "
        f"After: {final_treatment}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=7,
        description=(
            "Chẩn đoán và Hướng điều trị không bị thay đổi "
            "sau khi Doctor B truy cập"
        )
    )

    # ============================================================
    # STEP 8
    # Kiểm tra hồ sơ vẫn thuộc Doctor A
    # và lịch vẫn Đã hoàn thành.
    # ============================================================

    final_patient = (
        owner_record_page.get_patient_name()
    )

    final_doctor = (
        owner_record_page.get_doctor_information()
    )

    assert final_patient == original_patient, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected patient: {original_patient} | "
        f"Actual: {final_patient}"
    )

    assert final_doctor == original_doctor, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected doctor: {original_doctor} | "
        f"Actual: {final_doctor}"
    )

    assert doctor_name in final_doctor, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected hồ sơ thuộc Doctor A: {doctor_name} | "
        f"Actual: {final_doctor}"
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
            f"vẫn thuộc Doctor A ({doctor_name}) "
            "và lịch vẫn ở trạng thái Đã hoàn thành"
        )
    )