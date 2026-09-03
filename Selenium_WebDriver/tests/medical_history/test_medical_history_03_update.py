import time

from api.MedicalRecordApi import MedicalRecordApi

from pages.MedicalRecordPage import MedicalRecordPage
from pages.PatientMedicalHistoryPage import PatientMedicalHistoryPage

from tests.helpers.booking_helpers import login_account

from tests.helpers.medical_history_helpers import (
    get_patient_record_ids,
    prepare_medical_history_update_record,
    switch_account,
)

from utils.data_reader import (
    get_test_data_csv,
    MEDICAL_HISTORY_TEST_DATA_CSV,
)

from utils.test_reporter import report_step


HOME_URL = "http://localhost:3000/"


def test_tc_medicalhistory_006_update_history_after_doctor_edit(driver):
    """
    TC-MEDICALHISTORY-006
    Kiểm tra Lịch sử khám bệnh được cập nhật
    sau khi Doctor chỉnh sửa hồ sơ bệnh án.
    """

    test_case_id = "TC-MEDICALHISTORY-006"

    test_case_description = (
        "Kiểm tra Lịch sử khám bệnh được cập nhật "
        "sau khi Doctor chỉnh sửa hồ sơ bệnh án."
    )

    print(
        f"\n{test_case_id} | DESCRIPTION | "
        f"{test_case_description}\n"
    )

    test_data = get_test_data_csv(
        MEDICAL_HISTORY_TEST_DATA_CSV,
        test_case_id
    )

    patient_id = int(test_data["patient_id"])
    doctor_id = int(test_data["doctor_id"])

    setup_diagnosis = test_data["diagnosis"]
    setup_treatment = test_data["treatment"]

    medical_record_api = MedicalRecordApi()

    # ============================================================
    # TEST SETUP
    # Chuẩn bị một completed Medical Record và reset baseline.
    # Không tính là Step của Test Case.
    # ============================================================

    prepared = prepare_medical_history_update_record(
        medical_record_api=medical_record_api,
        patient_id=patient_id,
        doctor_id=doctor_id,
        test_data=test_data,
        test_case_id=test_case_id,
        diagnosis=setup_diagnosis,
        treatment=setup_treatment
    )

    appointment_id = prepared["appointment_id"]
    record_id = prepared["record_id"]

    # ========================================================
    # STEP 1
    # Đăng nhập bằng Patient đã có hồ sơ bệnh án hoàn thành.
    # ========================================================

    login_account(
        driver,
        test_data["patient_username"],
        test_data["patient_password"]
    )

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description=(
            "Đăng nhập bằng tài khoản Patient "
            "đã có hồ sơ bệnh án hoàn thành thành công"
        )
    )

    # ========================================================
    # STEP 2
    # Mở Lịch sử khám bệnh và ghi nhận thông tin một bản ghi.
    # ========================================================

    history_page = PatientMedicalHistoryPage(driver)
    history_page.open_page()

    actual_title = history_page.get_page_title()

    assert actual_title == "Lịch sử khám bệnh", (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected title: Lịch sử khám bệnh | "
        f"Actual: {actual_title}"
    )

    record_ids_before = get_patient_record_ids(
        medical_record_api,
        patient_id
    )

    assert str(record_id) in history_page.get_record_ids(), (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected UI có Medical Record ID: {record_id} | "
        f"Actual UI IDs: {history_page.get_record_ids()}"
    )

    record_before = medical_record_api.get_medical_record_by_id(
        record_id
    )

    original_diagnosis = record_before["diagnosis"]
    original_treatment = record_before["treatment"]

    assert original_diagnosis == setup_diagnosis, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected diagnosis baseline: {setup_diagnosis} | "
        f"Actual: {original_diagnosis}"
    )

    assert original_treatment == setup_treatment, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected treatment baseline: {setup_treatment} | "
        f"Actual: {original_treatment}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description=(
            "Mở Lịch sử khám bệnh và ghi nhận "
            "thông tin bản ghi thành công"
        ),
        detail=f"Medical Record ID: {record_id}"
    )

    # ========================================================
    # STEP 3
    # Đăng xuất Patient và đăng nhập Doctor phụ trách.
    # ========================================================

    switch_account(
        driver,
        test_data["doctor_username"],
        test_data["doctor_password"]
    )

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            "Đăng xuất Patient và đăng nhập "
            "Doctor phụ trách thành công"
        )
    )

    # ========================================================
    # STEP 4
    # Mở hồ sơ bệnh án tương ứng và chọn Cập nhật hồ sơ.
    # ========================================================

    medical_record_page = MedicalRecordPage(driver)

    medical_record_page.open_page(
        appointment_id
    )

    actual_record_title = (
        medical_record_page.get_page_title()
    )

    assert actual_record_title == "Chi tiết hồ sơ bệnh án", (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected title: Chi tiết hồ sơ bệnh án | "
        f"Actual: {actual_record_title}"
    )

    assert medical_record_page.is_edit_button_present(), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Có nút Cập nhật hồ sơ | "
        "Actual: Không tìm thấy nút"
    )

    medical_record_page.click_edit_button()

    assert medical_record_page.is_edit_form_present(), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Form cập nhật được hiển thị | "
        "Actual: Không tìm thấy form"
    )

    diagnosis_input = (
        medical_record_page.get_diagnosis_input_value()
    )

    treatment_input = (
        medical_record_page.get_treatment_input_value()
    )

    assert diagnosis_input == original_diagnosis, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected diagnosis preload: {original_diagnosis} | "
        f"Actual: {diagnosis_input}"
    )

    assert treatment_input == original_treatment, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected treatment preload: {original_treatment} | "
        f"Actual: {treatment_input}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description=(
            "Mở hồ sơ bệnh án và chọn "
            "Cập nhật hồ sơ thành công"
        ),
        detail=f"Medical Record ID: {record_id}"
    )

    # ========================================================
    # STEP 5
    # Thay đổi thông tin khám và lưu cập nhật.
    # ========================================================

    unique_value = str(int(time.time()))

    new_diagnosis = (
        f"Chẩn đoán cập nhật TC-MEDICALHISTORY-006 "
        f"{unique_value}"
    )

    new_treatment = (
        f"Hướng điều trị cập nhật TC-MEDICALHISTORY-006 "
        f"{unique_value}"
    )

    medical_record_page.enter_diagnosis(
        new_diagnosis
    )

    medical_record_page.enter_treatment(
        new_treatment
    )

    assert (
        medical_record_page.get_diagnosis_input_value()
        == new_diagnosis
    ), (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected diagnosis input: {new_diagnosis} | "
        "Actual: "
        f"{medical_record_page.get_diagnosis_input_value()}"
    )

    assert (
        medical_record_page.get_treatment_input_value()
        == new_treatment
    ), (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected treatment input: {new_treatment} | "
        "Actual: "
        f"{medical_record_page.get_treatment_input_value()}"
    )

    medical_record_page.click_save_changes()

    update_message = (
        medical_record_page.get_update_success_message()
    )

    assert (
        update_message
        == "Cập nhật hồ sơ bệnh án thành công."
    ), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected message: "
        "Cập nhật hồ sơ bệnh án thành công. | "
        f"Actual: {update_message}"
    )

    assert not medical_record_page.is_edit_form_present(), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Form cập nhật đóng sau khi lưu | "
        "Actual: Form vẫn hiển thị"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            "Thay đổi thông tin khám "
            "và lưu cập nhật thành công"
        ),
        detail=(
            f"Diagnosis: {new_diagnosis} | "
            f"Treatment: {new_treatment}"
        )
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
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            "Đăng xuất Doctor và đăng nhập lại "
            "bằng Patient thành công"
        )
    )

    # ========================================================
    # STEP 7
    # Mở trang Lịch sử khám bệnh.
    # ========================================================

    history_page = PatientMedicalHistoryPage(driver)
    history_page.open_page()

    actual_title = history_page.get_page_title()

    assert actual_title == "Lịch sử khám bệnh", (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected title: Lịch sử khám bệnh | "
        f"Actual: {actual_title}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=7,
        description=(
            "Mở trang Lịch sử khám bệnh thành công"
        )
    )

    # ========================================================
    # STEP 8
    # Kiểm tra bản ghi vừa được Doctor cập nhật.
    # ========================================================

    record_ids_after = get_patient_record_ids(
        medical_record_api,
        patient_id
    )

    assert record_ids_after == record_ids_before, (
        f"{test_case_id} | STEP 8 FAILED | "
        "Expected: Không tạo hoặc mất Medical Record "
        "sau khi cập nhật | "
        f"Before IDs: {sorted(record_ids_before)} | "
        f"After IDs: {sorted(record_ids_after)}"
    )

    assert str(record_id) in history_page.get_record_ids(), (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected UI vẫn có Record ID: {record_id} | "
        f"Actual UI IDs: {history_page.get_record_ids()}"
    )

    updated_record = (
        medical_record_api.get_medical_record_by_id(
            record_id
        )
    )

    assert updated_record["diagnosis"] == new_diagnosis, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected diagnosis: {new_diagnosis} | "
        f"Actual: {updated_record.get('diagnosis')}"
    )

    assert updated_record["treatment"] == new_treatment, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected treatment: {new_treatment} | "
        f"Actual: {updated_record.get('treatment')}"
    )

    history_page.click_view_detail_by_record_id(
        record_id
    )

    assert (
        f"/patient-medical-record/{record_id}"
        in driver.current_url
    ), (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected URL chứa record {record_id} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=8,
        description=(
            "Bản ghi vừa được Doctor cập nhật "
            "hiển thị đúng trong Lịch sử khám bệnh"
        ),
        detail=(
            f"Record ID giữ nguyên: {record_id} | "
            f"Tổng record: {len(record_ids_after)}"
        )
    )