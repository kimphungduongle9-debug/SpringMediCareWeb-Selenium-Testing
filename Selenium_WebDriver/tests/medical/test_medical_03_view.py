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
# TC-MEDICAL-005
# ============================================================

def test_tc_medical_005_view_medical_record(driver):
    """
    TC-MEDICAL-005:
    Kiểm tra bác sĩ có thể xem đúng hồ sơ bệnh án
    của lịch hẹn đã hoàn thành.
    """

    test_case_id = "TC-MEDICAL-005"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra bác sĩ xem đúng hồ sơ bệnh án "
        "của lịch hẹn đã hoàn thành"
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
    patient_name = test_data["patient_name"]
    doctor_name = test_data["doctor_name"]
    diagnosis = test_data["diagnosis"]
    treatment = test_data["treatment"]

    medical_record_api = MedicalRecordApi()

    # ============================================================
    # STEP 1:
    # Chuẩn bị lịch Đã hoàn thành
    # và đã có hồ sơ bệnh án.
    # ============================================================

    appointment_id = prepare_completed_medical_record(
        medical_record_api=medical_record_api,
        patient_id=patient_id,
        doctor_id=doctor_id,
        note=note,
        diagnosis=diagnosis,
        treatment=treatment,
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
    # và tìm đúng lịch.
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

    actual_status = (
        appointment_page
        .get_status_by_id(
            appointment_id
        )
    )

    assert actual_status == "Đã hoàn thành", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected status: Đã hoàn thành | "
        f"Actual: {actual_status}"
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
    # Kiểm tra lịch có nút Xem hồ sơ.
    # ============================================================

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

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            f"Appointment #{appointment_id} "
            "có nút Xem hồ sơ"
        )
    )

    # ============================================================
    # STEP 5:
    # Nhấn Xem hồ sơ.
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

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            "Nhấn Xem hồ sơ và mở thành công "
            "trang Chi tiết hồ sơ bệnh án"
        )
    )

    # ============================================================
    # STEP 6:
    # Kiểm tra appointmentId,
    # bệnh nhân và bác sĩ phụ trách.
    # ============================================================

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected URL chứa appointmentId="
        f"{appointment_id} | "
        f"Actual URL: {driver.current_url}"
    )

    actual_patient_name = (
        medical_record_page
        .get_patient_name()
    )

    assert actual_patient_name == patient_name, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected patient: {patient_name} | "
        f"Actual: {actual_patient_name}"
    )

    actual_doctor_information = (
        medical_record_page
        .get_doctor_information()
    )

    assert (
        doctor_name
        in actual_doctor_information
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected doctor chứa: {doctor_name} | "
        f"Actual: {actual_doctor_information}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            f"Hồ sơ gắn đúng appointment #{appointment_id}, "
            f"bệnh nhân {patient_name} "
            f"và bác sĩ {doctor_name}"
        )
    )

    # ============================================================
    # STEP 7:
    # Kiểm tra Chẩn đoán và Hướng điều trị
    # khớp với dữ liệu đã lưu.
    # ============================================================

    actual_diagnosis = (
        medical_record_page
        .get_diagnosis_information()
    )

    actual_treatment = (
        medical_record_page
        .get_treatment_information()
    )

    assert diagnosis in actual_diagnosis, (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected diagnosis chứa: {diagnosis} | "
        f"Actual: {actual_diagnosis}"
    )

    assert treatment in actual_treatment, (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected treatment chứa: {treatment} | "
        f"Actual: {actual_treatment}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=7,
        description=(
            "Chẩn đoán và Hướng điều trị "
            "hiển thị đúng dữ liệu đã lưu"
        )
    )

    # ============================================================
    # STEP 8:
    # Kiểm tra thao tác xem hồ sơ
    # không làm thay đổi dữ liệu hoặc trạng thái lịch.
    # ============================================================

    # Mở lại chính hồ sơ đó.
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

    assert (
        final_diagnosis
        == actual_diagnosis
    ), (
        f"{test_case_id} | STEP 8 FAILED | "
        "Chẩn đoán bị thay đổi sau thao tác xem. "
        f"Before: {actual_diagnosis} | "
        f"After: {final_diagnosis}"
    )

    assert (
        final_treatment
        == actual_treatment
    ), (
        f"{test_case_id} | STEP 8 FAILED | "
        "Hướng điều trị bị thay đổi sau thao tác xem. "
        f"Before: {actual_treatment} | "
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
            "Thao tác xem hồ sơ không làm thay đổi "
            "dữ liệu và lịch vẫn ở trạng thái "
            "Đã hoàn thành"
        )
    )