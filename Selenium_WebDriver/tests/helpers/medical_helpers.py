from selenium.webdriver.support.ui import WebDriverWait

from pages.LoginPage import LoginPage
from datetime import datetime, timedelta

from api.DoctorScheduleApi import DoctorScheduleApi
from api.MedicalRecordApi import MedicalRecordApi

HOME_URL = "http://localhost:3000/"


def login_doctor(driver, username, password):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login(username, password)

    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == HOME_URL
    )

    assert driver.current_url == HOME_URL, (
        "LOGIN FAILED | "
        f"Expected: {HOME_URL} | Actual: {driver.current_url}"
    )


def logout_current_user(driver):
    login_page = LoginPage(driver)
    login_page.logout()

    WebDriverWait(driver, 10).until(
        lambda d: "/login" in d.current_url
    )

    assert "/login" in driver.current_url, (
        "LOGOUT FAILED | "
        f"Expected URL chứa /login | Actual: {driver.current_url}"
    )

def get_or_create_medical_booking_slot(
    doctor_id,
    test_data,
    schedule_note
):
    """
    Tìm slot hợp lệ cho Medical test.

    Nếu bác sĩ không còn ca làm việc available trong tương lai
    hoặc toàn bộ slot đã bị sử dụng:
    - tự tạo một schedule test mới bằng Admin API
    - sau đó tìm lại booking slot.

    Mục đích:
    Test không phụ thuộc vào dữ liệu tình cờ có sẵn trong DB.
    """

    medical_record_api = MedicalRecordApi()

    try:
        return medical_record_api.find_available_booking_slot(
            doctor_id
        )

    except AssertionError as error:
        error_message = str(error)

        allowed_setup_errors = (
            "Không tìm thấy ca làm việc available",
            "Không tìm thấy giờ đặt lịch còn trống",
        )

        if not any(
            message in error_message
            for message in allowed_setup_errors
        ):
            raise

    doctor_schedule_api = DoctorScheduleApi()

    admin_token = doctor_schedule_api.get_token(
        test_data["admin_username"],
        test_data["admin_password"]
    )
    doctor_name = test_data["doctor_name"].strip()

    assert doctor_name, (
        f"{schedule_note} | "
        "Thiếu doctor_name trong medical_test_data.csv."
    )
    created_work_date = None

    # Tìm một ngày trong 30 ngày tới chưa có ca sáng.
    for days_ahead in range(1, 31):

        work_date_obj = (
            datetime.now().date()
            + timedelta(days=days_ahead)
        )

        work_date = work_date_obj.strftime(
            "%Y-%m-%d"
        )

        existing_schedule = (
            doctor_schedule_api.find_schedule(
                doctor_name=doctor_name,
                work_date=work_date,
                shift="morning"
            )
        )

        if existing_schedule is not None:
            continue

        doctor_schedule_api.create_schedule(
            doctor_name=doctor_name,
            work_date=work_date,
            shift="morning",
            start_time="07:00:00",
            end_time="11:30:00",
            status="available",
            note=schedule_note,
            token=admin_token
        )

        created_work_date = work_date
        break

    assert created_work_date is not None, (
        f"{schedule_note} | "
        "Không thể tự tạo lịch làm việc test "
        "cho bác sĩ trong 30 ngày tới."
    )

    booking_slot = (
        medical_record_api
        .find_available_booking_slot(
            doctor_id
        )
    )

    assert booking_slot is not None, (
        f"{schedule_note} | "
        "Đã tạo schedule nhưng vẫn không tìm được booking slot."
    )

    return booking_slot

def prepare_completed_medical_record(
    medical_record_api,
    patient_id,
    doctor_id,
    note,
    diagnosis,
    treatment,
    test_data,
    test_case_id
):
    """
    Chuẩn bị appointment ở trạng thái Completed
    và đã có hồ sơ bệnh án.

    Nếu DB không còn schedule/slot hợp lệ:
    - tự tạo schedule test
    - sau đó thử chuẩn bị dữ liệu lại.
    """

    try:
        return (
            medical_record_api
            .prepare_completed_medical_record(
                patient_id=patient_id,
                doctor_id=doctor_id,
                notes=note,
                diagnosis=diagnosis,
                treatment=treatment
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
                "Không thể chuẩn bị appointment "
                "Đã hoàn thành và hồ sơ bệnh án. "
                f"Actual: {setup_error}"
            ) from error

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
                .prepare_completed_medical_record(
                    patient_id=patient_id,
                    doctor_id=doctor_id,
                    notes=note,
                    diagnosis=diagnosis,
                    treatment=treatment
                )
            )

        except AssertionError as retry_error:
            raise AssertionError(
                f"{test_case_id} | STEP 1 FAILED | "
                "Đã tự tạo schedule nhưng vẫn không thể "
                "chuẩn bị hồ sơ bệnh án hoàn chỉnh. "
                f"Actual: {retry_error}"
            ) from retry_error