import time
import pytest
from datetime import datetime, timedelta
from pages.LoginPage import LoginPage
from pages.DoctorScheduleAdminPage import DoctorScheduleAdminPage
from doctor_schedule_data import (
    doctor_schedule_tc2_data,
    doctor_schedule_tc3_data,
    doctor_schedule_tc4_data,
    doctor_schedule_tc7_data,
    doctor_schedule_tc8_data,
    doctor_schedule_tc9_data,
    doctor_schedule_tc10_data,
    doctor_schedule_tc11_data,
    doctor_schedule_tc12_data,
    doctor_schedule_tc13_data,
    doctor_schedule_tc18_data,
    doctor_schedule_tc19_data,
    doctor_schedule_tc20_data
)

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

    assert (schedule_page.get_form_title()== "Thêm lịch làm việc")
    assert (schedule_page.is_doctor_select_displayed())
    assert (schedule_page.is_work_date_input_displayed())
    assert (schedule_page.is_shift_select_displayed())
    assert (schedule_page.is_status_select_displayed())
    assert (schedule_page.is_note_input_displayed())
    assert (schedule_page.is_add_button_displayed())

    assert (schedule_page.get_selected_doctor_text()== "-- Chọn bác sĩ --")

    schedule_page.click_doctor_select()

    time.sleep(2)

    doctor_options = (schedule_page.get_doctor_options())

    assert ("-- Chọn bác sĩ --"in doctor_options)
    assert ("Vu Thinh"in doctor_options)
    assert ("Ly Minh"in doctor_options)

    assert ("Pham Dung"in doctor_options)

    assert ("Tran Binh"in doctor_options)
    assert (schedule_page.get_selected_shift_text()== "Ca sáng: 07:00 - 11:30")

    schedule_page.click_shift_select()

    time.sleep(2)

    shift_options = (schedule_page.get_shift_options())

    assert len(shift_options) == 3
    assert (shift_options[0]== "Ca sáng: 07:00 - 11:30")
    assert (shift_options[1]== "Ca chiều: 13:00 - 17:00")
    assert (shift_options[2]== "Ca tối: 17:30 - 21:00")
    assert (schedule_page.get_selected_status_text()== "Có lịch làm việc")

    schedule_page.click_status_select()

    time.sleep(2)

    status_options = (
        schedule_page.get_status_options()
    )

    assert len(status_options) == 2
    assert (status_options[0]== "Có lịch làm việc")
    assert (status_options[1]== "Không làm việc")
    assert (schedule_page.get_note_value()== "")

def test_admin_add_available_doctor_schedule(
        driver,
        doctor_schedule_tc2_data):
    """
    TC-DS-ADMIN-002:
    Thêm lịch làm việc hợp lệ
    với trạng thái Có lịch làm việc.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(driver)

    schedule_page.open_page()

    time.sleep(2)

    schedule_page.select_doctor(doctor_schedule_tc2_data["doctor_name"])

    assert (schedule_page.get_selected_doctor_text()== doctor_schedule_tc2_data["doctor_name"])
    schedule_page.select_work_date_day_8()
    assert (
        schedule_page
        .get_work_date_value()
        == doctor_schedule_tc2_data[
            "work_date_list"
        ]
    )
    schedule_page.select_shift(
        doctor_schedule_tc2_data[
            "shift_form"
        ]
    )
    assert (
        schedule_page
        .get_selected_shift_text()
        == doctor_schedule_tc2_data[
            "shift_form"
        ]
    )
    schedule_page.select_status(doctor_schedule_tc2_data["status_form"])
    assert (
        schedule_page
        .get_selected_status_text()
        == doctor_schedule_tc2_data[
            "status_form"
        ]
    )
    schedule_page.enter_note(doctor_schedule_tc2_data["note"])

    assert (schedule_page.get_note_value()== doctor_schedule_tc2_data["note"])
    schedule_page.click_add_button()

    schedule_page.scroll_to_success_message()

    assert (
            schedule_page.get_success_message()
            == "Thêm lịch làm việc thành công!"
    )
    assert (
        schedule_page.scroll_to_schedule_in_list(
            doctor_schedule_tc2_data[
                "doctor_name"
            ],
            doctor_schedule_tc2_data[
                "work_date_list"
            ],
            doctor_schedule_tc2_data[
                "shift_name"
            ],
            doctor_schedule_tc2_data[
                "status_display"
            ],
            doctor_schedule_tc2_data[
                "note"
            ]
        )
    )
def test_admin_add_unavailable_doctor_schedule(
        driver,
        doctor_schedule_tc3_data):
    """
    TC-DS-ADMIN-003:
    Thêm lịch với trạng thái
    Không làm việc.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)
    schedule_page.select_doctor(
        doctor_schedule_tc3_data[
            "doctor_name"
        ]
    )

    assert (
        schedule_page
        .get_selected_doctor_text()
        == doctor_schedule_tc3_data[
            "doctor_name"
        ]
    )
    schedule_page.select_work_date_day_8()

    assert (
        schedule_page
        .get_work_date_value()
        == doctor_schedule_tc3_data[
            "work_date_list"
        ]
    )
    schedule_page.select_shift(
        doctor_schedule_tc3_data[
            "shift_form"
        ]
    )

    assert (
        schedule_page
        .get_selected_shift_text()
        == doctor_schedule_tc3_data[
            "shift_form"
        ]
    )
    schedule_page.select_status(
        doctor_schedule_tc3_data[
            "status_form"
        ]
    )

    assert (
        schedule_page
        .get_selected_status_text()
        == doctor_schedule_tc3_data[
            "status_form"
        ]
    )
    schedule_page.enter_note(
        doctor_schedule_tc3_data[
            "note"
        ]
    )
    assert (
        schedule_page
        .get_note_value()
        == doctor_schedule_tc3_data[
            "note"
        ]
    )
    schedule_page.click_add_button()

    schedule_page.scroll_to_success_message()

    assert (
        schedule_page.get_success_message()
        == "Thêm lịch làm việc thành công!"
    )
    assert (
        schedule_page.scroll_to_schedule_in_list(
            doctor_schedule_tc3_data[
                "doctor_name"
            ],
            doctor_schedule_tc3_data[
                "work_date_list"
            ],
            doctor_schedule_tc3_data[
                "shift_name"
            ],
            doctor_schedule_tc3_data[
                "status_display"
            ],
            doctor_schedule_tc3_data[
                "note"
            ]
        )
    )
    assert (
        schedule_page.is_schedule_present_in_list(
            doctor_schedule_tc3_data[
                "doctor_name"
            ],
            doctor_schedule_tc3_data[
                "work_date_list"
            ],
            doctor_schedule_tc3_data[
                "shift_name"
            ],
            doctor_schedule_tc3_data[
                "status_display"
            ],
            doctor_schedule_tc3_data[
                "note"
            ]
        )
    )
