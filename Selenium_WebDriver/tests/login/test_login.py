from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.LoginPage import LoginPage
from utils.test_reporter import report_step
from utils.data_reader import get_test_data_csv, LOGIN_TEST_DATA_CSV


HOME_URL = "http://localhost:3000/"
LOGIN_URL = "http://localhost:3000/login"


# ============================================================
# COMMON HELPERS
# ============================================================

def get_login_test_data(test_case_id):
    return get_test_data_csv(LOGIN_TEST_DATA_CSV, test_case_id)


def wait_for_url(driver, expected_url, timeout=10):
    WebDriverWait(driver, timeout).until(EC.url_to_be(expected_url))


def print_test_description(test_case_id, description):
    print(f"\n{test_case_id} | {description}")


def assert_not_logged_in(driver, login_page, test_case_id, step_number):
    assert driver.current_url == LOGIN_URL, (
        f"{test_case_id} | STEP {step_number} FAILED | "
        f"Expected URL: {LOGIN_URL} | Actual: {driver.current_url}"
    )

    assert not login_page.is_logout_button_present(), (
        f"{test_case_id} | STEP {step_number} FAILED | "
        "Expected: Người dùng chưa đăng nhập | "
        "Actual: Nút Đăng xuất vẫn hiển thị."
    )


# ============================================================
# TC-LOGIN-001
# ============================================================

def test_tc_login_001_valid_username(driver):
    """
    TC-LOGIN-001:
    Kiểm tra đăng nhập thành công bằng tên đăng nhập hợp lệ.
    """
    test_case_id = "TC-LOGIN-001"
    description = "Kiểm tra đăng nhập thành công bằng tên đăng nhập hợp lệ"
    print_test_description(test_case_id, description)

    data = get_login_test_data(test_case_id)
    username = data["username"]
    password = data["password"]
    expected_name = data["expected_name"]

    login_page = LoginPage(driver)

    # Step 1
    login_page.open_page()

    assert driver.current_url == LOGIN_URL, (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected URL: {LOGIN_URL} | Actual: {driver.current_url}"
    )

    report_step(test_case_id, 1, "Mở trang đăng nhập thành công")

    # Step 2
    login_page.enter_username(username)

    actual_username = login_page.get_username_value()
    assert actual_username == username, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected username: {username} | Actual: {actual_username}"
    )

    report_step(test_case_id, 2, "Nhập tài khoản hợp lệ")

    # Step 3
    login_page.enter_password(password)

    actual_password = login_page.get_password_value()
    assert actual_password == password, (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Mật khẩu được nhập đúng | "
        f"Actual length: {len(actual_password)}"
    )

    report_step(test_case_id, 3, "Nhập đúng mật khẩu")

    # Step 4
    login_page.click_login()
    wait_for_url(driver, HOME_URL)

    report_step(test_case_id, 4, "Nhấn Đăng nhập")

    # Step 5
    greeting = login_page.get_user_greeting()

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected URL: {HOME_URL} | Actual: {driver.current_url}"
    )

    assert expected_name in greeting, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected tên người dùng chứa: {expected_name} | "
        f"Actual: {greeting}"
    )

    assert login_page.is_logout_button_displayed(), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Có nút Đăng xuất | Actual: Không tìm thấy."
    )

    report_step(
        test_case_id,
        5,
        "Đăng nhập thành công, chuyển đúng trang và hiển thị trạng thái đã đăng nhập"
    )


# ============================================================
# TC-LOGIN-002
# ============================================================

def test_tc_login_002_valid_email(driver):
    """
    TC-LOGIN-002:
    Kiểm tra đăng nhập thành công bằng email hợp lệ.
    """
    test_case_id = "TC-LOGIN-002"
    description = "Kiểm tra đăng nhập thành công bằng email hợp lệ"
    print_test_description(test_case_id, description)

    data = get_login_test_data(test_case_id)
    email = data["email"]
    password = data["password"]
    expected_name = data["expected_name"]

    login_page = LoginPage(driver)

    # Step 1
    login_page.open_page()

    assert driver.current_url == LOGIN_URL, (
        f"{test_case_id} | STEP 1 FAILED | "
        f"Expected URL: {LOGIN_URL} | Actual: {driver.current_url}"
    )

    report_step(test_case_id, 1, "Mở trang đăng nhập thành công")

    # Step 2
    login_page.enter_username(email)

    actual_email = login_page.get_username_value()
    assert actual_email == email, (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected email: {email} | Actual: {actual_email}"
    )

    report_step(test_case_id, 2, "Nhập email hợp lệ")

    # Step 3
    login_page.enter_password(password)

    actual_password = login_page.get_password_value()
    assert actual_password == password, (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Mật khẩu được nhập đúng | "
        f"Actual length: {len(actual_password)}"
    )

    report_step(test_case_id, 3, "Nhập đúng mật khẩu")

    # Step 4
    login_page.click_login()
    wait_for_url(driver, HOME_URL)

    report_step(test_case_id, 4, "Nhấn Đăng nhập")

    # Step 5
    greeting = login_page.get_user_greeting()

    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected URL: {HOME_URL} | Actual: {driver.current_url}"
    )

    assert expected_name in greeting, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected tên người dùng chứa: {expected_name} | "
        f"Actual: {greeting}"
    )

    assert login_page.is_logout_button_displayed(), (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Có nút Đăng xuất | Actual: Không tìm thấy."
    )

    report_step(
        test_case_id,
        5,
        "Đăng nhập bằng email thành công và chuyển đến giao diện người dùng"
    )


