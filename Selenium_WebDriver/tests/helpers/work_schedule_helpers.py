from selenium.webdriver.support.ui import WebDriverWait

from pages.LoginPage import LoginPage

from datetime import datetime, timedelta

from api.DoctorScheduleApi import DoctorScheduleApi

HOME_URL = "http://localhost:3000/"
LOGIN_URL = "http://localhost:3000/login"


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

def ensure_current_week_schedule(
        doctor_name,
        admin_username,
        admin_password
):
    schedule_api = DoctorScheduleApi()

    today = datetime.now().date()

    # Python: Monday = 0, Sunday = 6
    monday = today - timedelta(days=today.weekday())

    shifts = [
        ("morning", "07:00:00", "11:30:00"),
        ("afternoon", "13:00:00", "17:00:00"),
        ("evening", "18:00:00", "21:00:00"),
    ]

    # Nếu trong tuần hiện tại đã có lịch thì dùng luôn,
    # không tạo thêm và không xóa dữ liệu có sẵn.
    for day_offset in range(7):
        work_date = (
            monday + timedelta(days=day_offset)
        ).strftime("%Y-%m-%d")

        for shift, _, _ in shifts:
            existing_schedule = schedule_api.find_schedule(
                doctor_name=doctor_name,
                work_date=work_date,
                shift=shift
            )

            if existing_schedule is not None:
                return {
                    "created": False,
                    "schedule_id": None
                }

    token = schedule_api.get_token(
        admin_username,
        admin_password
    )

    # Nếu cả tuần chưa có lịch,
    # tạo một lịch test vào ngày hôm nay.
    work_date = today.strftime("%Y-%m-%d")

    shift = "morning"
    start_time = "07:00:00"
    end_time = "11:30:00"

    schedule_api.create_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        start_time=start_time,
        end_time=end_time,
        status="available",
        note="Selenium TC-WORKSCHEDULE-004",
        token=token
    )

    created_schedule = schedule_api.find_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift
    )

    assert created_schedule is not None, (
        "SETUP FAILED | "
        "Không tạo được lịch làm việc tạm cho TC-WORKSCHEDULE-004"
    )

    return {
        "created": True,
        "schedule_id": created_schedule["scheduleId"],
        "token": token
    }

def cleanup_created_schedule(schedule_setup):
    if not schedule_setup.get("created"):
        return

    schedule_api = DoctorScheduleApi()

    schedule_api.delete_schedule(
        schedule_id=schedule_setup["schedule_id"],
        token=schedule_setup["token"]
    )