def test_admin_add_doctor_schedule_without_note(
        driver,
        doctor_schedule_tc4_data):
    """
    TC-DS-ADMIN-004:
    Thêm lịch làm việc
    khi để trống Ghi chú.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)
    schedule_page.select_doctor(
        doctor_schedule_tc4_data[
            "doctor_name"
        ]
    )

    assert (
        schedule_page
        .get_selected_doctor_text()
        == doctor_schedule_tc4_data[
            "doctor_name"
        ]
    )
    schedule_page.select_work_date_day_8()

    assert (
        schedule_page
        .get_work_date_value()
        == doctor_schedule_tc4_data[
            "work_date_list"
        ]
    )
    schedule_page.select_shift(
        doctor_schedule_tc4_data[
            "shift_form"
        ]
    )

    assert (
        schedule_page
        .get_selected_shift_text()
        == doctor_schedule_tc4_data[
            "shift_form"
        ]
    )
    schedule_page.select_status(
        doctor_schedule_tc4_data[
            "status_form"
        ]
    )

    assert (
        schedule_page
        .get_selected_status_text()
        == doctor_schedule_tc4_data[
            "status_form"
        ]
    )
    assert (
        schedule_page.get_note_value()
        == ""
    )
    schedule_page.click_add_button()

    schedule_page.scroll_to_success_message()

    assert (
        schedule_page.get_success_message()
        == "Thêm lịch làm việc thành công!"
    )
    assert (
        schedule_page.scroll_to_schedule_in_list(
            doctor_schedule_tc4_data[
                "doctor_name"
            ],
            doctor_schedule_tc4_data[
                "work_date_list"
            ],
            doctor_schedule_tc4_data[
                "shift_name"
            ],
            doctor_schedule_tc4_data[
                "status_display"
            ],
            doctor_schedule_tc4_data[
                "note"
            ]
        )
    )
    assert (
        schedule_page.is_schedule_present_in_list(
            doctor_schedule_tc4_data[
                "doctor_name"
            ],
            doctor_schedule_tc4_data[
                "work_date_list"
            ],
            doctor_schedule_tc4_data[
                "shift_name"
            ],
            doctor_schedule_tc4_data[
                "status_display"
            ],
            doctor_schedule_tc4_data[
                "note"
            ]
        )
    )
def test_admin_add_schedule_without_doctor(
        driver):
    """
    TC-DS-ADMIN-005:
    Kiểm tra hệ thống xử lý
    khi Admin chưa chọn bác sĩ.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)
    assert (
        schedule_page
        .get_selected_doctor_text()
        == "-- Chọn bác sĩ --"
    )
    schedule_page.select_work_date_day_8()

    assert (
        schedule_page.get_work_date_value()
        == "08/08/2026"
    )
    assert (
        schedule_page
        .get_selected_shift_text()
        == "Ca sáng: 07:00 - 11:30"
    )
    assert (
        schedule_page
        .get_selected_status_text()
        == "Có lịch làm việc"
    )
    schedule_page.enter_note(
        "Ca sáng"
    )

    assert (
        schedule_page.get_note_value()
        == "Ca sáng"
    )
    schedule_page.click_add_button()
    schedule_page.scroll_to_doctor_select()

    assert (
        schedule_page.is_doctor_value_missing()
    )