# ============================================================
# TC-LOGIN-003
# ============================================================

def test_tc_login_003_blank_username(driver):
    """
    TC-LOGIN-003:
    Kiểm tra không thể đăng nhập khi bỏ trống tên đăng nhập.
    """
    test_case_id = "TC-LOGIN-003"
    description = "Kiểm tra không thể đăng nhập khi bỏ trống tên đăng nhập"
    print_test_description(test_case_id, description)

    data = get_login_test_data(test_case_id)
    password = data["password"]

    login_page = LoginPage(driver)

    # Step 1
    login_page.open_page()
    report_step(test_case_id, 1, "Mở trang đăng nhập")

    # Step 2
    login_page.enter_username("")

    actual_username = login_page.get_username_value()
    assert actual_username == "", (
        f"{test_case_id} | STEP 2 FAILED | "
        f"Expected: Tên đăng nhập trống | Actual: {actual_username}"
    )

    report_step(test_case_id, 2, "Để trống tên đăng nhập")

    # Step 3
    login_page.enter_password(password)
    report_step(test_case_id, 3, "Nhập mật khẩu")

    # Step 4
    login_page.click_login()
    report_step(test_case_id, 4, "Nhấn Đăng nhập")

    # Step 5
    validation = login_page.get_username_validation_message()

    assert validation != "", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Có validation tên đăng nhập | Actual: Không có validation."
    )

    assert_not_logged_in(driver, login_page, test_case_id, 5)

    report_step(
        test_case_id,
        5,
        "Hiển thị validation tên đăng nhập và không đăng nhập"
    )


# ============================================================
# TC-LOGIN-004
# ============================================================

def test_tc_login_004_blank_password(driver):
    """
    TC-LOGIN-004:
    Kiểm tra không thể đăng nhập khi bỏ trống mật khẩu.
    """
    test_case_id = "TC-LOGIN-004"
    description = "Kiểm tra không thể đăng nhập khi bỏ trống mật khẩu"
    print_test_description(test_case_id, description)

    data = get_login_test_data(test_case_id)
    username = data["username"]

    login_page = LoginPage(driver)

    # Step 1
    login_page.open_page()
    report_step(test_case_id, 1, "Mở trang đăng nhập")

    # Step 2
    login_page.enter_username(username)
    report_step(test_case_id, 2, "Nhập tên đăng nhập hợp lệ")

    # Step 3
    login_page.enter_password("")

    actual_password = login_page.get_password_value()
    assert actual_password == "", (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: Mật khẩu trống | Actual: {actual_password}"
    )

    report_step(test_case_id, 3, "Để trống mật khẩu")

    # Step 4
    login_page.click_login()
    report_step(test_case_id, 4, "Nhấn Đăng nhập")

    # Step 5
    validation = login_page.get_password_validation_message()

    assert validation != "", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Có validation mật khẩu | Actual: Không có validation."
    )

    assert_not_logged_in(driver, login_page, test_case_id, 5)

    report_step(
        test_case_id,
        5,
        "Hiển thị validation mật khẩu và không đăng nhập"
    )


# ============================================================
# TC-LOGIN-005
# ============================================================

def test_tc_login_005_blank_username_and_password(driver):
    """
    TC-LOGIN-005:
    Kiểm tra không thể đăng nhập khi bỏ trống tên đăng nhập và mật khẩu.
    """
    test_case_id = "TC-LOGIN-005"
    description = "Kiểm tra không thể đăng nhập khi bỏ trống tên đăng nhập và mật khẩu"
    print_test_description(test_case_id, description)

    get_login_test_data(test_case_id)

    login_page = LoginPage(driver)

    # Step 1
    login_page.open_page()
    report_step(test_case_id, 1, "Mở trang đăng nhập")

    # Step 2
    login_page.enter_username("")
    report_step(test_case_id, 2, "Để trống tên đăng nhập")

    # Step 3
    login_page.enter_password("")
    report_step(test_case_id, 3, "Để trống mật khẩu")

    # Step 4
    login_page.click_login()
    report_step(test_case_id, 4, "Nhấn Đăng nhập")

    # Step 5
    username_validation = login_page.get_username_validation_message()
    password_validation = login_page.get_password_validation_message()

    assert username_validation != "", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Có validation tên đăng nhập | Actual: Không có."
    )

    assert password_validation != "", (
        f"{test_case_id} | STEP 5 FAILED | "
        "Expected: Có validation mật khẩu | Actual: Không có."
    )

    assert_not_logged_in(driver, login_page, test_case_id, 5)

    report_step(
        test_case_id,
        5,
        "Hiển thị validation các trường bắt buộc và không đăng nhập"
    )


