from api.MedicalRecordApi import MedicalRecordApi
from pages.LoginPage import LoginPage
from pages.PatientMedicalHistoryPage import (
    PatientMedicalHistoryPage,
)

from pages.PatientMedicalRecordDetailPage import (
    PatientMedicalRecordDetailPage,
)

from tests.helpers.booking_helpers import (
    login_account,
)

from utils.data_reader import (
    get_test_data_csv,
    MEDICAL_HISTORY_TEST_DATA_CSV,
)

from utils.test_reporter import report_step


HOME_URL = "http://localhost:3000/"


def test_tc_medicalhistory_004_view_medical_record_detail(driver):
    """
    TC-MEDICALHISTORY-004
    Kiểm tra thông tin chi tiết của một bản ghi
    Lịch sử khám bệnh.
    """

    test_case_id = "TC-MEDICALHISTORY-004"

    test_case_description = (
        "Kiểm tra thông tin chi tiết của một bản ghi "
        "Lịch sử khám bệnh."
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
    medical_record_api = MedicalRecordApi()

    # ============================================================
    # TEST SETUP
    # Lấy dữ liệu Medical History hiện tại của Patient.
    # ============================================================

    medical_records = (
        medical_record_api
        .get_medical_records_by_patient(patient_id)
    )

    assert medical_records, (
        f"{test_case_id} | TEST SETUP FAILED | "
        "Expected: Patient có ít nhất một Medical Record | "
        "Actual: Danh sách Medical Record rỗng"
    )

    # ========================================================
    # STEP 1
    # Đăng nhập bằng tài khoản Patient đã có Lịch sử khám bệnh.
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
            "đã có Lịch sử khám bệnh thành công"
        )
    )

    # ========================================================
    # STEP 2
    # Mở trang Lịch sử khám bệnh.
    # ========================================================

    history_page = PatientMedicalHistoryPage(driver)
    history_page.open_page()

    actual_title = history_page.get_page_title()

    assert actual_title == "Lịch sử khám bệnh", (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected title: Lịch sử khám bệnh | "
        f"Actual title: {actual_title}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description="Mở trang Lịch sử khám bệnh thành công"
    )

    # ========================================================
    # STEP 3
    # Chọn một bản ghi và ghi nhận thông tin nhận diện.
    # ========================================================

    record_id = history_page.get_first_record_id()

    selected_record = next(
        (
            record
            for record in medical_records
            if str(record["recordId"]) == str(record_id)
        ),
        None
    )

    assert selected_record is not None, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: API có Medical Record ID {record_id} | "
        "Actual: Không tìm thấy record tương ứng"
    )

    expected_patient_name = (
        selected_record["patientId"]["fullName"]
    )

    expected_doctor_name = (
        selected_record["doctorId"]["fullName"]
    )

    expected_diagnosis = (
        selected_record["diagnosis"]
    )

    expected_treatment = (
        selected_record["treatment"]
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description=(
            "Chọn một bản ghi và ghi nhận "
            "thông tin nhận diện thành công"
        ),
        detail=f"Medical Record ID: {record_id}"
    )

    # ========================================================
    # STEP 4
    # Nhấn Xem chi tiết.
    # ========================================================

    history_page.click_view_detail_by_record_id(
        record_id
    )

    expected_url = (
        f"http://localhost:3000/"
        f"patient-medical-record/{record_id}"
    )

    assert driver.current_url == expected_url, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected URL: {expected_url} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description="Nhấn Xem chi tiết thành công",
        detail=f"Medical Record ID: {record_id}"
    )

    # ========================================================
    # STEP 5
    # Kiểm tra trang chi tiết của bản ghi vừa chọn.
    # ========================================================

    detail_page = PatientMedicalRecordDetailPage(driver)

    actual_detail_title = (
        detail_page.get_page_title()
    )

    actual_record_id = (
        detail_page.get_record_id()
    )

    actual_patient_name = (
        detail_page.get_patient_name()
    )

    actual_doctor_info = (
        detail_page.get_doctor_information()
    )

    actual_diagnosis_info = (
        detail_page.get_diagnosis_information()
    )

    actual_treatment_info = (
        detail_page.get_treatment_information()
    )

    assert actual_detail_title == "Chi tiết hồ sơ bệnh án", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected title: Chi tiết hồ sơ bệnh án | "
        f"Actual title: {actual_detail_title}"
    )

    assert actual_record_id == str(record_id), (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected Record ID: {record_id} | "
        f"Actual Record ID: {actual_record_id}"
    )

    assert actual_patient_name == expected_patient_name, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected Patient: {expected_patient_name} | "
        f"Actual Patient: {actual_patient_name}"
    )

    assert expected_doctor_name in actual_doctor_info, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected Doctor: {expected_doctor_name} | "
        f"Actual: {actual_doctor_info}"
    )

    assert expected_diagnosis in actual_diagnosis_info, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected Diagnosis: {expected_diagnosis} | "
        f"Actual: {actual_diagnosis_info}"
    )

    assert expected_treatment in actual_treatment_info, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected Treatment: {expected_treatment} | "
        f"Actual: {actual_treatment_info}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            "Trang chi tiết hiển thị đúng "
            "bản ghi vừa chọn"
        ),
        detail=(
            f"Record ID: {record_id} | "
            f"Doctor: {expected_doctor_name}"
        )
    )