def test_admin_add_schedule_without_work_date(
        driver):
    """
    TC-DS-ADMIN-006:
    Kiểm tra hệ thống xử lý
    khi Admin chưa chọn ngày làm việc.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)

    schedule_page.select_doctor(
        "Tran Binh"
    )

    assert (
        schedule_page
        .get_selected_doctor_text()
        == "Tran Binh"
    )

    assert (
        schedule_page.get_work_date_value()
        == ""
    )

    assert (
        schedule_page
        .get_selected_shift_text()
        == "Ca sáng: 07:00 - 11:30"
    )

    assert (
        schedule_page
        .get_selected_status_text()
        == "Có lịch làm việc"
    )

    schedule_page.enter_note(
        "Ca sáng"
    )

    assert (
        schedule_page.get_note_value()
        == "Ca sáng"
    )

    schedule_page.click_add_button()

    schedule_page.scroll_to_work_date_input()

    assert (
        schedule_page.is_work_date_value_missing()
    )
@pytest.mark.xfail(
    reason=(
        "BUG: Hệ thống hiện vẫn cho phép "
        "tạo lịch làm việc cho ngày đã qua."
    ),
    strict=True
)
def test_admin_cannot_add_schedule_for_past_date(
        driver,
        doctor_schedule_tc7_data):
    """
    TC-DS-ADMIN-007:
    Không cho phép tạo lịch làm việc
    cho ngày đã qua.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)

    schedule_page.select_doctor(
        doctor_schedule_tc7_data[
            "doctor_name"
        ]
    )

    schedule_page.select_work_date_day_1()

    assert (
        schedule_page.get_work_date_value()
        == doctor_schedule_tc7_data[
            "work_date_list"
        ]
    )

    assert (
        schedule_page
        .get_selected_shift_text()
        == "Ca sáng: 07:00 - 11:30"
    )

    assert (
        schedule_page
        .get_selected_status_text()
        == "Có lịch làm việc"
    )

    schedule_page.enter_note(
        doctor_schedule_tc7_data[
            "note"
        ]
    )

    schedule_page.click_add_button()

    schedule_page.scroll_to_success_message()

    assert (
        schedule_page.get_success_message()
        != "Thêm lịch làm việc thành công!"
    )

def test_admin_cannot_add_duplicate_doctor_schedule(
        driver,
        doctor_schedule_tc8_data):
    """
    TC-DS-ADMIN-008:
    Không cho phép tạo hai lịch
    trùng hoàn toàn cho cùng bác sĩ.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)

    schedule_page.select_doctor(
        doctor_schedule_tc8_data[
            "doctor_name"
        ]
    )

    schedule_page.select_work_date_day_8()

    schedule_page.select_shift(
        doctor_schedule_tc8_data[
            "shift_form"
        ]
    )

    schedule_page.select_status(
        doctor_schedule_tc8_data[
            "status_form"
        ]
    )

    schedule_page.enter_note(
        doctor_schedule_tc8_data[
            "note"
        ]
    )

    schedule_page.click_add_button()

    schedule_page.scroll_to_success_message()

    assert (
        schedule_page.get_success_message()
        == "Thêm lịch làm việc thành công!"
    )

    assert (
        doctor_schedule_tc8_data[
            "schedule_api"
        ].count_matching_schedules(
            doctor_schedule_tc8_data[
                "doctor_name"
            ],
            doctor_schedule_tc8_data[
                "work_date_api"
            ],
            "evening"
        )
        == 1
    )

    schedule_page.select_doctor(
        doctor_schedule_tc8_data[
            "doctor_name"
        ]
    )

    schedule_page.select_work_date_day_8()

    schedule_page.select_shift(
        doctor_schedule_tc8_data[
            "shift_form"
        ]
    )

    schedule_page.select_status(
        doctor_schedule_tc8_data[
            "status_form"
        ]
    )

    schedule_page.enter_note(
        doctor_schedule_tc8_data[
            "note"
        ]
    )

    schedule_page.click_add_button()

    schedule_page.scroll_to_success_message()

    assert (
        schedule_page.get_success_message()
        == (
            "Lịch làm việc của bác sĩ "
            "trong ngày và ca này đã tồn tại."
        )
    )

    assert (
        doctor_schedule_tc8_data[
            "schedule_api"
        ].count_matching_schedules(
            doctor_schedule_tc8_data[
                "doctor_name"
            ],
            doctor_schedule_tc8_data[
                "work_date_api"
            ],
            "evening"
        )
        == 1
    )
    assert (
        schedule_page.scroll_to_schedule_in_list(
            doctor_schedule_tc8_data[
                "doctor_name"
            ],
            doctor_schedule_tc8_data[
                "work_date_list"
            ],
            "Ca tối",
            "Có lịch",
            doctor_schedule_tc8_data[
                "note"
            ]
        )
    )
def test_admin_add_multiple_shifts_same_doctor_same_day(
        driver,
        doctor_schedule_tc9_data):
    """
    TC-DS-ADMIN-009:
    Một bác sĩ được phép làm
    nhiều ca khác nhau trong cùng ngày.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)

    schedule_page.select_doctor(
        doctor_schedule_tc9_data[
            "doctor_name"
        ]
    )

    schedule_page.select_work_date_day_8()

    schedule_page.select_shift(
        "Ca tối: 17:30 - 21:00"
    )

    schedule_page.select_status(
        doctor_schedule_tc9_data[
            "status_form"
        ]
    )

    schedule_page.enter_note(
        "Ca tối"
    )

    schedule_page.click_add_button()

    schedule_page.scroll_to_success_message()

    assert (
        schedule_page.get_success_message()
        == "Thêm lịch làm việc thành công!"
    )

    assert (
        doctor_schedule_tc9_data[
            "schedule_api"
        ].count_matching_schedules(
            doctor_schedule_tc9_data[
                "doctor_name"
            ],
            doctor_schedule_tc9_data[
                "work_date_api"
            ],
            "evening"
        )
        == 1
    )

    schedule_page.select_doctor(
        doctor_schedule_tc9_data[
            "doctor_name"
        ]
    )

    schedule_page.select_work_date_day_8()

    schedule_page.select_shift(
        "Ca chiều: 13:00 - 17:00"
    )

    schedule_page.select_status(
        doctor_schedule_tc9_data[
            "status_form"
        ]
    )

    schedule_page.enter_note(
        "Ca chiều"
    )

    schedule_page.click_add_button()

    schedule_page.scroll_to_success_message()

    assert (
        schedule_page.get_success_message()
        == "Thêm lịch làm việc thành công!"
    )

    assert (
        doctor_schedule_tc9_data[
            "schedule_api"
        ].count_matching_schedules(
            doctor_schedule_tc9_data[
                "doctor_name"
            ],
            doctor_schedule_tc9_data[
                "work_date_api"
            ],
            "evening"
        )
        == 1
    )

    assert (
        doctor_schedule_tc9_data[
            "schedule_api"
        ].count_matching_schedules(
            doctor_schedule_tc9_data[
                "doctor_name"
            ],
            doctor_schedule_tc9_data[
                "work_date_api"
            ],
            "afternoon"
        )
        == 1
    )

    assert (
        schedule_page.scroll_to_schedule_in_list(
            doctor_schedule_tc9_data[
                "doctor_name"
            ],
            doctor_schedule_tc9_data[
                "work_date_list"
            ],
            "Ca chiều",
            doctor_schedule_tc9_data[
                "status_display"
            ],
            "Ca chiều"
        )
    )

    assert (
        schedule_page.is_schedule_present_in_list(
            doctor_schedule_tc9_data[
                "doctor_name"
            ],
            doctor_schedule_tc9_data[
                "work_date_list"
            ],
            "Ca chiều",
            doctor_schedule_tc9_data[
                "status_display"
            ],
            "Ca chiều"
        )
    )

    assert (
        schedule_page.scroll_to_schedule_in_list(
            doctor_schedule_tc9_data[
                "doctor_name"
            ],
            doctor_schedule_tc9_data[
                "work_date_list"
            ],
            "Ca tối",
            doctor_schedule_tc9_data[
                "status_display"
            ],
            "Ca tối"
        )
    )

    assert (
        schedule_page.is_schedule_present_in_list(
            doctor_schedule_tc9_data[
                "doctor_name"
            ],
            doctor_schedule_tc9_data[
                "work_date_list"
            ],
            "Ca tối",
            doctor_schedule_tc9_data[
                "status_display"
            ],
            "Ca tối"
        )
    )
