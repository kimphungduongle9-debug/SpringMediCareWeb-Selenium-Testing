from api.AppointmentApi import AppointmentApi
from pages.MyAppointmentPage import MyAppointmentPage
from pages.AdminAppointmentPage import AdminAppointmentPage
from utils.data_reader import get_test_data_csv, MY_APPOINTMENT_TEST_DATA_CSV
from utils.test_reporter import report_step
from tests.helpers.my_appointment_helpers import (
    login_account,
    logout_current_user,
    create_unique_note,
    get_or_create_booking_slot,
    book_appointment_by_ui,
    cleanup_appointment,
)


def report_test_case_start(test_case_id, description):
    print()
    print("=" * 100)
    print(f"{test_case_id} | {description}")
    print("=" * 100)


# ============================================================
# TC-MYAPPOINTMENT-001
# ============================================================

def test_tc_myappointment_001(driver):
    test_case_id = "TC-MYAPPOINTMENT-001"
    description = (
        "Kiểm tra lịch hẹn sau khi Patient đặt thành công được hiển thị "
        "trong trang Lịch hẹn của tôi với trạng thái ban đầu là Chờ xác nhận."
    )

    report_test_case_start(test_case_id, description)

    test_data = get_test_data_csv(MY_APPOINTMENT_TEST_DATA_CSV, test_case_id)
    doctor_id = int(test_data["doctor_id"])
    note = create_unique_note(test_data)

    appointment_api = AppointmentApi()
    booking_slot = get_or_create_booking_slot(test_data)
    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    try:
        # Step 1: Đăng nhập bằng tài khoản Patient
        login_account(
            driver,
            test_data["patient_username"],
            test_data["patient_password"]
        )

        report_step(
            test_case_id,
            1,
            "Đăng nhập bằng tài khoản Patient thành công"
        )

        # Step 2: Thực hiện đặt một lịch khám hợp lệ
        message = book_appointment_by_ui(
            driver,
            test_data,
            booking_date,
            booking_time,
            note
        )

        expected_message = test_data["expected_booking_message"]

        assert expected_message in message, (
            f"{test_case_id} | STEP 2 FAILED | "
            f"Expected: {expected_message} | Actual: {message}"
        )

        report_step(
            test_case_id,
            2,
            "Patient thực hiện đặt một lịch khám hợp lệ",
            detail=message
        )

        # Step 3: Xác nhận hệ thống đặt lịch thành công
        created = appointment_api.find_appointment_by_note(
            doctor_id=doctor_id,
            note=note
        )

        assert created is not None, (
            f"{test_case_id} | STEP 3 FAILED | "
            "Expected: Appointment được tạo | Actual: Không tìm thấy Appointment"
        )

        report_step(
            test_case_id,
            3,
            "Hệ thống tạo lịch hẹn thành công"
        )

        # Step 4: Ghi nhận thông tin lịch vừa tạo
        appointment_id = created["appointmentId"]

        assert appointment_id, (
            f"{test_case_id} | STEP 4 FAILED | "
            "Expected: Có Appointment ID | Actual: Không lấy được Appointment ID"
        )

        report_step(
            test_case_id,
            4,
            f"Ghi nhận Appointment ID {appointment_id}, Doctor {test_data['doctor_name']}, "
            f"ngày {booking_date}, giờ {booking_time}"
        )

        # Step 5: Mở trang Lịch hẹn của tôi
        my_page = MyAppointmentPage(driver)
        my_page.open_page()

        actual_title = my_page.get_page_title()
        expected_title = "Lịch hẹn của tôi"

        assert actual_title == expected_title, (
            f"{test_case_id} | STEP 5 FAILED | "
            f"Expected: {expected_title} | Actual: {actual_title}"
        )

        report_step(
            test_case_id,
            5,
            "Mở trang Lịch hẹn của tôi thành công"
        )

        # Step 6: Tìm lịch hẹn vừa tạo
        appointment = my_page.wait_for_appointment_by_note(note)

        assert appointment is not None, (
            f"{test_case_id} | STEP 6 FAILED | "
            f"Expected: Tìm thấy lịch có note {note} | Actual: Không tìm thấy"
        )

        report_step(
            test_case_id,
            6,
            "Tìm thấy lịch hẹn vừa tạo trong danh sách"
        )

        # Step 7: Kiểm tra Doctor, ngày giờ và ghi chú
        assert appointment["doctor"] == test_data["doctor_name"], (
            f"{test_case_id} | STEP 7 FAILED | "
            f"Expected Doctor: {test_data['doctor_name']} | Actual: {appointment['doctor']}"
        )

        assert booking_date in appointment["time"], (
            f"{test_case_id} | STEP 7 FAILED | "
            f"Expected date: {booking_date} | Actual: {appointment['time']}"
        )

        assert booking_time in appointment["time"], (
            f"{test_case_id} | STEP 7 FAILED | "
            f"Expected time: {booking_time} | Actual: {appointment['time']}"
        )

        assert appointment["note"] == note, (
            f"{test_case_id} | STEP 7 FAILED | "
            f"Expected note: {note} | Actual: {appointment['note']}"
        )

        report_step(
            test_case_id,
            7,
            "Doctor, ngày giờ khám và ghi chú hiển thị đúng"
        )

        # Step 8: Kiểm tra trạng thái Chờ xác nhận
        expected_status = test_data["expected_pending_status"]
        actual_status = appointment["status"]

        assert actual_status == expected_status, (
            f"{test_case_id} | STEP 8 FAILED | "
            f"Expected: {expected_status} | Actual: {actual_status}"
        )

        report_step(
            test_case_id,
            8,
            "Lịch hẹn hiển thị trạng thái Chờ xác nhận"
        )

    finally:
        cleanup_appointment(test_data, note)


