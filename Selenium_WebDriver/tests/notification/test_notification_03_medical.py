from datetime import datetime

import pytest
from pages.PrescriptionPage import PrescriptionPage
from pages.TestResultPage import TestResultPage

from tests.helpers.notification_helpers import (
    create_completed_medical_record,
    open_notification_page,
    switch_account,
)

from utils.data_reader import (
    get_test_data_csv,
    NOTIFICATION_TEST_DATA_CSV,
)

from utils.test_reporter import report_step


HOME_URL = "http://localhost:3000/"

def test_tc_notification_007_patient_receives_notification_after_doctor_adds_test_result(
        driver):
    """
    TC-NOTIFICATION-007
    Kiểm tra Patient nhận được thông báo đúng
    sau khi Doctor thêm và lưu kết quả xét nghiệm
    vào hồ sơ bệnh án của Patient.
    """

    test_case_id = "TC-NOTIFICATION-007"

    test_data = get_test_data_csv(
        NOTIFICATION_TEST_DATA_CSV,
        test_case_id
    )

    # ========================================================
    # STEP 1
    # Chuẩn bị Patient có hồ sơ bệnh án đã được Doctor tạo.
    # ========================================================

    medical = create_completed_medical_record(
        driver,
        test_data,
        test_case_id
    )

    appointment_id = medical["appointment_id"]

    assert medical["booking_status"] == "pending", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected booking status: pending | "
        f"Actual: {medical['booking_status']}"
    )

    assert medical["confirm_status"] == "Đã xác nhận", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected confirm status: Đã xác nhận | "
        f"Actual: {medical['confirm_status']}"
    )

    assert medical["actual_note"] == medical["note"], (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected note: {medical['note']} | "
        f"Actual: {medical['actual_note']}"
    )

    assert medical["doctor_status"] == "Đã xác nhận", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected Doctor status: Đã xác nhận | "
        f"Actual: {medical['doctor_status']}"
    )

    assert (
        medical["record_page_title"]
        == "Chi tiết hồ sơ bệnh án"
    ), (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected page: Chi tiết hồ sơ bệnh án | "
        f"Actual: {medical['record_page_title']}"
    )

    assert (
        medical["diagnosis"]
        in medical["actual_diagnosis"]
    ), (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected Diagnosis: {medical['diagnosis']} | "
        f"Actual: {medical['actual_diagnosis']}"
    )

    assert (
        medical["treatment"]
        in medical["actual_treatment"]
    ), (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected Treatment: {medical['treatment']} | "
        f"Actual: {medical['actual_treatment']}"
    )

    report_step(
        test_case_id,
        1,
        f"Chuẩn bị appointment #{appointment_id}, "
        "Admin xác nhận và Doctor tạo hồ sơ bệnh án thành công"
    )

    # ========================================================
    # STEP 2
    # Xác nhận Doctor đang truy cập hồ sơ bệnh án.
    # ========================================================

    medical_record_page = medical["medical_record_page"]

    assert (
        medical_record_page
        .is_medical_record_information_present()
    ), (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected: Doctor đang truy cập hồ sơ bệnh án | "
        "Actual: Không tìm thấy thông tin hồ sơ"
    )

    report_step(
        test_case_id,
        2,
        "Doctor đang đăng nhập và truy cập được hồ sơ bệnh án"
    )

    # ========================================================
    # STEP 3
    # Mở Chi tiết hồ sơ bệnh án của Patient.
    # ========================================================

    medical_record_page.open_page(
        appointment_id
    )

    page_title = (
        medical_record_page.get_page_title()
    )

    assert page_title == "Chi tiết hồ sơ bệnh án", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Chi tiết hồ sơ bệnh án | "
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

    assert (
        medical["diagnosis"]
        in medical_record_page.get_diagnosis_information()
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Hiển thị đúng Diagnosis đã lưu | "
        f"Actual: "
        f"{medical_record_page.get_diagnosis_information()}"
    )

    report_step(
        test_case_id,
        3,
        f"Mở hồ sơ bệnh án của appointment "
        f"#{appointment_id} thành công"
    )

    # ========================================================
    # STEP 4
    # Chuyển đến phần Xét nghiệm.
    # ========================================================

    test_result_page = TestResultPage(driver)
    test_result_page.open_test_result_tab()

    assert test_result_page.is_test_result_form_present(), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Có form nhập kết quả xét nghiệm | "
        "Actual: Không tìm thấy form"
    )

    report_step(
        test_case_id,
        4,
        "Mở phần Xét nghiệm thành công"
    )

    # ========================================================
    # STEP 5
    # Nhập kết quả xét nghiệm hợp lệ.
    # ========================================================

    test_name = (
        test_data["test_name_prefix"]
        + medical["unique_value"]
    )

    test_result = (
        test_data["test_result_prefix"]
        + medical["unique_value"]
    )

    test_result_page.enter_test_name(
        test_name
    )

    test_result_page.enter_test_result(
        test_result
    )

    report_step(
        test_case_id,
        5,
        f"Nhập xét nghiệm '{test_name}' "
        "và kết quả hợp lệ"
    )

    # ========================================================
    # STEP 6
    # Lưu kết quả xét nghiệm.
    # ========================================================

    test_result_page.click_save_test_result()

    save_message = (
        test_result_page.get_success_message()
    )

    assert (
        save_message
        == "Thêm kết quả xét nghiệm thành công."
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: Thêm kết quả xét nghiệm thành công. | "
        f"Actual: {save_message}"
    )

    assert test_result_page.has_test_result(
        test_name,
        test_result
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: Có xét nghiệm '{test_name}' vừa lưu | "
        "Actual: Không tìm thấy"
    )

    report_step(
        test_case_id,
        6,
        f"Lưu kết quả xét nghiệm "
        f"'{test_name}' thành công"
    )

    # ========================================================
    # STEP 7
    # Đăng xuất Doctor và đăng nhập lại Patient.
    # ========================================================

    switch_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id,
        7,
        "Đăng xuất Doctor và đăng nhập lại Patient thành công"
    )

    # ========================================================
    # STEP 8
    # Patient mở trang Thông báo.
    # ========================================================

    notification_page = open_notification_page(
        driver
    )

    page_title = notification_page.get_page_title()

    assert page_title == "Thông báo của tôi", (
        f"{test_case_id} | STEP 8 FAILED | "
        "Expected: Thông báo của tôi | "
        f"Actual: {page_title}"
    )

    report_step(
        test_case_id,
        8,
        "Patient mở trang Thông báo thành công"
    )

    # ========================================================
    # STEP 9
    # Kiểm tra notification kết quả xét nghiệm vừa lưu.
    # ========================================================

    notification = (
        notification_page
        .get_latest_notification_by_type_and_keyword(
            test_data["notification_type"],
            test_name
        )
    )

    assert notification is not None, (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected: Có notification cho xét nghiệm "
        f"'{test_name}' | "
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
        f"Expected type: "
        f"{test_data['notification_type']} | "
        f"Actual: {notification_type}"
    )

    normalized_name = notification_page.normalize_text(
        test_name
    )

    normalized_content = notification_page.normalize_text(
        notification_content
    )

    assert normalized_name in normalized_content, (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected content chứa: {test_name} | "
        f"Actual: {notification_content}"
    )

    normalized_expected = notification_page.normalize_text(
        test_data["expected_keyword"]
    )

    assert normalized_expected in normalized_content, (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected keyword: "
        f"{test_data['expected_keyword']} | "
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
            f"Expected format: "
            f"{test_data['time_format']} | "
            f"Actual: {notification_time} | "
            f"Error: {exc}"
        )

    report_step(
        test_case_id,
        9,
        f"Patient nhận notification cho xét nghiệm "
        f"'{test_name}' đúng loại, nội dung và thời gian"
    )

