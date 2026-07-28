import sys
import time
from pathlib import Path

import pytest
from selenium import webdriver

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from api.AppointmentApi import AppointmentApi

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