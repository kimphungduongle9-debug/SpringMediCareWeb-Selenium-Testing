from pages.RegisterPage import RegisterPage
from tests.helpers.register_helpers import (
    get_register_test_data,
    get_avatar_path,
    create_unique_value
)
from utils.test_reporter import report_step


REGISTER_URL = "http://localhost:3000/register"


# ============================================================
# TC-REGISTER-010
# ============================================================

def test_tc_register_010_invalid_email_format(driver):
    """
    TC-REGISTER-010:
    Kiểm tra đăng ký với Email sai định dạng.
    """

    test_case_id = "TC-REGISTER-010"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký với Email sai định dạng"
    )

    data = get_register_test_data(test_case_id)

    first_name = data["first_name"]
    last_name = data["last_name"]
    invalid_email = data["email_prefix"]
    phone = data["phone"]
    password = data["password"]
    confirm_password = data["confirm_password"]

    username = create_unique_value(
        data["username_prefix"]
    )

    avatar_path = get_avatar_path(
        data["avatar"]
    )

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
    # STEP 2: Nhập Email sai định dạng
    # ========================================================

    register_page.enter_email(invalid_email)

    report_step(
        test_case_id,
        2,
        f"Nhập Email sai định dạng: {invalid_email}"
    )

    # ========================================================
    # STEP 3: Nhập hợp lệ các trường còn lại
    # ========================================================

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
            f"Username: {username}"
        )
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

    actual_message = register_page.get_email_validation_message()

    assert actual_message.strip() != "", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: hiển thị thông báo Email không hợp lệ | "
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
            "thông báo Email không hợp lệ | "
            f"Expected: Email không hợp lệ | "
            f"Actual message: {actual_message}"
        )
    )

# ============================================================
# TC-REGISTER-011
# ============================================================

def test_tc_register_011_invalid_phone_format(driver):
    """
    TC-REGISTER-011:
    Kiểm tra đăng ký với Số điện thoại sai định dạng.
    """

    test_case_id = "TC-REGISTER-011"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký với Số điện thoại sai định dạng"
    )

    data = get_register_test_data(test_case_id)

    first_name = data["first_name"]
    last_name = data["last_name"]
    invalid_phone = data["phone"]
    password = data["password"]
    confirm_password = data["confirm_password"]

    email = (
        f"{create_unique_value(data['email_prefix'])}"
        f"@gmail.com"
    )

    username = create_unique_value(
        data["username_prefix"]
    )

    avatar_path = get_avatar_path(
        data["avatar"]
    )

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
    # STEP 2: Nhập Số điện thoại sai định dạng
    # ========================================================

    register_page.enter_phone(invalid_phone)

    report_step(
        test_case_id,
        2,
        f"Nhập Số điện thoại sai định dạng: {invalid_phone}"
    )

    # ========================================================
    # STEP 3: Nhập hợp lệ các trường còn lại
    # ========================================================

    register_page.enter_first_name(first_name)
    register_page.enter_last_name(last_name)
    register_page.enter_email(email)
    register_page.enter_username(username)
    register_page.enter_password(password)
    register_page.enter_confirm_password(confirm_password)
    register_page.upload_avatar(avatar_path)

    report_step(
        test_case_id,
        3,
        (
            "Nhập hợp lệ các trường còn lại | "
            f"Email: {email} | "
            f"Username: {username}"
        )
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
    actual_message = register_page.get_error_message()

    expected_message = "Số điện thoại phải gồm đúng 10 chữ số"

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
            "thông báo Số điện thoại không hợp lệ | "
            f"Expected: {expected_message} | "
            f"Actual: {actual_message}"
        )
    )

# ============================================================
# TC-REGISTER-012
# ============================================================

