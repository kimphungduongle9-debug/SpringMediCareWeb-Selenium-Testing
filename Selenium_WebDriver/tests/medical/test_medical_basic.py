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

def test_tc_medical_001_create_medical_record(driver):
    """
    TC-MEDICAL-001:
    Kiểm tra bác sĩ tạo hồ sơ bệnh án thành công
    cho lịch hẹn đã được xác nhận.
    """

    test_case_id = "TC-MEDICAL-001"

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
    # Chuẩn bị một lịch hẹn Đã xác nhận,
    # chưa có hồ sơ bệnh án và ghi nhận thông tin lịch.
    # ============================================================

    appointment_id = (
        medical_record_api
        .prepare_confirmed_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes=note
        )
    )

    medical_record_api.assert_appointment_status(
        doctor_id=doctor_id,
        appointment_id=appointment_id,
        expected_status="confirmed"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description=(
            f"Chuẩn bị appointment #{appointment_id} "
            "ở trạng thái Đã xác nhận và chưa có hồ sơ bệnh án"
        )
    )

    # ============================================================
    # Step 2:
    # Đăng nhập bằng bác sĩ phụ trách lịch hẹn.
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
    # Mở trang Lịch hẹn bệnh nhân và tìm đúng lịch đã chuẩn bị.
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
        "TC-MEDICAL-001 | STEP 3 FAILED | "
        f"Expected note: {note} | "
        f"Actual: {actual_note}"
    )

    actual_status = (
        appointment_page
        .get_status_by_id(
            appointment_id
        )
    )

    assert actual_status == "Đã xác nhận", (
        "TC-MEDICAL-001 | STEP 3 FAILED | "
        "Expected: Đã xác nhận | "
        f"Actual: {actual_status}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            f"Tìm đúng appointment #{appointment_id} "
            "ở trạng thái Đã xác nhận"
        )
    )

    # ============================================================
    # Step 4:
    # Nhấn Khám bệnh.
    # ============================================================

    assert (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    ), (
        "TC-MEDICAL-001 | STEP 4 FAILED | "
        "Không tìm thấy nút Khám bệnh."
    )

    appointment_page.click_examine(
        appointment_id
    )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            f"Nhấn Khám bệnh cho appointment "
            f"#{appointment_id} thành công"
        )
    )

    # ============================================================
    # Step 5:
    # Kiểm tra trang Khám bệnh được mở đúng cho lịch hẹn.
    # ============================================================

    examination_page = DoctorExaminationPage(driver)

    page_title = (
        examination_page
        .get_page_title()
    )

    assert page_title == "Khám bệnh", (
        "TC-MEDICAL-001 | STEP 5 FAILED | "
        "Expected: Khám bệnh | "
        f"Actual: {page_title}"
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        "TC-MEDICAL-001 | STEP 5 FAILED | "
        f"URL không chứa appointmentId={appointment_id}. "
        f"Actual URL: {driver.current_url}"
    )

    assert (
        examination_page
        .is_appointment_information_present()
    ), (
        "TC-MEDICAL-001 | STEP 5 FAILED | "
        "Không hiển thị thông tin lịch hẹn."
    )

    assert (
        examination_page
        .is_create_record_form_present()
    ), (
        "TC-MEDICAL-001 | STEP 5 FAILED | "
        "Không tìm thấy form ghi nhận kết quả khám."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            f"Mở đúng trang Khám bệnh của appointment "
            f"#{appointment_id}"
        )
    )

    # ============================================================
    # Step 6:
    # Nhập Chẩn đoán và Hướng điều trị hợp lệ.
    # ============================================================

    examination_page.enter_diagnosis(
        diagnosis
    )

    examination_page.enter_treatment(
        treatment
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            "Nhập Chẩn đoán và Hướng điều trị hợp lệ"
        )
    )

    # ============================================================
    # Step 7:
    # Nhấn Lưu hồ sơ bệnh án.
    # ============================================================

    examination_page.click_save_medical_record()

    medical_record_page = MedicalRecordPage(driver)

    record_page_title = (
        medical_record_page
        .get_page_title()
    )

    assert record_page_title == "Chi tiết hồ sơ bệnh án", (
        "TC-MEDICAL-001 | STEP 7 FAILED | "
        "Expected: Chi tiết hồ sơ bệnh án | "
        f"Actual: {record_page_title}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=7,
        description=(
            "Lưu hồ sơ bệnh án thành công"
        )
    )

    # ============================================================
    # Step 8:
    # Kiểm tra hồ sơ được tạo đúng và
    # lịch hẹn chuyển sang Đã hoàn thành.
    # ============================================================

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        "TC-MEDICAL-001 | STEP 8 FAILED | "
        f"URL không chứa appointmentId={appointment_id}. "
        f"Actual URL: {driver.current_url}"
    )

    actual_diagnosis = (
        medical_record_page
        .get_diagnosis_information()
    )

    assert diagnosis in actual_diagnosis, (
        "TC-MEDICAL-001 | STEP 8 FAILED | "
        f"Expected diagnosis chứa: {diagnosis} | "
        f"Actual: {actual_diagnosis}"
    )

    actual_treatment = (
        medical_record_page
        .get_treatment_information()
    )

    assert treatment in actual_treatment, (
        "TC-MEDICAL-001 | STEP 8 FAILED | "
        f"Expected treatment chứa: {treatment} | "
        f"Actual: {actual_treatment}"
    )

    medical_record_api.assert_appointment_status(
        doctor_id=doctor_id,
        appointment_id=appointment_id,
        expected_status="completed"
    )

    appointment_page.open_page()

    final_status = (
        appointment_page
        .get_status_by_id(
            appointment_id
        )
    )

    assert final_status == "Đã hoàn thành", (
        "TC-MEDICAL-001 | STEP 8 FAILED | "
        "Expected: Đã hoàn thành | "
        f"Actual: {final_status}"
    )

    assert (
        appointment_page
        .is_view_medical_record_button_present_by_id(
            appointment_id
        )
    ), (
        "TC-MEDICAL-001 | STEP 8 FAILED | "
        "Không tìm thấy nút Xem hồ sơ."
    )

    assert not (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    ), (
        "TC-MEDICAL-001 | STEP 8 FAILED | "
        "Nút Khám bệnh vẫn còn hiển thị "
        "sau khi lịch đã hoàn thành."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=8,
        description=(
            f"Hồ sơ appointment #{appointment_id} được tạo đúng "
            "và lịch chuyển sang Đã hoàn thành"
        )
    )

