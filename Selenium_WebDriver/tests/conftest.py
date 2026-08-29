import sys
import time
import re
from pathlib import Path
import inspect
import pytest
from selenium import webdriver
from tests.helpers.appointment_helpers import get_or_create_booking_slot
from utils.data_reader import (
    get_test_data_csv,
    APPOINTMENT_TEST_DATA_CSV,
    MEDICAL_TEST_DATA_CSV,
)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import các module của project SAU KHI đã thêm PROJECT_ROOT vào sys.path.
from api.AppointmentApi import AppointmentApi
from api.MedicalRecordApi import MedicalRecordApi
from utils.test_reporter import (
    generate_word_report,
    reset_test_report,
    save_test_result,
    report_failed_step,
)
pytest_plugins = ["utils.pytest_report_hooks",]

@pytest.fixture
def driver():
    browser = webdriver.Chrome()

    browser.maximize_window()
    browser.implicitly_wait(3)

    yield browser

    browser.quit()


@pytest.fixture
def booking_test_data():
    appointment_api = AppointmentApi()

    doctor_id = 1
    booking_date = "11/04/2026"
    patient_ids = [1, 2]

    test_times = [
        "09:00",
        "09:30",
        "14:00",
        "15:30",
        "15:31"
    ]

    # Dọn dữ liệu cũ trước khi chạy test
    for booking_time in test_times:
        appointment_api.cancel_matching_appointments(
            doctor_id=doctor_id,
            booking_date=booking_date,
            booking_time=booking_time,
            patient_ids=patient_ids
        )

    yield appointment_api

    # Dọn dữ liệu vừa tạo sau khi test kết thúc
    for booking_time in test_times:
        appointment_api.cancel_matching_appointments(
            doctor_id=doctor_id,
            booking_date=booking_date,
            booking_time=booking_time,
            patient_ids=patient_ids
        )
def prepare_medical_test_data(test_case_id):
    test_data = get_test_data_csv(
        MEDICAL_TEST_DATA_CSV,
        test_case_id
    )

    medical_record_api = MedicalRecordApi()

    patient_id = int(test_data["patient_id"])
    doctor_id = int(test_data["doctor_id"])
    note = test_data["note"]

    confirmed_cases = {
        "TC-MEDICAL-001",
        "TC-MEDICAL-002",
        "TC-MEDICAL-003",
    }

    if test_case_id in confirmed_cases:
        appointment_id = (
            medical_record_api
            .prepare_confirmed_appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                notes=note
            )
        )
    else:
        appointment_id = (
            medical_record_api
            .prepare_completed_medical_record(
                patient_id=patient_id,
                doctor_id=doctor_id,
                notes=note,
                diagnosis=test_data["diagnosis"],
                treatment=test_data["treatment"]
            )
        )

    return {
        **test_data,
        "appointment_id": appointment_id,
        "medical_record_api": medical_record_api
    }


@pytest.fixture
def medical_record_tc1_data():
    yield prepare_medical_test_data(
        "TC-MEDICAL-001"
    )


@pytest.fixture
def medical_record_tc2_data():
    yield prepare_medical_test_data(
        "TC-MEDICAL-002"
    )


@pytest.fixture
def medical_record_tc3_data():
    yield prepare_medical_test_data(
        "TC-MEDICAL-003"
    )


@pytest.fixture
def medical_record_tc4_data():
    yield prepare_medical_test_data(
        "TC-MEDICAL-004"
    )


@pytest.fixture
def medical_record_tc5_data():
    yield prepare_medical_test_data(
        "TC-MEDICAL-005"
    )


@pytest.fixture
def medical_record_tc6_data():
    yield prepare_medical_test_data(
        "TC-MEDICAL-006"
    )


@pytest.fixture
def medical_record_tc7_data():
    yield prepare_medical_test_data(
        "TC-MEDICAL-007"
    )


@pytest.fixture
def medical_record_tc8_data():
    yield prepare_medical_test_data(
        "TC-MEDICAL-008"
    )