def test_admin_add_same_shift_for_different_doctors(
        driver,
        doctor_schedule_tc10_data):
    """
    TC-DS-ADMIN-010:
    Nhiều bác sĩ được phép làm
    cùng ngày và cùng ca.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)

    schedule_page.select_doctor(
        "Tran Binh"
    )

    schedule_page.select_work_date_day_8()

    schedule_page.select_shift(
        doctor_schedule_tc10_data[
            "shift_form"
        ]
    )

    schedule_page.select_status(
        doctor_schedule_tc10_data[
            "status_form"
        ]
    )

    schedule_page.enter_note(
        "Ca sáng Tran Binh"
    )

    schedule_page.click_add_button()

    schedule_page.scroll_to_success_message()

    assert (
        schedule_page.get_success_message()
        == "Thêm lịch làm việc thành công!"
    )

    schedule_page.select_doctor(
        "Ly Minh"
    )

    schedule_page.select_work_date_day_8()

    schedule_page.select_shift(
        doctor_schedule_tc10_data[
            "shift_form"
        ]
    )

    schedule_page.select_status(
        doctor_schedule_tc10_data[
            "status_form"
        ]
    )

    schedule_page.enter_note(
        "Ca sáng Ly Minh"
    )

    schedule_page.click_add_button()

    schedule_page.scroll_to_success_message()

    assert (
        schedule_page.get_success_message()
        == "Thêm lịch làm việc thành công!"
    )

    assert (
        doctor_schedule_tc10_data[
            "schedule_api"
        ].count_matching_schedules(
            "Tran Binh",
            doctor_schedule_tc10_data[
                "work_date_api"
            ],
            "morning"
        )
        == 1
    )

    assert (
        doctor_schedule_tc10_data[
            "schedule_api"
        ].count_matching_schedules(
            "Ly Minh",
            doctor_schedule_tc10_data[
                "work_date_api"
            ],
            "morning"
        )
        == 1
    )

    assert (
        schedule_page.scroll_to_schedule_in_list(
            "Tran Binh",
            doctor_schedule_tc10_data[
                "work_date_list"
            ],
            doctor_schedule_tc10_data[
                "shift_name"
            ],
            doctor_schedule_tc10_data[
                "status_display"
            ],
            "Ca sáng Tran Binh"
        )
    )

    assert (
        schedule_page.is_schedule_present_in_list(
            "Tran Binh",
            doctor_schedule_tc10_data[
                "work_date_list"
            ],
            doctor_schedule_tc10_data[
                "shift_name"
            ],
            doctor_schedule_tc10_data[
                "status_display"
            ],
            "Ca sáng Tran Binh"
        )
    )

    assert (
        schedule_page.scroll_to_schedule_in_list(
            "Ly Minh",
            doctor_schedule_tc10_data[
                "work_date_list"
            ],
            doctor_schedule_tc10_data[
                "shift_name"
            ],
            doctor_schedule_tc10_data[
                "status_display"
            ],
            "Ca sáng Ly Minh"
        )
    )

    assert (
        schedule_page.is_schedule_present_in_list(
            "Ly Minh",
            doctor_schedule_tc10_data[
                "work_date_list"
            ],
            doctor_schedule_tc10_data[
                "shift_name"
            ],
            doctor_schedule_tc10_data[
                "status_display"
            ],
            "Ca sáng Ly Minh"
        )
    )

    assert (
        schedule_page.is_schedule_present_in_week_view(
            "Tran Binh",
            doctor_schedule_tc10_data[
                "work_date_week"
            ],
            "Ca sáng",
            "Có lịch",
            "Ca sáng Tran Binh"
        )
    )

    assert (
        schedule_page.is_schedule_present_in_week_view(
            "Ly Minh",
            doctor_schedule_tc10_data[
                "work_date_week"
            ],
            "Ca sáng",
            "Có lịch",
            "Ca sáng Ly Minh"
        )
    )
def test_admin_cannot_add_conflicting_schedule_status(
        driver,
        doctor_schedule_tc11_data):
    """
    TC-DS-ADMIN-011:
    Không cho phép tồn tại hai trạng thái
    mâu thuẫn cho cùng bác sĩ, ngày và ca.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)

    schedule_page.select_doctor(
        doctor_schedule_tc11_data[
            "doctor_name"
        ]
    )

    schedule_page.select_work_date_day_8()

    schedule_page.select_shift(
        doctor_schedule_tc11_data[
            "shift_form"
        ]
    )

    schedule_page.select_status(
        "Có lịch làm việc"
    )

    schedule_page.enter_note(
        "Ca sáng"
    )

    schedule_page.click_add_button()

    schedule_page.scroll_to_success_message()

    assert (
        schedule_page.get_success_message()
        == "Thêm lịch làm việc thành công!"
    )

    assert (
        doctor_schedule_tc11_data[
            "schedule_api"
        ].count_matching_schedules(
            doctor_schedule_tc11_data[
                "doctor_name"
            ],
            doctor_schedule_tc11_data[
                "work_date_api"
            ],
            "morning"
        )
        == 1
    )

    schedule_page.select_doctor(
        doctor_schedule_tc11_data[
            "doctor_name"
        ]
    )

    schedule_page.select_work_date_day_8()

    schedule_page.select_shift(
        doctor_schedule_tc11_data[
            "shift_form"
        ]
    )

    schedule_page.select_status(
        "Không làm việc"
    )

    schedule_page.enter_note(
        "Nghỉ phép"
    )

    schedule_page.click_add_button()

    schedule_page.scroll_to_success_message()

    assert (
        schedule_page.get_success_message()
        != "Thêm lịch làm việc thành công!"
    )

    assert (
        doctor_schedule_tc11_data[
            "schedule_api"
        ].count_matching_schedules(
            doctor_schedule_tc11_data[
                "doctor_name"
            ],
            doctor_schedule_tc11_data[
                "work_date_api"
            ],
            "morning"
        )
        == 1
    )

    assert (
        schedule_page.scroll_to_schedule_in_list(
            doctor_schedule_tc11_data[
                "doctor_name"
            ],
            doctor_schedule_tc11_data[
                "work_date_list"
            ],
            doctor_schedule_tc11_data[
                "shift_name"
            ],
            "Có lịch",
            "Ca sáng"
        )
    )

    assert (
        schedule_page.is_schedule_present_in_list(
            doctor_schedule_tc11_data[
                "doctor_name"
            ],
            doctor_schedule_tc11_data[
                "work_date_list"
            ],
            doctor_schedule_tc11_data[
                "shift_name"
            ],
            "Có lịch",
            "Ca sáng"
        )
    )

    assert not (
        schedule_page.is_schedule_present_in_list(
            doctor_schedule_tc11_data[
                "doctor_name"
            ],
            doctor_schedule_tc11_data[
                "work_date_list"
            ],
            doctor_schedule_tc11_data[
                "shift_name"
            ],
            "Không làm",
            "Nghỉ phép"
        )
    )
