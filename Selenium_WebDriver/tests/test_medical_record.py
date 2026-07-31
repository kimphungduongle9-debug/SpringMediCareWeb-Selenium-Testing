import time

from pages.LoginPage import LoginPage
from pages.MedicalRecordPage import MedicalRecordPage
from pages.DoctorAppointmentPage import DoctorAppointmentPage
from pages.DoctorExaminationPage import DoctorExaminationPage

DOCTOR_USERNAME = "doctor_binh"
DOCTOR_PASSWORD = "Abc@123"

OWNER_DOCTOR_USERNAME = "doctor_minh"
OWNER_DOCTOR_PASSWORD = "Abc@123"

HOME_URL = "http://localhost:3000/"


def login_other_doctor(driver):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(DOCTOR_USERNAME,DOCTOR_PASSWORD)

    time.sleep(2)

    assert driver.current_url == HOME_URL

def login_owner_doctor(driver):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(OWNER_DOCTOR_USERNAME,OWNER_DOCTOR_PASSWORD)

    time.sleep(2)

    assert driver.current_url == HOME_URL

def test_other_doctor_cannot_view_medical_record(
        driver,
        medical_record_tc7_data):
    """
    TC-MEDICAL-007:
    Bác sĩ không được xem hồ sơ bệnh án
    không thuộc mình.
    """

    login_other_doctor(driver)
    medical_record_page = MedicalRecordPage(driver)
    medical_record_page.open_page(medical_record_tc7_data)
    message = (medical_record_page.get_access_denied_message())
    assert message == ("Bạn không có quyền xem "
        "hồ sơ bệnh án này."
    )
    assert not (medical_record_page.is_medical_record_information_present())
    assert not (medical_record_page.is_edit_button_present())

def test_owner_doctor_can_view_medical_record_from_appointment_list(
        driver,
        medical_record_tc5_data):
    """
    TC-MEDICAL-005:
    Đúng bác sĩ xem được hồ sơ bệnh án
    từ danh sách lịch hẹn đã hoàn thành.
    """

    login_owner_doctor(driver)

    appointment_page = DoctorAppointmentPage(driver)

    appointment_page.open_page()

    note = medical_record_tc5_data["note"]

    assert ( appointment_page.get_patient_name_by_note(note)== medical_record_tc5_data["patient_name"])

    assert (appointment_page.get_status_by_note(note)== "Đã hoàn thành")

    assert (appointment_page.is_view_medical_record_button_present(note))

    appointment_page.click_view_medical_record(note)

    medical_record_page = MedicalRecordPage(driver)

    assert (medical_record_page.get_page_title()== "Chi tiết hồ sơ bệnh án")

    assert (f"appointmentId="f"{medical_record_tc5_data['appointment_id']}"in driver.current_url)

    assert (medical_record_page.get_patient_name()== medical_record_tc5_data["patient_name"])

    assert medical_record_tc5_data["doctor_name"] in medical_record_page.get_doctor_information()

    assert medical_record_tc5_data["diagnosis"] in medical_record_page.get_diagnosis_information()

    assert medical_record_tc5_data["treatment"] in medical_record_page.get_treatment_information()

    assert (medical_record_page.is_medical_record_information_present())

    assert (medical_record_page.is_edit_button_present())

def test_owner_doctor_can_update_medical_record(
        driver,
        medical_record_tc6_data):
    """
    TC-MEDICAL-006:
    Đúng bác sĩ cập nhật được hồ sơ bệnh án
    của lịch hẹn thuộc mình.
    """

    login_owner_doctor(driver)

    appointment_page = DoctorAppointmentPage(driver)
    appointment_page.open_page()

    note = medical_record_tc6_data["note"]

    assert (appointment_page.get_status_by_note(note)== "Đã hoàn thành")

    assert (appointment_page.is_view_medical_record_button_present(note))

    appointment_page.click_view_medical_record(note)

    medical_record_page = MedicalRecordPage(driver)

    assert (
        f"appointmentId="
        f"{medical_record_tc6_data['appointment_id']}"
        in driver.current_url
    )

    medical_record_page.click_edit_button()

    assert (medical_record_page.is_edit_form_present())

    update_time = str(int(time.time()))

    new_diagnosis = (
            "Chẩn đoán cập nhật TC-MEDICAL-006 "
            + update_time
    )

    new_treatment = (
            "Hướng điều trị cập nhật TC-MEDICAL-006 "
            + update_time
    )

    medical_record_page.enter_diagnosis(
        new_diagnosis
    )

    medical_record_page.enter_treatment(
        new_treatment
    )

    medical_record_page.click_save_changes()

    assert (
        medical_record_page
        .get_update_success_message()
        == "Cập nhật hồ sơ bệnh án thành công."
    )

    assert not (medical_record_page.is_edit_form_present())

    assert new_diagnosis in (
        medical_record_page
        .get_diagnosis_information()
    )

    assert new_treatment in (
        medical_record_page
        .get_treatment_information()
    )
    assert (medical_record_page.is_edit_button_present())

