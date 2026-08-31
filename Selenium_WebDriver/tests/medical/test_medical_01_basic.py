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

from tests.helpers.medical_helpers import (
    get_or_create_medical_booking_slot,
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


def prepare_confirmed_appointment(
    medical_record_api,
    patient_id,
    doctor_id,
    note,
    test_data,
    test_case_id
):
    """
    Chuẩn bị appointment ở trạng thái confirmed.

    Nếu DB không còn schedule/slot hợp lệ:
    - tự tạo schedule test mới
    - sau đó thử tạo appointment lại.
    """

    try:
        return (
            medical_record_api
            .prepare_confirmed_appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                notes=note
            )
        )

    except AssertionError as error:
        setup_error = str(error)

        allowed_setup_errors = (
            "Không tìm thấy ca làm việc available",
            "Không tìm thấy giờ đặt lịch còn trống",
        )

        if not any(
            message in setup_error
            for message in allowed_setup_errors
        ):
            raise AssertionError(
                f"{test_case_id} | STEP 1 FAILED | "
                "Không thể chuẩn bị appointment. "
                f"Actual: {setup_error}"
            ) from error

        # DB hết slot -> tự tạo schedule test.
        get_or_create_medical_booking_slot(
            doctor_id=doctor_id,
            test_data=test_data,
            schedule_note=(
                f"{test_case_id}-AUTO-SCHEDULE"
            )
        )

        try:
            return (
                medical_record_api
                .prepare_confirmed_appointment(
                    patient_id=patient_id,
                    doctor_id=doctor_id,
                    notes=note
                )
            )

        except AssertionError as retry_error:
            raise AssertionError(
                f"{test_case_id} | STEP 1 FAILED | "
                "Đã tự tạo schedule nhưng vẫn không thể "
                "chuẩn bị appointment Đã xác nhận. "
                f"Actual: {retry_error}"
            ) from retry_error


# ============================================================
# TC-MEDICAL-001
# ============================================================

