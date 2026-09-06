from pages.StatPage import StatPage
from utils.test_reporter import report_step


def test_tc_stat_001_drugs_by_category(driver):
    """
    TC-STAT-001:
    Kiểm tra hệ thống hiển thị đúng thống kê số lượng thuốc
    theo từng danh mục dưới dạng biểu đồ và bảng dữ liệu.
    """

    test_case_id = "TC-STAT-001"
    page = StatPage(driver)

    # Step 1:
    page.login_admin()

    assert driver.current_url == "http://localhost:3000/", (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected URL: http://localhost:3000/ | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản Admin hợp lệ thành công"
    )

    # Step 2:
    driver.get("http://localhost:3000/admin-drugs")

    report_step(
        test_case_id,
        2,
        "Mở menu Quản lý Kho thuốc"
    )

    # Step 3:
    page.open_drug_statistics()

    assert driver.current_url == page.DRUG_STAT_URL, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected URL: {page.DRUG_STAT_URL} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        3,
        "Truy cập trang Thống kê thuốc thành công"
    )

    # Step 4:
    chart_displayed = page.is_chart_displayed(
        "Thuốc theo danh mục"
    )

    assert chart_displayed, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: biểu đồ Thuốc theo danh mục hiển thị | "
        "Actual: không tìm thấy biểu đồ"
    )

    report_step(
        test_case_id,
        4,
        "Biểu đồ Thuốc theo danh mục được hiển thị"
    )

    # Step 5:
    headers = page.get_table_headers(
        "Thuốc theo danh mục"
    )

    assert headers == [
        "Danh mục thuốc",
        "Số lượng"
    ], (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: ['Danh mục thuốc', 'Số lượng'] | "
        f"Actual: {headers}"
    )

    report_step(
        test_case_id,
        5,
        "Bảng thống kê danh mục thuốc được hiển thị",
        detail=f"Headers: {headers}"
    )

    # Step 6:
    rows = page.get_table_rows(
        "Thuốc theo danh mục"
    )

    assert len(rows) > 0, (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: bảng có dữ liệu | "
        "Actual: bảng rỗng"
    )

    report_step(
        test_case_id,
        6,
        "Ghi nhận số lượng thuốc theo các danh mục",
        detail=f"Data: {rows}"
    )

    # Step 7:
    chart_labels = page.get_chart_labels(
        "Thuốc theo danh mục"
    )

    table_labels = [
        row[0]
        for row in rows
    ]

    # Bỏ các tick số thuộc trục giá trị.
    visible_category_labels = [
        label
        for label in chart_labels
        if not label.replace(".", "").replace(",", "").isdigit()
    ]

    assert visible_category_labels, (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected: biểu đồ có nhãn danh mục | "
        f"Actual chart labels: {chart_labels}"
    )

    # Recharts có thể ẩn bớt label nếu không đủ không gian,
    # nhưng những label đang hiển thị phải thuộc dữ liệu bảng.
    assert all(
        label in table_labels
        for label in visible_category_labels
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected categories thuộc: {table_labels} | "
        f"Actual visible categories: {visible_category_labels}"
    )

    bar_count = page.get_bar_count(
        "Thuốc theo danh mục"
    )

    assert bar_count == len(rows), (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected bars: {len(rows)} | "
        f"Actual bars: {bar_count}"
    )

    report_step(
        test_case_id,
        7,
        "Dữ liệu biểu đồ tương ứng với bảng thống kê",
        detail=(
            f"Table rows: {len(rows)} | "
            f"Chart bars: {bar_count} | "
            f"Visible labels: {visible_category_labels}"
        )
    )

    # Step 8:
    valid_rows = all(
        row[0]
        and row[1].isdigit()
        for row in rows
    )

    assert valid_rows, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Actual data: {rows}"
    )

    report_step(
        test_case_id,
        8,
        "Các danh mục và số lượng hiển thị đầy đủ, "
        "không phát sinh lỗi"
    )


