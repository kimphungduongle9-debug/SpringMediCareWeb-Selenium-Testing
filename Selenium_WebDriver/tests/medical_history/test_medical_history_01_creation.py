from api.MedicalRecordApi import MedicalRecordApi

from pages.PatientMedicalHistoryPage import (
    PatientMedicalHistoryPage,
)

from tests.helpers.booking_helpers import (
    login_account,
)
from pages.AdminAppointmentPage import AdminAppointmentPage
from tests.helpers.medical_history_helpers import (
    cleanup_appointment,
    create_pending_appointment,
    get_patient_record_ids,
    get_ui_record_ids,
    switch_account,
)

from utils.data_reader import (
    get_test_data_csv,
    MEDICAL_HISTORY_TEST_DATA_CSV,
)

from utils.test_reporter import report_step
from pages.DoctorAppointmentPage import DoctorAppointmentPage
from pages.DoctorExaminationPage import DoctorExaminationPage
from pages.MedicalRecordPage import MedicalRecordPage

HOME_URL = "http://localhost:3000/"


def test_tc_medicalhistory_001_unexamined_appointment_no_history(driver):
    """
    TC-MEDICALHISTORY-001
    Kiểm tra lịch hẹn chưa được Doctor khám
    không phát sinh Lịch sử khám bệnh.
    """

    test_case_id = "TC-MEDICALHISTORY-001"
    test_case_description = (
        "Kiểm tra lịch hẹn chưa được Doctor khám "
        "không phát sinh Lịch sử khám bệnh."
    )

    print(f"\n{test_case_id} | DESCRIPTION | {test_case_description}\n")

    test_data = get_test_data_csv(
        MEDICAL_HISTORY_TEST_DATA_CSV,
        test_case_id
    )

    patient_id = int(test_data["patient_id"])
    doctor_id = int(test_data["doctor_id"])

    medical_record_api = MedicalRecordApi()
    appointment_id = None

    # ============================================================
    # TEST SETUP
    # Ghi nhận Medical History trước khi tạo appointment.
    # Đây là setup kỹ thuật, không phải Step của Test Case.
    # ============================================================

    record_ids_before = get_patient_record_ids(
        medical_record_api,
        patient_id
    )

    try:

        # ========================================================
        # STEP 1
        # Đăng nhập bằng tài khoản Patient.
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
                "Đăng nhập bằng tài khoản Patient thành công"
            )
        )

        # ========================================================
        # STEP 2
        # Tạo một lịch hẹn hợp lệ.
        # ========================================================

        booking_result = create_pending_appointment(
            driver=driver,
            doctor_id=doctor_id,
            test_data=test_data,
            test_case_id=test_case_id
        )

        appointment = booking_result["appointment"]
        success_message = booking_result["success_message"]

        appointment_id = appointment.get("appointmentId")
        actual_status = appointment.get("status")

        assert "Đặt lịch thành công" in success_message, (
            f"{test_case_id} | STEP 2 FAILED | "
            "Expected message chứa: Đặt lịch thành công | "
            f"Actual: {success_message}"
        )

        assert appointment_id is not None, (
            f"{test_case_id} | STEP 2 FAILED | "
            "Expected: Lịch hẹn được tạo và có ID | "
            "Actual: Không lấy được Appointment ID"
        )

        assert actual_status == "pending", (
            f"{test_case_id} | STEP 2 FAILED | "
            "Expected status: pending | "
            f"Actual status: {actual_status}"
        )

        report_step(
            test_case_id=test_case_id,
            step_number=2,
            description=(
                "Tạo một lịch hẹn hợp lệ thành công"
            ),
            detail=(
                f"Appointment ID: {appointment_id} | "
                f"Status: {actual_status}"
            )
        )

        # ========================================================
        # STEP 3
        # Mở trang Lịch sử khám bệnh.
        # ========================================================

        history_page = PatientMedicalHistoryPage(driver)
        history_page.open_page()

        actual_title = history_page.get_page_title()

        assert actual_title == "Lịch sử khám bệnh", (
            f"{test_case_id} | STEP 3 FAILED | "
            "Expected title: Lịch sử khám bệnh | "
            f"Actual title: {actual_title}"
        )

        report_step(
            test_case_id=test_case_id,
            step_number=3,
            description=(
                "Mở trang Lịch sử khám bệnh thành công"
            )
        )

        # ========================================================
        # STEP 4
        # Kiểm tra lịch hẹn vừa tạo
        # trong danh sách lịch sử khám.
        # ========================================================

        record_ids_after_api = get_patient_record_ids(
            medical_record_api,
            patient_id
        )

        record_ids_after_ui = get_ui_record_ids(
            history_page
        )

        new_record_ids = (
            record_ids_after_api
            - record_ids_before
        )

        assert not new_record_ids, (
            f"{test_case_id} | STEP 4 FAILED | "
            "Expected: Không phát sinh Medical Record "
            "khi Doctor chưa khám | "
            "Actual: Phát sinh Medical Record ID "
            f"{sorted(new_record_ids)}"
        )

        assert record_ids_after_ui == record_ids_after_api, (
            f"{test_case_id} | STEP 4 FAILED | "
            "Expected UI record IDs: "
            f"{sorted(record_ids_after_api)} | "
            "Actual UI record IDs: "
            f"{sorted(record_ids_after_ui)}"
        )

        report_step(
            test_case_id=test_case_id,
            step_number=4,
            description=(
                "Lịch hẹn chưa được Doctor khám "
                "không phát sinh Lịch sử khám bệnh"
            ),
            detail=(
                f"Medical Record trước: {len(record_ids_before)} | "
                f"Medical Record sau: {len(record_ids_after_api)}"
            )
        )

    finally:

        # ========================================================
        # CLEANUP
        # Hủy appointment được tạo riêng cho TC001.
        # ========================================================

        cleanup_appointment(
            appointment_id
        )