def test_admin_click_add_schedule_multiple_times(
        driver,
        doctor_schedule_tc12_data):
    """
    TC-DS-ADMIN-012:
    Nhấn nút Thêm lịch nhiều lần liên tục
    không được tạo nhiều bản ghi trùng nhau.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)

    schedule_page.select_doctor(
        doctor_schedule_tc12_data[
            "doctor_name"
        ]
    )

    schedule_page.select_work_date_day_8()

    schedule_page.select_shift(
        doctor_schedule_tc12_data[
            "shift_form"
        ]
    )

    schedule_page.select_status(
        doctor_schedule_tc12_data[
            "status_form"
        ]
    )

    schedule_page.enter_note(
        doctor_schedule_tc12_data[
            "note"
        ]
    )
    schedule_page.click_add_button_multiple_times(
        times=3
    )
    assert (
        doctor_schedule_tc12_data[
            "schedule_api"
        ].count_matching_schedules(
            doctor_schedule_tc12_data[
                "doctor_name"
            ],
            doctor_schedule_tc12_data[
                "work_date_api"
            ],
            "afternoon"
        )
        == 1
    )

    assert (
        schedule_page.scroll_to_schedule_in_list(
            doctor_schedule_tc12_data[
                "doctor_name"
            ],
            doctor_schedule_tc12_data[
                "work_date_list"
            ],
            doctor_schedule_tc12_data[
                "shift_name"
            ],
            doctor_schedule_tc12_data[
                "status_display"
            ],
            doctor_schedule_tc12_data[
                "note"
            ]
        )
    )

    assert (
        schedule_page.is_schedule_present_in_list(
            doctor_schedule_tc12_data[
                "doctor_name"
            ],
            doctor_schedule_tc12_data[
                "work_date_list"
            ],
            doctor_schedule_tc12_data[
                "shift_name"
            ],
            doctor_schedule_tc12_data[
                "status_display"
            ],
            doctor_schedule_tc12_data[
                "note"
            ]
        )
    )
def test_admin_form_resets_after_add_schedule_success(
        driver,
        doctor_schedule_tc13_data):
    """
    TC-DS-ADMIN-013:
    Kiểm tra form được reset
    sau khi thêm lịch thành công.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)

    schedule_page.select_doctor(
        doctor_schedule_tc13_data[
            "doctor_name"
        ]
    )

    schedule_page.select_work_date_day_8()

    schedule_page.select_shift(
        doctor_schedule_tc13_data[
            "shift_form"
        ]
    )

    schedule_page.select_status(
        doctor_schedule_tc13_data[
            "status_form"
        ]
    )

    schedule_page.enter_note(
        doctor_schedule_tc13_data[
            "note"
        ]
    )

    assert (
        schedule_page
        .get_selected_doctor_text()
        == doctor_schedule_tc13_data[
            "doctor_name"
        ]
    )

    assert (
        schedule_page.get_work_date_value()
        == doctor_schedule_tc13_data[
            "work_date_list"
        ]
    )

    assert (
        schedule_page
        .get_selected_shift_text()
        == doctor_schedule_tc13_data[
            "shift_form"
        ]
    )

    assert (
        schedule_page
        .get_selected_status_text()
        == doctor_schedule_tc13_data[
            "status_form"
        ]
    )

    assert (
        schedule_page.get_note_value()
        == doctor_schedule_tc13_data[
            "note"
        ]
    )

    schedule_page.click_add_button()

    schedule_page.scroll_to_success_message()

    assert (
        schedule_page.get_success_message()
        == "Thêm lịch làm việc thành công!"
    )

    assert (
        schedule_page
        .get_selected_doctor_text()
        == "-- Chọn bác sĩ --"
    )

    assert (
        schedule_page.get_work_date_value()
        == ""
    )

    assert (
        schedule_page
        .get_selected_shift_text()
        == "Ca sáng: 07:00 - 11:30"
    )

    assert (
        schedule_page
        .get_selected_status_text()
        == "Có lịch làm việc"
    )

    assert (
        schedule_page.get_note_value()
        == ""
    )

    assert (
        doctor_schedule_tc13_data[
            "schedule_api"
        ].count_matching_schedules(
            doctor_schedule_tc13_data[
                "doctor_name"
            ],
            doctor_schedule_tc13_data[
                "work_date_api"
            ],
            "evening"
        )
        == 1
    )

    assert (
        schedule_page.scroll_to_schedule_in_list(
            doctor_schedule_tc13_data[
                "doctor_name"
            ],
            doctor_schedule_tc13_data[
                "work_date_list"
            ],
            doctor_schedule_tc13_data[
                "shift_name"
            ],
            doctor_schedule_tc13_data[
                "status_display"
            ],
            doctor_schedule_tc13_data[
                "note"
            ]
        )
    )

    assert (
        schedule_page.is_schedule_present_in_list(
            doctor_schedule_tc13_data[
                "doctor_name"
            ],
            doctor_schedule_tc13_data[
                "work_date_list"
            ],
            doctor_schedule_tc13_data[
                "shift_name"
            ],
            doctor_schedule_tc13_data[
                "status_display"
            ],
            doctor_schedule_tc13_data[
                "note"
            ]
        )
    )