def test_tc_stat_002_patient_statistics(driver):
    """
    TC-STAT-002:
    Kiểm tra thống kê bệnh nhân theo giới tính,
    nhóm tuổi và chuyên khoa; số liệu biểu đồ
    tương ứng với bảng chi tiết.
    """

    test_case_id = "TC-STAT-002"
    page = StatPage(driver)

    # Step 1:
    page.login_admin()

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản Admin hợp lệ thành công"
    )

    # Step 2:
    page.open_admin_statistics()

    assert driver.current_url == page.ADMIN_STAT_URL, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected: {page.ADMIN_STAT_URL} | "
        f"Actual: {driver.current_url}"
    )

    report_step(
        test_case_id,
        2,
        "Mở trang Thống kê và báo cáo thành công"
    )

    # Step 3:
    gender_section = page.scroll_to_section(
        "Bệnh nhân theo giới tính"
    )

    assert gender_section.is_displayed(), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Không tìm thấy khu vực Bệnh nhân theo giới tính"
    )

    report_step(
        test_case_id,
        3,
        "Xác định khu vực Bệnh nhân theo giới tính"
    )

    # Step 4:
    gender_rows = page.get_table_rows(
        "Bệnh nhân theo giới tính"
    )

    assert page.is_chart_displayed(
        "Bệnh nhân theo giới tính"
    ), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Không hiển thị biểu đồ giới tính"
    )

    assert len(gender_rows) > 0, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Bảng giới tính không có dữ liệu"
    )

    report_step(
        test_case_id,
        4,
        "Biểu đồ và bảng bệnh nhân theo giới tính "
        "được hiển thị",
        detail=f"Data: {gender_rows}"
    )

    # Step 5:
    gender_labels = page.get_chart_labels(
        "Bệnh nhân theo giới tính"
    )

    gender_chart_labels = [
        label
        for label in gender_labels
        if not label.replace(".", "").replace(",", "").isdigit()
    ]

    expected_gender_labels = [
        row[0]
        for row in gender_rows
    ]

    assert gender_chart_labels == expected_gender_labels, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: {expected_gender_labels} | "
        f"Actual: {gender_chart_labels}"
    )

    gender_bar_count = page.get_bar_count(
        "Bệnh nhân theo giới tính"
    )

    assert gender_bar_count == len(gender_rows), (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected bars: {len(gender_rows)} | "
        f"Actual bars: {gender_bar_count}"
    )

    report_step(
        test_case_id,
        5,
        "Số nhóm dữ liệu giới tính trên biểu đồ "
        "tương ứng với bảng",
        detail=(
            f"Labels: {gender_chart_labels} | "
            f"Bars: {gender_bar_count}"
        )
    )

    # Step 6:
    age_rows = page.get_table_rows(
        "Bệnh nhân theo nhóm tuổi"
    )

    assert page.is_chart_displayed(
        "Bệnh nhân theo nhóm tuổi"
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        "Không hiển thị biểu đồ nhóm tuổi"
    )

    assert len(age_rows) > 0, (
        f"{test_case_id} | STEP 6 FAILED | "
        "Bảng nhóm tuổi không có dữ liệu"
    )

    report_step(
        test_case_id,
        6,
        "Kiểm tra thống kê Bệnh nhân theo nhóm tuổi",
        detail=f"Data: {age_rows}"
    )

    # Step 7:
    age_labels = page.get_chart_labels(
        "Bệnh nhân theo nhóm tuổi"
    )

    age_chart_labels = [
        label
        for label in age_labels
        if not label.replace(".", "").replace(",", "").isdigit()
    ]

    expected_age_labels = [
        row[0]
        for row in age_rows
    ]

    assert age_chart_labels, (
        f"{test_case_id} | STEP 7 FAILED | "
        "Expected: biểu đồ có nhãn nhóm tuổi | "
        f"Actual labels: {age_labels}"
    )

    assert all(
        label in expected_age_labels
        for label in age_chart_labels
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected groups: {expected_age_labels} | "
        f"Actual chart labels: {age_chart_labels}"
    )

    age_bar_count = page.get_bar_count(
        "Bệnh nhân theo nhóm tuổi"
    )

    assert age_bar_count == len(age_rows), (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected bars: {len(age_rows)} | "
        f"Actual bars: {age_bar_count}"
    )

    report_step(
        test_case_id,
        7,
        "Dữ liệu nhóm tuổi trên biểu đồ tương ứng với bảng",
        detail=(
            f"Visible labels: {age_chart_labels} | "
            f"Bars: {age_bar_count}"
        )
    )

    # Step 8:
    page.scroll_to_section(
        "Bệnh nhân theo chuyên khoa"
    )

    report_step(
        test_case_id,
        8,
        "Di chuyển đến khu vực Bệnh nhân theo chuyên khoa"
    )

    # Step 9:
    specialty_rows = page.get_table_rows(
        "Bệnh nhân theo chuyên khoa"
    )

    assert len(specialty_rows) > 0, (
        f"{test_case_id} | STEP 9 FAILED | "
        "Bảng bệnh nhân theo chuyên khoa không có dữ liệu"
    )

    assert page.is_chart_displayed(
        "Bệnh nhân theo chuyên khoa"
    ), (
        f"{test_case_id} | STEP 9 FAILED | "
        "Không hiển thị biểu đồ bệnh nhân theo chuyên khoa"
    )

    specialty_labels = page.get_chart_labels(
        "Bệnh nhân theo chuyên khoa"
    )

    specialty_chart_labels = [
        label
        for label in specialty_labels
        if not label.replace(".", "").replace(",", "").isdigit()
    ]

    expected_specialty_labels = [
        row[0]
        for row in specialty_rows
    ]

    assert specialty_chart_labels, (
        f"{test_case_id} | STEP 9 FAILED | "
        "Expected: biểu đồ có nhãn chuyên khoa | "
        f"Actual labels: {specialty_labels}"
    )

    assert all(
        label in expected_specialty_labels
        for label in specialty_chart_labels
    ), (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected specialties: {expected_specialty_labels} | "
        f"Actual chart labels: {specialty_chart_labels}"
    )

    specialty_bar_count = page.get_bar_count(
        "Bệnh nhân theo chuyên khoa"
    )

    assert specialty_bar_count == len(specialty_rows), (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected bars: {len(specialty_rows)} | "
        f"Actual bars: {specialty_bar_count}"
    )

    report_step(
        test_case_id,
        9,
        "Biểu đồ và bảng chuyên khoa có dữ liệu tương ứng",
        detail=(
            f"Data: {specialty_rows} | "
            f"Visible labels: {specialty_chart_labels}"
        )
    )

    # Step 10:
    assert not driver.find_elements(
        "css selector",
        ".alert-danger"
    ), (
        f"{test_case_id} | STEP 10 FAILED | "
        "Trang xuất hiện thông báo lỗi"
    )

    report_step(
        test_case_id,
        10,
        "Các khu vực thống kê hiển thị bình thường, "
        "không phát sinh lỗi"
    )