def test_tc_notification_008_patient_receives_new_notification_when_doctor_creates_another_prescription(
        driver):
    """
    TC-NOTIFICATION-008
    Kiểm tra Patient nhận được notification Đơn thuốc mới
    khi Doctor kê thêm một đơn thuốc cho Patient
    đã có đơn thuốc trước đó.
    """

    test_case_id = "TC-NOTIFICATION-008"

    test_data = get_test_data_csv(
        NOTIFICATION_TEST_DATA_CSV,
        test_case_id
    )

    # ========================================================
    # STEP 1
    # Chuẩn bị Patient đã có một đơn thuốc trước đó.
    # ========================================================

    medical = create_completed_medical_record(
        driver,
        test_data,
        test_case_id
    )

    appointment_id = medical["appointment_id"]

    assert medical["booking_status"] == "pending", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected booking status: pending | "
        f"Actual: {medical['booking_status']}"
    )

    assert medical["confirm_status"] == "Đã xác nhận", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected confirm status: Đã xác nhận | "
        f"Actual: {medical['confirm_status']}"
    )

    prescription_page = PrescriptionPage(driver)
    prescription_page.open_prescription_tab()

    assert prescription_page.is_prescription_form_present(), (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected: Có form kê đơn thuốc | "
        "Actual: Không tìm thấy form"
    )

    selected_drug = prescription_page.select_drug_by_index(
        test_data["drug_option_index"]
    )

    assert selected_drug, (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected: Chọn được thuốc | "
        "Actual: Giá trị thuốc rỗng"
    )

    first_dosage = (
        "FIRST-"
        + test_data["prescription_dosage"]
        + "-"
        + medical["unique_value"]
    )

    prescription_page.enter_quantity(
        test_data["prescription_quantity"]
    )

    prescription_page.enter_dosage(
        first_dosage
    )

    prescription_page.click_add_to_prescription()

    assert prescription_page.get_prescription_item_count() == 1, (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected: Đơn thuốc thứ nhất có 1 thuốc | "
        f"Actual: "
        f"{prescription_page.get_prescription_item_count()}"
    )

    prescription_page.click_save_prescription()

    first_message = (
        prescription_page.get_prescription_success_message()
    )

    assert first_message == "Kê đơn thuốc thành công.", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected: Kê đơn thuốc thành công. | "
        f"Actual: {first_message}"
    )

    report_step(
        test_case_id,
        1,
        f"Chuẩn bị appointment #{appointment_id}, "
        "hồ sơ bệnh án và đơn thuốc thứ nhất thành công"
    )

    # ========================================================
    # STEP 2
    # Patient ghi nhận notification của đơn thuốc thứ nhất.
    # ========================================================

    switch_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    notification_page = open_notification_page(
        driver
    )

    assert notification_page.get_page_title() == "Thông báo của tôi", (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected: Thông báo của tôi | "
        f"Actual: {notification_page.get_page_title()}"
    )

    first_notification = (
        notification_page
        .get_latest_notification_by_type_and_keyword(
            test_data["notification_type"],
            test_data["expected_keyword"]
        )
    )

    assert first_notification is not None, (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected: Có notification của đơn thuốc thứ nhất | "
        "Actual: Không tìm thấy"
    )

    first_content = (
        notification_page.get_notification_content(
            first_notification
        )
    )

    first_time = (
        notification_page.get_notification_time(
            first_notification
        )
    )

    assert first_time.strip(), (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected: Notification cũ có thời gian | "
        "Actual: Thời gian rỗng"
    )

    report_step(
        test_case_id,
        2,
        "Ghi nhận notification của đơn thuốc thứ nhất thành công"
    )

    # ========================================================
    # STEP 3
    # Đăng nhập lại Doctor.
    # ========================================================

    switch_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id,
        3,
        "Đăng nhập lại Doctor thành công"
    )

    # ========================================================
    # STEP 4
    # Doctor mở phần Đơn thuốc của hồ sơ.
    # ========================================================

    medical_record_page = medical["medical_record_page"]

    medical_record_page.open_page(
        appointment_id
    )

    assert (
        medical_record_page.get_page_title()
        == "Chi tiết hồ sơ bệnh án"
    ), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Chi tiết hồ sơ bệnh án | "
        f"Actual: {medical_record_page.get_page_title()}"
    )

    prescription_page = PrescriptionPage(driver)
    prescription_page.open_prescription_tab()

    assert prescription_page.is_prescription_form_present(), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Có form kê đơn thuốc | "
        "Actual: Không tìm thấy form"
    )

    report_step(
        test_case_id,
        4,
        "Doctor mở phần Đơn thuốc thành công"
    )

    # ========================================================
    # STEP 5
    # Kê thêm đơn thuốc mới với dữ liệu khác.
    # ========================================================

    selected_drug = prescription_page.select_drug_by_index(
        test_data["drug_option_index"]
    )

    assert selected_drug, (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Chọn được thuốc | "
        "Actual: Giá trị thuốc rỗng"
    )

    second_quantity = (
        int(test_data["prescription_quantity"]) + 1
    )

    second_dosage = (
        "SECOND-"
        + test_data["prescription_dosage"]
        + "-"
        + medical["unique_value"]
    )

    prescription_page.enter_quantity(
        second_quantity
    )

    prescription_page.enter_dosage(
        second_dosage
    )

    prescription_page.click_add_to_prescription()

    assert prescription_page.get_prescription_item_count() == 1, (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Đơn thuốc thứ hai có 1 thuốc | "
        f"Actual: "
        f"{prescription_page.get_prescription_item_count()}"
    )

    report_step(
        test_case_id,
        5,
        "Nhập dữ liệu cho đơn thuốc thứ hai thành công"
    )

    # ========================================================
    # STEP 6
    # Lưu đơn thuốc mới.
    # ========================================================

    prescription_page.click_save_prescription()

    second_message = (
        prescription_page.get_prescription_success_message()
    )

    assert second_message == "Kê đơn thuốc thành công.", (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: Kê đơn thuốc thành công. | "
        f"Actual: {second_message}"
    )

    report_step(
        test_case_id,
        6,
        "Lưu đơn thuốc thứ hai thành công"
    )

    # ========================================================
    # STEP 7
    # Đăng xuất Doctor và đăng nhập Patient.
    # ========================================================

    switch_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id,
        7,
        "Đăng xuất Doctor và đăng nhập lại Patient thành công"
    )

    # ========================================================
    # STEP 8
    # Patient mở trang Thông báo.
    # ========================================================

    notification_page = open_notification_page(
        driver
    )

    assert notification_page.get_page_title() == "Thông báo của tôi", (
        f"{test_case_id} | STEP 8 FAILED | "
        "Expected: Thông báo của tôi | "
        f"Actual: {notification_page.get_page_title()}"
    )

    report_step(
        test_case_id,
        8,
        "Patient mở trang Thông báo thành công"
    )

    # ========================================================
    # STEP 9
    # Kiểm tra notification mới của đơn thuốc thứ hai.
    # ========================================================

    second_notification = (
        notification_page
        .get_latest_notification_by_type_and_keyword(
            test_data["notification_type"],
            test_data["expected_keyword"]
        )
    )

    assert second_notification is not None, (
        f"{test_case_id} | STEP 9 FAILED | "
        "Expected: Có notification của đơn thuốc thứ hai | "
        "Actual: Không tìm thấy"
    )

    second_type = (
        notification_page.get_notification_type(
            second_notification
        )
    )

    second_content = (
        notification_page.get_notification_content(
            second_notification
        )
    )

    second_time = (
        notification_page.get_notification_time(
            second_notification
        )
    )

    assert second_type == test_data["notification_type"], (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected type: {test_data['notification_type']} | "
        f"Actual: {second_type}"
    )

    normalized_expected = notification_page.normalize_text(
        test_data["expected_keyword"]
    )

    normalized_content = notification_page.normalize_text(
        second_content
    )

    assert normalized_expected in normalized_content, (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected keyword: "
        f"{test_data['expected_keyword']} | "
        f"Actual: {second_content}"
    )

    assert second_content != first_content, (
        f"{test_case_id} | STEP 9 FAILED | "
        "Expected: Notification mới khác notification cũ | "
        "Actual: Hai nội dung giống nhau"
    )

    assert second_time.strip(), (
        f"{test_case_id} | STEP 9 FAILED | "
        "Expected: Notification mới có thời gian | "
        "Actual: Thời gian rỗng"
    )

    try:
        datetime.strptime(
            second_time,
            test_data["time_format"]
        )

    except ValueError as exc:
        pytest.fail(
            f"{test_case_id} | STEP 9 FAILED | "
            f"Expected format: "
            f"{test_data['time_format']} | "
            f"Actual: {second_time} | "
            f"Error: {exc}"
        )

    assert first_time.strip(), (
        f"{test_case_id} | STEP 9 FAILED | "
        "Expected: Notification cũ vẫn còn thời gian | "
        "Actual: Thời gian notification cũ bị mất"
    )

    report_step(
        test_case_id,
        9,
        "Patient nhận notification mới của đơn thuốc thứ hai, "
        "không trùng notification cũ và đúng định dạng thời gian"
    )