def test_admin_filters_schedule_by_doctor(
        driver):
    """
    TC-DS-ADMIN-014:
    Kiểm tra Admin có thể lọc lịch làm việc
    theo một bác sĩ cụ thể.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)

    schedule_page.select_filter_doctor(
        "Tran Binh"
    )
    schedule_page.scroll_to_week_view()
    assert (
        schedule_page
        .get_selected_filter_doctor_text()
        == "Tran Binh"
    )

    doctor_names = (
        schedule_page
        .get_week_view_doctor_names()
    )

    assert len(doctor_names) > 0

    assert all(
        doctor_name == "Tran Binh"
        for doctor_name in doctor_names
    )
def test_admin_resets_doctor_schedule_filter(
        driver):
    """
    TC-DS-ADMIN-015:
    Kiểm tra hiển thị lại lịch của tất cả bác sĩ
    sau khi bỏ điều kiện lọc.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)

    doctor_names_before = (
        schedule_page.get_week_view_doctor_names()
    )

    assert len(doctor_names_before) > 0

    assert any(
        doctor_name != "Tran Binh"
        for doctor_name in doctor_names_before
    )

    schedule_page.select_filter_doctor(
        "Tran Binh"
    )

    assert (
        schedule_page.get_selected_filter_doctor_text()
        == "Tran Binh"
    )

    doctor_names_filtered = (
        schedule_page.get_week_view_doctor_names()
    )

    assert len(doctor_names_filtered) > 0

    assert all(
        doctor_name == "Tran Binh"
        for doctor_name in doctor_names_filtered
    )

    schedule_page.select_filter_doctor(
        "Tất cả bác sĩ"
    )

    schedule_page.scroll_to_week_view()

    assert (
        schedule_page.get_selected_filter_doctor_text()
        == "Tất cả bác sĩ"
    )

    doctor_names_after = (
        schedule_page.get_week_view_doctor_names()
    )

    assert sorted(doctor_names_after) == sorted(
        doctor_names_before
    )