def test_tc_register_012_confirm_password_mismatch(driver):
    """
    TC-REGISTER-012:
    Kiểm tra đăng ký khi Xác nhận mật khẩu không khớp.
    """

    test_case_id = "TC-REGISTER-012"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký khi Xác nhận mật khẩu không khớp"
    )

    data = get_register_test_data(test_case_id)

    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    password = data["password"]
    confirm_password = data["confirm_password"]

    email = (
        f"{create_unique_value(data['email_prefix'])}"
        f"@gmail.com"
    )

    username = create_unique_value(
        data["username_prefix"]
    )

    avatar_path = get_avatar_path(
        data["avatar"]
    )

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
    # STEP 2: Nhập mật khẩu và xác nhận mật khẩu không khớp
    # ========================================================

    register_page.enter_password(password)
    register_page.enter_confirm_password(confirm_password)

    report_step(
        test_case_id,
        2,
        (
            "Nhập Mật khẩu và Xác nhận mật khẩu không khớp | "
            f"Password: {password} | "
            f"Confirm Password: {confirm_password}"
        )
    )

    # ========================================================
    # STEP 3: Nhập hợp lệ các trường còn lại
    # ========================================================

    register_page.enter_first_name(first_name)
    register_page.enter_last_name(last_name)
    register_page.enter_email(email)
    register_page.enter_phone(phone)
    register_page.enter_username(username)
    register_page.upload_avatar(avatar_path)

    report_step(
        test_case_id,
        3,
        (
            "Nhập hợp lệ các trường còn lại | "
            f"Email: {email} | "
            f"Username: {username}"
        )
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

    actual_message = register_page.get_error_message()

    expected_message = "Mật khẩu xác nhận không khớp"

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
            "thông báo Xác nhận mật khẩu không khớp | "
            f"Expected: {expected_message} | "
            f"Actual: {actual_message}"
        )
    )

# ============================================================
# TC-REGISTER-013
# ============================================================

def test_tc_register_013_password_too_short(driver):
    """
    TC-REGISTER-013:
    Kiểm tra đăng ký với Mật khẩu ngắn hơn 7 ký tự.
    """

    test_case_id = "TC-REGISTER-013"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký với Mật khẩu ngắn hơn 7 ký tự"
    )

    data = get_register_test_data(test_case_id)

    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    password = data["password"]
    confirm_password = data["confirm_password"]

    email = (
        f"{create_unique_value(data['email_prefix'])}"
        f"@gmail.com"
    )

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

    # STEP 2: Nhập mật khẩu ngắn hơn 7 ký tự
    register_page.enter_password(password)

    report_step(
        test_case_id,
        2,
        f"Nhập Mật khẩu ngắn hơn 7 ký tự: {password}"
    )

    # STEP 3: Nhập Xác nhận mật khẩu trùng khớp
    register_page.enter_confirm_password(confirm_password)

    report_step(
        test_case_id,
        3,
        "Nhập Xác nhận mật khẩu trùng khớp"
    )

    # STEP 4: Nhập hợp lệ các trường còn lại
    register_page.enter_first_name(first_name)
    register_page.enter_last_name(last_name)
    register_page.enter_email(email)
    register_page.enter_phone(phone)
    register_page.enter_username(username)
    register_page.upload_avatar(avatar_path)

    report_step(
        test_case_id,
        4,
        (
            "Nhập hợp lệ các trường còn lại | "
            f"Email: {email} | "
            f"Username: {username}"
        )
    )

    # STEP 5: Nhấn nút Đăng ký
    register_page.click_register()

    report_step(
        test_case_id,
        5,
        "Nhấn nút Đăng ký"
    )

    # STEP 6: Kiểm tra kết quả
    actual_message = register_page.get_error_message()

    expected_message = "Mật khẩu phải có ít nhất 7 ký tự"

    assert expected_message in actual_message, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: '{expected_message}' | "
        f"Actual: '{actual_message}'"
    )

    assert driver.current_url == REGISTER_URL, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected URL: {REGISTER_URL} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        6,
        (
            "Hệ thống không tạo tài khoản và hiển thị "
            "thông báo Mật khẩu không hợp lệ | "
            f"Expected: {expected_message} | "
            f"Actual: {actual_message}"
        )
    )

# ============================================================
# TC-REGISTER-014
# ============================================================

