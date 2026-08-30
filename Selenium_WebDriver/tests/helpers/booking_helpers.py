from datetime import datetime, timedelta

from pages.LoginPage import LoginPage
from pages.BookingPage import BookingPage
from pages.DoctorPage import DoctorPage

from api.MedicalRecordApi import MedicalRecordApi
from api.DoctorScheduleApi import DoctorScheduleApi


BOOKING_URL = "http://localhost:3000/booking?doctorId=1"

def login_account(driver, username, password):
    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        username,
        password,
        delay=0
    )

    login_page.wait.until(
        lambda d: d.current_url == "http://localhost:3000/"
    )

    assert driver.current_url == "http://localhost:3000/", (
        "Đăng nhập không thành công. "
        f"Expected URL: http://localhost:3000/ | "
        f"Actual URL: {driver.current_url}"
    )
def open_tran_binh_booking_page(driver):
    doctor_page = DoctorPage(driver)

    doctor_page.open_page()

    doctor_page.book_tran_binh()

    booking_page = BookingPage(driver)

    booking_page.wait.until(
        lambda d: d.current_url == BOOKING_URL
    )

    assert driver.current_url == BOOKING_URL, (
        "Không mở đúng trang đặt lịch của bác sĩ Trần Bình. "
        f"Expected URL: {BOOKING_URL} | "
        f"Actual URL: {driver.current_url}"
    )

    return booking_page


def get_or_create_booking_slot(
        doctor_id,
        test_data,
        schedule_note
):
    """
    Tìm slot đặt lịch còn trống.
    Nếu không còn slot thì tự tạo một ca làm việc test
    trong tương lai rồi tìm lại slot.
    """

    medical_record_api = MedicalRecordApi()

    try:
        return medical_record_api.find_available_booking_slot(
            doctor_id
        )

    except AssertionError:
        doctor_schedule_api = DoctorScheduleApi()

        admin_token = doctor_schedule_api.get_token(
            test_data["admin_username"],
            test_data["admin_password"]
        )

        doctor_name = "Tran Binh"
        created_work_date = None

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

            if existing_schedule is None:
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
            "Không thể chuẩn bị lịch làm việc cho bác sĩ."
        )

        return medical_record_api.find_available_booking_slot(
            doctor_id
        )