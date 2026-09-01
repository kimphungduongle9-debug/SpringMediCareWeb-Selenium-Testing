from pages.RegisterPage import RegisterPage
from tests.helpers.register_helpers import (
    get_register_test_data,
    get_avatar_path,
    create_unique_value
)
from utils.test_reporter import report_step


REGISTER_URL = "http://localhost:3000/register"


# ============================================================
# TC-REGISTER-018
# ============================================================

def test_tc_register_018_existing_username(driver):
    """
    TC-REGISTER-018:
    Kiểm tra đăng ký với Tên đăng nhập đã tồn tại.
    """

    test_case_id = "TC-REGISTER-018"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký với Tên đăng nhập đã tồn tại"
    )

    data = get_register_test_data(test_case_id)

    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    username = data["username_prefix"]
    password = data["password"]
    confirm_password = data["confirm_password"]

    email = (
        f"{create_unique_value(data['email_prefix'])}"
        f"@gmail.com"
    )

    avatar_path = get_avatar_path(
        data["avatar"]
    )

    register_page = RegisterPage(driver)

    # STEP 1: Mở trang đăng ký
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

    # STEP 2: Nhập Tên đăng nhập đã tồn tại
    register_page.enter_username(username)

    report_step(
        test_case_id,
        2,
        f"Nhập Tên đăng nhập đã tồn tại: {username}"
    )

    # STEP 3: Nhập hợp lệ các trường còn lại
    register_page.enter_first_name(first_name)
    register_page.enter_last_name(last_name)
    register_page.enter_email(email)
    register_page.enter_phone(phone)
    register_page.enter_password(password)
    register_page.enter_confirm_password(confirm_password)
    register_page.upload_avatar(avatar_path)

    report_step(
        test_case_id,
        3,
        (
            "Nhập hợp lệ các trường còn lại | "
            f"Email: {email}"
        )
    )

    # STEP 4: Nhấn nút Đăng ký
    register_page.click_register()

    report_step(
        test_case_id,
        4,
        "Nhấn nút Đăng ký"
    )

    # STEP 5: Kiểm tra kết quả
    actual_message = register_page.get_error_message()

    expected_message = "Tên đăng nhập đã tồn tại"

    assert expected_message in actual_message, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: '{expected_message}' | "
        f"Actual: '{actual_message}'"
    )

    assert driver.current_url == REGISTER_URL, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected URL: {REGISTER_URL} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        5,
        (
            "Hệ thống không tạo tài khoản và hiển thị "
            "thông báo Tên đăng nhập đã tồn tại | "
            f"Expected: {expected_message} | "
            f"Actual: {actual_message}"
        )
    )

# ============================================================
# TC-REGISTER-019
# ============================================================

def test_tc_register_019_existing_email(driver):
    """
    TC-REGISTER-019:
    Kiểm tra đăng ký với Email đã tồn tại.
    """

    test_case_id = "TC-REGISTER-019"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký với Email đã tồn tại"
    )

    data = get_register_test_data(test_case_id)

    first_name = data["first_name"]
    last_name = data["last_name"]
    existing_email = data["email_prefix"]
    phone = data["phone"]
    password = data["password"]
    confirm_password = data["confirm_password"]

    # Username phải mới để lỗi thực sự đến từ Email
    username = create_unique_value(
        data["username_prefix"]
    )

    avatar_path = get_avatar_path(
        data["avatar"]
    )

    register_page = RegisterPage(driver)

    # STEP 1: Mở trang đăng ký
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

    # STEP 2: Nhập Email đã tồn tại
    register_page.enter_email(existing_email)

    report_step(
        test_case_id,
        2,
        f"Nhập Email đã tồn tại: {existing_email}"
    )

    # STEP 3: Nhập hợp lệ các trường còn lại
    register_page.enter_first_name(first_name)
    register_page.enter_last_name(last_name)
    register_page.enter_phone(phone)
    register_page.enter_username(username)
    register_page.enter_password(password)
    register_page.enter_confirm_password(confirm_password)
    register_page.upload_avatar(avatar_path)

    report_step(
        test_case_id,
        3,
        (
            "Nhập hợp lệ các trường còn lại | "
            f"Username mới: {username}"
        )
    )

    # STEP 4: Nhấn nút Đăng ký
    register_page.click_register()

    report_step(
        test_case_id,
        4,
        "Nhấn nút Đăng ký"
    )

    # STEP 5: Kiểm tra kết quả
    actual_message = register_page.get_error_message()

    expected_message = "Email đã tồn tại"

    assert expected_message in actual_message, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: '{expected_message}' | "
        f"Actual: '{actual_message}'"
    )

    assert driver.current_url == REGISTER_URL, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected URL: {REGISTER_URL} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        5,
        (
            "Hệ thống không tạo tài khoản và hiển thị "
            "thông báo Email đã tồn tại | "
            f"Expected: {expected_message} | "
            f"Actual: {actual_message}"
        )
    )