def test_tc_medicalhistory_002_confirmed_appointment_no_history(driver):
    """
    TC-MEDICALHISTORY-002
    Kiểm tra lịch hẹn đã được Admin xác nhận nhưng chưa được Doctor khám
    không phát sinh Lịch sử khám bệnh.
    """

    test_case_id = "TC-MEDICALHISTORY-002"

    test_case_description = (
        "Kiểm tra lịch hẹn đã được Admin xác nhận nhưng chưa được Doctor khám "
        "không phát sinh Lịch sử khám bệnh."
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

    medical_record_api = MedicalRecordApi()
    appointment_id = None

    # ============================================================
    # TEST SETUP
    # Ghi nhận Medical History trước khi tạo appointment.
    # ============================================================

    record_ids_before = get_patient_record_ids(
        medical_record_api,
        patient_id
    )

    try:

        # ========================================================
        # STEP 1
        # Đăng nhập bằng tài khoản Patient.
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
            description="Đăng nhập bằng tài khoản Patient thành công"
        )

        # ========================================================
        # STEP 2
        # Tạo một lịch hẹn hợp lệ.
        # ========================================================

        booking_result = create_pending_appointment(
            driver=driver,
            doctor_id=doctor_id,
            test_data=test_data,
            test_case_id=test_case_id
        )

        appointment = booking_result["appointment"]
        note = booking_result["note"]
        success_message = booking_result["success_message"]

        appointment_id = appointment.get("appointmentId")
        actual_status = appointment.get("status")

        assert "Đặt lịch thành công" in success_message, (
            f"{test_case_id} | STEP 2 FAILED | "
            "Expected message chứa: Đặt lịch thành công | "
            f"Actual: {success_message}"
        )

        assert appointment_id is not None, (
            f"{test_case_id} | STEP 2 FAILED | "
            "Expected: Lịch hẹn được tạo và có ID | "
            "Actual: Không lấy được Appointment ID"
        )

        assert actual_status == "pending", (
            f"{test_case_id} | STEP 2 FAILED | "
            "Expected status: pending | "
            f"Actual status: {actual_status}"
        )

        report_step(
            test_case_id=test_case_id,
            step_number=2,
            description="Tạo một lịch hẹn hợp lệ thành công",
            detail=(
                f"Appointment ID: {appointment_id} | "
                f"Status: {actual_status}"
            )
        )

        # ========================================================
        # STEP 3
        # Đăng xuất Patient và đăng nhập bằng tài khoản Admin.
        # ========================================================

        switch_account(
            driver,
            test_data["admin_username"],
            test_data["admin_password"]
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
                "bằng tài khoản Admin thành công"
            )
        )

        # ========================================================
        # STEP 4
        # Xác nhận lịch hẹn vừa tạo.
        # ========================================================

        admin_page = AdminAppointmentPage(driver)
        admin_page.open_page()

        actual_id = admin_page.get_appointment_id_by_note(note)
        status_before = admin_page.get_status_by_note(note)

        assert actual_id == str(appointment_id), (
            f"{test_case_id} | STEP 4 FAILED | "
            f"Expected Appointment ID: {appointment_id} | "
            f"Actual: {actual_id}"
        )

        assert status_before == "Chờ xác nhận", (
            f"{test_case_id} | STEP 4 FAILED | "
            "Expected status trước xác nhận: Chờ xác nhận | "
            f"Actual: {status_before}"
        )

        admin_page.click_confirm(note)

        success_confirm = (
            admin_page.get_confirm_success_message()
        )

        status_after = (
            admin_page.wait_for_status_by_note(
                note,
                "Đã xác nhận"
            )
        )

        assert success_confirm == "Xác nhận lịch hẹn thành công.", (
            f"{test_case_id} | STEP 4 FAILED | "
            "Expected message: Xác nhận lịch hẹn thành công. | "
            f"Actual: {success_confirm}"
        )

        assert status_after == "Đã xác nhận", (
            f"{test_case_id} | STEP 4 FAILED | "
            "Expected status sau xác nhận: Đã xác nhận | "
            f"Actual: {status_after}"
        )

        report_step(
            test_case_id=test_case_id,
            step_number=4,
            description="Xác nhận lịch hẹn vừa tạo thành công",
            detail=(
                f"Appointment ID: {appointment_id} | "
                f"Status: {status_after}"
            )
        )

        # ========================================================
        # STEP 5
        # Đăng xuất Admin và đăng nhập lại bằng Patient.
        # ========================================================

        switch_account(
            driver,
            test_data["patient_username"],
            test_data["patient_password"]
        )

        assert driver.current_url == HOME_URL, (
            f"{test_case_id} | STEP 5 FAILED | "
            f"Expected URL: {HOME_URL} | "
            f"Actual URL: {driver.current_url}"
        )

        report_step(
            test_case_id=test_case_id,
            step_number=5,
            description=(
                "Đăng xuất Admin và đăng nhập lại "
                "bằng tài khoản Patient thành công"
            )
        )

        # ========================================================
        # STEP 6
        # Mở trang Lịch sử khám bệnh.
        # ========================================================

        history_page = PatientMedicalHistoryPage(driver)
        history_page.open_page()

        actual_title = history_page.get_page_title()

        assert actual_title == "Lịch sử khám bệnh", (
            f"{test_case_id} | STEP 6 FAILED | "
            "Expected title: Lịch sử khám bệnh | "
            f"Actual title: {actual_title}"
        )

        report_step(
            test_case_id=test_case_id,
            step_number=6,
            description="Mở trang Lịch sử khám bệnh thành công"
        )

        # ========================================================
        # STEP 7
        # Kiểm tra lịch hẹn vừa được xác nhận
        # trong danh sách Lịch sử khám bệnh.
        # ========================================================

        record_ids_after_api = get_patient_record_ids(
            medical_record_api,
            patient_id
        )

        record_ids_after_ui = get_ui_record_ids(
            history_page
        )

        new_record_ids = (
            record_ids_after_api
            - record_ids_before
        )

        assert not new_record_ids, (
            f"{test_case_id} | STEP 7 FAILED | "
            "Expected: Không phát sinh Medical Record "
            "khi lịch chỉ mới được Admin xác nhận | "
            "Actual: Phát sinh Medical Record ID "
            f"{sorted(new_record_ids)}"
        )

        assert record_ids_after_ui == record_ids_after_api, (
            f"{test_case_id} | STEP 7 FAILED | "
            "Expected UI record IDs: "
            f"{sorted(record_ids_after_api)} | "
            "Actual UI record IDs: "
            f"{sorted(record_ids_after_ui)}"
        )

        report_step(
            test_case_id=test_case_id,
            step_number=7,
            description=(
                "Lịch hẹn đã xác nhận nhưng chưa được Doctor khám "
                "không phát sinh Lịch sử khám bệnh"
            ),
            detail=(
                f"Medical Record trước: {len(record_ids_before)} | "
                f"Medical Record sau: {len(record_ids_after_api)}"
            )
        )

    finally:

        # ========================================================
        # CLEANUP
        # Hủy appointment phục vụ riêng TC002.
        # ========================================================

        cleanup_appointment(
            appointment_id
        )

