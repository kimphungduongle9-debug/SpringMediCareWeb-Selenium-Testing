import time

from pages.AdminAppointmentPage import AdminAppointmentPage

from utils.test_reporter import report_step

from tests.helpers.appointment_helpers import (
    login_admin,
    login_patient,
    logout_current_user,
    open_tran_binh_booking_page,
)
def test_tc_appointment_001_patient_booking_visible_to_admin(
    driver,
    appointment_tc1_data
):
    """
    TC-APPOINTMENT-001:
    Kiểm tra lịch hẹn bệnh nhân vừa đặt
    được hiển thị đúng trên trang Quản lý lịch hẹn của Admin.
    """

    test_case_id = "TC-APPOINTMENT-001"

    booking_date = appointment_tc1_data["booking_date"]
    booking_time = appointment_tc1_data["booking_time"]
    note = appointment_tc1_data["note"]

    # Step 1 - Patient đăng nhập và mở trang đặt lịch
    login_patient(driver)
    booking_page = open_tran_binh_booking_page(driver)

    report_step(
        test_case_id, 1,
        "Đăng nhập Patient và mở trang đặt lịch của bác sĩ thành công"
    )

    # Step 2 - Chọn ngày, giờ và nhập ghi chú
    booking_page.enter_date(booking_date)
    booking_page.enter_time(booking_time)
    booking_page.enter_notes(note)

    assert booking_page.get_time_value() == booking_time, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected time: {booking_time} | "
        f"Actual: {booking_page.get_time_value()}"
    )

    report_step(
        test_case_id, 2,
        f"Chọn ngày {booking_date}, giờ {booking_time} và nhập ghi chú"
    )

    # Step 3 - Đặt lịch thành công
    booking_page.click_booking_button()

    message = booking_page.get_message()

    assert "Đặt lịch thành công" in message, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Actual: {message}"
    )

    report_step(
        test_case_id, 3,
        "Nhấn Đặt lịch và tạo lịch hẹn thành công",
        detail=message
    )

    # Lấy dữ liệu lịch vừa tạo để đối chiếu phía Admin
    time.sleep(1)

    appointment_api = appointment_tc1_data["appointment_api"]

    appointment = appointment_api.find_appointment_by_note(
        doctor_id=appointment_tc1_data["doctor_id"],
        note=note
    )

    appointment_id = appointment["appointmentId"]

    assert appointment.get("status") == "pending", (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected API status: pending | "
        f"Actual: {appointment.get('status')}"
    )

    expected_time = appointment_api.parse_appointment_date(
        appointment["appointmentDate"]
    ).strftime("%H:%M %d/%m/%Y")

    # Step 4 - Đăng nhập Admin
    logout_current_user(driver)
    login_admin(driver)

    report_step(
        test_case_id, 4,
        "Đăng xuất Patient và đăng nhập Admin thành công"
    )

    # Step 5 - Admin mở Quản lý lịch hẹn và tìm lịch
    admin_page = AdminAppointmentPage(driver)
    admin_page.open_page()

    assert admin_page.get_page_title() == "Quản lý lịch hẹn", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Không mở đúng trang Quản lý lịch hẹn"
    )

    assert admin_page.get_appointment_id_by_note(note) == str(
        appointment_id
    ), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Admin không tìm thấy đúng lịch vừa tạo"
    )

    report_step(
        test_case_id, 5,
        "Admin mở trang Quản lý lịch hẹn và tìm thấy lịch vừa tạo"
    )

    # Step 6 - Kiểm tra thông tin và trạng thái
    assert admin_page.get_patient_name_by_note(note) == "Nguyen An", (
        f"{test_case_id} | STEP 6 FAILED | Sai tên bệnh nhân"
    )

    assert admin_page.get_doctor_name_by_note(note) == "Tran Binh", (
        f"{test_case_id} | STEP 6 FAILED | Sai tên bác sĩ"
    )

    assert admin_page.get_appointment_time_by_note(note) == expected_time, (
        f"{test_case_id} | STEP 6 FAILED | Sai thời gian lịch hẹn"
    )

    assert admin_page.get_status_by_note(note) == "Chờ xác nhận", (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Actual status: {admin_page.get_status_by_note(note)}"
    )

    assert admin_page.is_confirm_button_present(note), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Không có nút Xác nhận"
    )

    assert admin_page.is_cancel_button_present(note), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Không có nút Hủy"
    )

    report_step(
        test_case_id, 6,
        "Lịch hiển thị đúng thông tin, trạng thái Chờ xác nhận và đủ nút thao tác"
    )