def test_tc_medical_002_blank_diagnosis(driver):
    """
    TC-MEDICAL-002:
    Kiểm tra không thể tạo hồ sơ bệnh án
    khi bỏ trống Chẩn đoán.
    """

    test_case_id = "TC-MEDICAL-002"

    test_data = get_test_data_csv(
        MEDICAL_TEST_DATA_CSV,
        test_case_id
    )

    patient_id = int(test_data["patient_id"])
    doctor_id = int(test_data["doctor_id"])

    note = test_data["note"]
    treatment = test_data["treatment"]

    medical_record_api = MedicalRecordApi()

    # ============================================================
    # Step 1:
    # Chuẩn bị lịch hẹn Đã xác nhận,
    # chưa có hồ sơ bệnh án.
    # ============================================================

    appointment_id = (
        medical_record_api
        .prepare_confirmed_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes=note
        )
    )

    medical_record_api.assert_appointment_status(
        doctor_id=doctor_id,
        appointment_id=appointment_id,
        expected_status="confirmed"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description=(
            f"Chuẩn bị appointment #{appointment_id} "
            "ở trạng thái Đã xác nhận và chưa có hồ sơ bệnh án"
        )
    )

    # ============================================================
    # Step 2:
    # Đăng nhập bác sĩ phụ trách và mở trang Khám bệnh.
    # ============================================================

    login_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    appointment_page = DoctorAppointmentPage(driver)

    appointment_page.open_page()

    assert appointment_page.get_note_by_id(
        appointment_id
    ) == note, (
        "TC-MEDICAL-002 | STEP 2 FAILED | "
        f"Không tìm thấy đúng appointment #{appointment_id}."
    )

    assert appointment_page.is_examine_button_present(
        appointment_id
    ), (
        "TC-MEDICAL-002 | STEP 2 FAILED | "
        "Không tìm thấy nút Khám bệnh."
    )

    appointment_page.click_examine(
        appointment_id
    )

    examination_page = DoctorExaminationPage(driver)

    assert examination_page.get_page_title() == "Khám bệnh", (
        "TC-MEDICAL-002 | STEP 2 FAILED | "
        "Không mở được trang Khám bệnh."
    )

    assert f"appointmentId={appointment_id}" in driver.current_url, (
        "TC-MEDICAL-002 | STEP 2 FAILED | "
        f"URL không chứa appointmentId={appointment_id}. "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description=(
            f"Đăng nhập bác sĩ phụ trách và mở trang Khám bệnh "
            f"của appointment #{appointment_id}"
        )
    )

    # ============================================================
    # Step 3:
    # Để trống Chẩn đoán và nhập Hướng điều trị hợp lệ.
    # ============================================================

    examination_page.enter_diagnosis("")
    examination_page.enter_treatment(
        treatment
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            "Để trống Chẩn đoán và nhập Hướng điều trị hợp lệ"
        )
    )

    # ============================================================
    # Step 4:
    # Nhấn Lưu hồ sơ bệnh án.
    # ============================================================

    examination_page.click_save_medical_record()

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description="Nhấn Lưu hồ sơ bệnh án"
    )

    # ============================================================
    # Step 5:
    # Kiểm tra thông báo validation cho dữ liệu thiếu.
    # ============================================================

    validation_message = (
        examination_page
        .get_validation_message()
    )

    expected_message = (
        "Vui lòng nhập đầy đủ chẩn đoán và hướng điều trị."
    )

    assert validation_message == expected_message, (
        "TC-MEDICAL-002 | STEP 5 FAILED | "
        f"Expected: {expected_message} | "
        f"Actual: {validation_message}"
    )

    assert examination_page.is_create_record_form_present(), (
        "TC-MEDICAL-002 | STEP 5 FAILED | "
        "Form tạo hồ sơ bệnh án không còn hiển thị."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            "Hiển thị đúng thông báo yêu cầu nhập đầy đủ "
            "Chẩn đoán và Hướng điều trị"
        )
    )

    # ============================================================
    # Step 6:
    # Kiểm tra hồ sơ không được tạo và
    # lịch hẹn vẫn ở trạng thái Đã xác nhận.
    # ============================================================

    medical_record_api.assert_appointment_status(
        doctor_id=doctor_id,
        appointment_id=appointment_id,
        expected_status="confirmed"
    )

    appointment_page.open_page()

    final_status = (
        appointment_page
        .get_status_by_id(
            appointment_id
        )
    )

    assert final_status == "Đã xác nhận", (
        "TC-MEDICAL-002 | STEP 6 FAILED | "
        "Expected: Đã xác nhận | "
        f"Actual: {final_status}"
    )

    assert appointment_page.is_examine_button_present(
        appointment_id
    ), (
        "TC-MEDICAL-002 | STEP 6 FAILED | "
        "Expected: Nút Khám bệnh vẫn được hiển thị."
    )

    assert not (
        appointment_page
        .is_view_medical_record_button_present_by_id(
            appointment_id
        )
    ), (
        "TC-MEDICAL-002 | STEP 6 FAILED | "
        "Hồ sơ bệnh án đã được tạo dù Chẩn đoán bị bỏ trống."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            f"Không tạo hồ sơ bệnh án và appointment "
            f"#{appointment_id} vẫn ở trạng thái Đã xác nhận"
        )
    )

