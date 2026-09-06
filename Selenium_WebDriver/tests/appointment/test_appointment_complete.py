from pages.DoctorAppointmentPage import DoctorAppointmentPage
from pages.DoctorExaminationPage import DoctorExaminationPage
from pages.MedicalRecordPage import MedicalRecordPage

from utils.test_reporter import report_step

from tests.helpers.appointment_helpers import login_doctor
def test_tc_appointment_009_doctor_completes_appointment(
    driver,
    appointment_tc9_data
):
    """
    TC-APPOINTMENT-009:
    Kiểm tra bác sĩ lưu hồ sơ bệnh án thành công
    và hoàn thành lịch hẹn đã được xác nhận.
    """

    test_case_id = "TC-APPOINTMENT-009"

    appointment_id = appointment_tc9_data["appointment_id"]
    note = appointment_tc9_data["note"]
    diagnosis = appointment_tc9_data["diagnosis"]
    treatment = appointment_tc9_data["treatment"]

    # Step 1:
    login_doctor(driver)

    appointment_page = DoctorAppointmentPage(driver)
    appointment_page.open_page()

    assert appointment_page.get_note_by_id(
        appointment_id
    ) == note, (
        f"{test_case_id} | STEP 1 FAILED | "
        "Không tìm thấy đúng lịch hẹn"
    )

    assert appointment_page.get_status_by_id(
        appointment_id
    ) == "Đã xác nhận", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Lịch chưa ở trạng thái Đã xác nhận"
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập đúng bác sĩ và mở lịch hẹn đã được xác nhận"
    )

    # Step 2:
    assert appointment_page.is_examine_button_present(
        appointment_id
    ), (
        f"{test_case_id} | STEP 2 FAILED | "
        "Không tìm thấy nút Khám bệnh"
    )

    appointment_page.click_examine(
        appointment_id
    )

    examination_page = DoctorExaminationPage(driver)

    assert examination_page.get_page_title() == "Khám bệnh", (
        f"{test_case_id} | STEP 2 FAILED | "
        "Không mở đúng trang Khám bệnh"
    )

    assert f"appointmentId={appointment_id}" in driver.current_url, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"URL không chứa appointmentId={appointment_id}"
    )

    report_step(
        test_case_id,
        2,
        "Nhấn Khám bệnh và mở đúng trang khám của lịch hẹn"
    )

    # Step 3:
    assert examination_page.is_create_record_form_present(), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Không hiển thị form tạo hồ sơ bệnh án"
    )

    examination_page.enter_diagnosis(
        diagnosis
    )

    examination_page.enter_treatment(
        treatment
    )

    report_step(
        test_case_id,
        3,
        "Nhập Chẩn đoán và Hướng điều trị hợp lệ"
    )

    # Step 4:
    examination_page.click_save_medical_record()

    medical_record_page = MedicalRecordPage(driver)

    assert medical_record_page.get_page_title() == (
        "Chi tiết hồ sơ bệnh án"
    ), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Không mở đúng trang Chi tiết hồ sơ bệnh án"
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
        f"{test_case_id} | STEP 4 FAILED | "
        "Chẩn đoán vừa nhập chưa được lưu đúng"
    )

    assert treatment in actual_treatment, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Hướng điều trị vừa nhập chưa được lưu đúng"
    )

    report_step(
        test_case_id,
        4,
        "Lưu hồ sơ bệnh án thành công"
    )

    # Step 5:
    appointment_page.open_page()

    status_after = appointment_page.get_status_by_id(
        appointment_id
    )

    assert status_after == "Đã hoàn thành", (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: Đã hoàn thành | "
        f"Actual: {status_after}"
    )

    assert not appointment_page.is_examine_button_present(
        appointment_id
    ), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Lịch đã hoàn thành vẫn còn nút Khám bệnh"
    )

    report_step(
        test_case_id,
        5,
        "Lịch chuyển sang Đã hoàn thành và không còn nút Khám bệnh"
    )

    # Step 6:
    medical_record_page.open_page(
        appointment_id
    )

    assert diagnosis in (
        medical_record_page
        .get_diagnosis_information()
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Không hiển thị lại đúng Chẩn đoán"
    )

    assert treatment in (
        medical_record_page
        .get_treatment_information()
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Không hiển thị lại đúng Hướng điều trị"
    )

    report_step(
        test_case_id,
        6,
        "Mở lại hồ sơ và hiển thị đúng Chẩn đoán, Hướng điều trị đã lưu"
    )