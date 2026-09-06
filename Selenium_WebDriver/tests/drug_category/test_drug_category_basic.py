import csv
from pathlib import Path

from pages.DrugPage import DrugPage
from utils.test_reporter import report_step


DATA_FILE = (
    Path(__file__).resolve().parents[2]
    / "test_data"
    / "drug_category_test_data.csv"
)


def get_test_data(test_case_id):
    with open(DATA_FILE, encoding="utf-8-sig", newline="") as file:
        rows = csv.DictReader(file)

        for row in rows:
            if row["test_case_id"] == test_case_id:
                return row

    raise ValueError(
        f"Không tìm thấy dữ liệu cho {test_case_id}"
    )


# ============================================================
# TC-DRUG-CATEGORY-001
# Kiểm tra hệ thống hiển thị đầy đủ các danh mục thuốc
# ============================================================
def test_tc_drug_category_001_display_categories(driver):
    """
    TC-DRUG-CATEGORY-001:
    Kiểm tra các danh mục thuốc được hiển thị đầy đủ
    trên trang Quản lý kho dược phẩm.
    """
    test_case_id = "TC-DRUG-CATEGORY-001"
    data = get_test_data(test_case_id)

    page = DrugPage(driver)

    # Step 1:
    page.login_admin(
        data["admin_username"],
        data["admin_password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản Admin hợp lệ thành công"
    )

    # Step 2:
    # Menu Quản lý Kho thuốc tồn tại trên giao diện sau đăng nhập.
    assert "Quản lý Kho thuốc" in driver.page_source, (
        f"{test_case_id} | STEP 2 FAILED | "
        "Không tìm thấy menu Quản lý Kho thuốc"
    )

    report_step(
        test_case_id,
        2,
        "Mở menu Quản lý Kho thuốc"
    )

    # Step 3:
    page.open_list()

    assert "Quản lý kho dược phẩm" in driver.page_source, (
        f"{test_case_id} | STEP 3 FAILED | "
        "Không mở được trang Quản lý kho dược phẩm"
    )

    report_step(
        test_case_id,
        3,
        "Truy cập trang Quản lý kho dược phẩm thành công"
    )

    # Step 4:
    categories = page.get_category_names()

    assert categories, (
        f"{test_case_id} | STEP 4 FAILED | "
        "Không tìm thấy khu vực lọc danh mục thuốc"
    )

    report_step(
        test_case_id,
        4,
        "Xác định khu vực các nút lọc danh mục thuốc",
        detail=f"Categories: {categories}"
    )

    # Step 5:
    assert "Tất cả" in categories, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: Tất cả | Actual: {categories}"
    )

    report_step(
        test_case_id,
        5,
        "Nút Tất cả được hiển thị"
    )

    # Step 6:
    drug_categories = [
        category
        for category in categories
        if category != "Tất cả"
    ]

    assert len(drug_categories) > 0, (
        f"{test_case_id} | STEP 6 FAILED | "
        "Không có danh mục thuốc nào được hiển thị"
    )

    report_step(
        test_case_id,
        6,
        "Các danh mục thuốc được hiển thị dưới dạng nút lọc",
        detail=f"Categories: {drug_categories}"
    )

    # Step 7:
    assert all(
        category.strip()
        for category in drug_categories
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        "Có tên danh mục bị rỗng"
    )

    assert len(drug_categories) == len(set(drug_categories)), (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Có danh mục bị trùng | Actual: {drug_categories}"
    )

    report_step(
        test_case_id,
        7,
        "Tên các danh mục không rỗng và không bị trùng lặp"
    )


