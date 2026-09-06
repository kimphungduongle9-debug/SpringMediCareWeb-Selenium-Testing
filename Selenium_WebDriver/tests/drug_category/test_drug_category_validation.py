import csv
import time
import pytest
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


def unique_drug_name(base_name):
    """
    Tạo tên thuốc riêng cho từng lần chạy để test có thể
    chạy lặp lại mà không phụ thuộc dữ liệu của lần chạy trước.
    """
    return f"{base_name} {int(time.time())}"


# ============================================================
# TC-DRUG-CATEGORY-007
# Thêm thuốc với dữ liệu hợp lệ
# ============================================================

def test_tc_drug_category_007_add_valid_drug(driver):
    """
    TC-DRUG-CATEGORY-007:
    Kiểm tra Admin có thể thêm thuốc mới khi nhập
    đầy đủ các thông tin hợp lệ.
    """
    test_case_id = "TC-DRUG-CATEGORY-007"
    data = get_test_data(test_case_id)

    page = DrugPage(driver)
    drug_name = unique_drug_name(data["drug_name"])

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

    report_step(
        test_case_id,
        3,
        "Mở trang Quản lý kho dược phẩm thành công"
    )

    # Step 4:
    page.click_add_button()

    report_step(
        test_case_id,
        4,
        "Nhấn nút Thêm thuốc và mở form thêm thuốc"
    )

    # Step 5:
    page.fill_form(
        category_name=data["category_name"],
        name=drug_name,
        price=data["price"],
        quantity=data["quantity"],
        min_quantity=data["min_quantity"],
        production_date=data["production_date"],
        expiry_date=data["expiry_date"],
        dosage_form=data["dosage_form"],
        unit=data["unit"],
        strength=data["strength"],
        manufacturer=data["manufacturer"],
        status=data["status"]
    )

    report_step(
        test_case_id,
        5,
        "Nhập đầy đủ các thông tin hợp lệ của thuốc",
        detail=f"Drug name: {drug_name}"
    )

    # Step 6:
    page.submit_form()

    report_step(
        test_case_id,
        6,
        "Nhấn nút lưu để thêm thuốc"
    )
    # Step 7:
    try:
        page.wait.until(
            lambda d: "/admin-drugs" in d.current_url
        )
    except Exception:
        validation_errors = page.get_form_validation_errors()
        alert_text = page.get_alert_text()

        assert False, (
            f"{test_case_id} | STEP 7 FAILED | "
            "Hệ thống không chuyển về danh sách sau khi thêm thuốc | "
            f"Current URL: {driver.current_url} | "
            f"Validation: {validation_errors} | "
            f"Alert: {alert_text}"
        )

    report_step(
        test_case_id,
        7,
        "Hệ thống thêm thuốc thành công và quay lại danh sách"
    )

    # Step 8:
    page.open_list()

    report_step(
        test_case_id,
        8,
        "Quay lại danh sách thuốc"
    )

    # Step 9:
    page.search_drug(drug_name)

    report_step(
        test_case_id,
        9,
        f"Tìm kiếm thuốc vừa thêm: {drug_name}"
    )

    # Step 10:
    drug = page.get_drug(drug_name)

    assert drug is not None, (
        f"{test_case_id} | STEP 10 FAILED | "
        f"Expected: thuốc {drug_name} xuất hiện | "
        "Actual: không tìm thấy thuốc"
    )

    report_step(
        test_case_id,
        10,
        "Thuốc vừa thêm xuất hiện trong danh sách",
        detail=str(drug)
    )


# ============================================================
# TC-DRUG-CATEGORY-008
# Thêm thuốc khi thiếu tên thuốc
# ============================================================