def test_tc_stat_003_monthly_revenue(driver):
    """
    TC-STAT-003:
    Kiểm tra hệ thống hiển thị đúng doanh thu đã thanh toán
    theo các tháng của năm được Admin lựa chọn.
    """

    test_case_id = "TC-STAT-003"
    page = StatPage(driver)

    # Step 1:
    page.login_admin()

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản Admin hợp lệ thành công"
    )

    # Step 2:
    page.open_admin_statistics()

    report_step(
        test_case_id,
        2,
        "Mở trang Thống kê và báo cáo thành công"
    )

    # Step 3:
    page.scroll_to_section(
        "Doanh thu theo tháng"
    )

    report_step(
        test_case_id,
        3,
        "Di chuyển đến khu vực Doanh thu theo tháng"
    )

    # Step 4:
    page.enter_year(2026)

    report_step(
        test_case_id,
        4,
        "Nhập năm 2026"
    )

    # Step 5:
    page.click_view_revenue()

    report_step(
        test_case_id,
        5,
        "Nhấn nút Xem doanh thu"
    )

    # Step 6:
    rows = page.get_table_rows(
        "Doanh thu theo tháng"
    )

    assert len(rows) > 0, (
        f"{test_case_id} | STEP 6 FAILED | "
        "Expected: có dữ liệu doanh thu năm 2026 | "
        "Actual: bảng rỗng"
    )

    report_step(
        test_case_id,
        6,
        "Hệ thống tải dữ liệu doanh thu năm 2026",
        detail=f"Data: {rows}"
    )

    # Step 7:
    assert page.is_chart_displayed(
        "Doanh thu theo tháng"
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        "Không hiển thị biểu đồ doanh thu"
    )

    report_step(
        test_case_id,
        7,
        "Biểu đồ doanh thu theo tháng được hiển thị"
    )

    # Step 8:
    headers = page.get_table_headers(
        "Doanh thu theo tháng"
    )

    assert headers == [
        "Tháng",
        "Doanh thu đã thanh toán"
    ], (
        f"{test_case_id} | STEP 8 FAILED | "
        "Expected headers: "
        "['Tháng', 'Doanh thu đã thanh toán'] | "
        f"Actual headers: {headers}"
    )

    report_step(
        test_case_id,
        8,
        "Bảng doanh thu được hiển thị bên dưới biểu đồ",
        detail=f"Data: {rows}"
    )
    # Step 9:
    chart_labels = page.get_chart_labels(
        "Doanh thu theo tháng"
    )

    chart_months = [
        label
        for label in chart_labels
        if label.startswith("Tháng ")
    ]

    table_months = [
        row[0]
        for row in rows
    ]

    assert chart_months == table_months, (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected months: {table_months} | "
        f"Actual chart months: {chart_months}"
    )

    report_step(
        test_case_id,
        9,
        "Tháng trên biểu đồ tương ứng với dữ liệu trong bảng",
        detail=(
            f"Table months: {table_months} | "
            f"Chart months: {chart_months}"
        )
    )

    # Step 10:
    invalid_currency = [
        row
        for row in rows
        if not page.is_currency_format(row[1])
    ]

    assert not invalid_currency, (
        f"{test_case_id} | STEP 10 FAILED | "
        f"Invalid currency rows: {invalid_currency}"
    )

    report_step(
        test_case_id,
        10,
        "Doanh thu hiển thị đúng định dạng tiền tệ",
        detail=f"Data: {rows}"
    )


