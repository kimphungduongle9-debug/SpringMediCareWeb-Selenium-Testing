from pages.DoctorPage import DoctorPage
from utils.test_reporter import report_step


def test_tc_doctor_001_display_doctor_list(driver):
    """
    TC-DOCTOR-001:
    Kiểm tra danh sách bác sĩ và thông tin bác sĩ
    được hiển thị đầy đủ khi mở trang.
    """

    test_case_id = "TC-DOCTOR-001"
    doctor_page = DoctorPage(driver)

    # Step 1 - Mở trang bác sĩ
    doctor_page.open_page()
    doctor_page.wait_until_doctors_loaded()

    assert driver.current_url.startswith(
        DoctorPage.URL
    ), (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected URL: {DoctorPage.URL} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        1,
        "Mở trang Bác sĩ thành công"
    )

    # Step 2 - Kiểm tra tiêu đề và số lượng bác sĩ
    actual_title = doctor_page.get_title()
    displayed_count = doctor_page.get_displayed_count()

    assert actual_title == "Danh sách bác sĩ", (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected title: Danh sách bác sĩ | "
        f"Actual title: {actual_title}"
    )

    assert displayed_count == 4, (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected doctor count: 4 | "
        f"Actual doctor count: {displayed_count}"
    )

    report_step(
        test_case_id,
        2,
        "Hiển thị đúng tiêu đề và số lượng bác sĩ",
        detail=f"Số lượng: {displayed_count}"
    )

    # Step 3 - Quan sát các card bác sĩ
    cards = doctor_page.get_doctor_cards()
    actual_card_count = len(cards)

    assert actual_card_count == displayed_count, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected card count: {displayed_count} | "
        f"Actual card count: {actual_card_count}"
    )

    assert actual_card_count == 4, (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: 4 card bác sĩ | "
        f"Actual: {actual_card_count}"
    )

    report_step(
        test_case_id,
        3,
        "Danh sách hiển thị đầy đủ 4 card bác sĩ"
    )

    # Step 4 - Kiểm tra thông tin từng card
    names = []

    for card in cards:
        info = doctor_page.get_doctor_card_information(
            card
        )

        assert info["image"], (
            f"{test_case_id} | STEP 4 FAILED | "
            f"Bác sĩ {info['name']} thiếu hình ảnh"
        )

        assert info["name"], (
            f"{test_case_id} | STEP 4 FAILED | "
            "Có card bác sĩ bị thiếu tên"
        )

        assert info["specialty"], (
            f"{test_case_id} | STEP 4 FAILED | "
            f"Bác sĩ {info['name']} thiếu chuyên khoa"
        )

        assert info["experience"], (
            f"{test_case_id} | STEP 4 FAILED | "
            f"Bác sĩ {info['name']} thiếu kinh nghiệm"
        )

        assert info["booking_button_displayed"], (
            f"{test_case_id} | STEP 4 FAILED | "
            f"Bác sĩ {info['name']} thiếu nút Đặt lịch hẹn"
        )

        names.append(info["name"])

    assert len(names) == len(set(names)), (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected: không trùng bác sĩ | "
        f"Actual names: {names}"
    )

    report_step(
        test_case_id,
        4,
        "Mỗi card hiển thị đầy đủ hình ảnh, tên, chuyên khoa, "
        "kinh nghiệm và nút Đặt lịch hẹn",
        detail=f"Doctors: {', '.join(names)}"
    )