def test_tc_medicalhistory_005_separate_history_between_patients(driver):
    """
    TC-MEDICALHISTORY-005
    Kiểm tra Lịch sử khám bệnh được phân tách
    theo từng Patient.
    """

    test_case_id = "TC-MEDICALHISTORY-005"

    test_case_description = (
        "Kiểm tra Lịch sử khám bệnh được phân tách "
        "theo từng Patient."
    )

    print(
        f"\n{test_case_id} | DESCRIPTION | "
        f"{test_case_description}\n"
    )

    test_data = get_test_data_csv(
        MEDICAL_HISTORY_TEST_DATA_CSV,
        test_case_id
    )

    patient_a_id = int(test_data["patient_id"])

    patient_b_id_raw = test_data.get("patient_b_id")
    patient_b_username = test_data.get("patient_b_username")
    patient_b_password = test_data.get("patient_b_password")

    assert patient_b_id_raw, (
        f"{test_case_id} | TEST SETUP FAILED | "
        "Thiếu patient_b_id trong medical_history_test_data.csv"
    )

    assert patient_b_username, (
        f"{test_case_id} | TEST SETUP FAILED | "
        "Thiếu patient_b_username trong medical_history_test_data.csv"
    )

    assert patient_b_password, (
        f"{test_case_id} | TEST SETUP FAILED | "
        "Thiếu patient_b_password trong medical_history_test_data.csv"
    )

    patient_b_id = int(patient_b_id_raw)

    medical_record_api = MedicalRecordApi()

    # ============================================================
    # TEST SETUP
    # Lấy dữ liệu Medical History thực tế của hai Patient.
    # ============================================================

    patient_a_api_ids = {
        str(record["recordId"])
        for record in (
            medical_record_api
            .get_medical_records_by_patient(patient_a_id)
        )
    }

    patient_b_api_ids = {
        str(record["recordId"])
        for record in (
            medical_record_api
            .get_medical_records_by_patient(patient_b_id)
        )
    }

    assert patient_a_api_ids, (
        f"{test_case_id} | TEST SETUP FAILED | "
        "Expected: Patient A có Medical History | "
        "Actual: Không có Medical Record"
    )

    assert patient_b_api_ids, (
        f"{test_case_id} | TEST SETUP FAILED | "
        "Expected: Patient B có Medical History | "
        "Actual: Không có Medical Record"
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
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=1,
        description="Đăng nhập bằng Patient A thành công"
    )

    # ========================================================
    # STEP 2
    # Mở trang Lịch sử khám bệnh
    # và ghi nhận các bản ghi hiển thị.
    # ========================================================

    history_page = PatientMedicalHistoryPage(driver)
    history_page.open_page()

    actual_title = history_page.get_page_title()

    assert actual_title == "Lịch sử khám bệnh", (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected title: Lịch sử khám bệnh | "
        f"Actual title: {actual_title}"
    )

    patient_a_ui_ids = set(
        history_page.get_record_ids()
    )

    assert patient_a_ui_ids == patient_a_api_ids, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected Patient A IDs: {sorted(patient_a_api_ids)} | "
        f"Actual UI IDs: {sorted(patient_a_ui_ids)}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=2,
        description=(
            "Mở Lịch sử khám bệnh và ghi nhận "
            "các bản ghi của Patient A thành công"
        ),
        detail=(
            f"Số Medical Record: "
            f"{len(patient_a_ui_ids)}"
        )
    )

    # ========================================================
    # STEP 3
    # Đăng xuất Patient A.
    # ========================================================

    login_page = LoginPage(driver)
    login_page.logout()

    assert driver.current_url == LoginPage.URL, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected URL: {LoginPage.URL} | "
        f"Actual URL: {driver.current_url}"
    )

    assert login_page.is_login_button_displayed(), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Trang đăng nhập được hiển thị | "
        "Actual: Không tìm thấy nút Đăng nhập"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=3,
        description="Đăng xuất Patient A thành công"
    )

    # ========================================================
    # STEP 4
    # Đăng nhập bằng Patient B.
    # ========================================================

    login_account(
        driver,
        patient_b_username,
        patient_b_password
    )

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected URL: {HOME_URL} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=4,
        description="Đăng nhập bằng Patient B thành công"
    )

    # ========================================================
    # STEP 5
    # Mở trang Lịch sử khám bệnh.
    # ========================================================

    history_page = PatientMedicalHistoryPage(driver)
    history_page.open_page()

    actual_title = history_page.get_page_title()

    assert actual_title == "Lịch sử khám bệnh", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected title: Lịch sử khám bệnh | "
        f"Actual title: {actual_title}"
    )

    patient_b_ui_ids = set(
        history_page.get_record_ids()
    )

    report_step(
        test_case_id=test_case_id,
        step_number=5,
        description=(
            "Mở trang Lịch sử khám bệnh "
            "của Patient B thành công"
        ),
        detail=(
            f"Số Medical Record: "
            f"{len(patient_b_ui_ids)}"
        )
    )

    # ========================================================
    # STEP 6
    # So sánh danh sách lịch sử khám của hai Patient.
    # ========================================================

    assert patient_b_ui_ids == patient_b_api_ids, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected Patient B IDs: {sorted(patient_b_api_ids)} | "
        f"Actual UI IDs: {sorted(patient_b_ui_ids)}"
    )

    records_a_in_patient_b = (
        patient_a_ui_ids
        & patient_b_ui_ids
    )

    records_b_in_patient_a = (
        patient_b_ui_ids
        & patient_a_ui_ids
    )

    assert not records_a_in_patient_b, (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: Không có Medical Record của Patient A "
        "trong danh sách Patient B | "
        f"Actual ID trùng: {sorted(records_a_in_patient_b)}"
    )

    assert not records_b_in_patient_a, (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: Không có Medical Record của Patient B "
        "trong danh sách Patient A | "
        f"Actual ID trùng: {sorted(records_b_in_patient_a)}"
    )

    report_step(
        test_case_id=test_case_id,
        step_number=6,
        description=(
            "Lịch sử khám bệnh được phân tách "
            "đúng giữa Patient A và Patient B"
        ),
        detail=(
            f"Patient A: {len(patient_a_ui_ids)} record | "
            f"Patient B: {len(patient_b_ui_ids)} record"
        )
    )