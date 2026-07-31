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