from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.RegisterPage import RegisterPage
from tests.helpers.register_helpers import (
    get_register_test_data,
    get_avatar_path,
    create_unique_value
)
from utils.test_reporter import report_step
from pathlib import Path

REGISTER_URL = "http://localhost:3000/register"

# ============================================================
# TC-REGISTER-001
# ============================================================

def test_tc_register_001_valid_registration(driver):
    """
    TC-REGISTER-001:
    Kiểm tra đăng ký tài khoản với thông tin hợp lệ.
    """

    test_case_id = "TC-REGISTER-001"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký tài khoản với thông tin hợp lệ"
    )

    data = get_register_test_data(test_case_id)

    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    password = data["password"]
    confirm_password = data["confirm_password"]
    expected_url = data["expected_url"]

    unique_email_value = create_unique_value(
        data["email_prefix"]
    )

    unique_username = create_unique_value(
        data["username_prefix"]
    )

    email = f"{unique_email_value}@gmail.com"
    username = unique_username

    avatar_path = get_avatar_path(data["avatar"])

    register_page = RegisterPage(driver)

    # ========================================================
    # STEP 1: Mở trang đăng ký
    # ========================================================

    register_page.open_page()

    assert driver.current_url == REGISTER_URL, (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected URL: {REGISTER_URL} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        1,
        "Mở trang đăng ký thành công"
    )

    # ========================================================
    # STEP 2: Nhập đầy đủ thông tin hợp lệ
    # ========================================================

    register_page.enter_first_name(first_name)
    register_page.enter_last_name(last_name)
    register_page.enter_email(email)
    register_page.enter_phone(phone)
    register_page.enter_username(username)
    register_page.enter_password(password)
    register_page.enter_confirm_password(confirm_password)

    report_step(
        test_case_id,
        2,
        (
            "Nhập đầy đủ thông tin hợp lệ | "
            f"Email: {email} | "
            f"Username: {username}"
        )
    )

    # ========================================================
    # STEP 3: Chọn ảnh đại diện hợp lệ
    # ========================================================

    assert Path(avatar_path).exists(), (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Không tìm thấy file avatar: {avatar_path}"
    )

    register_page.upload_avatar(avatar_path)

    report_step(
        test_case_id,
        3,
        f"Chọn ảnh đại diện hợp lệ: {data['avatar']}"
    )

    # ========================================================
    # STEP 4: Nhấn nút Đăng ký
    # ========================================================

    register_page.click_register()

    report_step(
        test_case_id,
        4,
        "Nhấn nút Đăng ký"
    )

    # ========================================================
    # STEP 5: Kiểm tra kết quả
    # ========================================================

    WebDriverWait(driver, 10).until(
        EC.url_to_be(expected_url)
    )

    actual_url = driver.current_url

    assert actual_url == expected_url, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected URL: {expected_url} | "
        f"Actual URL: {actual_url}"
    )

    report_step(
        test_case_id,
        5,
        (
            "Đăng ký thành công | "
            f"Expected URL: {expected_url} | "
            f"Actual URL: {actual_url}"
        )
    )