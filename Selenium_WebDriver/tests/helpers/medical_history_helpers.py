import time

from api.AppointmentApi import AppointmentApi

from pages.LoginPage import LoginPage

from tests.helpers.booking_helpers import (
    get_or_create_booking_slot,
    login_account,
    open_tran_binh_booking_page,
)
from api.DoctorScheduleApi import DoctorScheduleApi

from tests.helpers.medical_helpers import (
    prepare_completed_medical_record,
)
def get_patient_record_ids(medical_record_api, patient_id):
    """
    Lấy danh sách Medical Record ID hiện tại của Patient.
    Dùng để so sánh dữ liệu trước và sau test.
    """
    records = medical_record_api.get_medical_records_by_patient(patient_id)

    return {
        str(record["recordId"])
        for record in records
    }


def create_pending_appointment(
        driver,
        doctor_id,
        test_data,
        test_case_id):
    """
    Tạo một lịch hẹn hợp lệ ở trạng thái pending.

    Đây là helper kỹ thuật cho Step tạo lịch hẹn.
    Không tự ghi report Step.
    """
    appointment_api = AppointmentApi()

    booking_slot = get_or_create_booking_slot(
        doctor_id=doctor_id,
        test_data=test_data,
        schedule_note=f"{test_case_id}-AUTO-SCHEDULE"
    )

    booking_page = open_tran_binh_booking_page(driver)

    booking_page.enter_date(
        booking_slot["booking_date"]
    )
    booking_page.enter_time(
        booking_slot["booking_time"]
    )

    note = (
        f"{test_data['note_prefix']}"
        f"{int(time.time())}"
    )

    booking_page.enter_notes(note)
    booking_page.click_booking_button()

    success_message = booking_page.get_message()

    appointment = appointment_api.find_appointment_by_note(
        doctor_id=doctor_id,
        note=note
    )

    return {
        "appointment": appointment,
        "success_message": success_message,
        "note": note,
    }


def get_ui_record_ids(history_page):
    """
    Lấy danh sách Medical Record ID đang hiển thị trên UI.
    """
    return set(history_page.get_record_ids())


def cleanup_appointment(appointment_id):
    """
    Hủy appointment được tạo riêng cho test.
    Không thực hiện nếu appointment chưa được tạo.
    """
    if appointment_id is None:
        return

    AppointmentApi().cancel_appointment(
        appointment_id
    )

def switch_account(driver, username, password):
    """
    Đăng xuất tài khoản hiện tại và đăng nhập tài khoản khác.
    Đây là helper kỹ thuật, không tự ghi report Step.
    """
    login_page = LoginPage(driver)
    login_page.logout()

    login_page.wait.until(
        lambda d: d.current_url == "http://localhost:3000/login"
    )

    login_account(
        driver,
        username,
        password
    )

def get_related_id(value, field_name):
    """
    API có thể trả relationship dưới dạng object hoặc ID trực tiếp.
    """
    if isinstance(value, dict):
        return value.get(field_name)

    return value


def find_record_by_appointment(records, appointment_id):
    """
    Tìm Medical Record thuộc đúng appointment.
    """

    for record in records:
        actual_appointment_id = get_related_id(
            record.get("appointmentId"),
            "appointmentId"
        )

        if str(actual_appointment_id) == str(appointment_id):
            return record

    return None


def prepare_medical_history_update_record(
        medical_record_api,
        patient_id,
        doctor_id,
        test_data,
        test_case_id,
        diagnosis,
        treatment):
    """
    Chuẩn bị một completed appointment có Medical Record dành cho TC006.

    Nếu dữ liệu đã tồn tại thì tái sử dụng.
    Sau đó reset Diagnosis/Treatment về baseline
    để mỗi lần chạy test đều bắt đầu giống nhau.
    """

    note = f"{test_case_id}-UPDATE-RECORD"

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

    records = medical_record_api.get_medical_records_by_patient(
        patient_id
    )

    record = find_record_by_appointment(
        records,
        appointment_id
    )

    assert record is not None, (
        f"{test_case_id} | TEST SETUP FAILED | "
        f"Không tìm thấy Medical Record của "
        f"appointment #{appointment_id}"
    )

    record_id = record["recordId"]

    doctor_schedule_api = DoctorScheduleApi()

    doctor_token = doctor_schedule_api.get_token(
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    medical_record_api.update_medical_record(
        record_id=record_id,
        diagnosis=diagnosis,
        treatment=treatment,
        token=doctor_token
    )

    record_after_reset = (
        medical_record_api.get_medical_record_by_id(
            record_id
        )
    )

    assert record_after_reset["diagnosis"] == diagnosis, (
        f"{test_case_id} | TEST SETUP FAILED | "
        f"Expected diagnosis: {diagnosis} | "
        f"Actual: {record_after_reset.get('diagnosis')}"
    )

    assert record_after_reset["treatment"] == treatment, (
        f"{test_case_id} | TEST SETUP FAILED | "
        f"Expected treatment: {treatment} | "
        f"Actual: {record_after_reset.get('treatment')}"
    )

    return {
        "appointment_id": appointment_id,
        "record_id": record_id,
    }