def test_tc_drug_category_008_missing_drug_name(driver):
    """
    TC-DRUG-CATEGORY-008:
    Kiểm tra hệ thống không cho phép Admin thêm thuốc
    khi bỏ trống trường Tên thuốc bắt buộc.
    """
    test_case_id = "TC-DRUG-CATEGORY-008"
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

    report_step(
        test_case_id,
        3,
        "Mở trang Quản lý kho dược phẩm thành công"
    )

    # Step 4:
    page.click_add_button()

    report_step(
        test_case_id,
        4,
        "Nhấn nút Thêm thuốc"
    )

    # Step 5:
    page.fill_form(
        category_name=data["category_name"],
        name="",
        price=data["price"],
        quantity=data["quantity"],
        min_quantity=data["min_quantity"],
        production_date=data["production_date"],
        expiry_date=data["expiry_date"],
        dosage_form=data["dosage_form"],
        unit=data["unit"],
        strength=data["strength"],
        manufacturer=data["manufacturer"],
        status=data["status"]
    )

    report_step(
        test_case_id,
        5,
        "Để trống trường Tên thuốc và nhập hợp lệ các trường còn lại"
    )

    # Step 6:
    page.submit_form()

    report_step(
        test_case_id,
        6,
        "Nhấn nút lưu để thêm thuốc"
    )

    # Step 7:
    assert "/drugs/add" in driver.current_url, (
        f"{test_case_id} | STEP 7 FAILED | "
        "Hệ thống vẫn cho phép thêm thuốc khi thiếu Tên thuốc | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        7,
        "Hệ thống không cho phép thêm thuốc khi thiếu Tên thuốc"
    )

    # Step 8:
    validation_message = page.get_validation_message(
        page.NAME_INPUT
    )

    assert validation_message.strip(), (
        f"{test_case_id} | STEP 8 FAILED | "
        "Expected: trường Tên thuốc được yêu cầu nhập | "
        "Actual: không có validation message"
    )

    report_step(
        test_case_id,
        8,
        "Trường Tên thuốc được yêu cầu nhập",
        detail=f"Validation: {validation_message}"
    )

    # Step 9:
    assert "/drugs/add" in driver.current_url, (
        f"{test_case_id} | STEP 9 FAILED | "
        "Thuốc đã được tạo ngoài mong đợi"
    )

    report_step(
        test_case_id,
        9,
        "Thuốc không được tạo trong danh sách"
    )


# ============================================================
# TC-DRUG-CATEGORY-009
# Thêm thuốc với giá trị âm
# ============================================================

def test_tc_drug_category_009_negative_values(driver):
    """
    TC-DRUG-CATEGORY-009:
    Kiểm tra hệ thống không cho phép thêm thuốc
    khi các trường số chứa giá trị âm.
    """
    test_case_id = "TC-DRUG-CATEGORY-009"
    data = get_test_data(test_case_id)

    page = DrugPage(driver)
    drug_name = unique_drug_name(data["drug_name"])

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

    report_step(
        test_case_id,
        3,
        "Mở trang Quản lý kho dược phẩm thành công"
    )

    # Step 4:
    page.click_add_button()

    report_step(
        test_case_id,
        4,
        "Nhấn nút Thêm thuốc"
    )

    # Step 5:
    page.fill_form(
        category_name=data["category_name"],
        name=drug_name,
        price="12000",
        quantity="107",
        min_quantity="20",
        production_date=data["production_date"],
        expiry_date=data["expiry_date"],
        dosage_form=data["dosage_form"],
        unit=data["unit"],
        strength=data["strength"],
        manufacturer=data["manufacturer"],
        status=data["status"]
    )

    report_step(
        test_case_id,
        5,
        "Nhập đầy đủ thông tin hợp lệ của thuốc",
        detail=f"Drug name: {drug_name}"
    )

    # Step 6:
    page.typing(
        *page.PRICE_INPUT,
        "-12000"
    )

    assert page.get_field_value(page.PRICE_INPUT) == "-12000", (
        f"{test_case_id} | STEP 6 FAILED | "
        "Không nhập được giá trị âm vào trường Giá thuốc"
    )

    report_step(
        test_case_id,
        6,
        "Nhập giá trị âm vào trường Giá thuốc"
    )

    # Step 7:
    page.typing(
        *page.QUANTITY_INPUT,
        "-107"
    )

    assert page.get_field_value(page.QUANTITY_INPUT) == "-107", (
        f"{test_case_id} | STEP 7 FAILED | "
        "Không nhập được giá trị âm vào trường Số lượng tồn kho"
    )

    report_step(
        test_case_id,
        7,
        "Nhập giá trị âm vào trường Số lượng tồn kho"
    )

    # Step 8:
    page.typing(
        *page.MIN_QUANTITY_INPUT,
        "-20"
    )

    assert page.get_field_value(page.MIN_QUANTITY_INPUT) == "-20", (
        f"{test_case_id} | STEP 8 FAILED | "
        "Không nhập được giá trị âm vào trường Số lượng tồn tối thiểu"
    )

    report_step(
        test_case_id,
        8,
        "Nhập giá trị âm vào trường Số lượng tồn tối thiểu"
    )

    # Step 9:
    page.submit_form()

    report_step(
        test_case_id,
        9,
        "Nhấn nút lưu để thêm thuốc"
    )

    # Step 10:
    validation_messages = [
        page.get_validation_message(page.PRICE_INPUT),
        page.get_validation_message(page.QUANTITY_INPUT),
        page.get_validation_message(page.MIN_QUANTITY_INPUT),
    ]

    assert "/drugs/add" in driver.current_url, (
        f"{test_case_id} | STEP 10 FAILED | "
        "Hệ thống vẫn cho phép tạo thuốc với giá trị âm"
    )

    assert any(
        message.strip()
        for message in validation_messages
    ), (
        f"{test_case_id} | STEP 10 FAILED | "
        "Không xuất hiện validation cho các trường giá trị âm"
    )

    report_step(
        test_case_id,
        10,
        "Hệ thống không cho phép thêm thuốc với các giá trị âm",
        detail=f"Validation: {validation_messages}"
    )

    # Step 11:
    assert "/drugs/add" in driver.current_url, (
        f"{test_case_id} | STEP 11 FAILED | "
        "Thuốc đã được tạo ngoài mong đợi"
    )

    report_step(
        test_case_id,
        11,
        "Thuốc không được tạo trong danh sách"
    )


