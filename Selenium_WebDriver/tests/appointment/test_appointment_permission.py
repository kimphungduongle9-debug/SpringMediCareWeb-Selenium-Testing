import pytest

from pages.DoctorAppointmentPage import DoctorAppointmentPage
from pages.DoctorExaminationPage import DoctorExaminationPage

from utils.test_reporter import report_step
from tests.helpers.appointment_helpers import (
    login_doctor,
    login_other_doctor,
)
from tests.helpers.appointment_helpers import login_doctor
@pytest.mark.xfail(
    reason=(
        "Known bug: bác sĩ chưa thể xem hồ sơ "
        "bệnh nhân khi lịch đang chờ xác nhận."
    ),
    strict=True
)
def test_tc_appointment_004_doctor_can_view_profile_while_pending(
    driver,
    appointment_tc4_data
):
    """
    TC-APPOINTMENT-004:
    Kiểm tra quyền xem hồ sơ bệnh nhân của bác sĩ
    khi lịch đang ở trạng thái Chờ xác nhận.
    """

    test_case_id = "TC-APPOINTMENT-004"

    appointment_id = appointment_tc4_data["appointment_id"]
    note = appointment_tc4_data["note"]

    # Step 1:
    # Đăng nhập đúng Doctor của lịch
    login_doctor(driver)

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng đúng tài khoản bác sĩ của lịch thành công"
    )

    # Step 2:
    # Mở trang Lịch hẹn bệnh nhân và tìm đúng lịch
    appointment_page = DoctorAppointmentPage(driver)
    appointment_page.open_page()

    actual_note = appointment_page.get_note_by_id(
        appointment_id
    )

    patient_name = appointment_page.get_patient_name_by_note(
        note
    )

    assert actual_note == note, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected note: {note} | Actual: {actual_note}"
    )

    assert patient_name == appointment_tc4_data["patient_name"], (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected patient: {appointment_tc4_data['patient_name']} | "
        f"Actual: {patient_name}"
    )

    report_step(
        test_case_id,
        2,
        "Mở trang Lịch hẹn bệnh nhân và tìm thấy đúng lịch"
    )
    # Step 3:
    # Kiểm tra trạng thái và các nút thao tác
    status = appointment_page.get_status_by_id(
        appointment_id
    )

    assert status == "Chờ xác nhận", (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: Chờ xác nhận | Actual: {status}"
    )

    assert not appointment_page.is_examine_button_present(
        appointment_id
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Lịch Chờ xác nhận vẫn hiển thị nút Khám bệnh"
    )

    assert appointment_page.is_patient_profile_button_present(
        appointment_id
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Bác sĩ không có nút Xem hồ sơ khi lịch đang Chờ xác nhận"
    )

    report_step(
        test_case_id,
        3,
        "Lịch ở trạng thái Chờ xác nhận, không có nút Khám bệnh và có nút Xem hồ sơ"
    )

    # Step 4:
    # Nhấn Xem hồ sơ
    appointment_page.click_view_medical_record(
        note
    )

    report_step(
        test_case_id,
        4,
        "Nhấn Xem hồ sơ bệnh nhân thành công"
    )