# ============================================================
# TC-LOGIN-006
# ============================================================

def test_tc_login_006_wrong_password(driver):
    """
    TC-LOGIN-006:
    Kiểm tra không thể đăng nhập khi nhập sai mật khẩu.
    """
    test_case_id = "TC-LOGIN-006"
    description = "Kiểm tra không thể đăng nhập khi nhập sai mật khẩu"
    print_test_description(test_case_id, description)

    data = get_login_test_data(test_case_id)
    username = data["username"]
    invalid_password = data["invalid_password"]
    expected_error = data["expected_error"]

    login_page = LoginPage(driver)

    # Step 1
    login_page.open_page()
    report_step(test_case_id, 1, "Mở trang đăng nhập")

    # Step 2
    login_page.enter_username(username)
    report_step(test_case_id, 2, "Nhập tên đăng nhập hợp lệ")

    # Step 3
    login_page.enter_password(invalid_password)
    report_step(test_case_id, 3, "Nhập mật khẩu sai")

    # Step 4
    login_page.click_login()
    report_step(test_case_id, 4, "Nhấn Đăng nhập")

    # Step 5
    error_message = login_page.get_error_message()

    assert error_message == expected_error, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: {expected_error} | Actual: {error_message}"
    )

    assert_not_logged_in(driver, login_page, test_case_id, 5)

    report_step(
        test_case_id,
        5,
        "Hiển thị thông báo lỗi và không đăng nhập"
    )


# ============================================================
# TC-LOGIN-007
# ============================================================

def test_tc_login_007_nonexistent_account(driver):
    """
    TC-LOGIN-007:
    Kiểm tra không thể đăng nhập với tài khoản không tồn tại.
    """
    test_case_id = "TC-LOGIN-007"
    description = "Kiểm tra không thể đăng nhập với tài khoản không tồn tại"
    print_test_description(test_case_id, description)

    data = get_login_test_data(test_case_id)
    invalid_username = data["invalid_username"]
    password = data["password"]
    expected_error = data["expected_error"]

    login_page = LoginPage(driver)

    # Step 1
    login_page.open_page()
    report_step(test_case_id, 1, "Mở trang đăng nhập")

    # Step 2
    login_page.enter_username(invalid_username)
    report_step(test_case_id, 2, "Nhập tài khoản không tồn tại")

    # Step 3
    login_page.enter_password(password)

    actual_password = login_page.get_password_value()
    assert actual_password == password and password != "", (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected: Mật khẩu bất kỳ không được để trống | "
        f"Actual: {'Trống' if not actual_password else 'Đã nhập'}"
    )

    report_step(test_case_id, 3, "Nhập mật khẩu bất kỳ")
    # Step 4
    login_page.click_login()
    report_step(test_case_id, 4, "Nhấn Đăng nhập")

    # Step 5
    error_message = login_page.get_error_message()

    assert error_message == expected_error, (
        f"{test_case_id} | STEP 5 FAILED | "
        f"Expected: {expected_error} | Actual: {error_message}"
    )

    assert_not_logged_in(driver, login_page, test_case_id, 5)

    report_step(
        test_case_id,
        5,
        "Hiển thị thông báo lỗi và không đăng nhập"
    )


# ============================================================
# TC-LOGIN-008
# ============================================================

def test_tc_login_008_logout_success(driver):
    """
    TC-LOGIN-008:
    Kiểm tra đăng xuất thành công sau khi đã đăng nhập.
    """
    test_case_id = "TC-LOGIN-008"
    description = "Kiểm tra đăng xuất thành công sau khi đã đăng nhập"
    print_test_description(test_case_id, description)

    data = get_login_test_data(test_case_id)
    username = data["username"]
    password = data["password"]

    login_page = LoginPage(driver)

    # Step 1
    login_page.open_page()
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login()
    wait_for_url(driver, HOME_URL)

    assert login_page.is_logout_button_displayed(), (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected: Đăng nhập thành công | "
        "Actual: Không tìm thấy nút Đăng xuất."
    )

    report_step(test_case_id, 1, "Đăng nhập thành công")

    # Step 2
    login_page.logout()
    wait_for_url(driver, LOGIN_URL)

    report_step(test_case_id, 2, "Nhấn Đăng xuất")

    # Step 3
    assert driver.current_url == LOGIN_URL, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected URL: {LOGIN_URL} | Actual: {driver.current_url}"
    )

    assert login_page.is_login_button_displayed(), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Hiển thị nút Đăng nhập | Actual: Không tìm thấy."
    )

    assert not login_page.is_logout_button_present(), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Không còn nút Đăng xuất | "
        "Actual: Nút Đăng xuất vẫn còn."
    )

    report_step(
        test_case_id,
        3,
        "Đăng xuất thành công và hệ thống chuyển về trạng thái chưa đăng nhập"
    )