# ============================================================
# TC-DRUG-CATEGORY-002
# Kiểm tra lọc thuốc theo danh mục
# ============================================================
def test_tc_drug_category_002_filter_category(driver):
    """
    TC-DRUG-CATEGORY-002:
    Kiểm tra hệ thống chỉ hiển thị các thuốc
    thuộc danh mục được Admin lựa chọn.
    """
    test_case_id = "TC-DRUG-CATEGORY-002"
    data = get_test_data(test_case_id)

    page = DrugPage(driver)

    # Step 1:
    page.login_admin(
        data["admin_username"],
        data["admin_password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản Admin hợp lệ thành công"
    )

    # Step 2:
    page.open_list()

    report_step(
        test_case_id,
        2,
        "Mở trang Quản lý kho dược phẩm thành công"
    )

    # Step 3:
    category = data["category_name"]

    page.select_category(category)

    report_step(
        test_case_id,
        3,
        f"Chọn danh mục {category}"
    )

    # Step 4:
    rows = page.get_table_data()

    assert rows, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Không có thuốc sau khi chọn danh mục {category}"
    )

    report_step(
        test_case_id,
        4,
        "Danh sách thuốc được cập nhật",
        detail=f"Total rows: {len(rows)}"
    )

    # Step 5:
    assert len(rows) > 0, (
        f"{test_case_id} | STEP 5 FAILED | "
        "Không lấy được dòng thuốc nào trong bảng"
    )

    report_step(
        test_case_id,
        5,
        "Lấy các dòng thuốc đang hiển thị trong bảng",
        detail=f"Rows: {len(rows)}"
    )

    # Step 6:
    actual_categories = [
        row["category"]
        for row in rows
    ]

    report_step(
        test_case_id,
        6,
        "Đọc giá trị cột Danh mục của từng thuốc",
        detail=f"Actual: {actual_categories}"
    )

    # Step 7:
    assert all(
        actual == category
        for actual in actual_categories
    ), (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected category: {category} | "
        f"Actual: {actual_categories}"
    )

    report_step(
        test_case_id,
        7,
        f"Tất cả thuốc hiển thị đều thuộc danh mục {category}"
    )


# ============================================================
# TC-DRUG-CATEGORY-003
# Kiểm tra cập nhật giá Franrogyl
# ============================================================
def test_tc_drug_category_003_update_drug(driver):
    """
    TC-DRUG-CATEGORY-003:
    Kiểm tra Admin có thể cập nhật thông tin
    của một thuốc đang tồn tại trong hệ thống.
    """
    test_case_id = "TC-DRUG-CATEGORY-003"
    data = get_test_data(test_case_id)

    page = DrugPage(driver)

    drug_name = data["drug_name"]
    new_price = data["new_price"]

    # Step 1:
    page.login_admin(
        data["admin_username"],
        data["admin_password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản Admin hợp lệ thành công"
    )

    # Step 2:
    page.open_list()

    report_step(
        test_case_id,
        2,
        "Truy cập trang Quản lý kho dược phẩm thành công"
    )

    # Step 3:
    page.search_drug(drug_name)

    drug = page.get_drug(drug_name)

    assert drug is not None, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Không tìm thấy thuốc {drug_name}"
    )

    report_step(
        test_case_id,
        3,
        f"Tìm thấy thuốc {drug_name}",
        detail=str(drug)
    )

    # Step 4:
    page.click_edit_drug(drug_name)

    report_step(
        test_case_id,
        4,
        f"Nhấn nút Sửa của thuốc {drug_name}"
    )

    # Step 5:
    actual_name = page.get_field_value(
        page.NAME_INPUT
    )

    assert actual_name == drug_name, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: {drug_name} | "
        f"Actual: {actual_name}"
    )

    report_step(
        test_case_id,
        5,
        "Trang Cập nhật thuốc hiển thị đúng thông tin Franrogyl"
    )

    # Step 6:
    page.set_price(new_price)

    actual_price = page.get_field_value(
        page.PRICE_INPUT
    )

    assert actual_price == new_price, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected input price: {new_price} | "
        f"Actual: {actual_price}"
    )

    report_step(
        test_case_id,
        6,
        f"Thay đổi trường Giá thành {new_price}"
    )

    # Step 7:
    page.submit_form()

    report_step(
        test_case_id,
        7,
        "Nhấn nút Cập nhật/Lưu"
    )

    # Step 8:
    page.wait.until(
        lambda d:
        "/admin-drugs" in d.current_url
    )

    report_step(
        test_case_id,
        8,
        "Hệ thống xử lý và quay lại danh sách thuốc"
    )

    # Step 9:
    page.search_drug(drug_name)

    updated_drug = page.get_drug(
        drug_name
    )

    assert updated_drug is not None, (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Không tìm thấy {drug_name} sau khi cập nhật"
    )

    report_step(
        test_case_id,
        9,
        f"Tìm lại thuốc {drug_name} thành công"
    )

    # Step 10:
    actual_price = updated_drug["price"]

    assert "12.000" in actual_price, (
        f"{test_case_id} | STEP 10 FAILED | "
        f"Expected price: 12.000đ | "
        f"Actual: {actual_price}"
    )

    report_step(
        test_case_id,
        10,
        "Giá Franrogyl đã được cập nhật thành 12.000đ",
        detail=f"Actual: {actual_price}"
    )