@pytest.fixture
def medical_record_tc9_data():
    yield prepare_medical_test_data(
        "TC-MEDICAL-009"
    )

@pytest.fixture
def appointment_tc2_data():
    test_data = get_test_data_csv(
        APPOINTMENT_TEST_DATA_CSV,
        "TC-APPOINTMENT-002"
    )

    appointment_api = AppointmentApi()

    patient_id = int(test_data["patient_id"])
    doctor_id = int(test_data["doctor_id"])

    booking_slot = get_or_create_booking_slot(
        doctor_id=doctor_id,
        doctor_name=test_data["doctor_name"],
        schedule_note=test_data["note_prefix"]
    )

    note = (
        test_data["note_prefix"]
        + str(int(time.time()))
    )

    appointment = appointment_api.create_appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        booking_date=booking_slot["booking_date"],
        booking_time=booking_slot["booking_time"],
        notes=note
    )

    yield {
        **test_data,
        "appointment_id": appointment["appointmentId"],
        "note": note,
        "appointment_time": (
            booking_slot["booking_time"]
            + " "
            + booking_slot["booking_date"]
        )
    }
@pytest.fixture
def appointment_tc3_data():
    test_data = get_test_data_csv(
        APPOINTMENT_TEST_DATA_CSV,
        "TC-APPOINTMENT-003"
    )

    appointment_api = AppointmentApi()

    patient_id = int(test_data["patient_id"])
    doctor_id = int(test_data["doctor_id"])

    booking_slot = get_or_create_booking_slot(
        doctor_id=doctor_id,
        doctor_name=test_data["doctor_name"],
        schedule_note=test_data["note_prefix"]
    )

    note = (
        test_data["note_prefix"]
        + str(int(time.time()))
    )

    appointment = appointment_api.create_appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        booking_date=booking_slot["booking_date"],
        booking_time=booking_slot["booking_time"],
        notes=note
    )

    yield {
        **test_data,
        "appointment_id": appointment["appointmentId"],
        "note": note,
        "appointment_time": (
            booking_slot["booking_time"]
            + " "
            + booking_slot["booking_date"]
        )
    }
@pytest.fixture
def appointment_tc5_data():
    test_data = get_test_data_csv(
        APPOINTMENT_TEST_DATA_CSV,
        "TC-APPOINTMENT-005"
    )

    appointment_api = AppointmentApi()

    patient_id = int(test_data["patient_id"])
    doctor_id = int(test_data["doctor_id"])
    note = test_data["note_prefix"]

    appointment = None

    appointments = appointment_api.get_appointments_by_doctor(
        doctor_id
    )

    for item in appointments:
        if (
            item.get("notes") == note
            and item.get("status") == "pending"
        ):
            appointment = item
            break

    if appointment is None:
        booking_slot = get_or_create_booking_slot(
            doctor_id=doctor_id,
            doctor_name=test_data["doctor_name"],
            schedule_note=note
        )

        appointment = appointment_api.create_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            booking_date=booking_slot["booking_date"],
            booking_time=booking_slot["booking_time"],
            notes=note
        )

    yield {
        **test_data,
        "appointment_id": appointment["appointmentId"],
        "note": note
    }

@pytest.fixture
def appointment_tc6_data():
    test_data = get_test_data_csv(
        APPOINTMENT_TEST_DATA_CSV,
        "TC-APPOINTMENT-006"
    )

    medical_record_api = MedicalRecordApi()

    patient_id = int(test_data["patient_id"])
    doctor_id = int(test_data["doctor_id"])
    note = test_data["note_prefix"]

    appointment_id = (
        medical_record_api
        .prepare_confirmed_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes=note
        )
    )

    yield {
        **test_data,
        "appointment_id": appointment_id,
        "note": note
    }