def test_admin_views_previous_week_schedule(
        driver):
    """
    TC-DS-ADMIN-016:
    Kiểm tra Admin có thể chuyển sang tuần trước
    để xem lịch làm việc.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)

    week_range_before = (
        schedule_page.get_week_range_text()
    )

    dates_before = (
        schedule_page.get_week_header_dates()
    )

    assert len(dates_before) == 7

    schedule_page.click_previous_week()

    week_range_after = (
        schedule_page.get_week_range_text()
    )

    dates_after = (
        schedule_page.get_week_header_dates()
    )

    assert week_range_after != week_range_before

    assert len(dates_after) == 7

    first_date_before = datetime.strptime(
        dates_before[0],
        "%d/%m/%Y"
    )

    first_date_after = datetime.strptime(
        dates_after[0],
        "%d/%m/%Y"
    )

    assert (
        first_date_after
        == first_date_before - timedelta(days=7)
    )

    schedule_page.scroll_to_week_view()

    time.sleep(2)

def test_admin_views_next_week_schedule(
        driver):
    """
    TC-DS-ADMIN-017:
    Kiểm tra Admin có thể chuyển sang tuần sau
    để xem lịch làm việc.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)

    week_range_before = (
        schedule_page.get_week_range_text()
    )

    dates_before = (
        schedule_page.get_week_header_dates()
    )

    assert len(dates_before) == 7

    schedule_page.click_next_week()

    week_range_after = (
        schedule_page.get_week_range_text()
    )

    dates_after = (
        schedule_page.get_week_header_dates()
    )

    assert week_range_after != week_range_before

    assert len(dates_after) == 7

    first_date_before = datetime.strptime(
        dates_before[0],
        "%d/%m/%Y"
    )

    first_date_after = datetime.strptime(
        dates_after[0],
        "%d/%m/%Y"
    )

    assert (
        first_date_after
        == first_date_before + timedelta(days=7)
    )

    schedule_page.scroll_to_week_view()

    time.sleep(2)

