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
    Nếu không còn slot thì tự tạo thêm ca làm việc test
    trong tương lai rồi tìm lại slot.
    """

    medical_record_api = MedicalRecordApi()

    # Ưu tiên dùng slot đang có sẵn.
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

        shifts = [
            ("morning", "07:00:00", "11:30:00"),
            ("afternoon", "13:00:00", "17:00:00"),
            ("evening", "18:00:00", "21:00:00"),
        ]

        # Tìm tối đa 60 ngày tiếp theo.
        for days_ahead in range(1, 61):
            work_date = (
                datetime.now().date()
                + timedelta(days=days_ahead)
            ).strftime("%Y-%m-%d")

            for shift, start_time, end_time in shifts:
                existing_schedule = (
                    doctor_schedule_api.find_schedule(
                        doctor_name=doctor_name,
                        work_date=work_date,
                        shift=shift
                    )
                )

                # Ca này đã tồn tại thì thử ca khác.
                if existing_schedule is not None:
                    continue

                doctor_schedule_api.create_schedule(
                    doctor_name=doctor_name,
                    work_date=work_date,
                    shift=shift,
                    start_time=start_time,
                    end_time=end_time,
                    status="available",
                    note=schedule_note,
                    token=admin_token
                )

                # Sau khi tạo schedule mới,
                # kiểm tra thật sự đã có slot đặt lịch chưa.
                try:
                    return (
                        medical_record_api
                        .find_available_booking_slot(
                            doctor_id
                        )
                    )

                except AssertionError:
                    # Chưa có slot thì tiếp tục thử
                    # ca/ngày tiếp theo.
                    continue

        raise AssertionError(
            f"{schedule_note} | "
            "Không thể chuẩn bị slot đặt lịch "
            "còn trống cho bác sĩ."
        )