# ============================================================
# TC-DRUG-CATEGORY-004
# Tìm Franrogyl khi chọn Tất cả
# ============================================================
def test_tc_drug_category_004_search_all(driver):
    """
    TC-DRUG-CATEGORY-004:
    Kiểm tra hệ thống tìm kiếm và hiển thị đúng thuốc
    theo tên được Admin nhập.
    """
    test_case_id = "TC-DRUG-CATEGORY-004"
    data = get_test_data(test_case_id)

    page = DrugPage(driver)

    # Step 1:
    page.login_admin(
        data["admin_username"],
        data["admin_password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản Admin hợp lệ thành công"
    )

    # Step 2:
    page.open_list()

    report_step(
        test_case_id,
        2,
        "Mở trang Quản lý kho dược phẩm thành công"
    )

    # Step 3:
    page.select_category("Tất cả")

    report_step(
        test_case_id,
        3,
        "Chọn danh mục Tất cả"
    )

    # Step 4:
    keyword = data["search_keyword"]

    page.search_drug(keyword)

    report_step(
        test_case_id,
        4,
        f'Nhập "{keyword}" vào ô tìm kiếm và thực hiện tìm kiếm'
    )

    # Step 5:
    rows = page.get_table_data()

    assert rows, (
        f"{test_case_id} | STEP 5 FAILED | "
        "Không có kết quả tìm kiếm"
    )

    report_step(
        test_case_id,
        5,
        "Hệ thống trả về kết quả tìm kiếm",
        detail=f"Rows: {rows}"
    )

    # Step 6:
    names = [
        row["name"]
        for row in rows
    ]

    assert all(
        keyword.lower() in name.lower()
        for name in names
    ), (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Keyword: {keyword} | Actual: {names}"
    )

    report_step(
        test_case_id,
        6,
        "Danh sách chỉ hiển thị các thuốc phù hợp với từ khóa",
        detail=f"Names: {names}"
    )


# ============================================================
# TC-DRUG-CATEGORY-005
# Tìm Franrogyl trong sai danh mục
# ============================================================
def test_tc_drug_category_005_search_wrong_category(driver):
    """
    TC-DRUG-CATEGORY-005:
    Kiểm tra hệ thống xử lý đúng khi Admin tìm một thuốc
    không thuộc danh mục đang được chọn.
    """
    test_case_id = "TC-DRUG-CATEGORY-005"
    data = get_test_data(test_case_id)

    page = DrugPage(driver)

    # Step 1:
    page.login_admin(
        data["admin_username"],
        data["admin_password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản Admin hợp lệ thành công"
    )

    # Step 2:
    page.open_list()

    report_step(
        test_case_id,
        2,
        "Mở trang Quản lý kho dược phẩm thành công"
    )

    # Step 3:
    category = data["category_name"]

    page.select_category(category)

    report_step(
        test_case_id,
        3,
        f"Chọn danh mục {category}"
    )

    # Step 4:
    rows = page.get_table_data()

    assert all(
        row["category"] == category
        for row in rows
    ), (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Danh sách chứa thuốc ngoài danh mục {category}"
    )

    report_step(
        test_case_id,
        4,
        f"Danh sách được lọc theo danh mục {category}"
    )

    # Step 5:
    keyword = data["search_keyword"]

    page.search_drug(keyword)

    report_step(
        test_case_id,
        5,
        f'Nhập "{keyword}" vào ô tìm kiếm'
    )

    # Step 6:
    rows = page.get_table_data()

    report_step(
        test_case_id,
        6,
        "Hệ thống trả về kết quả tìm kiếm",
        detail=f"Rows: {rows}"
    )

    # Step 7:
    names = [
        row["name"]
        for row in rows
    ]

    assert data["drug_name"] not in names, (
        f"{test_case_id} | STEP 7 FAILED | "
        f"{data['drug_name']} vẫn xuất hiện trong "
        f"danh mục {category}"
    )

    report_step(
        test_case_id,
        7,
        f"{data['drug_name']} không xuất hiện trong kết quả"
    )

    # Step 8:
    assert all(
        row["category"] == category
        for row in rows
    ), (
        f"{test_case_id} | STEP 8 FAILED | "
        "Có thuốc thuộc danh mục khác xuất hiện"
    )

    report_step(
        test_case_id,
        8,
        "Không có thuốc thuộc danh mục khác xuất hiện"
    )


# ============================================================
# TC-DRUG-CATEGORY-006
# Tìm Franrogyl trong đúng danh mục
# ============================================================
def test_tc_drug_category_006_search_correct_category(driver):
    """
    TC-DRUG-CATEGORY-006:
    Kiểm tra hệ thống xử lý đúng khi Admin tìm một thuốc
    thuộc danh mục đang được chọn.
    """
    test_case_id = "TC-DRUG-CATEGORY-006"
    data = get_test_data(test_case_id)

    page = DrugPage(driver)

    # Step 1:
    page.login_admin(
        data["admin_username"],
        data["admin_password"]
    )

    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản Admin hợp lệ thành công"
    )

    # Step 2:
    page.open_list()

    report_step(
        test_case_id,
        2,
        "Mở trang Quản lý kho dược phẩm thành công"
    )

    # Step 3:
    category = data["category_name"]

    page.select_category(category)

    report_step(
        test_case_id,
        3,
        f"Chọn danh mục {category}"
    )

    # Step 4:
    rows = page.get_table_data()

    assert rows, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Không có dữ liệu trong danh mục {category}"
    )

    assert all(
        row["category"] == category
        for row in rows
    )

    report_step(
        test_case_id,
        4,
        f"Danh sách được lọc theo danh mục {category}"
    )

    # Step 5:
    keyword = data["search_keyword"]

    page.search_drug(keyword)

    report_step(
        test_case_id,
        5,
        f'Nhập "{keyword}" vào ô tìm kiếm'
    )

    # Step 6:
    rows = page.get_table_data()

    report_step(
        test_case_id,
        6,
        "Hệ thống trả về kết quả tìm kiếm",
        detail=f"Rows: {rows}"
    )

    # Step 7:
    drug = page.get_drug(
        data["drug_name"]
    )

    assert drug is not None, (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Không tìm thấy {data['drug_name']}"
    )

    report_step(
        test_case_id,
        7,
        f"{data['drug_name']} xuất hiện trong kết quả"
    )

    # Step 8:
    assert drug["category"] == category, (
        f"{test_case_id} | STEP 8 FAILED | "
        f"Expected: {category} | "
        f"Actual: {drug['category']}"
    )

    report_step(
        test_case_id,
        8,
        f"{data['drug_name']} thuộc đúng danh mục {category}"
    )