# ============================================================
# TC-MYAPPOINTMENT-002
# ============================================================

def test_tc_myappointment_002(driver):
    test_case_id = "TC-MYAPPOINTMENT-002"
    description = (
        "Kiểm tra trạng thái lịch hẹn của Patient được cập nhật "
        "sau khi Admin xác nhận lịch."
    )

    report_test_case_start(test_case_id, description)

    test_data = get_test_data_csv(MY_APPOINTMENT_TEST_DATA_CSV, test_case_id)
    doctor_id = int(test_data["doctor_id"])
    note = create_unique_note(test_data)

    appointment_api = AppointmentApi()
    booking_slot = get_or_create_booking_slot(test_data)
    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    try:
        # Step 1: Patient đặt lịch và ghi nhận thông tin
        login_account(
            driver,
            test_data["patient_username"],
            test_data["patient_password"]
        )

        message = book_appointment_by_ui(
            driver,
            test_data,
            booking_date,
            booking_time,
            note
        )

        expected_message = test_data["expected_booking_message"]

        assert expected_message in message, (
            f"{test_case_id} | STEP 1 FAILED | "
            f"Expected: {expected_message} | Actual: {message}"
        )

        created = appointment_api.find_appointment_by_note(
            doctor_id=doctor_id,
            note=note
        )

        assert created is not None, (
            f"{test_case_id} | STEP 1 FAILED | "
            "Expected: Appointment được tạo | Actual: Không tìm thấy Appointment"
        )

        appointment_id = str(created["appointmentId"])

        report_step(
            test_case_id,
            1,
            "Patient đặt lịch hợp lệ và ghi nhận thông tin lịch vừa tạo"
        )

        # Step 2: Admin đăng nhập và mở Quản lý lịch hẹn
        logout_current_user(driver)

        login_account(
            driver,
            test_data["admin_username"],
            test_data["admin_password"]
        )

        admin_page = AdminAppointmentPage(driver)
        admin_page.open_page()

        actual_title = admin_page.get_page_title()

        assert actual_title == "Quản lý lịch hẹn", (
            f"{test_case_id} | STEP 2 FAILED | "
            f"Expected: Quản lý lịch hẹn | Actual: {actual_title}"
        )

        report_step(
            test_case_id,
            2,
            "Admin đăng nhập và mở trang Quản lý lịch hẹn thành công"
        )

        # Step 3: Tìm đúng lịch đang Chờ xác nhận
        actual_id = admin_page.get_appointment_id_by_note(note)
        actual_status = admin_page.get_status_by_note(note)
        expected_status = test_data["expected_pending_status"]

        assert actual_id == appointment_id, (
            f"{test_case_id} | STEP 3 FAILED | "
            f"Expected ID: {appointment_id} | Actual: {actual_id}"
        )

        assert actual_status == expected_status, (
            f"{test_case_id} | STEP 3 FAILED | "
            f"Expected: {expected_status} | Actual: {actual_status}"
        )

        report_step(
            test_case_id,
            3,
            "Tìm thấy đúng lịch đang ở trạng thái Chờ xác nhận"
        )

        # Step 4: Admin xác nhận lịch hẹn
        assert admin_page.is_confirm_button_present(note), (
            f"{test_case_id} | STEP 4 FAILED | "
            "Expected: Có nút Xác nhận | Actual: Không tìm thấy"
        )

        admin_page.click_confirm(note)
        confirm_message = admin_page.get_confirm_success_message()

        assert confirm_message == "Xác nhận lịch hẹn thành công.", (
            f"{test_case_id} | STEP 4 FAILED | "
            f"Expected: Xác nhận lịch hẹn thành công. | Actual: {confirm_message}"
        )

        report_step(
            test_case_id,
            4,
            "Admin xác nhận lịch hẹn thành công",
            detail=confirm_message
        )

        # Step 5: Kiểm tra trạng thái trên Admin
        admin_page.open_page()

        admin_status = admin_page.get_status_by_note(note)
        expected_confirmed = test_data["expected_confirmed_status"]

        assert admin_status == expected_confirmed, (
            f"{test_case_id} | STEP 5 FAILED | "
            f"Expected: {expected_confirmed} | Actual: {admin_status}"
        )

        report_step(
            test_case_id,
            5,
            "Lịch hẹn trên trang Admin được cập nhật thành Đã xác nhận"
        )

        # Step 6: Đăng nhập lại bằng Patient
        logout_current_user(driver)

        login_account(
            driver,
            test_data["patient_username"],
            test_data["patient_password"]
        )

        report_step(
            test_case_id,
            6,
            "Đăng nhập lại bằng Patient sở hữu lịch hẹn"
        )

        # Step 7: Patient tìm lịch vừa được xác nhận
        my_page = MyAppointmentPage(driver)
        my_page.open_page()

        appointment = my_page.wait_for_appointment_by_note(note)

        assert appointment is not None, (
            f"{test_case_id} | STEP 7 FAILED | "
            "Expected: Patient tìm thấy lịch | Actual: Không tìm thấy"
        )

        report_step(
            test_case_id,
            7,
            "Patient tìm thấy lịch vừa được Admin xử lý"
        )

        # Step 8: Kiểm tra thông tin và trạng thái
        assert appointment["doctor"] == test_data["doctor_name"], (
            f"{test_case_id} | STEP 8 FAILED | "
            f"Expected Doctor: {test_data['doctor_name']} | Actual: {appointment['doctor']}"
        )

        assert booking_date in appointment["time"], (
            f"{test_case_id} | STEP 8 FAILED | "
            f"Expected date: {booking_date} | Actual: {appointment['time']}"
        )

        assert booking_time in appointment["time"], (
            f"{test_case_id} | STEP 8 FAILED | "
            f"Expected time: {booking_time} | Actual: {appointment['time']}"
        )

        assert appointment["note"] == note, (
            f"{test_case_id} | STEP 8 FAILED | "
            f"Expected note: {note} | Actual: {appointment['note']}"
        )

        assert appointment["status"] == expected_confirmed, (
            f"{test_case_id} | STEP 8 FAILED | "
            f"Expected: {expected_confirmed} | Actual: {appointment['status']}"
        )

        report_step(
            test_case_id,
            8,
            "Thông tin lịch không thay đổi và trạng thái là Đã xác nhận"
        )

    finally:
        cleanup_appointment(test_data, note)


