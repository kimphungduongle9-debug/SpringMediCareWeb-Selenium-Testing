import sys
import time
from pathlib import Path

import pytest
from selenium import webdriver

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from api.AppointmentApi import AppointmentApi
from api.MedicalRecordApi import MedicalRecordApi

@pytest.fixture
def driver():
    browser = webdriver.Chrome()

    browser.maximize_window()
    browser.implicitly_wait(3)

    yield browser

    time.sleep(3)

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

@pytest.fixture
def medical_record_tc7_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc7_data(
        patient_id=7,
        doctor_id=3
    )

    yield appointment_id

@pytest.fixture
def medical_record_tc5_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc5_data(
        patient_id=7,
        doctor_id=3
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-MEDICAL-005",
        "patient_name": "Duong Le Kim Phung",
        "doctor_name": "Ly Minh",
        "diagnosis": "Đau lưng do ngồi lâu",
        "treatment": (
            "Nghỉ ngơi và hạn chế vận động mạnh"
        )
    }

@pytest.fixture
def medical_record_tc6_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc6_data(
        patient_id=7,
        doctor_id=3
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-MEDICAL-006"
    }

@pytest.fixture
def medical_record_tc9_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc9_data(
        patient_id=7,
        doctor_id=3
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-MEDICAL-009"
    }

@pytest.fixture
def medical_record_tc1_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc1_data(
        patient_id=7,
        doctor_id=3
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-MEDICAL-001",
        "diagnosis": (
            "Đau đầu nhẹ do thiếu ngủ"
        ),
        "treatment": (
            "Nghỉ ngơi và uống đủ nước"
        )
    }

@pytest.fixture
def medical_record_tc2_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc2_data(
        patient_id=7,
        doctor_id=3
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-MEDICAL-002",
        "treatment": (
            "Nghỉ ngơi và uống thuốc theo hướng dẫn"
        )
    }

@pytest.fixture
def medical_record_tc3_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc3_data(
        patient_id=7,
        doctor_id=3
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-MEDICAL-003",
        "diagnosis": (
            "Đau vai do vận động sai tư thế"
        )
    }

@pytest.fixture
def medical_record_tc4_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc4_data(
        patient_id=7,
        doctor_id=3
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-MEDICAL-004"
    }

@pytest.fixture
def medical_record_tc8_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = medical_record_api.prepare_tc8_data(
        patient_id=7,
        doctor_id=3
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-MEDICAL-008"
    }

@pytest.fixture
def appointment_tc2_data():
    appointment_api = AppointmentApi()
    medical_record_api = MedicalRecordApi()

    patient_id = 7
    doctor_id = 3

    booking_slot = (
        medical_record_api
        .find_available_booking_slot(
            doctor_id
        )
    )

    note = (
        "SELENIUM-TC-APPOINTMENT-002-"
        + str(int(time.time()))
    )

    appointment = appointment_api.create_appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        booking_date=booking_slot["booking_date"],
        booking_time=booking_slot["booking_time"],
        notes=note
    )

    appointment_id = appointment["appointmentId"]

    yield {
        "appointment_id": appointment_id,
        "note": note,
        "patient_name": "Duong Le Kim Phung",
        "doctor_name": "Ly Minh",
        "appointment_time": (
            booking_slot["booking_time"]
            + " "
            + booking_slot["booking_date"]
        )
    }

@pytest.fixture
def appointment_tc3_data():
    appointment_api = AppointmentApi()
    medical_record_api = MedicalRecordApi()

    patient_id = 7
    doctor_id = 3

    booking_slot = (
        medical_record_api
        .find_available_booking_slot(
            doctor_id
        )
    )

    note = (
        "SELENIUM-TC-APPOINTMENT-003-"
        + str(int(time.time()))
    )

    appointment = appointment_api.create_appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        booking_date=booking_slot["booking_date"],
        booking_time=booking_slot["booking_time"],
        notes=note
    )

    appointment_id = appointment[
        "appointmentId"
    ]

    yield {
        "appointment_id": appointment_id,
        "note": note,
        "patient_name": "Duong Le Kim Phung",
        "doctor_name": "Ly Minh",
        "appointment_time": (
            booking_slot["booking_time"]
            + " "
            + booking_slot["booking_date"]
        )
    }

    appointments = (
        appointment_api
        .get_appointments_by_doctor(
            doctor_id
        )
    )

    for item in appointments:
        if (
            item.get("appointmentId")
            == appointment_id
            and item.get("status")
            != "cancelled"
        ):
            appointment_api.cancel_appointment(
                appointment_id
            )
            break