# ============================================================
# TC-MEDICAL-003
# ============================================================

def test_tc_medical_003_blank_treatment(driver):
    """
    TC-MEDICAL-003:
    Kiểm tra không thể tạo hồ sơ bệnh án
    khi bỏ trống Hướng điều trị.
    """

    test_case_id = "TC-MEDICAL-003"

    test_data = get_test_data_csv(
        MEDICAL_TEST_DATA_CSV,
        test_case_id
    )

    patient_id = int(test_data["patient_id"])
    doctor_id = int(test_data["doctor_id"])

    note = test_data["note"]
    diagnosis = test_data["diagnosis"]

    medical_record_api = MedicalRecordApi()

    # ============================================================
    # Step 1:
    # Chuẩn bị lịch hẹn Đã xác nhận,
    # chưa có hồ sơ bệnh án.
    # ============================================================

    appointment_id = (
        medical_record_api
        .prepare_confirmed_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes=note
        )
    )

    medical_record_api.assert_appointment_status(
        doctor_id=doctor_id,
        appointment_id=appointment_id,
        expected_status="confirmed"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description=(
            f"Chuẩn bị appointment #{appointment_id} "
            "ở trạng thái Đã xác nhận và chưa có hồ sơ bệnh án"
        )
    )

    # ============================================================
    # Step 2:
    # Đăng nhập bác sĩ phụ trách và mở trang Khám bệnh.
    # ============================================================

    login_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    appointment_page = DoctorAppointmentPage(driver)

    appointment_page.open_page()

    actual_note = (
        appointment_page
        .get_note_by_id(
            appointment_id
        )
    )

    assert actual_note == note, (
        "TC-MEDICAL-003 | STEP 2 FAILED | "
        f"Expected note: {note} | "
        f"Actual: {actual_note}"
    )

    actual_status = (
        appointment_page
        .get_status_by_id(
            appointment_id
        )
    )

    assert actual_status == "Đã xác nhận", (
        "TC-MEDICAL-003 | STEP 2 FAILED | "
        "Expected: Đã xác nhận | "
        f"Actual: {actual_status}"
    )

    assert (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    ), (
        "TC-MEDICAL-003 | STEP 2 FAILED | "
        "Không tìm thấy nút Khám bệnh."
    )

    appointment_page.click_examine(
        appointment_id
    )

    examination_page = DoctorExaminationPage(driver)

    page_title = (
        examination_page
        .get_page_title()
    )

    assert page_title == "Khám bệnh", (
        "TC-MEDICAL-003 | STEP 2 FAILED | "
        "Expected: Khám bệnh | "
        f"Actual: {page_title}"
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        "TC-MEDICAL-003 | STEP 2 FAILED | "
        f"URL không chứa appointmentId={appointment_id}. "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description=(
            f"Đăng nhập bác sĩ phụ trách và mở trang Khám bệnh "
            f"của appointment #{appointment_id}"
        )
    )

    # ============================================================
    # Step 3:
    # Nhập Chẩn đoán hợp lệ và để trống Hướng điều trị.
    # ============================================================

    examination_page.enter_diagnosis(
        diagnosis
    )

    examination_page.enter_treatment("")

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            "Nhập Chẩn đoán hợp lệ và để trống Hướng điều trị"
        )
    )

    # ============================================================
    # Step 4:
    # Nhấn Lưu hồ sơ bệnh án.
    # ============================================================

    examination_page.click_save_medical_record()

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description="Nhấn Lưu hồ sơ bệnh án"
    )

    # ============================================================
    # Step 5:
    # Kiểm tra thông báo validation cho dữ liệu thiếu.
    # ============================================================

    validation_message = (
        examination_page
        .get_validation_message()
    )

    expected_message = (
        "Vui lòng nhập đầy đủ chẩn đoán và hướng điều trị."
    )

    assert validation_message == expected_message, (
        "TC-MEDICAL-003 | STEP 5 FAILED | "
        f"Expected: {expected_message} | "
        f"Actual: {validation_message}"
    )

    assert (
        examination_page
        .is_create_record_form_present()
    ), (
        "TC-MEDICAL-003 | STEP 5 FAILED | "
        "Form tạo hồ sơ bệnh án không còn hiển thị."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            "Hiển thị đúng thông báo yêu cầu nhập đầy đủ "
            "Chẩn đoán và Hướng điều trị"
        )
    )

    # ============================================================
    # Step 6:
    # Kiểm tra hồ sơ không được tạo và
    # lịch hẹn vẫn ở trạng thái Đã xác nhận.
    # ============================================================

    medical_record_api.assert_appointment_status(
        doctor_id=doctor_id,
        appointment_id=appointment_id,
        expected_status="confirmed"
    )

    appointment_page.open_page()

    final_status = (
        appointment_page
        .get_status_by_id(
            appointment_id
        )
    )

    assert final_status == "Đã xác nhận", (
        "TC-MEDICAL-003 | STEP 6 FAILED | "
        "Expected: Đã xác nhận | "
        f"Actual: {final_status}"
    )

    assert (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    ), (
        "TC-MEDICAL-003 | STEP 6 FAILED | "
        "Expected: Nút Khám bệnh vẫn được hiển thị."
    )

    assert not (
        appointment_page
        .is_view_medical_record_button_present_by_id(
            appointment_id
        )
    ), (
        "TC-MEDICAL-003 | STEP 6 FAILED | "
        "Hồ sơ bệnh án đã được tạo dù Hướng điều trị bị bỏ trống."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            f"Không tạo hồ sơ bệnh án và appointment "
            f"#{appointment_id} vẫn ở trạng thái Đã xác nhận"
        )
    )