def test_tc_doctor_002_search_existing_doctor(driver):
    """
    TC-DOCTOR-002:
    Kiểm tra tìm kiếm bác sĩ với từ khóa hợp lệ.
    """

    test_case_id = "TC-DOCTOR-002"
    doctor_page = DoctorPage(driver)

    # Step 1
    doctor_page.open_page()

    report_step(
        test_case_id,
        1,
        "Mở trang Bác sĩ thành công"
    )

    # Step 2
    keyword = "Tran Binh"

    doctor_page.enter_search_keyword(
        keyword
    )

    report_step(
        test_case_id,
        2,
        f"Nhập từ khóa tìm kiếm: {keyword}"
    )

    # Step 3
    doctor_page.click_search()
    doctor_page.wait_for_search_results()

    report_step(
        test_case_id,
        3,
        "Nhấn nút Tìm kiếm"
    )

    # Step 4
    cards = doctor_page.get_doctor_cards()
    displayed_count = doctor_page.get_displayed_count()

    names = [
        doctor_page
        .get_doctor_card_information(card)["name"]
        for card in cards
    ]

    assert displayed_count == len(cards), (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected displayed count: {len(cards)} | "
        f"Actual: {displayed_count}"
    )

    assert len(cards) == 1, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: 1 bác sĩ Tran Binh | "
        f"Actual count: {len(cards)}"
    )

    assert all(
        keyword.lower() in name.lower()
        for name in names
    ), (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected keyword: {keyword} | "
        f"Actual doctors: {names}"
    )

    info = (
        doctor_page
        .get_doctor_card_information(cards[0])
    )

    assert (
        info["specialty"]
        and info["experience"]
        and info["booking_button_displayed"]
    ), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Card kết quả thiếu thông tin hoặc nút Đặt lịch"
    )

    report_step(
        test_case_id,
        4,
        "Tìm thấy đúng bác sĩ Tran Binh và không hiển thị "
        "bác sĩ không phù hợp",
        detail=f"Actual: {names}"
    )


def test_tc_doctor_003_search_non_existing_doctor(driver):
    """
    TC-DOCTOR-003:
    Kiểm tra tìm kiếm bác sĩ với từ khóa không tồn tại.
    """

    test_case_id = "TC-DOCTOR-003"
    doctor_page = DoctorPage(driver)

    # Step 1
    doctor_page.open_page()

    report_step(
        test_case_id,
        1,
        "Mở trang Bác sĩ thành công"
    )

    # Step 2
    keyword = "Nguyen Van A"

    doctor_page.enter_search_keyword(
        keyword
    )

    report_step(
        test_case_id,
        2,
        f"Nhập tên bác sĩ không tồn tại: {keyword}"
    )

    # Step 3
    doctor_page.click_search()
    doctor_page.wait_for_no_results()

    report_step(
        test_case_id,
        3,
        "Nhấn nút Tìm kiếm"
    )

    # Step 4
    displayed_count = doctor_page.get_displayed_count()
    actual_cards = doctor_page.get_card_count()
    message = doctor_page.get_no_result_message()

    assert displayed_count == 0, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected displayed count: 0 | "
        f"Actual: {displayed_count}"
    )

    assert actual_cards == 0, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected card count: 0 | "
        f"Actual: {actual_cards}"
    )

    assert "KHÔNG có kết quả phù hợp" in message, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: thông báo không có kết quả | "
        f"Actual: {message}"
    )

    report_step(
        test_case_id,
        4,
        "Không hiển thị bác sĩ không phù hợp và hiển thị "
        "trạng thái không có kết quả",
        detail=message
    )


def test_tc_doctor_004_booking_correct_doctor(driver):
    """
    TC-DOCTOR-004:
    Kiểm tra nút Đặt lịch hẹn điều hướng đúng
    đến bác sĩ được chọn.
    """

    test_case_id = "TC-DOCTOR-004"
    doctor_page = DoctorPage(driver)
    doctor_name = "Tran Binh"

    # Step 1
    doctor_page.open_page()

    report_step(
        test_case_id,
        1,
        "Mở trang Bác sĩ thành công"
    )

    # Step 2
    card = doctor_page.get_doctor_card_by_name(
        doctor_name
    )

    assert card.is_displayed(), (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Không tìm thấy bác sĩ {doctor_name}"
    )

    report_step(
        test_case_id,
        2,
        f"Chọn bác sĩ {doctor_name}"
    )

    # Step 3
    doctor_page.click_booking_of_doctor(
        doctor_name
    )

    report_step(
        test_case_id,
        3,
        f"Nhấn Đặt lịch hẹn của bác sĩ {doctor_name}"
    )

    # Step 4
    assert "/booking?doctorId=" in driver.current_url, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected URL chứa /booking?doctorId= | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        4,
        "Hệ thống điều hướng đến trang Đặt lịch hẹn",
        detail=f"URL: {driver.current_url}"
    )

    # Step 5
    actual_doctor = (
        doctor_page.get_booking_doctor_name()
    )

    assert actual_doctor == doctor_name, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected doctor: {doctor_name} | "
        f"Actual doctor: {actual_doctor}"
    )

    report_step(
        test_case_id,
        5,
        "Trang Đặt lịch hiển thị đúng bác sĩ đã chọn",
        detail=f"Expected: {doctor_name} | Actual: {actual_doctor}"
    )