def test_cancel_update_keeps_old_medical_record_data(
        driver,
        medical_record_tc9_data):
    """
    TC-MEDICAL-009:
    Nhấn Hủy khi cập nhật thì dữ liệu cũ
    của hồ sơ bệnh án vẫn được giữ nguyên.
    """

    login_owner_doctor(driver)

    appointment_page = DoctorAppointmentPage(
        driver
    )
    appointment_page.open_page()

    note = medical_record_tc9_data["note"]

    assert (
        appointment_page.get_status_by_note(note)
        == "Đã hoàn thành"
    )

    appointment_page.click_view_medical_record(
        note
    )

    medical_record_page = MedicalRecordPage(
        driver
    )

    assert (
        f"appointmentId="
        f"{medical_record_tc9_data['appointment_id']}"
        in driver.current_url
    )

    medical_record_page.click_edit_button()

    assert (
        medical_record_page.is_edit_form_present()
    )

    old_diagnosis = (
        medical_record_page
        .get_diagnosis_input_value()
    )

    old_treatment = (
        medical_record_page
        .get_treatment_input_value()
    )

    update_time = str(int(time.time()))

    new_diagnosis = (
        "Chẩn đoán không lưu TC-MEDICAL-009 "
        + update_time
    )

    new_treatment = (
        "Hướng điều trị không lưu TC-MEDICAL-009 "
        + update_time
    )

    medical_record_page.enter_diagnosis(
        new_diagnosis
    )

    medical_record_page.enter_treatment(
        new_treatment
    )

    assert (
        medical_record_page
        .get_diagnosis_input_value()
        == new_diagnosis
    )

    assert (
        medical_record_page
        .get_treatment_input_value()
        == new_treatment
    )

    medical_record_page.click_cancel_edit()

    assert not (
        medical_record_page.is_edit_form_present()
    )

    assert old_diagnosis in (
        medical_record_page
        .get_diagnosis_information()
    )

    assert old_treatment in (
        medical_record_page
        .get_treatment_information()
    )

    assert new_diagnosis not in (
        medical_record_page
        .get_diagnosis_information()
    )

    assert new_treatment not in (
        medical_record_page
        .get_treatment_information()
    )

def test_doctor_creates_medical_record_with_valid_data(
        driver,
        medical_record_tc1_data):
    """
    TC-MEDICAL-001:
    Bác sĩ tạo hồ sơ bệnh án
    với dữ liệu hợp lệ.
    """

    login_owner_doctor(driver)

    appointment_page = DoctorAppointmentPage(
        driver
    )
    appointment_page.open_page()

    appointment_id = (
        medical_record_tc1_data[
            "appointment_id"
        ]
    )

    assert (
        appointment_page.get_note_by_id(
            appointment_id
        )
        == medical_record_tc1_data["note"]
    )

    assert (
        appointment_page.get_status_by_id(
            appointment_id
        )
        == "Đã xác nhận"
    )

    assert (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    )

    appointment_page.click_examine(
        appointment_id
    )

    examination_page = DoctorExaminationPage(
        driver
    )

    assert (
        examination_page.get_page_title()
        == "Khám bệnh"
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    )

    assert (
        examination_page
        .is_appointment_information_present()
    )

    assert (
        examination_page
        .is_create_record_form_present()
    )

    examination_page.enter_diagnosis(
        medical_record_tc1_data[
            "diagnosis"
        ]
    )

    examination_page.enter_treatment(
        medical_record_tc1_data[
            "treatment"
        ]
    )

    examination_page.click_save_medical_record()

    medical_record_page = MedicalRecordPage(
        driver
    )

    assert (
        medical_record_page.get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    )

    assert (
        medical_record_tc1_data["diagnosis"]
        in medical_record_page
        .get_diagnosis_information()
    )

    assert (
        medical_record_tc1_data["treatment"]
        in medical_record_page
        .get_treatment_information()
    )

    assert (
        medical_record_page
        .is_edit_button_present()
    )