def test_tc_appointment_002_admin_confirms_pending_appointment(
    driver,
    appointment_tc2_data
):
    """
    TC-APPOINTMENT-002:
    Kiểm tra Admin xác nhận thành công
    lịch hẹn đang ở trạng thái Chờ xác nhận.
    """

    test_case_id = "TC-APPOINTMENT-002"
    note = appointment_tc2_data["note"]

    # Step 1 - Đăng nhập Admin và mở trang Quản lý lịch hẹn
    login_admin(driver)

    appointment_page = AdminAppointmentPage(driver)
    appointment_page.open_page()

    assert appointment_page.get_page_title() == "Quản lý lịch hẹn", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Không mở đúng trang Quản lý lịch hẹn"
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập Admin và mở trang Quản lý lịch hẹn thành công"
    )

    # Step 2 - Tìm lịch đang Chờ xác nhận
    actual_id = appointment_page.get_appointment_id_by_note(note)
    status_before = appointment_page.get_status_by_note(note)

    assert actual_id == str(appointment_tc2_data["appointment_id"]), (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected appointment ID: {appointment_tc2_data['appointment_id']} | "
        f"Actual: {actual_id}"
    )

    assert status_before == "Chờ xác nhận", (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected status: Chờ xác nhận | Actual: {status_before}"
    )

    assert appointment_page.is_confirm_button_present(note), (
        f"{test_case_id} | STEP 2 FAILED | "
        "Không có nút Xác nhận"
    )

    report_step(
        test_case_id,
        2,
        "Tìm thấy đúng lịch đang ở trạng thái Chờ xác nhận"
    )

    # Lưu thông tin trước khi xác nhận để đối chiếu Step 5
    patient_before = appointment_page.get_patient_name_by_note(note)
    doctor_before = appointment_page.get_doctor_name_by_note(note)
    time_before = appointment_page.get_appointment_time_by_note(note)

    # Step 3 - Nhấn Xác nhận
    appointment_page.click_confirm(note)

    report_step(
        test_case_id,
        3,
        "Nhấn Xác nhận lịch hẹn thành công"
    )

    # Step 4 - Kiểm tra thông báo thành công
    message = appointment_page.get_confirm_success_message()

    assert message == "Xác nhận lịch hẹn thành công.", (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Xác nhận lịch hẹn thành công. | "
        f"Actual: {message}"
    )

    report_step(
        test_case_id,
        4,
        "Hiển thị thông báo xác nhận lịch hẹn thành công",
        detail=message
    )

    # Step 5 - Kiểm tra trạng thái và dữ liệu sau xác nhận
    status_after = appointment_page.get_status_by_note(note)

    assert status_after == "Đã xác nhận", (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected status: Đã xác nhận | Actual: {status_after}"
    )

    assert not appointment_page.is_confirm_button_present(note), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Nút Xác nhận vẫn còn hiển thị"
    )

    assert not appointment_page.is_cancel_button_present(note), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Nút Hủy vẫn còn hiển thị"
    )

    assert appointment_page.get_patient_name_by_note(note) == patient_before, (
        f"{test_case_id} | STEP 5 FAILED | "
        "Thông tin bệnh nhân bị thay đổi"
    )

    assert appointment_page.get_doctor_name_by_note(note) == doctor_before, (
        f"{test_case_id} | STEP 5 FAILED | "
        "Thông tin bác sĩ bị thay đổi"
    )

    assert appointment_page.get_appointment_time_by_note(note) == time_before, (
        f"{test_case_id} | STEP 5 FAILED | "
        "Thời gian lịch hẹn bị thay đổi"
    )

    report_step(
        test_case_id,
        5,
        "Trạng thái chuyển sang Đã xác nhận, nút thao tác biến mất và thông tin lịch không thay đổi"
    )

