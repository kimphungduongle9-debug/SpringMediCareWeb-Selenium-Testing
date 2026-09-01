from pages.RegisterPage import RegisterPage
from tests.helpers.register_helpers import (
    get_register_test_data,
    get_avatar_path,
    create_unique_value
)
from utils.test_reporter import report_step


REGISTER_URL = "http://localhost:3000/register"


def test_tc_register_002_without_avatar(driver):
    """
    TC-REGISTER-002:
    Kiểm tra đăng ký khi không chọn ảnh đại diện.
    """

    test_case_id = "TC-REGISTER-002"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký khi không chọn ảnh đại diện"
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
    # STEP 3: Không chọn ảnh đại diện
    # ========================================================

    report_step(
        test_case_id,
        3,
        "Không chọn ảnh đại diện"
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

    actual_message = register_page.get_avatar_validation_message()

    assert actual_message.strip() != "", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: hiển thị thông báo yêu cầu chọn ảnh đại diện | "
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
            "thông báo yêu cầu chọn ảnh đại diện | "
            f"Actual message: {actual_message}"
        )
    )

def test_tc_register_003_without_first_name(driver):
    """
    TC-REGISTER-003:
    Kiểm tra đăng ký khi bỏ trống Họ.
    """

    test_case_id = "TC-REGISTER-003"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký khi bỏ trống Họ"
    )

    data = get_register_test_data(test_case_id)

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
    # STEP 2: Để trống trường Họ
    # ========================================================

    report_step(
        test_case_id,
        2,
        "Để trống trường Họ"
    )

    # ========================================================
    # STEP 3: Nhập hợp lệ các trường còn lại
    # ========================================================

    register_page.enter_last_name(last_name)
    register_page.enter_email(email)
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

    actual_message = register_page.get_first_name_validation_message()

    assert actual_message.strip() != "", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: hiển thị yêu cầu nhập Họ | "
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
            "Hệ thống không tạo tài khoản và yêu cầu nhập Họ | "
            f"Actual message: {actual_message}"
        )
    )

def test_tc_register_004_without_last_name(driver):
    """
    TC-REGISTER-004:
    Kiểm tra đăng ký khi bỏ trống Tên.
    """

    test_case_id = "TC-REGISTER-004"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký khi bỏ trống Tên"
    )

    data = get_register_test_data(test_case_id)

    first_name = data["first_name"]
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
    # STEP 2: Để trống trường Tên
    # ========================================================

    report_step(
        test_case_id,
        2,
        "Để trống trường Tên"
    )

    # ========================================================
    # STEP 3: Nhập hợp lệ các trường còn lại
    # ========================================================

    register_page.enter_first_name(first_name)
    register_page.enter_email(email)
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

    actual_message = register_page.get_last_name_validation_message()

    assert actual_message.strip() != "", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: hiển thị yêu cầu nhập Tên | "
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
            "Hệ thống không tạo tài khoản và yêu cầu nhập Tên | "
            f"Actual message: {actual_message}"
        )
    )

def test_tc_register_005_without_email(driver):
    """
    TC-REGISTER-005:
    Kiểm tra đăng ký khi bỏ trống Email.
    """

    test_case_id = "TC-REGISTER-005"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký khi bỏ trống Email"
    )

    data = get_register_test_data(test_case_id)

    first_name = data["first_name"]
    last_name = data["last_name"]
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
    # STEP 2: Để trống trường Email
    # ========================================================

    report_step(
        test_case_id,
        2,
        "Để trống trường Email"
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
        "Expected: hiển thị yêu cầu nhập Email | "
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
            "Hệ thống không tạo tài khoản và yêu cầu nhập Email | "
            f"Actual message: {actual_message}"
        )
    )