def test_create_medical_record_with_blank_diagnosis(
        driver,
        medical_record_tc2_data):
    """
    TC-MEDICAL-002:
    Không tạo hồ sơ bệnh án khi
    bỏ trống chẩn đoán.
    """

    login_owner_doctor(driver)

    appointment_page = DoctorAppointmentPage(
        driver
    )
    appointment_page.open_page()

    appointment_id = (
        medical_record_tc2_data[
            "appointment_id"
        ]
    )

    assert (
        appointment_page.get_note_by_id(
            appointment_id
        )
        == medical_record_tc2_data["note"]
    )

    assert (
        appointment_page.get_status_by_id(
            appointment_id
        )
        == "Đã xác nhận"
    )

    appointment_page.click_examine(
        appointment_id
    )

    examination_page = DoctorExaminationPage(
        driver
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    )

    assert (
        examination_page
        .is_create_record_form_present()
    )

    examination_page.enter_diagnosis("")

    examination_page.enter_treatment(
        medical_record_tc2_data[
            "treatment"
        ]
    )

    examination_page.click_save_medical_record()

    assert (
        examination_page.get_validation_message()
        == (
            "Vui lòng nhập đầy đủ chẩn đoán "
            "và hướng điều trị."
        )
    )

    assert (
        f"/doctor-examination?"
        f"appointmentId={appointment_id}"
        in driver.current_url
    )

    assert (
        examination_page
        .is_create_record_form_present()
    )

    appointment_page.open_page()

    assert (
        appointment_page.get_status_by_id(
            appointment_id
        )
        == "Đã xác nhận"
    )

    assert (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    )

def test_create_medical_record_with_blank_treatment(
        driver,
        medical_record_tc3_data):
    """
    TC-MEDICAL-003:
    Không tạo hồ sơ bệnh án khi
    bỏ trống hướng điều trị.
    """

    login_owner_doctor(driver)

    appointment_page = DoctorAppointmentPage(
        driver
    )
    appointment_page.open_page()

    appointment_id = (
        medical_record_tc3_data[
            "appointment_id"
        ]
    )

    assert (
        appointment_page.get_note_by_id(
            appointment_id
        )
        == medical_record_tc3_data["note"]
    )

    assert (
        appointment_page.get_status_by_id(
            appointment_id
        )
        == "Đã xác nhận"
    )

    appointment_page.click_examine(
        appointment_id
    )

    examination_page = DoctorExaminationPage(
        driver
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    )

    assert (
        examination_page
        .is_create_record_form_present()
    )

    examination_page.enter_diagnosis(
        medical_record_tc3_data[
            "diagnosis"
        ]
    )

    examination_page.enter_treatment("")

    examination_page.click_save_medical_record()

    assert (
        examination_page.get_validation_message()
        == (
            "Vui lòng nhập đầy đủ chẩn đoán "
            "và hướng điều trị."
        )
    )

    assert (
        f"/doctor-examination?"
        f"appointmentId={appointment_id}"
        in driver.current_url
    )

    assert (
        examination_page
        .is_create_record_form_present()
    )

    appointment_page.open_page()

    assert (
        appointment_page.get_status_by_id(
            appointment_id
        )
        == "Đã xác nhận"
    )

    assert (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    )

def test_cannot_create_second_medical_record(
        driver,
        medical_record_tc4_data):
    """
    TC-MEDICAL-004:
    Không cho tạo thêm hồ sơ bệnh án
    cho lịch hẹn đã hoàn thành.
    """

    login_owner_doctor(driver)

    appointment_page = DoctorAppointmentPage(
        driver
    )
    appointment_page.open_page()

    appointment_id = (
        medical_record_tc4_data[
            "appointment_id"
        ]
    )

    assert (
        appointment_page.get_note_by_id(
            appointment_id
        )
        == medical_record_tc4_data["note"]
    )

    assert (
        appointment_page.get_status_by_id(
            appointment_id
        )
        == "Đã hoàn thành"
    )

    assert not (
        appointment_page
        .is_examine_button_present(
            appointment_id
        )
    )

    assert (
        appointment_page
        .is_view_medical_record_button_present_by_id(
            appointment_id
        )
    )

    examination_page = DoctorExaminationPage(
        driver
    )

    examination_page.open_page(
        appointment_id
    )

    assert (
        examination_page
        .get_invalid_appointment_message()
        == (
            "Lịch hẹn chưa được xác nhận "
            "hoặc đã bị hủy."
        )
    )

    assert not (
        examination_page
        .is_appointment_information_present()
    )

    assert not (
        examination_page
        .is_create_record_form_present()
    )

    appointment_page.open_page()

    assert (
        appointment_page.get_status_by_id(
            appointment_id
        )
        == "Đã hoàn thành"
    )

def test_other_doctor_cannot_update_medical_record(
        driver,
        medical_record_tc8_data):
    """
    TC-MEDICAL-008:
    Bác sĩ khác không được cập nhật
    hồ sơ bệnh án không thuộc mình.
    """

    login_other_doctor(driver)

    appointment_id = (
        medical_record_tc8_data[
            "appointment_id"
        ]
    )

    medical_record_page = MedicalRecordPage(
        driver
    )

    medical_record_page.open_page(
        appointment_id
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    )

    assert (
        medical_record_page
        .get_access_denied_message()
        == (
            "Bạn không có quyền xem "
            "hồ sơ bệnh án này."
        )
    )

    assert not (
        medical_record_page
        .is_medical_record_information_present()
    )

    assert not (
        medical_record_page
        .is_edit_button_present()
    )

    assert not (
        medical_record_page
        .is_edit_form_present()
    )