def test_tc_appointment_005_doctor_cannot_examine_pending_by_url(
    driver,
    appointment_tc5_data
):
    """
    TC-APPOINTMENT-005:
    Kiểm tra bác sĩ không thể truy cập trực tiếp
    trang khám của lịch chưa được Admin xác nhận.
    """

    test_case_id = "TC-APPOINTMENT-005"
    appointment_id = appointment_tc5_data["appointment_id"]
    note = appointment_tc5_data["note"]

    # Step 1:
    login_doctor(driver)

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng đúng tài khoản bác sĩ của lịch thành công"
    )

    # Step 2:
    appointment_page = DoctorAppointmentPage(driver)
    appointment_page.open_page()

    status = appointment_page.get_status_by_id(
        appointment_id
    )

    assert status == "Chờ xác nhận", (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected: Chờ xác nhận | Actual: {status}"
    )

    assert appointment_page.get_note_by_id(
        appointment_id
    ) == note, (
        f"{test_case_id} | STEP 2 FAILED | "
        "Không tìm thấy đúng lịch hẹn cần kiểm tra"
    )

    report_step(
        test_case_id,
        2,
        "Xác nhận lịch đang ở trạng thái Chờ xác nhận"
    )

    # Step 3:
    examination_page = DoctorExaminationPage(driver)
    examination_page.open_page(
        appointment_id
    )

    invalid_message = (
        examination_page
        .get_invalid_appointment_message()
    )

    assert invalid_message == (
        "Lịch hẹn chưa được xác nhận hoặc đã bị hủy."
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Actual: {invalid_message}"
    )

    report_step(
        test_case_id,
        3,
        "Hệ thống chặn truy cập trực tiếp vào trang Khám bệnh"
    )

    # Step 4:
    assert not examination_page.is_appointment_information_present(), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Thông tin lịch hẹn vẫn được hiển thị"
    )

    assert not examination_page.is_create_record_form_present(), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Form tạo hồ sơ bệnh án vẫn được hiển thị"
    )

    report_step(
        test_case_id,
        4,
        "Không hiển thị thông tin khám và không cho phép tạo hồ sơ bệnh án"
    )

    # Step 5:
    appointment_page.open_page()

    status_after = appointment_page.get_status_by_id(
        appointment_id
    )

    assert status_after == "Chờ xác nhận", (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: Chờ xác nhận | Actual: {status_after}"
    )

    report_step(
        test_case_id,
        5,
        "Lịch vẫn giữ trạng thái Chờ xác nhận và không phát sinh dữ liệu khám"
    )

def test_tc_appointment_006_correct_doctor_can_examine_confirmed(
    driver,
    appointment_tc6_data
):
    """
    TC-APPOINTMENT-006:
    Kiểm tra đúng bác sĩ được phép khám bệnh
    khi lịch hẹn đã được Admin xác nhận.
    """

    test_case_id = "TC-APPOINTMENT-006"
    appointment_id = appointment_tc6_data["appointment_id"]
    note = appointment_tc6_data["note"]

    # Step 1:
    login_doctor(driver)

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng đúng tài khoản bác sĩ của lịch thành công"
    )

    # Step 2:
    appointment_page = DoctorAppointmentPage(driver)
    appointment_page.open_page()

    assert appointment_page.get_note_by_id(
        appointment_id
    ) == note, (
        f"{test_case_id} | STEP 2 FAILED | "
        "Không tìm thấy đúng lịch hẹn của bác sĩ"
    )

    report_step(
        test_case_id,
        2,
        "Mở trang Lịch hẹn bệnh nhân và tìm thấy đúng lịch"
    )

    # Step 3:
    status = appointment_page.get_status_by_id(
        appointment_id
    )

    assert status == "Đã xác nhận", (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: Đã xác nhận | Actual: {status}"
    )

    assert appointment_page.is_examine_button_present(
        appointment_id
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Không có nút Khám bệnh"
    )

    report_step(
        test_case_id,
        3,
        "Lịch ở trạng thái Đã xác nhận và hiển thị nút Khám bệnh"
    )

    # Step 4:
    appointment_page.click_examine(
        appointment_id
    )

    examination_page = DoctorExaminationPage(driver)

    assert examination_page.get_page_title() == "Khám bệnh", (
        f"{test_case_id} | STEP 4 FAILED | "
        "Không mở đúng trang Khám bệnh"
    )

    assert f"appointmentId={appointment_id}" in driver.current_url, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"URL không chứa appointmentId={appointment_id} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id,
        4,
        "Nhấn Khám bệnh và mở đúng lịch hẹn"
    )

    # Step 5:
    assert examination_page.is_create_record_form_present(), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Không hiển thị form khám bệnh"
    )

    report_step(
        test_case_id,
        5,
        "Trang Khám bệnh hiển thị đúng form nhập thông tin khám"
    )