# ============================================================
# TC-LOGIN-009
# ============================================================

def test_tc_login_009_protected_page_without_login(driver):
    """
    TC-LOGIN-009:
    Kiểm tra không thể truy cập trang yêu cầu xác thực khi chưa đăng nhập.
    """
    test_case_id = "TC-LOGIN-009"
    description = "Kiểm tra không thể truy cập trang yêu cầu xác thực khi chưa đăng nhập"
    print_test_description(test_case_id, description)

    data = get_login_test_data(test_case_id)
    protected_url = data["protected_url"]

    login_page = LoginPage(driver)

    # Step 1
    driver.delete_all_cookies()
    login_page.open_page()

    assert not login_page.is_logout_button_present(), (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected: Người dùng chưa đăng nhập | "
        "Actual: Phát hiện nút Đăng xuất."
    )

    report_step(test_case_id, 1, "Đảm bảo người dùng chưa đăng nhập")

    # Step 2
    login_page.open(protected_url)

    report_step(
        test_case_id,
        2,
        "Truy cập trực tiếp URL trang yêu cầu đăng nhập"
    )

    # Step 3
    assert driver.current_url == protected_url, (
        f"{test_case_id} | STEP 3 FAILED | "
        f"Expected URL: {protected_url} | Actual: {driver.current_url}"
    )

    assert login_page.is_login_required_message_displayed(), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Có thông báo yêu cầu đăng nhập | Actual: Không tìm thấy."
    )

    assert login_page.is_login_nav_link_displayed(), (
        f"{test_case_id} | STEP 3 FAILED | "
        "Expected: Có liên kết Đăng nhập | Actual: Không tìm thấy."
    )

    report_step(
        test_case_id,
        3,
        "Hệ thống chặn truy cập nội dung và yêu cầu người dùng đăng nhập"
    )


# ============================================================
# TC-LOGIN-010
# ============================================================

def test_tc_login_010_logout_then_browser_back(driver):
    """
    TC-LOGIN-010:
    Kiểm tra trạng thái đăng nhập sau khi đăng xuất và quay lại trang trước.
    """
    test_case_id = "TC-LOGIN-010"
    description = "Kiểm tra trạng thái đăng nhập sau khi đăng xuất và quay lại trang trước"
    print_test_description(test_case_id, description)

    data = get_login_test_data(test_case_id)
    username = data["username"]
    password = data["password"]

    login_page = LoginPage(driver)

    # Step 1
    login_page.open_page()
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login()
    wait_for_url(driver, HOME_URL)

    assert login_page.is_logout_button_displayed(), (
        f"{test_case_id} | STEP 1 FAILED | "
        "Expected: Đăng nhập thành công | "
        "Actual: Không tìm thấy nút Đăng xuất."
    )

    report_step(test_case_id, 1, "Đăng nhập thành công")

    # Step 2
    login_page.logout()
    wait_for_url(driver, LOGIN_URL)

    report_step(test_case_id, 2, "Nhấn Đăng xuất")

    # Step 3
    driver.back()

    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == HOME_URL
    )

    report_step(test_case_id, 3, "Nhấn nút Back của trình duyệt")

    # Step 4
    assert driver.current_url == HOME_URL, (
        f"{test_case_id} | STEP 4 FAILED | "
        f"Expected URL: {HOME_URL} | Actual: {driver.current_url}"
    )

    assert login_page.is_login_nav_link_displayed(), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Có liên kết Đăng nhập | Actual: Không tìm thấy."
    )

    assert not login_page.is_user_greeting_present(), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Không còn thông tin người dùng | "
        "Actual: Greeting vẫn hiển thị."
    )

    assert not login_page.is_logout_button_present(), (
        f"{test_case_id} | STEP 4 FAILED | "
        "Expected: Không còn nút Đăng xuất | "
        "Actual: Nút Đăng xuất vẫn hiển thị."
    )

    report_step(
        test_case_id,
        4,
        "Người dùng không thể quay lại trạng thái đã đăng nhập"
    )