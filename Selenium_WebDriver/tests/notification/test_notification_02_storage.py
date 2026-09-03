from datetime import datetime

import pytest
import time

from pages.DoctorAppointmentPage import DoctorAppointmentPage
from pages.DoctorExaminationPage import DoctorExaminationPage
from pages.MedicalRecordPage import MedicalRecordPage
from pages.PrescriptionPage import PrescriptionPage
from tests.helpers.notification_helpers import (
    confirm_appointment,
    create_pending_appointment,
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


HOME_URL = "http://localhost:3000/"
def test_tc_notification_004_notifications_are_stored_separately(driver):
    """
    TC-NOTIFICATION-004
    Kiểm tra nhiều notification của Patient được lưu riêng biệt
    và không ghi đè lẫn nhau.
    """

    test_case_id = "TC-NOTIFICATION-004"

    test_data = get_test_data_csv(
        NOTIFICATION_TEST_DATA_CSV,
        test_case_id
    )

    # ========================================================
    # STEP 1
    # Chuẩn bị Patient đã có một notification trước đó.
    # ========================================================

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    first_booking = create_pending_appointment(
        driver,
        test_data,
        test_case_id
    )

    first_id = first_booking["appointment_id"]
    first_note = first_booking["note"]

    assert first_booking["status"] == "pending", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected first status: pending | "
        f"Actual: {first_booking['status']}"
    )

    switch_account(
        driver,
        test_data["admin_username"],
        test_data["admin_password"]
    )

    first_confirm = confirm_appointment(
        driver,
        first_note
    )

    assert first_confirm["status_after"] == "Đã xác nhận", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected first status: Đã xác nhận | "
        f"Actual: {first_confirm['status_after']}"
    )

    switch_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    notification_page = open_notification_page(driver)

    old_notification = get_notification_data(
        notification_page,
        first_id
    )

    assert old_notification["element"] is not None, (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected notification của appointment #{first_id} | "
        "Actual: Không tìm thấy"
    )

    assert f"#{first_id}" in old_notification["content"], (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected content chứa #{first_id} | "
        f"Actual: {old_notification['content']}"
    )

    report_step(
        test_case_id,
        1,
        f"Patient đã có notification cũ của "
        f"appointment #{first_id}"
    )

    # ========================================================
    # STEP 2
    # Patient tạo thêm một lịch hẹn mới.
    # ========================================================

    second_booking = create_pending_appointment(
        driver,
        test_data,
        test_case_id
    )

    second_id = second_booking["appointment_id"]
    second_note = second_booking["note"]

    assert second_booking["status"] == "pending", (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected second status: pending | "
        f"Actual: {second_booking['status']}"
    )

    assert second_id != first_id, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected hai Appointment ID khác nhau | "
        f"Actual: {first_id} và {second_id}"
    )

    report_step(
        test_case_id,
        2,
        f"Patient tạo appointment mới #{second_id}, "
        f"khác appointment cũ #{first_id}"
    )

    # ========================================================
    # STEP 3
    # Admin xác nhận lịch hẹn mới.
    # ========================================================

    switch_account(
        driver,
        test_data["admin_username"],
        test_data["admin_password"]
    )

    second_confirm = confirm_appointment(
        driver,
        second_note
    )

    assert second_confirm["status_before"] == "Chờ xác nhận", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected status trước xác nhận: Chờ xác nhận | "
        f"Actual: {second_confirm['status_before']}"
    )

    assert (
        second_confirm["success_message"]
        == "Xác nhận lịch hẹn thành công."
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected message: Xác nhận lịch hẹn thành công. | "
        f"Actual: {second_confirm['success_message']}"
    )

    assert second_confirm["status_after"] == "Đã xác nhận", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected status: Đã xác nhận | "
        f"Actual: {second_confirm['status_after']}"
    )

    report_step(
        test_case_id,
        3,
        f"Admin xác nhận appointment mới "
        f"#{second_id} thành công"
    )

    # ========================================================
    # STEP 4
    # Đăng nhập lại bằng Patient.
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
    # Mở trang Thông báo.
    # ========================================================

    notification_page = open_notification_page(driver)

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
    # Kiểm tra notification mới.
    # ========================================================

    new_notification = get_notification_data(
        notification_page,
        second_id
    )

    assert new_notification["element"] is not None, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected notification của appointment #{second_id} | "
        "Actual: Không tìm thấy"
    )

    assert (
        new_notification["type"]
        == test_data["notification_type"]
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected type: {test_data['notification_type']} | "
        f"Actual: {new_notification['type']}"
    )

    assert f"#{second_id}" in new_notification["content"], (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected content chứa #{second_id} | "
        f"Actual: {new_notification['content']}"
    )

    assert (
        test_data["expected_keyword"]
        in new_notification["content"].lower()
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected keyword: {test_data['expected_keyword']} | "
        f"Actual: {new_notification['content']}"
    )

    assert new_notification["time"].strip(), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: Notification có thời gian | "
        "Actual: Thời gian rỗng"
    )

    try:
        datetime.strptime(
            new_notification["time"],
            test_data["time_format"]
        )

    except ValueError as exc:
        pytest.fail(
            f"{test_case_id} | STEP 6 FAILED | "
            f"Expected format: {test_data['time_format']} | "
            f"Actual: {new_notification['time']} | "
            f"Error: {exc}"
        )

    report_step(
        test_case_id,
        6,
        f"Notification mới của appointment "
        f"#{second_id} hiển thị đúng"
    )

    # ========================================================
    # STEP 7
    # Kiểm tra notification cũ không bị ghi đè.
    # ========================================================

    old_notification_after = get_notification_data(
        notification_page,
        first_id
    )

    assert old_notification_after["element"] is not None, (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected notification cũ #{first_id} vẫn tồn tại | "
        "Actual: Không tìm thấy"
    )

    assert f"#{first_id}" in old_notification_after["content"], (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected notification cũ chứa #{first_id} | "
        f"Actual: {old_notification_after['content']}"
    )

    assert (
        f"#{second_id}"
        not in old_notification_after["content"]
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected notification cũ không chứa ID mới | "
        f"Actual: {old_notification_after['content']}"
    )

    assert (
        f"#{first_id}"
        not in new_notification["content"]
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected notification mới không chứa ID cũ | "
        f"Actual: {new_notification['content']}"
    )

    assert (
        old_notification_after["content"]
        != new_notification["content"]
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected hai notification có nội dung riêng biệt | "
        "Actual: Nội dung giống nhau"
    )

    report_step(
        test_case_id,
        7,
        f"Notification #{first_id} và #{second_id} "
        "được lưu riêng biệt, không ghi đè nhau"
    )