# ============================================================
# TC-DRUG-CATEGORY-010
# Ngày hết hạn trước ngày sản xuất
# ============================================================

def test_tc_drug_category_010_expiry_before_production(driver):
    """
    TC-DRUG-CATEGORY-010:
    Kiểm tra hệ thống không cho phép thêm thuốc khi
    Ngày hết hạn nhỏ hơn Ngày sản xuất.

    Known bug:
    Hệ thống hiện tại có thể vẫn cho phép tạo thuốc
    với dữ liệu ngày không hợp lệ.
    """
    test_case_id = "TC-DRUG-CATEGORY-010"
    data = get_test_data(test_case_id)

    page = DrugPage(driver)
    drug_name = unique_drug_name(data["drug_name"])

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

    report_step(
        test_case_id,
        3,
        "Mở trang Quản lý kho dược phẩm thành công"
    )

    # Step 4:
    page.click_add_button()

    report_step(
        test_case_id,
        4,
        "Nhấn nút Thêm thuốc"
    )

    # Step 5:
    page.fill_form(
        category_name=data["category_name"],
        name=drug_name,
        price=data["price"],
        quantity=data["quantity"],
        min_quantity=data["min_quantity"],
        production_date=data["production_date"],
        expiry_date=data["expiry_date"],
        dosage_form=data["dosage_form"],
        unit=data["unit"],
        strength=data["strength"],
        manufacturer=data["manufacturer"],
        status=data["status"]
    )

    report_step(
        test_case_id,
        5,
        "Nhập đầy đủ thông tin của thuốc",
        detail=f"Drug name: {drug_name}"
    )

    # Step 6:
    production_date = page.get_field_value(
        page.PRODUCTION_DATE_INPUT
    )

    assert production_date == data["production_date"], (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: {data['production_date']} | "
        f"Actual: {production_date}"
    )

    report_step(
        test_case_id,
        6,
        f"Nhập Ngày sản xuất là {production_date}"
    )

    # Step 7:
    expiry_date = page.get_field_value(
        page.EXPIRY_DATE_INPUT
    )

    assert expiry_date == data["expiry_date"], (
        f"{test_case_id} | STEP 7 FAILED | "
        f"Expected: {data['expiry_date']} | "
        f"Actual: {expiry_date}"
    )

    report_step(
        test_case_id,
        7,
        f"Nhập Ngày hết hạn là {expiry_date}"
    )

    # Step 8:
    page.submit_form()

    report_step(
        test_case_id,
        8,
        "Nhấn nút lưu để thêm thuốc"
    )
    # Step 9:
    # Chờ hệ thống xử lý sau khi submit.
    # Nếu hệ thống chấp nhận dữ liệu, React sẽ chuyển về /admin-drugs.
    # Nếu validation đúng, form sẽ giữ lại tại /drugs/add.
    try:
        page.wait.until(
            lambda d:
            "/admin-drugs" in d.current_url
        )
        is_created = True
    except Exception:
        is_created = False

    report_step(
        test_case_id,
        9,
        "Kiểm tra hệ thống xử lý dữ liệu ngày sản xuất và ngày hết hạn",
        detail=(
            f"Production date: {production_date} | "
            f"Expiry date: {expiry_date} | "
            f"Current URL: {driver.current_url}"
        )
    )
    # Step 10:
    if is_created:
        report_step(
            test_case_id,
            10,
            "Hệ thống vẫn cho phép tạo thuốc khi "
            "Ngày hết hạn trước Ngày sản xuất",
            status="XFAIL",
            detail=(
                f"Expected: Không tạo thuốc khi HSD < NSX | "
                f"Actual: Hệ thống vẫn tạo thuốc và chuyển về "
                f"{driver.current_url}"
            )
        )

        # Cleanup thuốc sai đã được tạo
        page.open_list()
        page.search_drug(drug_name)

        if page.is_drug_present(drug_name):
            page.click_delete_drug(drug_name)
            page.confirm_delete()

        # Sau cleanup mới kết thúc TC bằng XFAIL
        pytest.xfail(
            f"{test_case_id} | STEP 10 | KNOWN BUG | "
            "Hệ thống vẫn cho phép tạo thuốc khi "
            "Ngày hết hạn trước Ngày sản xuất | "
            f"NSX: {production_date} | HSD: {expiry_date}"
        )

    report_step(
        test_case_id,
        10,
        "Hệ thống không cho phép tạo thuốc khi "
        "Ngày hết hạn trước Ngày sản xuất"
    )

    # Step 11:
    assert "/drugs/add" in driver.current_url, (
        f"{test_case_id} | STEP 11 FAILED | "
        f"Expected: thuốc không được tạo | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        11,
        "Thuốc không xuất hiện trong danh sách"
    )