def test_tc_medical_001_create_medical_record(driver):
    """
    TC-MEDICAL-001:
    Kiểm tra bác sĩ có thể tạo hồ sơ bệnh án thành công
    cho lịch hẹn đã được xác nhận.
    """

    test_case_id = "TC-MEDICAL-001"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra tạo hồ sơ bệnh án thành công "
        "cho lịch hẹn đã xác nhận"
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
    # Step 1:
    # Chuẩn bị một lịch hẹn Đã xác nhận
    # và chưa có hồ sơ bệnh án.
    # ============================================================

    appointment_id = prepare_confirmed_appointment(
        medical_record_api=medical_record_api,
        patient_id=patient_id,
        doctor_id=doctor_id,
        note=note,
        test_data=test_data,
        test_case_id=test_case_id
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
            "ở trạng thái Đã xác nhận và "
            "chưa có hồ sơ bệnh án"
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
            "Đăng nhập bằng tài khoản "
            "bác sĩ phụ trách thành công"
        )
    )

    # ============================================================
    # Step 3:
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
    # Step 4:
    # Kiểm tra lịch ở trạng thái Đã xác nhận
    # và có nút Khám bệnh.
    # ============================================================

    actual_status = (
        appointment_page
        .get_status_by_id(
            appointment_id
        )
    )

    assert actual_status == "Đã xác nhận", (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected status: Đã xác nhận | "
        f"Actual: {actual_status}"
    )

    assert (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    ), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Có nút Khám bệnh | "
        "Actual: Không tìm thấy nút Khám bệnh."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            f"Appointment #{appointment_id} "
            "ở trạng thái Đã xác nhận "
            "và có nút Khám bệnh"
        )
    )

    # ============================================================
    # Step 5:
    # Nhấn Khám bệnh.
    # ============================================================

    appointment_page.click_examine(
        appointment_id
    )

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            f"Nhấn Khám bệnh cho appointment "
            f"#{appointment_id} thành công"
        )
    )

    # ============================================================
    # Step 6:
    # Kiểm tra trang Khám bệnh
    # được mở đúng cho lịch hẹn.
    # ============================================================

    examination_page = DoctorExaminationPage(
        driver
    )

    page_title = (
        examination_page
        .get_page_title()
    )

    assert page_title == "Khám bệnh", (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected page title: Khám bệnh | "
        f"Actual: {page_title}"
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected URL chứa appointmentId="
        f"{appointment_id} | "
        f"Actual URL: {driver.current_url}"
    )

    assert (
        examination_page
        .is_appointment_information_present()
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: Hiển thị thông tin lịch hẹn | "
        "Actual: Không tìm thấy thông tin lịch hẹn."
    )

    assert (
        examination_page
        .is_create_record_form_present()
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: Hiển thị form ghi nhận "
        "kết quả khám | "
        "Actual: Không tìm thấy form."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            "Mở đúng trang Khám bệnh của "
            f"appointment #{appointment_id}"
        )
    )

    # ============================================================
    # Step 7:
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
        step_number=7,
        description=(
            "Nhập Chẩn đoán và "
            "Hướng điều trị hợp lệ"
        )
    )

    # ============================================================
    # Step 8:
    # Nhấn Lưu hồ sơ bệnh án.
    # ============================================================

    examination_page.click_save_medical_record()

    medical_record_page = MedicalRecordPage(
        driver
    )

    record_page_title = (
        medical_record_page
        .get_page_title()
    )

    assert (
        record_page_title
        == "Chi tiết hồ sơ bệnh án"
    ), (
        f"{test_case_id} | STEP 8 FAILED | "
        "Expected: Chi tiết hồ sơ bệnh án | "
        f"Actual: {record_page_title}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=8,
        description=(
            "Nhấn Lưu hồ sơ bệnh án "
            "và hệ thống mở trang "
            "Chi tiết hồ sơ bệnh án"
        )
    )

    # ============================================================
    # Step 9:
    # Kiểm tra hồ sơ được tạo đúng
    # và lịch chuyển sang Đã hoàn thành.
    # ============================================================

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected URL chứa appointmentId="
        f"{appointment_id} | "
        f"Actual URL: {driver.current_url}"
    )

    actual_diagnosis = (
        medical_record_page
        .get_diagnosis_information()
    )

    assert diagnosis in actual_diagnosis, (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected diagnosis chứa: "
        f"{diagnosis} | "
        f"Actual: {actual_diagnosis}"
    )

    actual_treatment = (
        medical_record_page
        .get_treatment_information()
    )

    assert treatment in actual_treatment, (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected treatment chứa: "
        f"{treatment} | "
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
        f"{test_case_id} | STEP 9 FAILED | "
        "Expected status: Đã hoàn thành | "
        f"Actual: {final_status}"
    )

    assert (
        appointment_page
        .is_view_medical_record_button_present_by_id(
            appointment_id
        )
    ), (
        f"{test_case_id} | STEP 9 FAILED | "
        "Expected: Có nút Xem hồ sơ | "
        "Actual: Không tìm thấy nút Xem hồ sơ."
    )

    assert not (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    ), (
        f"{test_case_id} | STEP 9 FAILED | "
        "Expected: Không còn nút Khám bệnh | "
        "Actual: Nút Khám bệnh vẫn còn hiển thị."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=9,
        description=(
            f"Hồ sơ appointment #{appointment_id} "
            "được tạo đúng, lịch chuyển sang "
            "Đã hoàn thành và nút Khám bệnh "
            "được thay bằng Xem hồ sơ"
        )
    )


# ============================================================
# TC-MEDICAL-002
# ============================================================