def test_tc_register_006_without_phone(driver):
    """
    TC-REGISTER-006:
    Kiểm tra đăng ký khi bỏ trống Số điện thoại.
    """

    test_case_id = "TC-REGISTER-006"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký khi bỏ trống Số điện thoại"
    )

    data = get_register_test_data(test_case_id)

    first_name = data["first_name"]
    last_name = data["last_name"]
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
    # STEP 2: Để trống trường Số điện thoại
    # ========================================================

    report_step(
        test_case_id,
        2,
        "Để trống trường Số điện thoại"
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

    actual_message = register_page.get_phone_validation_message()

    assert actual_message.strip() != "", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: hiển thị yêu cầu nhập Số điện thoại | "
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
            "Hệ thống không tạo tài khoản và yêu cầu nhập Số điện thoại | "
            f"Actual message: {actual_message}"
        )
    )

def test_tc_register_007_without_username(driver):
    """
    TC-REGISTER-007:
    Kiểm tra đăng ký khi bỏ trống Tên đăng nhập.
    """

    test_case_id = "TC-REGISTER-007"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký khi bỏ trống Tên đăng nhập"
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
    # STEP 2: Để trống trường Tên đăng nhập
    # ========================================================

    report_step(
        test_case_id,
        2,
        "Để trống trường Tên đăng nhập"
    )

    # ========================================================
    # STEP 3: Nhập hợp lệ các trường còn lại
    # ========================================================

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

    actual_message = register_page.get_username_validation_message()

    assert actual_message.strip() != "", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: hiển thị yêu cầu nhập Tên đăng nhập | "
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
            "Hệ thống không tạo tài khoản và yêu cầu nhập "
            "Tên đăng nhập | "
            f"Actual message: {actual_message}"
        )
    )

def test_tc_register_008_without_password(driver):
    """
    TC-REGISTER-008:
    Kiểm tra đăng ký khi bỏ trống Mật khẩu.
    """

    test_case_id = "TC-REGISTER-008"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký khi bỏ trống Mật khẩu"
    )

    data = get_register_test_data(test_case_id)

    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
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
    # STEP 2: Để trống trường Mật khẩu
    # ========================================================

    report_step(
        test_case_id,
        2,
        "Để trống trường Mật khẩu"
    )

    # ========================================================
    # STEP 3: Nhập hợp lệ các trường còn lại
    # ========================================================

    register_page.enter_first_name(first_name)
    register_page.enter_last_name(last_name)
    register_page.enter_email(email)
    register_page.enter_phone(phone)
    register_page.enter_username(username)
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

    actual_message = register_page.get_password_validation_message()

    assert actual_message.strip() != "", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: hiển thị yêu cầu nhập Mật khẩu | "
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
            "Hệ thống không tạo tài khoản và yêu cầu nhập "
            "Mật khẩu | "
            f"Actual message: {actual_message}"
        )
    )

def test_tc_register_009_without_confirm_password(driver):
    """
    TC-REGISTER-009:
    Kiểm tra đăng ký khi bỏ trống Xác nhận mật khẩu.
    """

    test_case_id = "TC-REGISTER-009"

    print(
        f"\n{test_case_id} | "
        "Kiểm tra đăng ký khi bỏ trống Xác nhận mật khẩu"
    )

    data = get_register_test_data(test_case_id)

    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    password = data["password"]

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
    # STEP 2: Để trống trường Xác nhận mật khẩu
    # ========================================================

    report_step(
        test_case_id,
        2,
        "Để trống trường Xác nhận mật khẩu"
    )

    # ========================================================
    # STEP 3: Nhập hợp lệ các trường còn lại
    # ========================================================

    register_page.enter_first_name(first_name)
    register_page.enter_last_name(last_name)
    register_page.enter_email(email)
    register_page.enter_phone(phone)
    register_page.enter_username(username)
    register_page.enter_password(password)
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

    actual_message = (
        register_page.get_confirm_password_validation_message()
    )

    assert actual_message.strip() != "", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: hiển thị yêu cầu nhập Xác nhận mật khẩu | "
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
            "Hệ thống không tạo tài khoản và yêu cầu nhập "
            "Xác nhận mật khẩu | "
            f"Actual message: {actual_message}"
        )
    )