def test_admin_updates_doctor_schedule(
        driver,
        doctor_schedule_tc18_data):
    """
    TC-DS-ADMIN-018:
    Kiểm tra Admin cập nhật lịch làm việc
    của bác sĩ thành công.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)

    assert (
        schedule_page.click_edit_schedule_by_id(
            doctor_schedule_tc18_data[
                "schedule_id"
            ]
        )
    )

    assert (
        schedule_page.get_update_form_title()
        == "Cập nhật lịch làm việc"
    )

    assert (
        schedule_page.get_selected_doctor_text()
        == doctor_schedule_tc18_data[
            "doctor_name"
        ]
    )

    assert (
        schedule_page.get_work_date_value()
        == doctor_schedule_tc18_data[
            "work_date_list"
        ]
    )

    assert (
        schedule_page.get_selected_shift_text()
        == doctor_schedule_tc18_data[
            "shift_form"
        ]
    )

    assert (
        schedule_page.get_selected_status_text()
        == doctor_schedule_tc18_data[
            "status_before_form"
        ]
    )

    assert (
        schedule_page.get_note_value()
        == doctor_schedule_tc18_data[
            "note_before"
        ]
    )

    time.sleep(2)
    schedule_page.select_status(
        doctor_schedule_tc18_data[
            "status_after_form"
        ]
    )

    assert (
        schedule_page.get_selected_status_text()
        == doctor_schedule_tc18_data[
            "status_after_form"
        ]
    )

    schedule_page.enter_note(
        doctor_schedule_tc18_data[
            "note_after"
        ]
    )

    assert (
        schedule_page.get_note_value()
        == doctor_schedule_tc18_data[
            "note_after"
        ]
    )

    schedule_page.click_update_button()

    schedule_page.scroll_to_success_message()

    assert (
        schedule_page.get_success_message()
        == "Cập nhật lịch làm việc thành công!"
    )
    assert (
        schedule_page.scroll_to_schedule_in_list(
            doctor_schedule_tc18_data[
                "doctor_name"
            ],
            doctor_schedule_tc18_data[
                "work_date_list"
            ],
            doctor_schedule_tc18_data[
                "shift_name"
            ],
            doctor_schedule_tc18_data[
                "status_after_display"
            ],
            doctor_schedule_tc18_data[
                "note_after"
            ]
        )
    )

    time.sleep(2)

def test_admin_cancels_edit_doctor_schedule(
        driver,
        doctor_schedule_tc19_data):
    """
    TC-DS-ADMIN-019:
    Kiểm tra chức năng Hủy sửa
    không làm thay đổi dữ liệu lịch.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)

    assert (
        schedule_page.click_edit_schedule_by_id(
            doctor_schedule_tc19_data[
                "schedule_id"
            ]
        )
    )

    assert (
        schedule_page.get_update_form_title()
        == "Cập nhật lịch làm việc"
    )

    assert (
        schedule_page.get_selected_status_text()
        == doctor_schedule_tc19_data[
            "status_before_form"
        ]
    )

    assert (
        schedule_page.get_note_value()
        == doctor_schedule_tc19_data[
            "note_before"
        ]
    )

    schedule_page.select_status(
        doctor_schedule_tc19_data[
            "status_changed_form"
        ]
    )

    schedule_page.enter_note(
        doctor_schedule_tc19_data[
            "note_changed"
        ]
    )

    assert (
        schedule_page.get_selected_status_text()
        == doctor_schedule_tc19_data[
            "status_changed_form"
        ]
    )

    assert (
        schedule_page.get_note_value()
        == doctor_schedule_tc19_data[
            "note_changed"
        ]
    )

    schedule_page.click_cancel_edit_button()

    assert (
        schedule_page.get_form_title()
        == "Thêm lịch làm việc"
    )

    assert (
        schedule_page.scroll_to_schedule_in_list(
            doctor_schedule_tc19_data[
                "doctor_name"
            ],
            doctor_schedule_tc19_data[
                "work_date_list"
            ],
            doctor_schedule_tc19_data[
                "shift_name"
            ],
            doctor_schedule_tc19_data[
                "status_before_display"
            ],
            doctor_schedule_tc19_data[
                "note_before"
            ]
        )
    )

    assert (
        schedule_page.is_schedule_present_in_list(
            doctor_schedule_tc19_data[
                "doctor_name"
            ],
            doctor_schedule_tc19_data[
                "work_date_list"
            ],
            doctor_schedule_tc19_data[
                "shift_name"
            ],
            doctor_schedule_tc19_data[
                "status_before_display"
            ],
            doctor_schedule_tc19_data[
                "note_before"
            ]
        )
    )

    time.sleep(2)

def test_admin_deletes_doctor_schedule(
        driver,
        doctor_schedule_tc20_data):
    """
    TC-DS-ADMIN-020:
    Kiểm tra Admin có thể xóa
    một lịch làm việc đã tồn tại.
    """

    login_admin(driver)

    schedule_page = DoctorScheduleAdminPage(
        driver
    )

    schedule_page.open_page()

    time.sleep(2)

    assert (
        schedule_page.scroll_to_schedule_in_list(
            doctor_schedule_tc20_data[
                "doctor_name"
            ],
            doctor_schedule_tc20_data[
                "work_date_list"
            ],
            doctor_schedule_tc20_data[
                "shift_name"
            ],
            doctor_schedule_tc20_data[
                "status_display"
            ],
            doctor_schedule_tc20_data[
                "note"
            ]
        )
    )

    assert (
        schedule_page.is_schedule_present_in_list(
            doctor_schedule_tc20_data[
                "doctor_name"
            ],
            doctor_schedule_tc20_data[
                "work_date_list"
            ],
            doctor_schedule_tc20_data[
                "shift_name"
            ],
            doctor_schedule_tc20_data[
                "status_display"
            ],
            doctor_schedule_tc20_data[
                "note"
            ]
        )
    )

    assert (
        schedule_page.click_delete_schedule_by_id(
            doctor_schedule_tc20_data[
                "schedule_id"
            ]
        )
    )

    alert = driver.switch_to.alert

    assert (
        alert.text
        == "Bạn chắc chắn muốn xóa lịch này không?"
    )

    time.sleep(2)

    alert.accept()

    time.sleep(2)

    schedule_page.scroll_to_success_message()

    assert (
            schedule_page.get_success_message()
            == "Xóa lịch làm việc thành công!"
    )

    assert not (
        schedule_page.is_schedule_present_in_list(
            doctor_schedule_tc20_data[
                "doctor_name"
            ],
            doctor_schedule_tc20_data[
                "work_date_list"
            ],
            doctor_schedule_tc20_data[
                "shift_name"
            ],
            doctor_schedule_tc20_data[
                "status_display"
            ],
            doctor_schedule_tc20_data[
                "note"
            ]
        )
    )

    deleted_schedule = (
        doctor_schedule_tc20_data[
            "schedule_api"
        ].find_schedule(
            doctor_schedule_tc20_data[
                "doctor_name"
            ],
            doctor_schedule_tc20_data[
                "work_date_api"
            ],
            doctor_schedule_tc20_data[
                "shift_value"
            ]
        )
    )

    assert deleted_schedule is None

    time.sleep(2)