# ============================================================
# TC-MYAPPOINTMENT-003
# ============================================================

def test_tc_myappointment_003(driver):
    test_case_id = "TC-MYAPPOINTMENT-003"
    description = (
        "Kiểm tra trạng thái lịch hẹn của Patient "
        "sau khi Admin thực hiện hủy lịch."
    )

    report_test_case_start(test_case_id, description)

    test_data = get_test_data_csv(MY_APPOINTMENT_TEST_DATA_CSV, test_case_id)
    doctor_id = int(test_data["doctor_id"])
    note = create_unique_note(test_data)

    appointment_api = AppointmentApi()
    booking_slot = get_or_create_booking_slot(test_data)
    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    # Step 1: Patient đặt một lịch hợp lệ
    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    message = book_appointment_by_ui(
        driver,
        test_data,
        booking_date,
        booking_time,
        note
    )

    expected_message = test_data["expected_booking_message"]

    assert expected_message in message, (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected: {expected_message} | Actual: {message}"
    )

    created = appointment_api.find_appointment_by_note(
        doctor_id=doctor_id,
        note=note
    )

    assert created is not None, (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected: Appointment được tạo | Actual: Không tìm thấy Appointment"
    )

    appointment_id = str(created["appointmentId"])

    report_step(
        test_case_id,
        1,
        "Patient đặt lịch hợp lệ và ghi nhận thông tin lịch vừa tạo"
    )

    # Step 2: Admin đăng nhập và mở Quản lý lịch hẹn
    logout_current_user(driver)

    login_account(
        driver,
        test_data["admin_username"],
        test_data["admin_password"]
    )

    admin_page = AdminAppointmentPage(driver)
    admin_page.open_page()

    actual_title = admin_page.get_page_title()

    assert actual_title == "Quản lý lịch hẹn", (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected: Quản lý lịch hẹn | Actual: {actual_title}"
    )

    report_step(
        test_case_id,
        2,
        "Admin đăng nhập và mở trang Quản lý lịch hẹn"
    )

    # Step 3: Tìm đúng lịch đang Chờ xác nhận
    actual_id = admin_page.get_appointment_id_by_note(note)
    actual_status = admin_page.get_status_by_note(note)
    expected_pending = test_data["expected_pending_status"]

    assert actual_id == appointment_id, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected ID: {appointment_id} | Actual: {actual_id}"
    )

    assert actual_status == expected_pending, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: {expected_pending} | Actual: {actual_status}"
    )

    report_step(
        test_case_id,
        3,
        "Tìm thấy đúng lịch đang ở trạng thái Chờ xác nhận"
    )

    # Step 4: Admin hủy lịch
    assert admin_page.is_cancel_button_present(note), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Có nút Hủy | Actual: Không tìm thấy"
    )

    admin_page.click_cancel(note)
    cancel_message = admin_page.get_cancel_success_message()

    assert cancel_message == "Hủy lịch hẹn thành công.", (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: Hủy lịch hẹn thành công. | Actual: {cancel_message}"
    )

    report_step(
        test_case_id,
        4,
        "Admin hủy lịch hẹn thành công",
        detail=cancel_message
    )

    # Step 5: Kiểm tra trạng thái Đã hủy trên Admin
    admin_page.open_page()

    actual_status = admin_page.get_status_by_note(note)
    expected_cancelled = test_data["expected_cancelled_status"]

    assert actual_status == expected_cancelled, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: {expected_cancelled} | Actual: {actual_status}"
    )

    report_step(
        test_case_id,
        5,
        "Lịch hẹn trên trang Admin được cập nhật thành Đã hủy"
    )

    # Step 6: Đăng nhập lại bằng Patient
    logout_current_user(driver)

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    report_step(
        test_case_id,
        6,
        "Đăng nhập lại bằng Patient sở hữu lịch hẹn"
    )

    # Step 7: Patient tìm lịch vừa bị hủy
    my_page = MyAppointmentPage(driver)
    my_page.open_page()

    appointment = my_page.wait_for_appointment_by_note(note)

    assert appointment is not None, (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected: Patient tìm thấy lịch đã hủy | Actual: Không tìm thấy"
    )

    report_step(
        test_case_id,
        7,
        "Patient tìm thấy lịch vừa bị Admin hủy"
    )

    # Step 8: Kiểm tra dữ liệu và trạng thái Đã hủy
    assert appointment["doctor"] == test_data["doctor_name"], (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected Doctor: {test_data['doctor_name']} | Actual: {appointment['doctor']}"
    )

    assert booking_date in appointment["time"], (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected date: {booking_date} | Actual: {appointment['time']}"
    )

    assert booking_time in appointment["time"], (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected time: {booking_time} | Actual: {appointment['time']}"
    )

    assert appointment["note"] == note, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected note: {note} | Actual: {appointment['note']}"
    )

    assert appointment["status"] == expected_cancelled, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected: {expected_cancelled} | Actual: {appointment['status']}"
    )

    report_step(
        test_case_id,
        8,
        "Lịch vẫn tồn tại, thông tin không thay đổi và trạng thái là Đã hủy"
    )