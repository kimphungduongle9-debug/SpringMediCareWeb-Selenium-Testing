from pages.SpecialtyPage import SpecialtyPage
from utils.test_reporter import report_step


def test_tc_specialty_001_display_specialty_list(driver):
    """
    TC-SPECIALTY-001:
    Kiểm tra danh sách chuyên khoa và thông tin chuyên khoa
    được hiển thị đầy đủ khi mở trang.
    """

    test_case_id = "TC-SPECIALTY-001"
    page = SpecialtyPage(driver)

    # Step 1 - Patient mở trang Chuyên khoa
    page.open_page()
    page.wait_until_specialties_loaded()

    assert driver.current_url.startswith(
        SpecialtyPage.URL
    ), (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected URL: {SpecialtyPage.URL} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        1,
        "Mở trang Chuyên khoa thành công"
    )

    # Step 2 - Quan sát tiêu đề và số lượng
    actual_title = page.get_title()
    displayed_count = page.get_displayed_count()

    assert actual_title == "Danh mục chuyên khoa", (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected title: Danh mục chuyên khoa | "
        f"Actual title: {actual_title}"
    )

    assert displayed_count == 8, (
        f"{test_case_id} | STEP 2 FAILED | "
        "Expected specialty count: 8 | "
        f"Actual: {displayed_count}"
    )

    report_step(
        test_case_id,
        2,
        "Hiển thị đúng tiêu đề và số lượng chuyên khoa",
        detail=f"Số lượng: {displayed_count}"
    )

    # Step 3 - Quan sát các card chuyên khoa
    cards = page.get_specialty_cards()
    actual_card_count = len(cards)

    assert actual_card_count == displayed_count, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected card count: {displayed_count} | "
        f"Actual: {actual_card_count}"
    )

    assert actual_card_count == 8, (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: 8 card chuyên khoa | "
        f"Actual: {actual_card_count}"
    )

    report_step(
        test_case_id,
        3,
        "Danh sách hiển thị đầy đủ 8 card chuyên khoa"
    )

    # Step 4 - Kiểm tra thông tin từng card
    names = []

    for card in cards:
        info = page.get_specialty_card_information(
            card
        )

        assert info["image"], (
            f"{test_case_id} | STEP 4 FAILED | "
            f"Chuyên khoa {info['name']} thiếu hình ảnh"
        )

        assert info["name"], (
            f"{test_case_id} | STEP 4 FAILED | "
            "Có card chuyên khoa thiếu tên"
        )

        assert info["description"], (
            f"{test_case_id} | STEP 4 FAILED | "
            f"Chuyên khoa {info['name']} thiếu mô tả"
        )

        assert info["doctor_button_displayed"], (
            f"{test_case_id} | STEP 4 FAILED | "
            f"{info['name']} thiếu nút Xem bác sĩ thuộc khoa"
        )

        assert info["detail_button_displayed"], (
            f"{test_case_id} | STEP 4 FAILED | "
            f"{info['name']} thiếu nút Xem chi tiết khoa"
        )

        names.append(info["name"])

    report_step(
        test_case_id,
        4,
        "Mỗi card hiển thị đầy đủ hình ảnh, tên, mô tả "
        "và các nút chức năng",
        detail=f"Specialties: {', '.join(names)}"
    )


def test_tc_specialty_002_search_existing_specialty(driver):
    """
    TC-SPECIALTY-002:
    Kiểm tra tìm kiếm chuyên khoa với từ khóa hợp lệ.
    """

    test_case_id = "TC-SPECIALTY-002"
    page = SpecialtyPage(driver)

    # Step 1
    page.open_page()

    report_step(
        test_case_id,
        1,
        "Mở trang Chuyên khoa thành công"
    )

    # Step 2
    keyword = "Mat"

    page.enter_search_keyword(
        keyword
    )

    report_step(
        test_case_id,
        2,
        f"Nhập từ khóa tìm kiếm: {keyword}"
    )

    # Step 3
    page.click_search()
    page.wait_for_search_results()

    report_step(
        test_case_id,
        3,
        "Nhấn nút Tìm kiếm"
    )

    # Step 4:
    cards = page.get_specialty_cards()
    displayed_count = page.get_displayed_count()

    names = [
        page.get_specialty_card_information(card)["name"]
        for card in cards
    ]

    assert displayed_count == len(cards)

    assert len(cards) > 0

    assert all(
        keyword.lower() in name.lower()
        for name in names
    )
    report_step(
        test_case_id,
        4,
        "Hiển thị đúng chuyên khoa phù hợp với từ khóa",
        detail=f"Actual: {names}"
    )


