from datetime import datetime
import time
import pytest

from tests.helpers.notification_helpers import (
    confirm_appointment,
    create_pending_appointment,
    cancel_appointment,
    get_notification_data,
    login_account,
    open_notification_page,
    switch_account,
)

from utils.data_reader import (
    get_test_data_csv,
    NOTIFICATION_TEST_DATA_CSV,
)

from utils.test_reporter import report_step
from pages.DoctorAppointmentPage import DoctorAppointmentPage
from pages.DoctorExaminationPage import DoctorExaminationPage
from pages.MedicalRecordPage import MedicalRecordPage

HOME_URL = "http://localhost:3000/"


def test_tc_notification_001_patient_receives_notification_after_admin_confirms(
        driver):
    """
    TC-NOTIFICATION-001
    Kiểm tra Patient nhận được thông báo đúng
    sau khi Admin xác nhận lịch hẹn mà Patient đã đặt.
    """

    test_case_id = "TC-NOTIFICATION-001"

    test_data = get_test_data_csv(
        NOTIFICATION_TEST_DATA_CSV,
        test_case_id
    )

    # ========================================================
    # STEP 1
    # Patient đặt một lịch khám hợp lệ.
    # ========================================================

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    booking = create_pending_appointment(
        driver,
        test_data,
        test_case_id
    )

    appointment_id = booking["appointment_id"]
    note = booking["note"]

    assert booking["actual_time"] == booking["expected_time"], (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected time: {booking['expected_time']} | "
        f"Actual: {booking['actual_time']}"
    )

    assert "Đặt lịch thành công" in booking["booking_message"], (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected message chứa: Đặt lịch thành công | "
        f"Actual: {booking['booking_message']}"
    )

    assert booking["status"] == "pending", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected status: pending | "
        f"Actual: {booking['status']}"
    )

    report_step(
        test_case_id,
        1,
        f"Patient đặt lịch hợp lệ, appointment "
        f"#{appointment_id} ở trạng thái pending"
    )

    # ========================================================
    # STEP 2
    # Đăng xuất Patient và đăng nhập Admin.
    # ========================================================

    switch_account(
        driver,
        test_data["admin_username"],
        test_data["admin_password"]
    )

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id,
        2,
        "Đăng xuất Patient và đăng nhập Admin thành công"
    )

    # ========================================================
    # STEP 3
    # Admin xác nhận lịch vừa tạo.
    # ========================================================

    confirm_result = confirm_appointment(
        driver,
        note
    )

    assert confirm_result["page_title"] == "Quản lý lịch hẹn", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected title: Quản lý lịch hẹn | "
        f"Actual: {confirm_result['page_title']}"
    )

    assert confirm_result["status_before"] == "Chờ xác nhận", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected status trước xác nhận: Chờ xác nhận | "
        f"Actual: {confirm_result['status_before']}"
    )

    assert (
        confirm_result["success_message"]
        == "Xác nhận lịch hẹn thành công."
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected message: Xác nhận lịch hẹn thành công. | "
        f"Actual: {confirm_result['success_message']}"
    )

    assert confirm_result["status_after"] == "Đã xác nhận", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected status: Đã xác nhận | "
        f"Actual: {confirm_result['status_after']}"
    )

    report_step(
        test_case_id,
        3,
        f"Admin xác nhận appointment "
        f"#{appointment_id} thành công"
    )

    # ========================================================
    # STEP 4
    # Đăng xuất Admin và đăng nhập lại Patient.
    # ========================================================

    switch_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id,
        4,
        "Đăng xuất Admin và đăng nhập lại Patient thành công"
    )

    # ========================================================
    # STEP 5
    # Patient mở trang Thông báo.
    # ========================================================

    notification_page = open_notification_page(
        driver
    )

    page_title = notification_page.get_page_title()

    assert page_title == "Thông báo của tôi", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected title: Thông báo của tôi | "
        f"Actual: {page_title}"
    )

    report_step(
        test_case_id,
        5,
        "Patient mở trang Thông báo thành công"
    )

    # ========================================================
    # STEP 6
    # Tìm notification của lịch vừa được xác nhận.
    # ========================================================

    notification = get_notification_data(
        notification_page,
        appointment_id
    )

    assert notification["element"] is not None, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: Có notification của "
        f"appointment #{appointment_id} | "
        "Actual: Không tìm thấy notification"
    )

    report_step(
        test_case_id,
        6,
        f"Tìm thấy notification của "
        f"appointment #{appointment_id}"
    )

    # ========================================================
    # STEP 7
    # Kiểm tra loại, nội dung và thời gian notification.
    # ========================================================

    assert (
        notification["type"]
        == test_data["notification_type"]
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected type: "
        f"{test_data['notification_type']} | "
        f"Actual: {notification['type']}"
    )

    assert f"#{appointment_id}" in notification["content"], (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected appointment: #{appointment_id} | "
        f"Actual: {notification['content']}"
    )

    assert (
        test_data["expected_keyword"]
        in notification["content"].lower()
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected keyword: "
        f"{test_data['expected_keyword']} | "
        f"Actual: {notification['content']}"
    )

    assert notification["time"].strip(), (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected: Notification có thời gian | "
        "Actual: Thời gian rỗng"
    )

    try:
        datetime.strptime(
            notification["time"],
            test_data["time_format"]
        )

    except ValueError as exc:
        pytest.fail(
            f"{test_case_id} | STEP 7 FAILED | "
            f"Expected format: "
            f"{test_data['time_format']} | "
            f"Actual: {notification['time']} | "
            f"Error: {exc}"
        )

    report_step(
        test_case_id,
        7,
        "Notification đúng loại, đúng appointment, "
        "đúng nội dung và đúng định dạng thời gian"
    )


