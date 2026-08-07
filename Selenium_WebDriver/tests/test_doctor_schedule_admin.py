import time

from pages.LoginPage import LoginPage
from pages.DoctorScheduleAdminPage import DoctorScheduleAdminPage


ADMIN_USERNAME = "admin_system"
ADMIN_PASSWORD = "Abc@123"

HOME_URL = "http://localhost:3000/"


def login_admin(driver):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )

    time.sleep(2)

    assert driver.current_url == HOME_URL

def test_admin_views_add_doctor_schedule_form(
        driver):
    """
    TC-DS-ADMIN-001:
    Kiểm tra form Thêm lịch làm việc
    hiển thị đầy đủ các trường,
    danh sách lựa chọn
    và giá trị mặc định.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)

    assert (
        schedule_page.get_form_title()
        == "Thêm lịch làm việc"
    )

    assert (
        schedule_page
        .is_doctor_select_displayed()
    )

    assert (
        schedule_page
        .is_work_date_input_displayed()
    )

    assert (
        schedule_page
        .is_shift_select_displayed()
    )

    assert (
        schedule_page
        .is_status_select_displayed()
    )

    assert (
        schedule_page
        .is_note_input_displayed()
    )

    assert (
        schedule_page
        .is_add_button_displayed()
    )

    assert (
            schedule_page
            .get_selected_doctor_text()
            == "-- Chọn bác sĩ --"
    )

    schedule_page.click_doctor_select()

    time.sleep(2)

    doctor_options = (
        schedule_page.get_doctor_options()
    )

    assert (
            "-- Chọn bác sĩ --"
            in doctor_options
    )

    assert (
            "Vu Thinh"
            in doctor_options
    )

    assert (
            "Ly Minh"
            in doctor_options
    )

    assert (
            "Pham Dung"
            in doctor_options
    )

    assert (
            "Tran Binh"
            in doctor_options
    )
    assert (
        schedule_page
        .get_selected_shift_text()
        == "Ca sáng: 07:00 - 11:30"
    )

    schedule_page.click_shift_select()

    time.sleep(2)

    shift_options = (
        schedule_page.get_shift_options()
    )

    assert len(shift_options) == 3

    assert (
        shift_options[0]
        == "Ca sáng: 07:00 - 11:30"
    )

    assert (
        shift_options[1]
        == "Ca chiều: 13:00 - 17:00"
    )

    assert (
        shift_options[2]
        == "Ca tối: 17:30 - 21:00"
    )

    assert (
        schedule_page
        .get_selected_status_text()
        == "Có lịch làm việc"
    )

    schedule_page.click_status_select()

    time.sleep(2)

    status_options = (
        schedule_page.get_status_options()
    )

    assert len(status_options) == 2

    assert (
        status_options[0]
        == "Có lịch làm việc"
    )

    assert (
        status_options[1]
        == "Không làm việc"
    )

    assert (
        schedule_page
        .get_note_value()
        == ""
    )