def test_tc_appointment_007_other_doctor_cannot_examine(
    driver,
    appointment_tc7_data
):
    """
    TC-APPOINTMENT-007:
    Kiểm tra bác sĩ khác không thể khám
    lịch hẹn đã xác nhận nhưng không thuộc mình.
    """

    test_case_id = "TC-APPOINTMENT-007"
    appointment_id = appointment_tc7_data["appointment_id"]
    note = appointment_tc7_data["note"]

    # Step 1:
    login_other_doctor(driver)

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản bác sĩ khác thành công"
    )

    # Step 2:
    appointment_page = DoctorAppointmentPage(driver)
    appointment_page.open_page()

    assert not appointment_page.is_appointment_present_by_note(
        note
    ), (
        f"{test_case_id} | STEP 2 FAILED | "
        "Lịch của bác sĩ khác vẫn xuất hiện trong danh sách"
    )

    report_step(
        test_case_id,
        2,
        "Lịch không thuộc bác sĩ hiện tại không xuất hiện trong danh sách"
    )

    # Step 3:
    examination_page = DoctorExaminationPage(driver)

    examination_page.open_page(
        appointment_id
    )

    assert f"appointmentId={appointment_id}" in driver.current_url, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"URL không chứa appointmentId={appointment_id} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id,
        3,
        "Truy cập trực tiếp URL trang Khám bệnh bằng appointmentId"
    )

    # Step 4:
    access_message = (
        examination_page
        .get_access_denied_message()
    )

    assert access_message == "Bạn không có quyền khám lịch hẹn này.", (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Bạn không có quyền khám lịch hẹn này. | "
        f"Actual: {access_message}"
    )

    report_step(
        test_case_id,
        4,
        "Hệ thống từ chối truy cập vì lịch không thuộc bác sĩ"
    )

    # Step 5:
    assert not examination_page.is_appointment_information_present(), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Thông tin lịch hẹn vẫn được hiển thị"
    )

    assert not examination_page.is_create_record_form_present(), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Form tạo hồ sơ bệnh án vẫn được hiển thị"
    )

    report_step(
        test_case_id,
        5,
        "Không hiển thị thông tin khám và không cho phép tạo hồ sơ bệnh án"
    )

def test_tc_appointment_008_doctor_cannot_examine_cancelled(
    driver,
    appointment_tc8_data
):
    """
    TC-APPOINTMENT-008:
    Kiểm tra bác sĩ không thể khám bệnh
    đối với lịch hẹn đã bị Admin hủy.
    """

    test_case_id = "TC-APPOINTMENT-008"
    appointment_id = appointment_tc8_data["appointment_id"]
    note = appointment_tc8_data["note"]

    # Step 1:
    login_doctor(driver)

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng đúng tài khoản bác sĩ của lịch thành công"
    )

    # Step 2:
    appointment_page = DoctorAppointmentPage(driver)
    appointment_page.open_page()

    assert appointment_page.is_appointment_present_by_note(
        note
    ), (
        f"{test_case_id} | STEP 2 FAILED | "
        "Không tìm thấy lịch đã hủy trong danh sách"
    )

    report_step(
        test_case_id,
        2,
        "Mở trang Lịch hẹn bệnh nhân và tìm thấy lịch đã hủy"
    )

    # Step 3:
    status = appointment_page.get_status_by_note(
        note
    )

    assert status == "Đã hủy", (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: Đã hủy | Actual: {status}"
    )

    assert not appointment_page.is_examine_button_present(
        appointment_id
    ), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Lịch đã hủy vẫn hiển thị nút Khám bệnh"
    )

    report_step(
        test_case_id,
        3,
        "Lịch ở trạng thái Đã hủy và không hiển thị nút Khám bệnh"
    )

    # Step 4:
    examination_page = DoctorExaminationPage(driver)

    examination_page.open_page(
        appointment_id
    )

    invalid_message = (
        examination_page
        .get_invalid_appointment_message()
    )

    assert invalid_message == (
        "Lịch hẹn chưa được xác nhận hoặc đã bị hủy."
    ), (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Actual: {invalid_message}"
    )

    report_step(
        test_case_id,
        4,
        "Hệ thống chặn truy cập trực tiếp trang Khám bệnh của lịch đã hủy"
    )

    # Step 5:
    assert not examination_page.is_appointment_information_present(), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Thông tin lịch hẹn vẫn được hiển thị"
    )

    assert not examination_page.is_create_record_form_present(), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Form tạo hồ sơ bệnh án vẫn được hiển thị"
    )

    report_step(
        test_case_id,
        5,
        "Không hiển thị thông tin khám và không cho phép tạo hồ sơ bệnh án"
    )