def test_tc_register_014_password_without_uppercase(driver):
    """
    TC-REGISTER-014:
    Kiểm tra đăng ký với Mật khẩu không có chữ in hoa.
    """

    test_case_id = "TC-REGISTER-014"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký với Mật khẩu không có chữ in hoa"
    )

    data = get_register_test_data(test_case_id)

    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    password = data["password"]
    confirm_password = data["confirm_password"]

    email = (
        f"{create_unique_value(data['email_prefix'])}"
        f"@gmail.com"
    )

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

    # STEP 2: Nhập mật khẩu không có chữ in hoa
    register_page.enter_password(password)

    report_step(
        test_case_id,
        2,
        f"Nhập Mật khẩu không có chữ in hoa: {password}"
    )

    # STEP 3: Nhập Xác nhận mật khẩu trùng khớp
    register_page.enter_confirm_password(confirm_password)

    report_step(
        test_case_id,
        3,
        "Nhập Xác nhận mật khẩu trùng khớp"
    )

    # STEP 4: Nhập hợp lệ các trường còn lại
    register_page.enter_first_name(first_name)
    register_page.enter_last_name(last_name)
    register_page.enter_email(email)
    register_page.enter_phone(phone)
    register_page.enter_username(username)
    register_page.upload_avatar(avatar_path)

    report_step(
        test_case_id,
        4,
        (
            "Nhập hợp lệ các trường còn lại | "
            f"Email: {email} | "
            f"Username: {username}"
        )
    )

    # STEP 5: Nhấn nút Đăng ký
    register_page.click_register()

    report_step(
        test_case_id,
        5,
        "Nhấn nút Đăng ký"
    )

    # STEP 6: Kiểm tra kết quả
    actual_message = register_page.get_error_message()

    expected_message = (
        "Mật khẩu phải chứa ít nhất 1 chữ in hoa"
    )

    assert expected_message in actual_message, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: '{expected_message}' | "
        f"Actual: '{actual_message}'"
    )

    assert driver.current_url == REGISTER_URL, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected URL: {REGISTER_URL} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        6,
        (
            "Hệ thống không tạo tài khoản và hiển thị "
            "thông báo Mật khẩu thiếu chữ in hoa | "
            f"Expected: {expected_message} | "
            f"Actual: {actual_message}"
        )
    )

# ============================================================
# TC-REGISTER-015
# ============================================================

def test_tc_register_015_password_without_lowercase(driver):
    """
    TC-REGISTER-015:
    Kiểm tra đăng ký với Mật khẩu không có chữ thường.
    """

    test_case_id = "TC-REGISTER-015"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký với Mật khẩu không có chữ thường"
    )

    data = get_register_test_data(test_case_id)

    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    password = data["password"]
    confirm_password = data["confirm_password"]

    email = (
        f"{create_unique_value(data['email_prefix'])}"
        f"@gmail.com"
    )

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

    # STEP 2: Nhập mật khẩu không có chữ thường
    register_page.enter_password(password)

    report_step(
        test_case_id,
        2,
        f"Nhập Mật khẩu không có chữ thường: {password}"
    )

    # STEP 3: Nhập Xác nhận mật khẩu trùng khớp
    register_page.enter_confirm_password(confirm_password)

    report_step(
        test_case_id,
        3,
        "Nhập Xác nhận mật khẩu trùng khớp"
    )

    # STEP 4: Nhập hợp lệ các trường còn lại
    register_page.enter_first_name(first_name)
    register_page.enter_last_name(last_name)
    register_page.enter_email(email)
    register_page.enter_phone(phone)
    register_page.enter_username(username)
    register_page.upload_avatar(avatar_path)

    report_step(
        test_case_id,
        4,
        (
            "Nhập hợp lệ các trường còn lại | "
            f"Email: {email} | "
            f"Username: {username}"
        )
    )

    # STEP 5: Nhấn nút Đăng ký
    register_page.click_register()

    report_step(
        test_case_id,
        5,
        "Nhấn nút Đăng ký"
    )

    # STEP 6: Kiểm tra kết quả
    actual_message = register_page.get_error_message()

    expected_message = (
        "Mật khẩu phải chứa ít nhất 1 chữ thường"
    )

    assert expected_message in actual_message, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: '{expected_message}' | "
        f"Actual: '{actual_message}'"
    )

    assert driver.current_url == REGISTER_URL, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected URL: {REGISTER_URL} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        6,
        (
            "Hệ thống không tạo tài khoản và hiển thị "
            "thông báo Mật khẩu thiếu chữ thường | "
            f"Expected: {expected_message} | "
            f"Actual: {actual_message}"
        )
    )

# ============================================================
# TC-REGISTER-016
# ============================================================