@pytest.fixture
def appointment_tc7_data():
    test_data = get_test_data_csv(
        APPOINTMENT_TEST_DATA_CSV,
        "TC-APPOINTMENT-007"
    )

    medical_record_api = MedicalRecordApi()

    patient_id = int(test_data["patient_id"])
    doctor_id = int(test_data["doctor_id"])
    note = test_data["note_prefix"]

    appointment_id = (
        medical_record_api
        .prepare_confirmed_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes=note
        )
    )

    yield {
        **test_data,
        "appointment_id": appointment_id,
        "note": note
    }

@pytest.fixture
def appointment_tc8_data():
    test_data = get_test_data_csv(
        APPOINTMENT_TEST_DATA_CSV,
        "TC-APPOINTMENT-008"
    )

    appointment_api = AppointmentApi()

    patient_id = int(test_data["patient_id"])
    doctor_id = int(test_data["doctor_id"])
    note = test_data["note_prefix"]

    appointment = None

    appointments = appointment_api.get_appointments_by_doctor(
        doctor_id
    )

    # Dùng lại lịch TC008 đã hủy nếu có
    for item in appointments:
        if (
            item.get("notes") == note
            and item.get("status") == "cancelled"
        ):
            appointment = item
            break

    # Chưa có thì tạo mới rồi hủy
    if appointment is None:
        booking_slot = get_or_create_booking_slot(
            doctor_id=doctor_id,
            doctor_name=test_data["doctor_name"],
            schedule_note=note
        )

        appointment = appointment_api.create_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            booking_date=booking_slot["booking_date"],
            booking_time=booking_slot["booking_time"],
            notes=note
        )

        appointment_api.cancel_appointment(
            appointment["appointmentId"]
        )

    yield {
        **test_data,
        "appointment_id": appointment["appointmentId"],
        "note": note
    }
@pytest.fixture
def appointment_tc9_data():
    test_data = get_test_data_csv(
        APPOINTMENT_TEST_DATA_CSV,
        "TC-APPOINTMENT-009"
    )

    medical_record_api = MedicalRecordApi()

    patient_id = int(test_data["patient_id"])
    doctor_id = int(test_data["doctor_id"])
    note = test_data["note_prefix"]

    appointment_id = (
        medical_record_api
        .prepare_confirmed_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes=note
        )
    )

    yield {
        **test_data,
        "appointment_id": appointment_id,
        "note": note
    }

@pytest.fixture
def appointment_tc1_data():
    appointment_api = AppointmentApi()
    medical_record_api = MedicalRecordApi()

    doctor_id = 1

    booking_slot = (
        medical_record_api
        .find_available_booking_slot(
            doctor_id
        )
    )

    note = (
        "SELENIUM-TC-APPOINTMENT-001-"
        + str(int(time.time()))
    )

    yield {
        "appointment_api": appointment_api,
        "doctor_id": doctor_id,
        "booking_date": booking_slot[
            "booking_date"
        ],
        "booking_time": booking_slot[
            "booking_time"
        ],
        "note": note
    }
@pytest.fixture
def appointment_tc4_data():
    test_data = get_test_data_csv(
        APPOINTMENT_TEST_DATA_CSV,
        "TC-APPOINTMENT-004"
    )

    appointment_api = AppointmentApi()

    patient_id = int(test_data["patient_id"])
    doctor_id = int(test_data["doctor_id"])
    note = test_data["note_prefix"]

    appointment = None

    appointments = appointment_api.get_appointments_by_doctor(
        doctor_id
    )

    # Dùng lại appointment pending của TC004 nếu đã có
    for item in appointments:
        if (
            item.get("notes") == note
            and item.get("status") == "pending"
        ):
            appointment = item
            break

    # Chưa có thì tạo mới
    if appointment is None:
        booking_slot = get_or_create_booking_slot(
            doctor_id=doctor_id,
            doctor_name=test_data["doctor_name"],
            schedule_note=note
        )

        appointment = appointment_api.create_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            booking_date=booking_slot["booking_date"],
            booking_time=booking_slot["booking_time"],
            notes=note
        )

    yield {
        **test_data,
        "appointment_id": appointment["appointmentId"],
        "note": note
    }