def test_tc_appointment_003_admin_cancels_pending_appointment(
    driver,
    appointment_tc3_data
):
    """
    TC-APPOINTMENT-003:
    Kiểm tra Admin hủy thành công
    lịch hẹn đang ở trạng thái Chờ xác nhận.
    """

    test_case_id = "TC-APPOINTMENT-003"
    note = appointment_tc3_data["note"]

    # Step 1 - Đăng nhập Admin và mở trang Quản lý lịch hẹn
    login_admin(driver)

    appointment_page = AdminAppointmentPage(driver)
    appointment_page.open_page()

    assert appointment_page.get_page_title() == "Quản lý lịch hẹn", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Không mở đúng trang Quản lý lịch hẹn"
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập Admin và mở trang Quản lý lịch hẹn thành công"
    )

    # Step 2 - Tìm lịch đang Chờ xác nhận
    actual_id = appointment_page.get_appointment_id_by_note(note)
    status_before = appointment_page.get_status_by_note(note)

    assert actual_id == str(
        appointment_tc3_data["appointment_id"]
    ), (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected appointment ID: "
        f"{appointment_tc3_data['appointment_id']} | "
        f"Actual: {actual_id}"
    )

    assert status_before == "Chờ xác nhận", (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected status: Chờ xác nhận | "
        f"Actual: {status_before}"
    )

    assert appointment_page.is_cancel_button_present(note), (
        f"{test_case_id} | STEP 2 FAILED | "
        "Không có nút Hủy"
    )

    report_step(
        test_case_id,
        2,
        "Tìm thấy đúng lịch đang ở trạng thái Chờ xác nhận"
    )

    patient_before = appointment_page.get_patient_name_by_note(note)
    doctor_before = appointment_page.get_doctor_name_by_note(note)
    time_before = appointment_page.get_appointment_time_by_note(note)

    # Step 3: Nhấn Hủy lịch hẹn
    appointment_page.click_cancel(note)

    report_step(
        test_case_id,
        3,
        "Nhấn Hủy lịch hẹn thành công"
    )

    # Step 4: Kiểm tra thông báo hủy thành công
    message = appointment_page.get_cancel_success_message()

    assert message == "Hủy lịch hẹn thành công.", (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: Hủy lịch hẹn thành công. | "
        f"Actual: {message}"
    )

    assert message == "Hủy lịch hẹn thành công.", (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: Hủy lịch hẹn thành công. | "
        f"Actual: {message}"
    )

    report_step(
        test_case_id,
        4,
        "Hiển thị thông báo hủy lịch hẹn thành công",
        detail=message
    )

    # Step 5 - Kiểm tra trạng thái và dữ liệu sau khi hủy
    status_after = appointment_page.get_status_by_note(note)

    assert status_after == "Đã hủy", (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected status: Đã hủy | "
        f"Actual: {status_after}"
    )

    assert not appointment_page.is_confirm_button_present(note), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Nút Xác nhận vẫn còn hiển thị"
    )

    assert not appointment_page.is_cancel_button_present(note), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Nút Hủy vẫn còn hiển thị"
    )

    assert appointment_page.get_patient_name_by_note(note) == patient_before, (
        f"{test_case_id} | STEP 5 FAILED | "
        "Thông tin bệnh nhân bị thay đổi"
    )

    assert appointment_page.get_doctor_name_by_note(note) == doctor_before, (
        f"{test_case_id} | STEP 5 FAILED | "
        "Thông tin bác sĩ bị thay đổi"
    )

    assert appointment_page.get_appointment_time_by_note(note) == time_before, (
        f"{test_case_id} | STEP 5 FAILED | "
        "Thời gian lịch hẹn bị thay đổi"
    )

    report_step(
        test_case_id,
        5,
        "Trạng thái chuyển sang Đã hủy, nút thao tác biến mất và thông tin lịch không thay đổi"
    )