def test_tc_medicalhistory_003_create_history_after_examination(driver):
    """
    TC-MEDICALHISTORY-003
    Kiểm tra Lịch sử khám bệnh được tạo sau khi Doctor
    hoàn thành khám và lưu hồ sơ bệnh án.
    """

    test_case_id = "TC-MEDICALHISTORY-003"

    test_case_description = (
        "Kiểm tra Lịch sử khám bệnh được tạo sau khi Doctor "
        "hoàn thành khám và lưu hồ sơ bệnh án."
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

    diagnosis = test_data["diagnosis"]
    treatment = test_data["treatment"]

    medical_record_api = MedicalRecordApi()
    appointment_id = None

    # ============================================================
    # TEST SETUP
    # Ghi nhận Medical History trước khi thực hiện khám.
    # ============================================================

    record_ids_before = get_patient_record_ids(
        medical_record_api,
        patient_id
    )

    try:

        # ========================================================
        # STEP 1
        # Đăng nhập bằng tài khoản Patient.
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
                "Đăng nhập bằng tài khoản Patient thành công"
            )
        )

        # ========================================================
        # STEP 2
        # Tạo một lịch hẹn hợp lệ.
        # ========================================================

        booking_result = create_pending_appointment(
            driver=driver,
            doctor_id=doctor_id,
            test_data=test_data,
            test_case_id=test_case_id
        )

        appointment = booking_result["appointment"]
        note = booking_result["note"]
        success_message = booking_result["success_message"]

        appointment_id = appointment.get("appointmentId")
        actual_status = appointment.get("status")

        assert "Đặt lịch thành công" in success_message, (
            f"{test_case_id} | STEP 2 FAILED | "
            "Expected message chứa: Đặt lịch thành công | "
            f"Actual: {success_message}"
        )

        assert appointment_id is not None, (
            f"{test_case_id} | STEP 2 FAILED | "
            "Expected: Lịch hẹn được tạo và có ID | "
            "Actual: Không lấy được Appointment ID"
        )

        assert actual_status == "pending", (
            f"{test_case_id} | STEP 2 FAILED | "
            "Expected status: pending | "
            f"Actual status: {actual_status}"
        )

        report_step(
            test_case_id=test_case_id,
            step_number=2,
            description="Tạo một lịch hẹn hợp lệ thành công",
            detail=(
                f"Appointment ID: {appointment_id} | "
                f"Status: {actual_status}"
            )
        )

        # ========================================================
        # STEP 3
        # Đăng xuất Patient và đăng nhập bằng tài khoản Admin.
        # ========================================================

        switch_account(
            driver,
            test_data["admin_username"],
            test_data["admin_password"]
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
                "bằng tài khoản Admin thành công"
            )
        )

        # ========================================================
        # STEP 4
        # Xác nhận lịch hẹn vừa tạo.
        # ========================================================

        admin_page = AdminAppointmentPage(driver)
        admin_page.open_page()

        actual_id = admin_page.get_appointment_id_by_note(note)

        assert actual_id == str(appointment_id), (
            f"{test_case_id} | STEP 4 FAILED | "
            f"Expected Appointment ID: {appointment_id} | "
            f"Actual: {actual_id}"
        )

        admin_page.click_confirm(note)

        confirm_message = (
            admin_page.get_confirm_success_message()
        )
        status_after_confirm = (
            admin_page.wait_for_status_by_note(
                note,
                "Đã xác nhận"
            )
        )
        assert confirm_message == "Xác nhận lịch hẹn thành công.", (
            f"{test_case_id} | STEP 4 FAILED | "
            "Expected message: Xác nhận lịch hẹn thành công. | "
            f"Actual: {confirm_message}"
        )

        assert status_after_confirm == "Đã xác nhận", (
            f"{test_case_id} | STEP 4 FAILED | "
            "Expected status: Đã xác nhận | "
            f"Actual: {status_after_confirm}"
        )

        report_step(
            test_case_id=test_case_id,
            step_number=4,
            description="Xác nhận lịch hẹn vừa tạo thành công",
            detail=(
                f"Appointment ID: {appointment_id} | "
                f"Status: {status_after_confirm}"
            )
        )

        # ========================================================
        # STEP 5
        # Đăng xuất Admin và đăng nhập bằng Doctor phụ trách.
        # ========================================================

        switch_account(
            driver,
            test_data["doctor_username"],
            test_data["doctor_password"]
        )

        assert driver.current_url == HOME_URL, (
            f"{test_case_id} | STEP 5 FAILED | "
            f"Expected URL: {HOME_URL} | "
            f"Actual URL: {driver.current_url}"
        )

        report_step(
            test_case_id=test_case_id,
            step_number=5,
            description=(
                "Đăng xuất Admin và đăng nhập bằng "
                "Doctor phụ trách thành công"
            )
        )

        # ========================================================
        # STEP 6
        # Mở lịch hẹn và chọn Khám bệnh.
        # ========================================================

        appointment_page = DoctorAppointmentPage(driver)
        appointment_page.open_page()

        actual_note = appointment_page.get_note_by_id(
            appointment_id
        )

        actual_doctor_status = (
            appointment_page.get_status_by_id(
                appointment_id
            )
        )

        assert actual_note == note, (
            f"{test_case_id} | STEP 6 FAILED | "
            f"Expected note: {note} | "
            f"Actual: {actual_note}"
        )

        assert actual_doctor_status == "Đã xác nhận", (
            f"{test_case_id} | STEP 6 FAILED | "
            "Expected status: Đã xác nhận | "
            f"Actual: {actual_doctor_status}"
        )

        assert appointment_page.is_examine_button_present(
            appointment_id
        ), (
            f"{test_case_id} | STEP 6 FAILED | "
            "Expected: Có nút Khám bệnh | "
            "Actual: Không tìm thấy nút Khám bệnh"
        )

        appointment_page.click_examine(
            appointment_id
        )

        examination_page = DoctorExaminationPage(driver)

        actual_title = examination_page.get_page_title()

        assert actual_title == "Khám bệnh", (
            f"{test_case_id} | STEP 6 FAILED | "
            "Expected title: Khám bệnh | "
            f"Actual: {actual_title}"
        )

        assert (
            f"appointmentId={appointment_id}"
            in driver.current_url
        ), (
            f"{test_case_id} | STEP 6 FAILED | "
            f"Expected URL chứa appointmentId={appointment_id} | "
            f"Actual URL: {driver.current_url}"
        )

        report_step(
            test_case_id=test_case_id,
            step_number=6,
            description=(
                "Mở lịch hẹn và chọn Khám bệnh thành công"
            ),
            detail=f"Appointment ID: {appointment_id}"
        )

        # ========================================================
        # STEP 7
        # Nhập thông tin khám và lưu hồ sơ bệnh án.
        # ========================================================

        examination_page.enter_diagnosis(
            diagnosis
        )

        examination_page.enter_treatment(
            treatment
        )

        examination_page.click_save_medical_record()

        medical_record_page = MedicalRecordPage(driver)

        record_title = (
            medical_record_page.get_page_title()
        )

        assert record_title == "Chi tiết hồ sơ bệnh án", (
            f"{test_case_id} | STEP 7 FAILED | "
            "Expected page: Chi tiết hồ sơ bệnh án | "
            f"Actual: {record_title}"
        )

        actual_diagnosis = (
            medical_record_page.get_diagnosis_information()
        )

        actual_treatment = (
            medical_record_page.get_treatment_information()
        )

        assert diagnosis in actual_diagnosis, (
            f"{test_case_id} | STEP 7 FAILED | "
            f"Expected diagnosis chứa: {diagnosis} | "
            f"Actual: {actual_diagnosis}"
        )

        assert treatment in actual_treatment, (
            f"{test_case_id} | STEP 7 FAILED | "
            f"Expected treatment chứa: {treatment} | "
            f"Actual: {actual_treatment}"
        )

        medical_record_api.assert_appointment_status(
            doctor_id=doctor_id,
            appointment_id=appointment_id,
            expected_status="completed"
        )

        report_step(
            test_case_id=test_case_id,
            step_number=7,
            description=(
                "Nhập thông tin khám và lưu hồ sơ bệnh án thành công"
            ),
            detail=(
                f"Diagnosis: {diagnosis} | "
                f"Treatment: {treatment}"
            )
        )

        # ========================================================
        # STEP 8
        # Đăng xuất Doctor và đăng nhập lại bằng Patient.
        # ========================================================

        switch_account(
            driver,
            test_data["patient_username"],
            test_data["patient_password"]
        )

        assert driver.current_url == HOME_URL, (
            f"{test_case_id} | STEP 8 FAILED | "
            f"Expected URL: {HOME_URL} | "
            f"Actual URL: {driver.current_url}"
        )

        report_step(
            test_case_id=test_case_id,
            step_number=8,
            description=(
                "Đăng xuất Doctor và đăng nhập lại "
                "bằng tài khoản Patient thành công"
            )
        )

        # ========================================================
        # STEP 9
        # Mở trang Lịch sử khám bệnh.
        # ========================================================

        history_page = PatientMedicalHistoryPage(driver)
        history_page.open_page()

        history_title = history_page.get_page_title()

        assert history_title == "Lịch sử khám bệnh", (
            f"{test_case_id} | STEP 9 FAILED | "
            "Expected title: Lịch sử khám bệnh | "
            f"Actual: {history_title}"
        )

        report_step(
            test_case_id=test_case_id,
            step_number=9,
            description=(
                "Mở trang Lịch sử khám bệnh thành công"
            )
        )

        # ========================================================
        # STEP 10
        # Kiểm tra bản ghi của lần khám vừa hoàn thành.
        # ========================================================

        record_ids_after_api = get_patient_record_ids(
            medical_record_api,
            patient_id
        )

        record_ids_after_ui = get_ui_record_ids(
            history_page
        )

        new_record_ids = (
            record_ids_after_api
            - record_ids_before
        )

        assert len(new_record_ids) == 1, (
            f"{test_case_id} | STEP 10 FAILED | "
            "Expected: Phát sinh đúng 1 Medical Record mới | "
            f"Actual Medical Record mới: "
            f"{sorted(new_record_ids)}"
        )

        new_record_id = next(iter(new_record_ids))

        assert new_record_id in record_ids_after_ui, (
            f"{test_case_id} | STEP 10 FAILED | "
            f"Expected UI có Medical Record ID: {new_record_id} | "
            f"Actual UI IDs: {sorted(record_ids_after_ui)}"
        )

        assert record_ids_after_ui == record_ids_after_api, (
            f"{test_case_id} | STEP 10 FAILED | "
            f"Expected UI IDs: {sorted(record_ids_after_api)} | "
            f"Actual UI IDs: {sorted(record_ids_after_ui)}"
        )

        report_step(
            test_case_id=test_case_id,
            step_number=10,
            description=(
                "Lần khám vừa hoàn thành được ghi nhận "
                "trong Lịch sử khám bệnh"
            ),
            detail=(
                f"Medical Record mới: {new_record_id} | "
                f"Trước: {len(record_ids_before)} | "
                f"Sau: {len(record_ids_after_api)}"
            )
        )

    finally:
        # TC003 đã hoàn thành khám nên không hủy appointment.
        # Không cleanup Medical Record vì đây là dữ liệu nghiệp vụ
        # đã được tạo hợp lệ trong quá trình test.
        pass