def test_tc_notification_002_patient_receives_notification_after_admin_cancels(
        driver):
    """
    TC-NOTIFICATION-002
    Kiểm tra Patient nhận được thông báo phù hợp
    khi Admin hủy lịch hẹn của Patient.
    """

    test_case_id = "TC-NOTIFICATION-002"

    test_data = get_test_data_csv(
        NOTIFICATION_TEST_DATA_CSV,
        test_case_id
    )

    # ========================================================
    # STEP 1
    # Patient đặt một lịch khám hợp lệ.
    # ========================================================

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    booking = create_pending_appointment(
        driver,
        test_data,
        test_case_id
    )

    appointment_id = booking["appointment_id"]
    note = booking["note"]

    assert booking["actual_time"] == booking["expected_time"], (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected time: {booking['expected_time']} | "
        f"Actual: {booking['actual_time']}"
    )

    assert "Đặt lịch thành công" in booking["booking_message"], (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected message chứa: Đặt lịch thành công | "
        f"Actual: {booking['booking_message']}"
    )

    assert booking["status"] == "pending", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected status: pending | "
        f"Actual: {booking['status']}"
    )

    report_step(
        test_case_id,
        1,
        f"Patient đặt lịch hợp lệ, appointment "
        f"#{appointment_id} ở trạng thái pending"
    )

    # ========================================================
    # STEP 2
    # Đăng xuất Patient và đăng nhập Admin.
    # ========================================================

    switch_account(
        driver,
        test_data["admin_username"],
        test_data["admin_password"]
    )

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id,
        2,
        "Đăng xuất Patient và đăng nhập Admin thành công"
    )

    # ========================================================
    # STEP 3
    # Admin hủy lịch vừa tạo.
    # ========================================================

    cancel_result = cancel_appointment(
        driver,
        note
    )

    assert cancel_result["page_title"] == "Quản lý lịch hẹn", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected title: Quản lý lịch hẹn | "
        f"Actual: {cancel_result['page_title']}"
    )

    assert cancel_result["status_before"] == "Chờ xác nhận", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected status trước hủy: Chờ xác nhận | "
        f"Actual: {cancel_result['status_before']}"
    )

    assert (
        cancel_result["success_message"]
        == "Hủy lịch hẹn thành công."
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected message: Hủy lịch hẹn thành công. | "
        f"Actual: {cancel_result['success_message']}"
    )

    assert cancel_result["status_after"] == "Đã hủy", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected status: Đã hủy | "
        f"Actual: {cancel_result['status_after']}"
    )

    report_step(
        test_case_id,
        3,
        f"Admin hủy appointment "
        f"#{appointment_id} thành công"
    )

    # ========================================================
    # STEP 4
    # Đăng xuất Admin và đăng nhập lại Patient.
    # ========================================================

    switch_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id,
        4,
        "Đăng xuất Admin và đăng nhập lại Patient thành công"
    )

    # ========================================================
    # STEP 5
    # Patient mở trang Thông báo.
    # ========================================================

    notification_page = open_notification_page(
        driver
    )

    page_title = notification_page.get_page_title()

    assert page_title == "Thông báo của tôi", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected title: Thông báo của tôi | "
        f"Actual: {page_title}"
    )

    report_step(
        test_case_id,
        5,
        "Patient mở trang Thông báo thành công"
    )

    # ========================================================
    # STEP 6
    # Tìm notification của lịch vừa bị hủy.
    # ========================================================

    notification = get_notification_data(
        notification_page,
        appointment_id
    )

    assert notification["element"] is not None, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: Có notification của "
        f"appointment #{appointment_id} | "
        "Actual: Không tìm thấy notification"
    )

    report_step(
        test_case_id,
        6,
        f"Tìm thấy notification của "
        f"appointment #{appointment_id}"
    )

    # ========================================================
    # STEP 7
    # Kiểm tra loại, nội dung và thời gian notification.
    # ========================================================

    assert (
        notification["type"]
        == test_data["notification_type"]
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected type: "
        f"{test_data['notification_type']} | "
        f"Actual: {notification['type']}"
    )

    assert f"#{appointment_id}" in notification["content"], (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected appointment: #{appointment_id} | "
        f"Actual: {notification['content']}"
    )

    assert (
        test_data["expected_keyword"]
        in notification["content"].lower()
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected keyword: "
        f"{test_data['expected_keyword']} | "
        f"Actual: {notification['content']}"
    )

    assert notification["time"].strip(), (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected: Notification có thời gian | "
        "Actual: Thời gian rỗng"
    )

    try:
        datetime.strptime(
            notification["time"],
            test_data["time_format"]
        )

    except ValueError as exc:
        pytest.fail(
            f"{test_case_id} | STEP 7 FAILED | "
            f"Expected format: "
            f"{test_data['time_format']} | "
            f"Actual: {notification['time']} | "
            f"Error: {exc}"
        )

    report_step(
        test_case_id,
        7,
        "Notification đúng loại, đúng appointment, "
        "đúng nội dung hủy lịch và đúng định dạng thời gian"
    )