def test_tc_medical_002_blank_diagnosis(driver):
    """
    TC-MEDICAL-002:
    Kiểm tra hệ thống không cho phép
    tạo hồ sơ bệnh án khi bỏ trống Chẩn đoán.
    """

    test_case_id = "TC-MEDICAL-002"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra không thể tạo hồ sơ bệnh án "
        "khi bỏ trống Chẩn đoán"
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
    treatment = test_data["treatment"]

    medical_record_api = MedicalRecordApi()

    # ============================================================
    # Step 1:
    # Chuẩn bị lịch hẹn Đã xác nhận
    # và chưa có hồ sơ bệnh án.
    # ============================================================

    appointment_id = prepare_confirmed_appointment(
        medical_record_api=medical_record_api,
        patient_id=patient_id,
        doctor_id=doctor_id,
        note=note,
        test_data=test_data,
        test_case_id=test_case_id
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
            "ở trạng thái Đã xác nhận và "
            "chưa có hồ sơ bệnh án"
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
            "Đăng nhập bằng tài khoản "
            "bác sĩ phụ trách thành công"
        )
    )

    # ============================================================
    # Step 3:
    # Mở trang Khám bệnh của lịch đã chuẩn bị.
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

    assert actual_status == "Đã xác nhận", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected status: Đã xác nhận | "
        f"Actual: {actual_status}"
    )

    assert (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Có nút Khám bệnh | "
        "Actual: Không tìm thấy nút Khám bệnh."
    )

    appointment_page.click_examine(
        appointment_id
    )

    examination_page = DoctorExaminationPage(
        driver
    )

    page_title = (
        examination_page
        .get_page_title()
    )

    assert page_title == "Khám bệnh", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected page title: Khám bệnh | "
        f"Actual: {page_title}"
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected URL chứa appointmentId="
        f"{appointment_id} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            "Mở đúng trang Khám bệnh của "
            f"appointment #{appointment_id}"
        )
    )

    # ============================================================
    # Step 4:
    # Để trống Chẩn đoán
    # và nhập Hướng điều trị hợp lệ.
    # ============================================================

    examination_page.enter_diagnosis("")

    examination_page.enter_treatment(
        treatment
    )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            "Để trống Chẩn đoán "
            "và nhập Hướng điều trị hợp lệ"
        )
    )

    # ============================================================
    # Step 5:
    # Nhấn Lưu hồ sơ bệnh án.
    # ============================================================

    examination_page.click_save_medical_record()

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            "Nhấn Lưu hồ sơ bệnh án"
        )
    )

    # ============================================================
    # Step 6:
    # Kiểm tra thông báo validation.
    # ============================================================

    validation_message = (
        examination_page
        .get_validation_message()
    )

    expected_message = (
        "Vui lòng nhập đầy đủ chẩn đoán "
        "và hướng điều trị."
    )

    assert (
        validation_message
        == expected_message
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: {expected_message} | "
        f"Actual: {validation_message}"
    )

    assert (
        examination_page
        .is_create_record_form_present()
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: Form tạo hồ sơ vẫn hiển thị | "
        "Actual: Form không còn hiển thị."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            "Hiển thị đúng thông báo yêu cầu "
            "nhập đầy đủ Chẩn đoán "
            "và Hướng điều trị"
        )
    )

    # ============================================================
    # Step 7:
    # Kiểm tra hồ sơ không được tạo
    # và lịch vẫn Đã xác nhận.
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
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected status: Đã xác nhận | "
        f"Actual: {final_status}"
    )

    assert (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected: Nút Khám bệnh vẫn hiển thị | "
        "Actual: Không tìm thấy nút Khám bệnh."
    )

    assert not (
        appointment_page
        .is_view_medical_record_button_present_by_id(
            appointment_id
        )
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        "Hồ sơ bệnh án đã được tạo "
        "dù Chẩn đoán bị bỏ trống."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=7,
        description=(
            "Không tạo hồ sơ bệnh án và "
            f"appointment #{appointment_id} "
            "vẫn ở trạng thái Đã xác nhận"
        )
    )


# ============================================================
# TC-MEDICAL-003
# ============================================================

