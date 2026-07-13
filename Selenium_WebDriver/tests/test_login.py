from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.LoginPage import LoginPage
import time

HOME_URL = "http://localhost:3000/"

VALID_USERNAME = "patient_an"
VALID_PASSWORD = "Abc@123"
EXPECTED_NAME = "Nguyen"

INVALID_PASSWORD = "Abc@124"
LOGIN_URL = "http://localhost:3000/login"

INVALID_USERNAME = "user_not_exist_999999"
ANY_PASSWORD = "Abc@123"

VALID_EMAIL = "an@gmail.com"

PROTECTED_URL = "http://localhost:3000/my-appointments"


def test_login_success_with_valid_username(driver):
    """
    TC-LOGIN-001:
    Đăng nhập thành công với tên đăng nhập hợp lệ.
    """

    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        VALID_USERNAME,
        VALID_PASSWORD
    )

    WebDriverWait(driver, 10).until(
        EC.url_to_be(HOME_URL)
    )

    assert driver.current_url == HOME_URL

    greeting = login_page.get_user_greeting()

    assert "Xin chào" in greeting
    assert EXPECTED_NAME in greeting

    assert login_page.is_logout_button_displayed()

def test_login_failed_with_wrong_password(driver):
    """
    TC-LOGIN-006:
    Đăng nhập thất bại khi nhập sai mật khẩu.
    """

    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        VALID_USERNAME,
        INVALID_PASSWORD
    )

    time.sleep(2)

    assert driver.current_url == LOGIN_URL

    assert login_page.get_error_message() == (
        "Sai tên đăng nhập hoặc mật khẩu"
    )

def test_login_failed_with_nonexistent_username(driver):
    """
    TC-LOGIN-007:
    Đăng nhập thất bại với tài khoản không tồn tại.
    """

    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        INVALID_USERNAME,
        ANY_PASSWORD
    )

    time.sleep(2)

    assert driver.current_url == LOGIN_URL

    assert login_page.get_error_message() == (
        "Sai tên đăng nhập hoặc mật khẩu"
    )

def test_login_success_with_valid_email(driver):
    """
    TC-LOGIN-002:
    Đăng nhập thành công với email hợp lệ.
    """

    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        VALID_EMAIL,
        VALID_PASSWORD
    )

    time.sleep(2)

    assert driver.current_url == HOME_URL

    greeting = login_page.get_user_greeting()

    assert "Xin chào" in greeting
    assert EXPECTED_NAME in greeting

    assert login_page.is_logout_button_displayed()

def test_login_failed_when_username_is_empty(driver):
    """
    TC-LOGIN-003:
    Không cho đăng nhập khi bỏ trống tên đăng nhập.
    """

    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        "",
        VALID_PASSWORD
    )

    time.sleep(2)

    assert driver.current_url == LOGIN_URL

    assert login_page.get_username_validation_message() != ""

def test_login_failed_when_password_is_empty(driver):
    """
    TC-LOGIN-004:
    Không cho đăng nhập khi bỏ trống mật khẩu.
    """

    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login(
        VALID_USERNAME,
        ""
    )

    time.sleep(2)

    assert driver.current_url == LOGIN_URL

    assert login_page.get_password_validation_message() != ""

def test_login_failed_when_username_and_password_are_empty(driver):
    """
    TC-LOGIN-005:
    Không cho đăng nhập khi bỏ trống tên đăng nhập và mật khẩu.
    """

    login_page = LoginPage(driver)

    login_page.open_page()

    login_page.login("", "")

    time.sleep(2)

    assert driver.current_url == LOGIN_URL

    assert login_page.find(
        *login_page.USERNAME_INPUT
    ).get_attribute("value") == ""

    assert login_page.find(
        *login_page.PASSWORD_INPUT
    ).get_attribute("value") == ""

    assert login_page.get_username_validation_message() != ""

def test_logout_success(driver):
    """
    TC-LOGIN-008:
    Đăng xuất thành công.
    """

    login_page = LoginPage(driver)

    login_page.open_page()
    login_page.login(
        VALID_USERNAME,
        VALID_PASSWORD
    )

    time.sleep(1)

    login_page.logout()

    time.sleep(2)

    assert driver.current_url == LOGIN_URL

    assert login_page.is_login_button_displayed()

def test_access_protected_page_without_login(driver):
    """
    TC-LOGIN-009:
    Không cho truy cập trang yêu cầu đăng nhập
    khi người dùng chưa đăng nhập.
    """

    login_page = LoginPage(driver)

    login_page.open(PROTECTED_URL)

    time.sleep(2)

    assert driver.current_url == PROTECTED_URL
    assert login_page.is_login_required_message_displayed()
    assert login_page.is_login_nav_link_displayed()

def test_login_state_after_logout_and_back(driver):
    """
    TC-LOGIN-010:
    Sau khi đăng xuất và bấm Back,
    hệ thống vẫn phải ở trạng thái chưa đăng nhập.
    """

    login_page = LoginPage(driver)

    login_page.open_page()
    login_page.login(
        VALID_USERNAME,
        VALID_PASSWORD
    )

    time.sleep(1)

    assert driver.current_url == HOME_URL
    assert login_page.is_logout_button_displayed()

    login_page.logout()

    time.sleep(1)

    assert driver.current_url == LOGIN_URL

    driver.back()

    time.sleep(2)

    assert driver.current_url == HOME_URL

    assert login_page.is_login_nav_link_displayed()

    assert not login_page.is_user_greeting_present()
    assert not login_page.is_logout_button_present()