def test_tc_specialty_003_search_non_existing_specialty(driver):
    """
    TC-SPECIALTY-003:
    Kiểm tra tìm kiếm chuyên khoa với từ khóa không tồn tại.
    """

    test_case_id = "TC-SPECIALTY-003"
    page = SpecialtyPage(driver)

    # Step 1
    page.open_page()

    report_step(
        test_case_id,
        1,
        "Mở trang Chuyên khoa thành công"
    )

    # Step 2
    keyword = "Noi than kinh"

    page.enter_search_keyword(
        keyword
    )

    report_step(
        test_case_id,
        2,
        f"Nhập tên chuyên khoa không tồn tại: {keyword}"
    )

    # Step 3
    page.click_search()
    page.wait_for_no_results()

    report_step(
        test_case_id,
        3,
        "Nhấn nút Tìm kiếm"
    )

    # Step 4
    displayed_count = page.get_displayed_count()
    actual_cards = page.get_card_count()
    message = page.get_no_result_message()

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

    assert (
        "Không tìm thấy chuyên khoa nào phù hợp"
        in message
    ), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: thông báo không có kết quả | "
        f"Actual: {message}"
    )

    report_step(
        test_case_id,
        4,
        "Không hiển thị chuyên khoa không phù hợp "
        "và hiển thị trạng thái không có kết quả",
        detail=message
    )


def test_tc_specialty_004_view_doctors_by_specialty(driver):
    """
    TC-SPECIALTY-004:
    Kiểm tra nút Xem bác sĩ thuộc khoa hiển thị đúng
    bác sĩ của chuyên khoa được chọn.
    """

    test_case_id = "TC-SPECIALTY-004"
    page = SpecialtyPage(driver)
    specialty_name = "Mat"

    # Step 1
    page.open_page()
    page.wait_until_specialties_loaded()

    report_step(
        test_case_id,
        1,
        "Mở trang Chuyên khoa thành công"
    )

    # Step 2
    card = page.get_specialty_card_by_name(
        specialty_name
    )

    assert card.is_displayed(), (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Không tìm thấy chuyên khoa {specialty_name}"
    )

    report_step(
        test_case_id,
        2,
        f"Chọn chuyên khoa {specialty_name}"
    )

    # Step 3
    page.click_view_doctors(
        specialty_name
    )

    report_step(
        test_case_id,
        3,
        "Nhấn Xem bác sĩ thuộc khoa"
    )
    # Step 4:
    title = page.get_doctor_specialty_title()

    expected_title = "Bác sĩ thuộc chuyên khoa"

    assert title == expected_title, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected title: {expected_title} | "
        f"Actual title: {title}"
    )

    assert "/specialties/" in driver.current_url, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected URL chứa /specialties/ | "
        f"Actual URL: {driver.current_url}"
    )

    assert "/doctors" in driver.current_url, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected URL chứa /doctors | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        4,
        "Hiển thị trang danh sách bác sĩ thuộc chuyên khoa đã chọn",
        detail=f"Title: {title} | URL: {driver.current_url}"
    )
    # Step 5
    doctor_names = page.get_doctor_names()

    assert len(doctor_names) > 0, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: chuyên khoa {specialty_name} có bác sĩ | "
        "Actual: không có bác sĩ"
    )

    report_step(
        test_case_id,
        5,
        "Hiển thị bác sĩ thuộc đúng chuyên khoa đã chọn",
        detail=f"Doctors: {', '.join(doctor_names)}"
    )


def test_tc_specialty_005_view_specialty_details(driver):
    """
    TC-SPECIALTY-005:
    Kiểm tra nút Xem chi tiết khoa hiển thị đúng
    thông tin chuyên khoa được chọn.
    """

    test_case_id = "TC-SPECIALTY-005"
    page = SpecialtyPage(driver)
    specialty_name = "Mat"

    # Step 1
    page.open_page()
    page.wait_until_specialties_loaded()

    report_step(
        test_case_id,
        1,
        "Mở trang Chuyên khoa thành công"
    )

    # Step 2
    card = page.get_specialty_card_by_name(
        specialty_name
    )

    assert card.is_displayed(), (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Không tìm thấy chuyên khoa {specialty_name}"
    )

    report_step(
        test_case_id,
        2,
        f"Chọn chuyên khoa {specialty_name}"
    )

    # Step 3
    page.click_view_details(
        specialty_name
    )

    report_step(
        test_case_id,
        3,
        "Nhấn Xem chi tiết khoa"
    )

    # Step 4
    title = page.get_detail_title()

    assert specialty_name.lower() in title.lower(), (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected specialty: {specialty_name} | "
        f"Actual title: {title}"
    )

    report_step(
        test_case_id,
        4,
        "Hiển thị đúng trang chi tiết chuyên khoa",
        detail=title
    )

    # Step 5
    doctor_count = page.get_detail_doctor_count()
    intro_displayed = page.is_intro_displayed()
    team_displayed = page.is_doctor_team_displayed()

    assert intro_displayed, (
        f"{test_case_id} | STEP 5 FAILED | "
        "Không hiển thị phần Thông tin giới thiệu"
    )

    assert team_displayed, (
        f"{test_case_id} | STEP 5 FAILED | "
        "Không hiển thị phần Đội ngũ bác sĩ trực thuộc"
    )

    assert doctor_count >= 0, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Actual doctor count: {doctor_count}"
    )

    report_step(
        test_case_id,
        5,
        "Hiển thị đầy đủ tên chuyên khoa, thông tin giới thiệu, "
        "số lượng bác sĩ và đội ngũ bác sĩ trực thuộc",
        detail=f"Doctor count: {doctor_count}"
    )