def test_tc_register_016_password_without_number(driver):
    """
    TC-REGISTER-016:
    Kiểm tra đăng ký với Mật khẩu không có chữ số.
    """

    test_case_id = "TC-REGISTER-016"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký với Mật khẩu không có chữ số"
    )

    data = get_register_test_data(test_case_id)

    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    password = data["password"]
    confirm_password = data["confirm_password"]

    email = (
        f"{create_unique_value(data['email_prefix'])}"
        f"@gmail.com"
    )

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

    # STEP 2: Nhập mật khẩu không có chữ số
    register_page.enter_password(password)

    report_step(
        test_case_id,
        2,
        f"Nhập Mật khẩu không có chữ số: {password}"
    )

    # STEP 3: Nhập Xác nhận mật khẩu trùng khớp
    register_page.enter_confirm_password(confirm_password)

    report_step(
        test_case_id,
        3,
        "Nhập Xác nhận mật khẩu trùng khớp"
    )

    # STEP 4: Nhập hợp lệ các trường còn lại
    register_page.enter_first_name(first_name)
    register_page.enter_last_name(last_name)
    register_page.enter_email(email)
    register_page.enter_phone(phone)
    register_page.enter_username(username)
    register_page.upload_avatar(avatar_path)

    report_step(
        test_case_id,
        4,
        (
            "Nhập hợp lệ các trường còn lại | "
            f"Email: {email} | "
            f"Username: {username}"
        )
    )

    # STEP 5: Nhấn nút Đăng ký
    register_page.click_register()

    report_step(
        test_case_id,
        5,
        "Nhấn nút Đăng ký"
    )

    # STEP 6: Kiểm tra kết quả
    actual_message = register_page.get_error_message()

    expected_message = (
        "Mật khẩu phải chứa ít nhất 1 chữ số"
    )

    assert expected_message in actual_message, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: '{expected_message}' | "
        f"Actual: '{actual_message}'"
    )

    assert driver.current_url == REGISTER_URL, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected URL: {REGISTER_URL} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        6,
        (
            "Hệ thống không tạo tài khoản và hiển thị "
            "thông báo Mật khẩu thiếu chữ số | "
            f"Expected: {expected_message} | "
            f"Actual: {actual_message}"
        )
    )

# ============================================================
# TC-REGISTER-017
# ============================================================

def test_tc_register_017_password_without_special_character(driver):
    """
    TC-REGISTER-017:
    Kiểm tra đăng ký với Mật khẩu không có ký tự đặc biệt.
    """

    test_case_id = "TC-REGISTER-017"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký với Mật khẩu không có ký tự đặc biệt"
    )

    data = get_register_test_data(test_case_id)

    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    password = data["password"]
    confirm_password = data["confirm_password"]

    email = (
        f"{create_unique_value(data['email_prefix'])}"
        f"@gmail.com"
    )

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

    # STEP 2: Nhập mật khẩu không có ký tự đặc biệt
    register_page.enter_password(password)

    report_step(
        test_case_id,
        2,
        f"Nhập Mật khẩu không có ký tự đặc biệt: {password}"
    )

    # STEP 3: Nhập Xác nhận mật khẩu trùng khớp
    register_page.enter_confirm_password(confirm_password)

    report_step(
        test_case_id,
        3,
        "Nhập Xác nhận mật khẩu trùng khớp"
    )

    # STEP 4: Nhập hợp lệ các trường còn lại
    register_page.enter_first_name(first_name)
    register_page.enter_last_name(last_name)
    register_page.enter_email(email)
    register_page.enter_phone(phone)
    register_page.enter_username(username)
    register_page.upload_avatar(avatar_path)

    report_step(
        test_case_id,
        4,
        (
            "Nhập hợp lệ các trường còn lại | "
            f"Email: {email} | "
            f"Username: {username}"
        )
    )

    # STEP 5: Nhấn nút Đăng ký
    register_page.click_register()

    report_step(
        test_case_id,
        5,
        "Nhấn nút Đăng ký"
    )

    # STEP 6: Kiểm tra kết quả
    actual_message = register_page.get_error_message()

    expected_message = (
        "Mật khẩu phải chứa ít nhất 1 ký tự đặc biệt"
    )

    assert expected_message in actual_message, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected: '{expected_message}' | "
        f"Actual: '{actual_message}'"
    )

    assert driver.current_url == REGISTER_URL, (
        f"{test_case_id} | STEP 6 FAILED | "
        f"Expected URL: {REGISTER_URL} | "
        f"Actual URL: {driver.current_url}"
    )

    report_step(
        test_case_id,
        6,
        (
            "Hệ thống không tạo tài khoản và hiển thị "
            "thông báo Mật khẩu thiếu ký tự đặc biệt | "
            f"Expected: {expected_message} | "
            f"Actual: {actual_message}"
        )
    )