def test_tc_stat_004_common_diagnoses(driver):
    """
    TC-STAT-004:
    Kiểm tra danh sách các chẩn đoán và số lượng bệnh nhân
    tại khu vực Bệnh phổ biến trong cộng đồng.
    """

    test_case_id = "TC-STAT-004"
    page = StatPage(driver)

    # Step 1:
    page.login_admin()

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản Admin hợp lệ thành công"
    )

    # Step 2:
    page.open_admin_statistics()

    report_step(
        test_case_id,
        2,
        "Mở trang Thống kê và báo cáo thành công"
    )

    # Step 3:
    page.scroll_to_section(
        "Bệnh phổ biến trong cộng đồng"
    )

    report_step(
        test_case_id,
        3,
        "Di chuyển đến khu vực Bệnh phổ biến trong cộng đồng"
    )

    # Step 4:
    rows = page.get_table_rows(
        "Bệnh phổ biến trong cộng đồng"
    )

    assert len(rows) > 0, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: bảng có dữ liệu | "
        "Actual: bảng rỗng"
    )

    report_step(
        test_case_id,
        4,
        "Bảng thống kê bệnh phổ biến được hiển thị"
    )

    # Step 5:
    headers = page.get_table_headers(
        "Bệnh phổ biến trong cộng đồng"
    )

    assert "Chẩn đoán" in headers, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Actual headers: {headers}"
    )

    report_step(
        test_case_id,
        5,
        "Hiển thị cột Chẩn đoán"
    )

    # Step 6:
    assert "Số lượng bệnh nhân" in headers, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Actual headers: {headers}"
    )

    report_step(
        test_case_id,
        6,
        "Hiển thị cột Số lượng bệnh nhân"
    )

    # Step 7:
    valid_rows = all(
        row[0]
        and row[1].isdigit()
        for row in rows
    )

    assert valid_rows, (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Actual rows: {rows}"
    )

    report_step(
        test_case_id,
        7,
        "Các dòng có chẩn đoán và số lượng bệnh nhân tương ứng",
        detail=f"Data: {rows}"
    )

    # Step 8:
    scroll_ok = page.scroll_inside_section(
        "Bệnh phổ biến trong cộng đồng"
    )

    assert scroll_ok, (
        f"{test_case_id} | STEP 8 FAILED | "
        "Không thể thao tác với bảng"
    )

    report_step(
        test_case_id,
        8,
        "Thực hiện cuộn danh sách dữ liệu"
    )

    # Step 9:
    rows_after_scroll = page.get_table_rows(
        "Bệnh phổ biến trong cộng đồng"
    )

    assert rows_after_scroll == rows, (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Before: {rows} | "
        f"After: {rows_after_scroll}"
    )

    report_step(
        test_case_id,
        9,
        "Dữ liệu vẫn hiển thị ổn định sau khi cuộn"
    )