@pytest.mark.xfail(
    reason=(
        "Known bug: Không phát sinh notification mới "
        "sau khi Doctor cập nhật hồ sơ bệnh án."
    ),
    strict=True
)
def test_tc_notification_009_patient_receives_new_notification_after_doctor_updates_existing_medical_record(
        driver):
    """
    TC-NOTIFICATION-009
    Kiểm tra Patient nhận được notification mới
    sau khi Doctor chỉnh sửa Chẩn đoán và Hướng điều trị
    của một hồ sơ bệnh án đã tồn tại.
    """

    test_case_id = "TC-NOTIFICATION-009"

    test_data = get_test_data_csv(
        NOTIFICATION_TEST_DATA_CSV,
        test_case_id
    )

    # ========================================================
    # STEP 1
    # Chuẩn bị Patient đã có hồ sơ bệnh án
    # và ghi nhận số notification trước khi update.
    # ========================================================

    medical = create_completed_medical_record(
        driver,
        test_data,
        test_case_id
    )

    appointment_id = medical["appointment_id"]

    assert medical["booking_status"] == "pending", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected booking status: pending | "
        f"Actual: {medical['booking_status']}"
    )

    assert medical["confirm_status"] == "Đã xác nhận", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected confirm status: Đã xác nhận | "
        f"Actual: {medical['confirm_status']}"
    )

    original_diagnosis = medical["diagnosis"]
    original_treatment = medical["treatment"]

    switch_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    notification_page = open_notification_page(
        driver
    )

    notifications_before = (
        notification_page.get_all_notification_contents()
    )

    notification_count_before = len(
        notifications_before
    )

    report_step(
        test_case_id,
        1,
        f"Chuẩn bị appointment #{appointment_id}, "
        "hồ sơ bệnh án ban đầu và ghi nhận "
        f"{notification_count_before} notification trước khi cập nhật"
    )

    # ========================================================
    # STEP 2
    # Đăng nhập Doctor phụ trách.
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
    # Mở hồ sơ khám của Patient.
    # ========================================================

    medical_record_page = medical["medical_record_page"]

    medical_record_page.open_page(
        appointment_id
    )

    page_title = (
        medical_record_page.get_page_title()
    )

    assert page_title == "Chi tiết hồ sơ bệnh án", (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Chi tiết hồ sơ bệnh án | "
        f"Actual: {page_title}"
    )

    actual_diagnosis = (
        medical_record_page.get_diagnosis_information()
    )

    actual_treatment = (
        medical_record_page.get_treatment_information()
    )

    assert original_diagnosis in actual_diagnosis, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected Diagnosis: {original_diagnosis} | "
        f"Actual: {actual_diagnosis}"
    )

    assert original_treatment in actual_treatment, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected Treatment: {original_treatment} | "
        f"Actual: {actual_treatment}"
    )

    assert medical_record_page.is_edit_button_present(), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Có nút Chỉnh sửa/Cập nhật hồ sơ | "
        "Actual: Không tìm thấy"
    )

    report_step(
        test_case_id,
        3,
        f"Doctor mở hồ sơ của appointment "
        f"#{appointment_id} thành công"
    )

    # ========================================================
    # STEP 4
    # Chỉnh sửa Chẩn đoán và Hướng điều trị.
    # ========================================================

    medical_record_page.click_edit_button()

    assert medical_record_page.is_edit_form_present(), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Có form chỉnh sửa hồ sơ | "
        "Actual: Không tìm thấy"
    )

    diagnosis_before = (
        medical_record_page.get_diagnosis_input_value()
    )

    treatment_before = (
        medical_record_page.get_treatment_input_value()
    )

    assert diagnosis_before == original_diagnosis, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected diagnosis cũ: {original_diagnosis} | "
        f"Actual: {diagnosis_before}"
    )

    assert treatment_before == original_treatment, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected treatment cũ: {original_treatment} | "
        f"Actual: {treatment_before}"
    )

    updated_diagnosis = (
        test_data["diagnosis_prefix"]
        + "UPDATED-"
        + medical["unique_value"]
    )

    updated_treatment = (
        test_data["treatment_prefix"]
        + "UPDATED-"
        + medical["unique_value"]
    )

    medical_record_page.enter_diagnosis(
        updated_diagnosis
    )

    medical_record_page.enter_treatment(
        updated_treatment
    )

    report_step(
        test_case_id,
        4,
        "Doctor chỉnh sửa Chẩn đoán và Hướng điều trị thành công"
    )

    # ========================================================
    # STEP 5
    # Lưu thông tin đã cập nhật.
    # ========================================================

    medical_record_page.click_save_changes()

    update_message = (
        medical_record_page.get_update_success_message()
    )

    assert (
        update_message
        == "Cập nhật hồ sơ bệnh án thành công."
    ), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Cập nhật hồ sơ bệnh án thành công. | "
        f"Actual: {update_message}"
    )

    actual_updated_diagnosis = (
        medical_record_page.get_diagnosis_information()
    )

    actual_updated_treatment = (
        medical_record_page.get_treatment_information()
    )

    assert (
        updated_diagnosis
        in actual_updated_diagnosis
    ), (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected Diagnosis mới: {updated_diagnosis} | "
        f"Actual: {actual_updated_diagnosis}"
    )

    assert (
        updated_treatment
        in actual_updated_treatment
    ), (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected Treatment mới: {updated_treatment} | "
        f"Actual: {actual_updated_treatment}"
    )

    assert (
        original_diagnosis
        not in actual_updated_diagnosis
    ), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Diagnosis cũ không còn hiển thị | "
        f"Actual: {actual_updated_diagnosis}"
    )

    assert (
        original_treatment
        not in actual_updated_treatment
    ), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Treatment cũ không còn hiển thị | "
        f"Actual: {actual_updated_treatment}"
    )

    report_step(
        test_case_id,
        5,
        "Cập nhật hồ sơ bệnh án thành công"
    )

    # ========================================================
    # STEP 6
    # Đăng xuất Doctor và đăng nhập Patient.
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
        "Expected: Thông báo của tôi | "
        f"Actual: {page_title}"
    )

    report_step(
        test_case_id,
        7,
        "Patient mở trang Thông báo thành công"
    )

    # ========================================================
    # STEP 8
    # Kiểm tra notification mới sau khi Doctor cập nhật hồ sơ.
    # ========================================================

    notifications_after = (
        notification_page.get_all_notification_contents()
    )

    notification_count_after = len(
        notifications_after
    )

    assert (
        notification_count_after
        > notification_count_before
    ), (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected số notification > "
        f"{notification_count_before} | "
        f"Actual: {notification_count_after}"
    )

    report_step(
        test_case_id,
        8,
        "Patient nhận thêm notification mới "
        "sau khi Doctor cập nhật hồ sơ bệnh án",
        detail=(
            f"Before: {notification_count_before} | "
            f"After: {notification_count_after}"
        )
    )