def test_tc_notification_005_notifications_are_isolated_between_patients(
        driver):
    """
    TC-NOTIFICATION-005
    Kiểm tra danh sách notification được phân tách
    giữa hai tài khoản Patient.
    """

    test_case_id = "TC-NOTIFICATION-005"

    test_data = get_test_data_csv(
        NOTIFICATION_TEST_DATA_CSV,
        test_case_id
    )

    # ========================================================
    # STEP 1
    # Đăng nhập bằng Patient A.
    # ========================================================

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập Patient A thành công"
    )

    # ========================================================
    # STEP 2
    # Mở Thông báo và ghi nhận notification Patient A.
    # ========================================================

    notification_page = open_notification_page(driver)

    page_title = notification_page.get_page_title()

    assert page_title == "Thông báo của tôi", (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected title: Thông báo của tôi | "
        f"Actual: {page_title}"
    )

    patient_a_notifications = (
        notification_page
        .get_all_notification_contents()
    )

    assert patient_a_notifications, (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected: Patient A có notification | "
        "Actual: Danh sách rỗng"
    )

    report_step(
        test_case_id,
        2,
        f"Patient A có "
        f"{len(patient_a_notifications)} notification"
    )

    # ========================================================
    # STEP 3
    # Đăng xuất Patient A và đăng nhập Patient B.
    # ========================================================

    switch_account(
        driver,
        test_data["patient_b_username"],
        test_data["patient_b_password"]
    )

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id,
        3,
        "Đăng xuất Patient A và đăng nhập Patient B thành công"
    )

    # ========================================================
    # STEP 4
    # Mở Thông báo và ghi nhận notification Patient B.
    # ========================================================

    notification_page = open_notification_page(driver)

    page_title = notification_page.get_page_title()

    assert page_title == "Thông báo của tôi", (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected title: Thông báo của tôi | "
        f"Actual: {page_title}"
    )

    patient_b_notifications = (
        notification_page
        .get_all_notification_contents()
    )

    assert patient_b_notifications, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Patient B có notification | "
        "Actual: Danh sách rỗng"
    )

    report_step(
        test_case_id,
        4,
        f"Patient B có "
        f"{len(patient_b_notifications)} notification"
    )

    # ========================================================
    # STEP 5
    # So sánh notification của hai Patient.
    # ========================================================

    assert (
        patient_a_notifications
        != patient_b_notifications
    ), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Hai Patient có danh sách notification riêng | "
        "Actual: Hai danh sách giống nhau hoàn toàn"
    )

    report_step(
        test_case_id,
        5,
        "Danh sách notification của Patient A và Patient B "
        "được phân tách riêng"
    )