def test_tc_notification_003_patient_receives_notification_after_doctor_updates_result(
        driver):
    """
    TC-NOTIFICATION-003
    Kiểm tra Patient nhận được thông báo
    sau khi Doctor cập nhật kết quả khám.
    """

    test_case_id = "TC-NOTIFICATION-003"

    test_data = get_test_data_csv(
        NOTIFICATION_TEST_DATA_CSV,
        test_case_id
    )

    # ========================================================
    # STEP 1
    # Chuẩn bị Patient có lịch hẹn đã được Admin xác nhận.
    # ========================================================

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    booking = create_pending_appointment(
        driver,
        test_data,
        test_case_id
    )

    appointment_id = booking["appointment_id"]
    note = booking["note"]

    assert booking["actual_time"] == booking["expected_time"], (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected time: {booking['expected_time']} | "
        f"Actual: {booking['actual_time']}"
    )

    assert "Đặt lịch thành công" in booking["booking_message"], (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected message chứa: Đặt lịch thành công | "
        f"Actual: {booking['booking_message']}"
    )

    assert booking["status"] == "pending", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected status: pending | "
        f"Actual: {booking['status']}"
    )

    switch_account(
        driver,
        test_data["admin_username"],
        test_data["admin_password"]
    )

    confirm_result = confirm_appointment(
        driver,
        note
    )

    assert confirm_result["status_after"] == "Đã xác nhận", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected status: Đã xác nhận | "
        f"Actual: {confirm_result['status_after']}"
    )

    report_step(
        test_case_id,
        1,
        f"Chuẩn bị appointment #{appointment_id} "
        "và Admin xác nhận lịch thành công"
    )

    # ========================================================
    # STEP 2
    # Đăng nhập Doctor phụ trách lịch hẹn.
    # ========================================================

    switch_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id,
        2,
        "Đăng nhập Doctor phụ trách thành công"
    )

    # ========================================================
    # STEP 3
    # Mở lịch hẹn của Patient và chọn Khám bệnh.
    # ========================================================

    appointment_page = DoctorAppointmentPage(driver)
    appointment_page.open_page()

    actual_note = appointment_page.get_note_by_id(
        appointment_id
    )

    actual_status = appointment_page.get_status_by_id(
        appointment_id
    )

    assert actual_note == note, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected note: {note} | "
        f"Actual: {actual_note}"
    )

    assert actual_status == "Đã xác nhận", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected status: Đã xác nhận | "
        f"Actual: {actual_status}"
    )

    assert appointment_page.is_examine_button_present(
        appointment_id
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Có nút Khám bệnh | "
        "Actual: Không tìm thấy nút"
    )

    appointment_page.click_examine(
        appointment_id
    )

    examination_page = DoctorExaminationPage(driver)

    page_title = examination_page.get_page_title()

    assert page_title == "Khám bệnh", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected page: Khám bệnh | "
        f"Actual: {page_title}"
    )

    assert (
        f"appointmentId={appointment_id}"
        in driver.current_url
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected URL chứa appointmentId={appointment_id} | "
        f"Actual: {driver.current_url}"
    )

    assert examination_page.is_create_record_form_present(), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Có form tạo hồ sơ bệnh án | "
        "Actual: Không tìm thấy form"
    )

    report_step(
        test_case_id,
        3,
        f"Doctor mở appointment #{appointment_id} "
        "và vào màn hình Khám bệnh thành công"
    )

    # ========================================================
    # STEP 4
    # Nhập Chẩn đoán và Hướng điều trị hợp lệ.
    # ========================================================

    unique_value = str(int(time.time()))

    diagnosis = (
        test_data["diagnosis_prefix"]
        + unique_value
    )

    treatment = (
        test_data["treatment_prefix"]
        + unique_value
    )

    examination_page.enter_diagnosis(
        diagnosis
    )

    examination_page.enter_treatment(
        treatment
    )

    report_step(
        test_case_id,
        4,
        "Doctor nhập Chẩn đoán và Hướng điều trị hợp lệ"
    )

    # ========================================================
    # STEP 5
    # Lưu hồ sơ bệnh án.
    # ========================================================

    examination_page.click_save_medical_record()

    medical_record_page = MedicalRecordPage(driver)

    record_title = medical_record_page.get_page_title()

    actual_diagnosis = (
        medical_record_page.get_diagnosis_information()
    )

    actual_treatment = (
        medical_record_page.get_treatment_information()
    )

    assert record_title == "Chi tiết hồ sơ bệnh án", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected page: Chi tiết hồ sơ bệnh án | "
        f"Actual: {record_title}"
    )

    assert diagnosis in actual_diagnosis, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected Diagnosis chứa: {diagnosis} | "
        f"Actual: {actual_diagnosis}"
    )

    assert treatment in actual_treatment, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected Treatment chứa: {treatment} | "
        f"Actual: {actual_treatment}"
    )

    report_step(
        test_case_id,
        5,
        "Doctor lưu hồ sơ bệnh án thành công"
    )

    # ========================================================
    # STEP 6
    # Đăng xuất Doctor và đăng nhập lại Patient.
    # ========================================================

    switch_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id,
        6,
        "Đăng xuất Doctor và đăng nhập lại Patient thành công"
    )

    # ========================================================
    # STEP 7
    # Mở trang Thông báo.
    # ========================================================

    notification_page = open_notification_page(
        driver
    )

    page_title = notification_page.get_page_title()

    assert page_title == "Thông báo của tôi", (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected title: Thông báo của tôi | "
        f"Actual: {page_title}"
    )

    report_step(
        test_case_id,
        7,
        "Patient mở trang Thông báo thành công"
    )

    # ========================================================
    # STEP 8
    # Kiểm tra notification sau khi Doctor lưu hồ sơ bệnh án.
    # ========================================================

    notification = (
        notification_page
        .get_latest_notification_by_type_and_keyword(
            test_data["notification_type"],
            test_data["expected_keyword"]
        )
    )

    assert notification is not None, (
        f"{test_case_id} | STEP 8 FAILED | "
        "Expected: Có notification sau khi Doctor "
        "lưu hồ sơ bệnh án | "
        "Actual: Không tìm thấy"
    )

    notification_type = (
        notification_page.get_notification_type(
            notification
        )
    )

    notification_content = (
        notification_page.get_notification_content(
            notification
        )
    )

    notification_time = (
        notification_page.get_notification_time(
            notification
        )
    )

    assert (
        notification_type
        == test_data["notification_type"]
    ), (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected type: "
        f"{test_data['notification_type']} | "
        f"Actual: {notification_type}"
    )

    expected_keyword = notification_page.normalize_text(
        test_data["expected_keyword"]
    )

    actual_content = notification_page.normalize_text(
        notification_content
    )

    assert expected_keyword in actual_content, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected keyword: "
        f"{test_data['expected_keyword']} | "
        f"Actual: {notification_content}"
    )

    assert notification_time.strip(), (
        f"{test_case_id} | STEP 8 FAILED | "
        "Expected: Notification có thời gian | "
        "Actual: Thời gian rỗng"
    )

    try:
        datetime.strptime(
            notification_time,
            test_data["time_format"]
        )

    except ValueError as exc:
        pytest.fail(
            f"{test_case_id} | STEP 8 FAILED | "
            f"Expected format: "
            f"{test_data['time_format']} | "
            f"Actual: {notification_time} | "
            f"Error: {exc}"
        )

    report_step(
        test_case_id,
        8,
        "Tìm thấy notification cập nhật kết quả khám "
        "và kiểm tra loại, nội dung, thời gian thành công"
    )
