import time

from api.AppointmentApi import AppointmentApi

from pages.MyAppointmentPage import MyAppointmentPage
from pages.AdminAppointmentPage import AdminAppointmentPage
from pages.DoctorAppointmentPage import DoctorAppointmentPage
from pages.DoctorExaminationPage import DoctorExaminationPage

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
# TC-MYAPPOINTMENT-004
# ============================================================

def test_tc_myappointment_004(driver):
    test_case_id = "TC-MYAPPOINTMENT-004"
    description = (
        "Kiểm tra lịch hẹn được cập nhật đúng xuyên suốt từ khi Patient đặt lịch, "
        "Admin xác nhận đến khi Doctor hoàn thành khám."
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

        created_api = appointment_api.find_appointment_by_note(
            doctor_id=doctor_id,
            note=note
        )

        assert created_api is not None, (
            f"{test_case_id} | STEP 1 FAILED | "
            "Expected: Appointment được tạo | Actual: Không tìm thấy Appointment"
        )

        appointment_id = str(created_api["appointmentId"])

        report_step(
            test_case_id,
            1,
            f"Patient đặt lịch thành công và ghi nhận Appointment ID {appointment_id}"
        )

        # Step 2: Kiểm tra lịch vừa tạo ở trạng thái Chờ xác nhận
        my_page = MyAppointmentPage(driver)
        my_page.open_page()

        pending = my_page.wait_for_appointment_by_note(note)

        assert pending is not None, (
            f"{test_case_id} | STEP 2 FAILED | "
            "Expected: Tìm thấy lịch vừa tạo | Actual: Không tìm thấy"
        )

        expected_pending = test_data["expected_pending_status"]

        assert pending["status"] == expected_pending, (
            f"{test_case_id} | STEP 2 FAILED | "
            f"Expected: {expected_pending} | Actual: {pending['status']}"
        )

        original_id = pending["id"]
        original_doctor = pending["doctor"]
        original_time = pending["time"]
        original_note = pending["note"]

        report_step(
            test_case_id,
            2,
            "Lịch vừa tạo hiển thị trạng thái Chờ xác nhận"
        )

        # Step 3: Admin tìm lịch và xác nhận
        logout_current_user(driver)

        login_account(
            driver,
            test_data["admin_username"],
            test_data["admin_password"]
        )

        admin_page = AdminAppointmentPage(driver)
        admin_page.open_page()

        actual_id = admin_page.get_appointment_id_by_note(note)
        actual_status = admin_page.get_status_by_note(note)

        assert actual_id == appointment_id, (
            f"{test_case_id} | STEP 3 FAILED | "
            f"Expected ID: {appointment_id} | Actual: {actual_id}"
        )

        assert actual_status == expected_pending, (
            f"{test_case_id} | STEP 3 FAILED | "
            f"Expected: {expected_pending} | Actual: {actual_status}"
        )

        assert admin_page.is_confirm_button_present(note), (
            f"{test_case_id} | STEP 3 FAILED | "
            "Expected: Có nút Xác nhận | Actual: Không tìm thấy"
        )

        admin_page.click_confirm(note)
        confirm_message = admin_page.get_confirm_success_message()

        assert confirm_message == "Xác nhận lịch hẹn thành công.", (
            f"{test_case_id} | STEP 3 FAILED | "
            f"Expected: Xác nhận lịch hẹn thành công. | Actual: {confirm_message}"
        )

        report_step(
            test_case_id,
            3,
            "Admin tìm đúng lịch và xác nhận thành công",
            detail=confirm_message
        )

        # Step 4: Kiểm tra lịch chuyển thành Đã xác nhận
        admin_page.open_page()

        expected_confirmed = test_data["expected_confirmed_status"]
        confirmed_status = admin_page.get_status_by_note(note)

        assert confirmed_status == expected_confirmed, (
            f"{test_case_id} | STEP 4 FAILED | "
            f"Expected: {expected_confirmed} | Actual: {confirmed_status}"
        )

        report_step(
            test_case_id,
            4,
            "Lịch được cập nhật thành Đã xác nhận"
        )

        # Step 5: Doctor đăng nhập và tìm lịch đã xác nhận
        logout_current_user(driver)

        login_account(
            driver,
            test_data["doctor_username"],
            test_data["doctor_password"]
        )

        doctor_page = DoctorAppointmentPage(driver)
        doctor_page.open_page()

        doctor_status = doctor_page.get_status_by_id(original_id)

        assert doctor_status == expected_confirmed, (
            f"{test_case_id} | STEP 5 FAILED | "
            f"Expected: {expected_confirmed} | Actual: {doctor_status}"
        )

        report_step(
            test_case_id,
            5,
            "Doctor đăng nhập và tìm thấy lịch đã được xác nhận"
        )

        # Step 6: Doctor mở chức năng Khám bệnh
        assert doctor_page.is_examine_button_present(original_id), (
            f"{test_case_id} | STEP 6 FAILED | "
            "Expected: Có nút Khám bệnh | Actual: Không tìm thấy"
        )

        doctor_page.click_examine(original_id)

        examination_page = DoctorExaminationPage(driver)
        actual_title = examination_page.get_page_title()

        assert actual_title == "Khám bệnh", (
            f"{test_case_id} | STEP 6 FAILED | "
            f"Expected: Khám bệnh | Actual: {actual_title}"
        )

        assert f"appointmentId={original_id}" in driver.current_url, (
            f"{test_case_id} | STEP 6 FAILED | "
            f"Expected URL chứa appointmentId={original_id} | "
            f"Actual: {driver.current_url}"
        )

        report_step(
            test_case_id,
            6,
            "Doctor mở đúng lịch và vào chức năng Khám bệnh"
        )

        # Step 7: Doctor nhập kết quả khám và lưu hồ sơ
        diagnosis = (
            test_data["diagnosis"]
            or f"Chẩn đoán {test_case_id} {int(time.time())}"
        )

        treatment = (
            test_data["treatment"]
            or f"Hướng điều trị {test_case_id}"
        )

        examination_page.enter_diagnosis(diagnosis)
        examination_page.enter_treatment(treatment)
        examination_page.click_save_medical_record()

        report_step(
            test_case_id,
            7,
            "Doctor nhập kết quả khám và lưu hồ sơ bệnh án thành công"
        )

        # Step 8: Patient đăng nhập lại và tìm lịch sau khi khám
        logout_current_user(driver)

        login_account(
            driver,
            test_data["patient_username"],
            test_data["patient_password"]
        )

        my_page = MyAppointmentPage(driver)
        my_page.open_page()

        completed = my_page.wait_for_appointment_by_note(note)

        assert completed is not None, (
            f"{test_case_id} | STEP 8 FAILED | "
            "Expected: Patient tìm thấy lịch sau khi khám | Actual: Không tìm thấy"
        )

        report_step(
            test_case_id,
            8,
            "Patient đăng nhập lại và tìm thấy lịch sau khi Doctor khám"
        )

        # Step 9: Kiểm tra Đã hoàn thành + dữ liệu không thay đổi
        expected_completed = test_data["expected_completed_status"]

        assert completed["status"] == expected_completed, (
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected: {expected_completed} | Actual: {completed['status']}"
        )

        assert completed["id"] == original_id, (
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected ID: {original_id} | Actual: {completed['id']}"
        )

        assert completed["doctor"] == original_doctor, (
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected Doctor: {original_doctor} | Actual: {completed['doctor']}"
        )

        assert completed["time"] == original_time, (
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected time: {original_time} | Actual: {completed['time']}"
        )

        assert completed["note"] == original_note, (
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected note: {original_note} | Actual: {completed['note']}"
        )

        report_step(
            test_case_id,
            9,
            "Lịch chuyển thành Đã hoàn thành và thông tin ban đầu không thay đổi"
        )

    finally:
        cleanup_appointment(test_data, note)

# ============================================================
# TC-MYAPPOINTMENT-005
# ============================================================

def test_tc_myappointment_005(driver):
    test_case_id = "TC-MYAPPOINTMENT-005"
    description = (
        "Kiểm tra khung giờ của một lịch hẹn đã bị hủy "
        "có thể được sử dụng để tạo lịch hẹn mới."
    )

    report_test_case_start(test_case_id, description)

    test_data = get_test_data_csv(MY_APPOINTMENT_TEST_DATA_CSV, test_case_id)

    doctor_id = int(test_data["doctor_id"])
    note_a = create_unique_note(test_data, "A")
    note_b = create_unique_note(test_data, "B")

    appointment_api = AppointmentApi()

    booking_slot = get_or_create_booking_slot(test_data)
    booking_date = booking_slot["booking_date"]
    booking_time = booking_slot["booking_time"]

    try:
        # Step 1: Patient A đặt lịch
        login_account(
            driver,
            test_data["patient_username"],
            test_data["patient_password"]
        )

        message_a = book_appointment_by_ui(
            driver,
            test_data,
            booking_date,
            booking_time,
            note_a
        )

        expected_message = test_data["expected_booking_message"]

        assert expected_message in message_a, (
            f"{test_case_id} | STEP 1 FAILED | "
            f"Expected: {expected_message} | Actual: {message_a}"
        )

        appointment_a_api = appointment_api.find_appointment_by_note(
            doctor_id=doctor_id,
            note=note_a
        )

        assert appointment_a_api is not None, (
            f"{test_case_id} | STEP 1 FAILED | "
            "Expected: Appointment A được tạo | Actual: Không tìm thấy"
        )

        appointment_a_id = str(appointment_a_api["appointmentId"])

        report_step(
            test_case_id,
            1,
            f"Patient A đặt lịch thành công với Appointment ID {appointment_a_id}"
        )

        # Step 2: Ghi nhận Doctor, ngày và giờ
        assert appointment_a_id, (
            f"{test_case_id} | STEP 2 FAILED | "
            "Expected: Có Appointment ID | Actual: Không lấy được ID"
        )

        report_step(
            test_case_id,
            2,
            f"Ghi nhận Doctor {test_data['doctor_name']}, ngày {booking_date}, giờ {booking_time}"
        )

        # Step 3: Admin tìm đúng lịch của Patient A và hủy
        logout_current_user(driver)

        login_account(
            driver,
            test_data["admin_username"],
            test_data["admin_password"]
        )

        admin_page = AdminAppointmentPage(driver)
        admin_page.open_page()

        actual_id = admin_page.get_appointment_id_by_note(note_a)

        assert actual_id == appointment_a_id, (
            f"{test_case_id} | STEP 3 FAILED | "
            f"Expected ID: {appointment_a_id} | Actual: {actual_id}"
        )

        assert admin_page.is_cancel_button_present(note_a), (
            f"{test_case_id} | STEP 3 FAILED | "
            "Expected: Có nút Hủy | Actual: Không tìm thấy"
        )

        admin_page.click_cancel(note_a)
        cancel_message = admin_page.get_cancel_success_message()

        assert cancel_message == "Hủy lịch hẹn thành công.", (
            f"{test_case_id} | STEP 3 FAILED | "
            f"Expected: Hủy lịch hẹn thành công. | Actual: {cancel_message}"
        )

        report_step(
            test_case_id,
            3,
            "Admin tìm đúng lịch của Patient A và hủy thành công",
            detail=cancel_message
        )

        # Step 4: Kiểm tra lịch A đã chuyển thành Đã hủy
        admin_page.open_page()

        expected_cancelled = test_data["expected_cancelled_status"]
        cancelled_status = admin_page.get_status_by_note(note_a)

        assert cancelled_status == expected_cancelled, (
            f"{test_case_id} | STEP 4 FAILED | "
            f"Expected: {expected_cancelled} | Actual: {cancelled_status}"
        )

        report_step(
            test_case_id,
            4,
            "Lịch của Patient A được cập nhật thành Đã hủy"
        )

        # Step 5: Patient B đăng nhập và mở trang đặt lịch cùng Doctor
        logout_current_user(driver)

        login_account(
            driver,
            test_data["patient_b_username"],
            test_data["patient_b_password"]
        )

        from pages.BookingPage import BookingPage
        booking_page = BookingPage(driver)
        booking_page.open_page_by_doctor(doctor_id)

        report_step(
            test_case_id,
            5,
            "Patient B đăng nhập và mở trang đặt lịch của cùng Doctor"
        )

        # Step 6: Chọn lại đúng ngày và giờ vừa bị hủy
        booking_page.enter_date(booking_date)
        booking_page.enter_time(booking_time)

        actual_time = booking_page.get_time_value()

        assert actual_time == booking_time, (
            f"{test_case_id} | STEP 6 FAILED | "
            f"Expected time: {booking_time} | Actual: {actual_time}"
        )

        report_step(
            test_case_id,
            6,
            "Patient B chọn lại đúng ngày và khung giờ của lịch đã bị hủy"
        )

        # Step 7: Patient B đặt lịch mới tại slot cũ
        booking_page.enter_notes(note_b)
        booking_page.click_booking_button()

        message_b = booking_page.get_message()

        assert expected_message in message_b, (
            f"{test_case_id} | STEP 7 FAILED | "
            f"Expected: {expected_message} | Actual: {message_b}"
        )

        report_step(
            test_case_id,
            7,
            "Patient B đặt lịch mới thành công tại slot đã được giải phóng",
            detail=message_b
        )

        # Step 8: Patient B tìm lịch mới trong Lịch hẹn của tôi
        my_page = MyAppointmentPage(driver)
        my_page.open_page()

        appointment_b = my_page.wait_for_appointment_by_note(note_b)

        assert appointment_b is not None, (
            f"{test_case_id} | STEP 8 FAILED | "
            "Expected: Tìm thấy lịch mới của Patient B | Actual: Không tìm thấy"
        )

        report_step(
            test_case_id,
            8,
            "Patient B tìm thấy lịch mới trong trang Lịch hẹn của tôi"
        )

        # Step 9: Kiểm tra lịch mới có ID khác và trạng thái Chờ xác nhận
        expected_pending = test_data["expected_pending_status"]

        assert appointment_b["status"] == expected_pending, (
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected: {expected_pending} | Actual: {appointment_b['status']}"
        )

        assert appointment_b["doctor"] == test_data["doctor_name"], (
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected Doctor: {test_data['doctor_name']} | Actual: {appointment_b['doctor']}"
        )

        assert booking_date in appointment_b["time"], (
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected date: {booking_date} | Actual: {appointment_b['time']}"
        )

        assert booking_time in appointment_b["time"], (
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected time: {booking_time} | Actual: {appointment_b['time']}"
        )

        assert appointment_b["id"] != appointment_a_id, (
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected: ID mới khác {appointment_a_id} | "
            f"Actual: {appointment_b['id']}"
        )

        report_step(
            test_case_id,
            9,
            "Lịch mới có ID khác và trạng thái Chờ xác nhận tại đúng slot đã giải phóng"
        )

    finally:
        cleanup_appointment(test_data, note_b)