def test_tc_notification_006_patient_receives_notification_after_doctor_creates_prescription(
        driver):
    """
    TC-NOTIFICATION-006
    Kiểm tra Patient nhận được thông báo đúng
    sau khi Doctor tạo và lưu đơn thuốc mới.
    """

    test_case_id = "TC-NOTIFICATION-006"

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

    assert confirm_result["status_before"] == "Chờ xác nhận", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected status trước xác nhận: Chờ xác nhận | "
        f"Actual: {confirm_result['status_before']}"
    )

    assert confirm_result["status_after"] == "Đã xác nhận", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected status sau xác nhận: Đã xác nhận | "
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
    # Doctor đăng nhập.
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
        "Đăng nhập Doctor thành công"
    )

    # ========================================================
    # STEP 3
    # Doctor mở đúng lịch hẹn của Patient.
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
    # Doctor nhập Chẩn đoán và Hướng điều trị.
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
    # Doctor lưu hồ sơ bệnh án.
    # ========================================================

    examination_page.click_save_medical_record()

    medical_record_page = MedicalRecordPage(driver)

    page_title = medical_record_page.get_page_title()

    actual_diagnosis = (
        medical_record_page.get_diagnosis_information()
    )

    actual_treatment = (
        medical_record_page.get_treatment_information()
    )

    assert page_title == "Chi tiết hồ sơ bệnh án", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected page: Chi tiết hồ sơ bệnh án | "
        f"Actual: {page_title}"
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
    # Doctor mở chức năng kê đơn thuốc.
    # ========================================================

    prescription_page = PrescriptionPage(driver)
    prescription_page.open_prescription_tab()

    assert prescription_page.is_prescription_form_present(), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: Có form kê đơn thuốc | "
        "Actual: Không tìm thấy form"
    )

    report_step(
        test_case_id,
        6,
        "Doctor mở form kê đơn thuốc thành công"
    )

    # ========================================================
    # STEP 7
    # Doctor tạo và lưu một đơn thuốc hợp lệ.
    # ========================================================

    selected_drug = prescription_page.select_drug_by_index(
        test_data["drug_option_index"]
    )

    assert selected_drug, (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected: Chọn được thuốc | "
        "Actual: Giá trị thuốc rỗng"
    )

    assert "-- Chọn thuốc --" not in selected_drug, (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected: Thuốc khác option mặc định | "
        f"Actual: {selected_drug}"
    )

    prescription_page.enter_quantity(
        test_data["prescription_quantity"]
    )

    prescription_page.enter_dosage(
        test_data["prescription_dosage"]
    )

    prescription_page.click_add_to_prescription()

    item_count = (
        prescription_page.get_prescription_item_count()
    )

    assert item_count == 1, (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected: 1 thuốc trong đơn | "
        f"Actual: {item_count}"
    )

    prescription_page.click_save_prescription()

    prescription_message = (
        prescription_page.get_prescription_success_message()
    )

    assert (
        prescription_message
        == "Kê đơn thuốc thành công."
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected message: Kê đơn thuốc thành công. | "
        f"Actual: {prescription_message}"
    )

    report_step(
        test_case_id,
        7,
        f"Doctor tạo và lưu đơn thuốc với "
        f"'{selected_drug}' thành công"
    )

    # ========================================================
    # STEP 8
    # Doctor đăng xuất và Patient đăng nhập lại.
    # ========================================================

    switch_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id,
        8,
        "Đăng xuất Doctor và đăng nhập lại Patient thành công"
    )

    # ========================================================
    # STEP 9
    # Patient kiểm tra notification sau khi Doctor kê đơn thuốc.
    # ========================================================

    notification_page = open_notification_page(
        driver
    )

    page_title = notification_page.get_page_title()

    assert page_title == "Thông báo của tôi", (
        f"{test_case_id} | STEP 9 FAILED | "
        "Expected title: Thông báo của tôi | "
        f"Actual: {page_title}"
    )

    notification = (
        notification_page
        .get_latest_notification_by_type_and_keyword(
            test_data["notification_type"],
            test_data["expected_keyword"]
        )
    )

    assert notification is not None, (
        f"{test_case_id} | STEP 9 FAILED | "
        "Expected: Có notification sau khi Doctor kê đơn thuốc | "
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
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected type: {test_data['notification_type']} | "
        f"Actual: {notification_type}"
    )

    expected_keyword = notification_page.normalize_text(
        test_data["expected_keyword"]
    )

    actual_content = notification_page.normalize_text(
        notification_content
    )

    assert expected_keyword in actual_content, (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected keyword: {test_data['expected_keyword']} | "
        f"Actual: {notification_content}"
    )

    assert notification_time.strip(), (
        f"{test_case_id} | STEP 9 FAILED | "
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
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected format: {test_data['time_format']} | "
            f"Actual: {notification_time} | "
            f"Error: {exc}"
        )

    report_step(
        test_case_id,
        9,
        "Patient nhận notification đơn thuốc đúng loại, "
        "đúng nội dung và đúng định dạng thời gian"
    )