@pytest.fixture
def appointment_tc5_data():
    appointment_api = AppointmentApi()
    medical_record_api = MedicalRecordApi()

    patient_id = 7
    doctor_id = 3
    note = "SELENIUM-TC-APPOINTMENT-005"

    appointment = None

    appointments = (
        appointment_api
        .get_appointments_by_doctor(
            doctor_id
        )
    )

    for item in appointments:
        if (
            item.get("notes") == note
            and item.get("status") == "pending"
        ):
            appointment = item
            break

    if appointment is None:
        booking_slot = (
            medical_record_api
            .find_available_booking_slot(
                doctor_id
            )
        )
        appointment = (
            appointment_api.create_appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                booking_date=booking_slot[
                    "booking_date"
                ],
                booking_time=booking_slot[
                    "booking_time"
                ],
                notes=note
            )
        )
    yield {
        "appointment_id": appointment[
            "appointmentId"
        ],
        "note": note
    }

@pytest.fixture
def appointment_tc6_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = (
        medical_record_api
        .prepare_confirmed_appointment(
            patient_id=7,
            doctor_id=3,
            notes="SELENIUM-TC-APPOINTMENT-006"
        )
    )
    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-APPOINTMENT-006",
        "patient_name": "Duong Le Kim Phung"
    }
@pytest.fixture
def appointment_tc7_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = (
        medical_record_api
        .prepare_confirmed_appointment(
            patient_id=7,
            doctor_id=3,
            notes="SELENIUM-TC-APPOINTMENT-007"
        )
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-APPOINTMENT-007"
    }

@pytest.fixture
def appointment_tc8_data():
    appointment_api = AppointmentApi()
    medical_record_api = MedicalRecordApi()

    patient_id = 7
    doctor_id = 3
    note = "SELENIUM-TC-APPOINTMENT-008"

    appointment = None

    appointments = (
        appointment_api
        .get_appointments_by_doctor(
            doctor_id
        )
    )

    # Dùng lại lịch TC8 đã hủy nếu có
    for item in appointments:
        if (
            item.get("notes") == note
            and item.get("status") == "cancelled"
        ):
            appointment = item
            break

    # Chưa có thì tạo lịch mới rồi hủy
    if appointment is None:
        booking_slot = (
            medical_record_api
            .find_available_booking_slot(
                doctor_id
            )
        )

        appointment = (
            appointment_api.create_appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                booking_date=booking_slot[
                    "booking_date"
                ],
                booking_time=booking_slot[
                    "booking_time"
                ],
                notes=note
            )
        )

        appointment_api.cancel_appointment(
            appointment["appointmentId"]
        )

    yield {
        "appointment_id": appointment[
            "appointmentId"
        ],
        "note": note
    }

@pytest.fixture
def appointment_tc9_data():
    medical_record_api = MedicalRecordApi()

    appointment_id = (
        medical_record_api
        .prepare_confirmed_appointment(
            patient_id=7,
            doctor_id=3,
            notes="SELENIUM-TC-APPOINTMENT-009"
        )
    )

    yield {
        "appointment_id": appointment_id,
        "note": "SELENIUM-TC-APPOINTMENT-009",
        "patient_name": "Duong Le Kim Phung",
        "doctor_name": "Ly Minh",
        "diagnosis": (
            "Đau cổ do ngồi sai tư thế"
        ),
        "treatment": (
            "Nghỉ ngơi và tập vận động nhẹ"
        )
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
    appointment_api = AppointmentApi()
    medical_record_api = MedicalRecordApi()

    patient_id = 7
    doctor_id = 3
    note = "SELENIUM-TC-APPOINTMENT-004"

    appointment = None

    appointments = (
        appointment_api
        .get_appointments_by_doctor(
            doctor_id
        )
    )

    # Dùng lại lịch TC4 đang chờ xác nhận
    for item in appointments:
        if (
            item.get("notes") == note
            and item.get("status") == "pending"
        ):
            appointment = item
            break

    # Chưa có thì tạo lịch mới
    if appointment is None:
        booking_slot = (
            medical_record_api
            .find_available_booking_slot(
                doctor_id
            )
        )

        appointment = (
            appointment_api
            .create_appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                booking_date=booking_slot[
                    "booking_date"
                ],
                booking_time=booking_slot[
                    "booking_time"
                ],
                notes=note
            )
        )

    yield {
        "appointment_id": appointment[
            "appointmentId"
        ],
        "note": note,
        "patient_name": "Duong Le Kim Phung"
    }