# ============================================================
# TC-DRUG-CATEGORY-011
# Xóa thuốc
# ============================================================

def test_tc_drug_category_011_delete_drug(driver):
    """
    TC-DRUG-CATEGORY-011:
    Kiểm tra Admin có thể xóa thuốc và thuốc đã xóa
    không còn xuất hiện trong danh sách.
    """
    test_case_id = "TC-DRUG-CATEGORY-011"
    data = get_test_data(test_case_id)

    page = DrugPage(driver)
    drug_name = unique_drug_name(data["drug_name"])

    # --------------------------------------------------------
    # SETUP
    # Tạo riêng một thuốc dùng cho TC011.
    # Không xóa dữ liệu cố định của hệ thống.
    # --------------------------------------------------------
    page.login_admin(
        data["admin_username"],
        data["admin_password"]
    )

    page.open_add()

    page.fill_form(
        category_name=data["category_name"],
        name=drug_name,
        price=data["price"],
        quantity=data["quantity"],
        min_quantity=data["min_quantity"],
        production_date=data["production_date"],
        expiry_date=data["expiry_date"],
        dosage_form=data["dosage_form"],
        unit=data["unit"],
        strength=data["strength"],
        manufacturer=data["manufacturer"],
        status=data["status"]
    )

    page.submit_form()

    page.wait.until(
        lambda d: "/admin-drugs" in d.current_url
    )

    # Step 1:
    report_step(
        test_case_id,
        1,
        "Đăng nhập bằng tài khoản Admin hợp lệ thành công"
    )

    # Step 2:
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

    report_step(
        test_case_id,
        3,
        "Mở trang Quản lý kho dược phẩm thành công"
    )

    # Step 4:
    page.search_drug(drug_name)

    drug = page.get_drug(drug_name)

    assert drug is not None, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Không tìm thấy thuốc cần xóa: {drug_name}"
    )

    report_step(
        test_case_id,
        4,
        "Tìm thấy thuốc cần xóa trong danh sách",
        detail=f"Drug: {drug_name}"
    )

    # Step 5:
    page.click_delete_drug(drug_name)

    report_step(
        test_case_id,
        5,
        "Nhấn nút Xóa của thuốc"
    )

    # Step 6:
    page.confirm_delete()

    report_step(
        test_case_id,
        6,
        "Xác nhận thao tác xóa thuốc"
    )

    # Step 7:
    page.wait_loading_finished()

    report_step(
        test_case_id,
        7,
        "Danh sách thuốc được cập nhật sau khi xóa"
    )

    # Step 8:
    page.search_drug(drug_name)

    report_step(
        test_case_id,
        8,
        "Tìm kiếm lại thuốc vừa xóa"
    )

    # Step 9:
    deleted_drug = page.get_drug(drug_name)

    assert deleted_drug is None, (
        f"{test_case_id} | STEP 9 FAILED | "
        f"Expected: {drug_name} không còn tồn tại | "
        f"Actual: {deleted_drug}"
    )

    report_step(
        test_case_id,
        9,
        "Thuốc đã xóa không còn xuất hiện trong danh sách"
    )