def test_tc_medical_003_blank_treatment(driver):
    """
    TC-MEDICAL-003:
    Kiểm tra hệ thống không cho phép
    tạo hồ sơ bệnh án khi bỏ trống Hướng điều trị.
    """

    test_case_id = "TC-MEDICAL-003"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra không thể tạo hồ sơ bệnh án "
        "khi bỏ trống Hướng điều trị"
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

    medical_record_api = MedicalRecordApi()

    # ============================================================
    # Step 1:
    # Chuẩn bị lịch hẹn Đã xác nhận
    # và chưa có hồ sơ bệnh án.
    # ============================================================

    appointment_id = prepare_confirmed_appointment(
        medical_record_api=medical_record_api,
        patient_id=patient_id,
        doctor_id=doctor_id,
        note=note,
        test_data=test_data,
        test_case_id=test_case_id
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
            "ở trạng thái Đã xác nhận và "
            "chưa có hồ sơ bệnh án"
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
            "Đăng nhập bằng tài khoản "
            "bác sĩ phụ trách thành công"
        )
    )

    # ============================================================
    # Step 3:
    # Mở trang Khám bệnh của lịch đã chuẩn bị.
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

    assert actual_status == "Đã xác nhận", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected status: Đã xác nhận | "
        f"Actual: {actual_status}"
    )

    assert (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Có nút Khám bệnh | "
        "Actual: Không tìm thấy nút Khám bệnh."
    )

    appointment_page.click_examine(
        appointment_id
    )

    examination_page = DoctorExaminationPage(
        driver
    )

    page_title = (
        examination_page
        .get_page_title()
    )

    assert page_title == "Khám bệnh", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected page title: Khám bệnh | "
        f"Actual: {page_title}"
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected URL chứa appointmentId="
        f"{appointment_id} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            "Mở đúng trang Khám bệnh của "
            f"appointment #{appointment_id}"
        )
    )

    # ============================================================
    # Step 4:
    # Nhập Chẩn đoán hợp lệ
    # và để trống Hướng điều trị.
    # ============================================================

    examination_page.enter_diagnosis(
        diagnosis
    )

    examination_page.enter_treatment("")

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            "Nhập Chẩn đoán hợp lệ "
            "và để trống Hướng điều trị"
        )
    )

    # ============================================================
    # Step 5:
    # Nhấn Lưu hồ sơ bệnh án.
    # ============================================================

    examination_page.click_save_medical_record()

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            "Nhấn Lưu hồ sơ bệnh án"
        )
    )

    # ============================================================
    # Step 6:
    # Kiểm tra thông báo validation.
    # ============================================================

    validation_message = (
        examination_page
        .get_validation_message()
    )

    expected_message = (
        "Vui lòng nhập đầy đủ chẩn đoán "
        "và hướng điều trị."
    )

    assert (
        validation_message
        == expected_message
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: {expected_message} | "
        f"Actual: {validation_message}"
    )

    assert (
        examination_page
        .is_create_record_form_present()
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: Form tạo hồ sơ vẫn hiển thị | "
        "Actual: Form không còn hiển thị."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            "Hiển thị đúng thông báo yêu cầu "
            "nhập đầy đủ Chẩn đoán "
            "và Hướng điều trị"
        )
    )

    # ============================================================
    # Step 7:
    # Kiểm tra hồ sơ không được tạo
    # và lịch vẫn Đã xác nhận.
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
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected status: Đã xác nhận | "
        f"Actual: {final_status}"
    )

    assert (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected: Nút Khám bệnh vẫn hiển thị | "
        "Actual: Không tìm thấy nút Khám bệnh."
    )

    assert not (
        appointment_page
        .is_view_medical_record_button_present_by_id(
            appointment_id
        )
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        "Hồ sơ bệnh án đã được tạo dù "
        "Hướng điều trị bị bỏ trống."
    )

    report_step(
        test_case_id=test_case_id,
        step_number=7,
        description=(
            "Không tạo hồ sơ bệnh án và "
            f"appointment #{appointment_id} "
            "vẫn ở trạng thái Đã xác nhận"
        )
    )