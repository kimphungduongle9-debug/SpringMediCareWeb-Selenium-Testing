from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.LoginPage import LoginPage
from pages.DoctorWorkSchedulePage import DoctorWorkSchedulePage
from datetime import datetime, timedelta

DOCTOR_USERNAME = "doctor_dung"
DOCTOR_PASSWORD = "Abc@123"
OTHER_DOCTOR_USERNAME = "doctor_binh"
OTHER_DOCTOR_PASSWORD = "Abc@123"

HOME_URL = "http://localhost:3000/"


def login_doctor(driver):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        DOCTOR_USERNAME,
        DOCTOR_PASSWORD
    )

    WebDriverWait(driver, 10).until(
        EC.url_to_be(HOME_URL)
    )

    assert driver.current_url == HOME_URL

def login_other_doctor(driver):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        OTHER_DOCTOR_USERNAME,
        OTHER_DOCTOR_PASSWORD
    )

    WebDriverWait(driver, 10).until(
        EC.url_to_be(HOME_URL)
    )

    assert driver.current_url == HOME_URL

def logout_current_user(driver):
    login_page = LoginPage(driver)

    login_page.logout()

    WebDriverWait(driver, 10).until(
        EC.url_contains("/login")
    )

def test_doctor_views_current_work_schedule(driver):
    """
    TC-WORKSCHEDULE-001:
    Doctor xem đúng thông tin cá nhân
    và lịch làm việc của tuần hiện tại.
    """

    login_doctor(driver)

    schedule_page = DoctorWorkSchedulePage(driver)
    schedule_page.open_page()

    assert (
        schedule_page.get_page_title()
        == "Lịch làm việc của tôi"
    )

    doctor_name = schedule_page.get_doctor_name()
    specialty = schedule_page.get_specialty()

    assert doctor_name != ""
    assert specialty != ""

    week_range = schedule_page.get_week_range()
    assert week_range != ""

    dates = schedule_page.get_week_header_dates()
    assert len(dates) == 7

    shifts = schedule_page.get_week_shift_rows()
    assert len(shifts) == 3

    assert "Ca sáng" in shifts[0]
    assert "Ca chiều" in shifts[1]
    assert "Ca tối" in shifts[2]

    doctor_names = schedule_page.get_week_doctor_names()

    assert all(
        name == doctor_name
        for name in doctor_names
    )

def test_doctor_views_previous_week_schedule(driver):
    """
    TC-WORKSCHEDULE-002:
    Doctor xem lịch làm việc của tuần trước.
    """

    login_doctor(driver)

    schedule_page = DoctorWorkSchedulePage(driver)
    schedule_page.open_page()

    dates_before = schedule_page.get_week_header_dates()

    assert len(dates_before) == 7

    first_date_before = datetime.strptime(
        dates_before[0],
        "%d/%m/%Y"
    )

    schedule_page.click_previous_week()

    dates_after = schedule_page.get_week_header_dates()

    assert len(dates_after) == 7

    first_date_after = datetime.strptime(
        dates_after[0],
        "%d/%m/%Y"
    )

    assert (
        first_date_after
        == first_date_before - timedelta(days=7)
    )

def test_doctor_views_next_week_schedule(driver):
    """
    TC-WORKSCHEDULE-003:
    Doctor xem lịch làm việc của tuần sau.
    """

    login_doctor(driver)

    schedule_page = DoctorWorkSchedulePage(driver)
    schedule_page.open_page()

    dates_before = schedule_page.get_week_header_dates()

    assert len(dates_before) == 7

    first_date_before = datetime.strptime(
        dates_before[0],
        "%d/%m/%Y"
    )

    schedule_page.click_next_week()

    dates_after = schedule_page.get_week_header_dates()

    assert len(dates_after) == 7

    first_date_after = datetime.strptime(
        dates_after[0],
        "%d/%m/%Y"
    )

    assert (
        first_date_after
        == first_date_before + timedelta(days=7)
    )
def test_week_schedule_matches_schedule_list(driver):
    """
    TC-WORKSCHEDULE-004:
    Lịch trong bảng tuần phải khớp
    với danh sách lịch làm việc.
    """

    login_doctor(driver)

    schedule_page = DoctorWorkSchedulePage(driver)
    schedule_page.open_page()

    week_records = (
        schedule_page.get_week_schedule_records()
    )

    schedule_page.scroll_to_schedule_list()

    list_records = (
        schedule_page.get_schedule_list_records()
    )

    assert sorted(week_records,key=lambda x: (x["date"],x["shift"])) == sorted(list_records,key=lambda x: (x["date"],x["shift"]))

def test_doctor_only_sees_own_work_schedule(driver):
    """
    TC-WORKSCHEDULE-005:
    Doctor chỉ thấy lịch làm việc của chính mình.
    """

    login_doctor(driver)

    schedule_page = DoctorWorkSchedulePage(driver)
    schedule_page.open_page()

    current_doctor = (
        schedule_page.get_doctor_name()
    )

    week_doctors = (
        schedule_page.get_week_doctor_names()
    )

    schedule_page.scroll_to_schedule_list()

    list_doctors = (
        schedule_page.get_schedule_list_doctor_names()
    )

    assert all(
        name == current_doctor
        for name in week_doctors
    )

    assert all(
        name == current_doctor
        for name in list_doctors
    )

def test_doctors_only_see_their_own_work_schedule(driver):
    """
    TC-WORKSCHEDULE-005:
    Doctor A và Doctor B chỉ thấy
    lịch làm việc của chính mình.
    """

    # Doctor A
    login_doctor(driver)

    schedule_page = DoctorWorkSchedulePage(driver)
    schedule_page.open_page()

    doctor_a = schedule_page.get_doctor_name()

    doctor_a_week_names = (
        schedule_page.get_week_doctor_names()
    )

    schedule_page.scroll_to_schedule_list()

    doctor_a_list_names = (
        schedule_page.get_schedule_list_doctor_names()
    )

    assert all(
        name == doctor_a
        for name in doctor_a_week_names
    )

    assert all(
        name == doctor_a
        for name in doctor_a_list_names
    )

    logout_current_user(driver)

    # Doctor B
    login_other_doctor(driver)

    schedule_page = DoctorWorkSchedulePage(driver)
    schedule_page.open_page()

    doctor_b = schedule_page.get_doctor_name()

    assert doctor_b != doctor_a

    doctor_b_week_names = (
        schedule_page.get_week_doctor_names()
    )

    schedule_page.scroll_to_schedule_list()

    doctor_b_list_names = (
        schedule_page.get_schedule_list_doctor_names()
    )

    assert all(
        name == doctor_b
        for name in doctor_b_week_names
    )

    assert all(
        name == doctor_b
        for name in doctor_b_list_names
    )

    assert doctor_a not in doctor_b_week_names
    assert doctor_a not in doctor_b_list_names