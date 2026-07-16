from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.RegisterPage import RegisterPage
import random

REGISTER_URL = "http://localhost:3000/register"
LOGIN_URL = "http://localhost:3000/login"

VALID_FIRST_NAME = "Duong"
VALID_LAST_NAME = "Phung"
VALID_EMAIL = (
    f"phungtest{random.randint(1000,9999)}@gmail.com"
)

VALID_PHONE = "0901234567"
VALID_USERNAME = (
    f"phung_auto_{random.randint(1000,9999)}"
)
VALID_PASSWORD = "Abc@123"

import os


AVATAR_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "test_data",
        "avatar.png"
    )
)

def test_register_success(driver):
    """
    TC-REGISTER-001:
    Đăng ký thành công với thông tin hợp lệ.
    """

    register_page = RegisterPage(driver)

    register_page.open_page()


    register_page.register(
        VALID_FIRST_NAME,
        VALID_LAST_NAME,
        VALID_EMAIL,
        VALID_PHONE,
        VALID_USERNAME,
        VALID_PASSWORD,
        VALID_PASSWORD,
        AVATAR_PATH
    )

    WebDriverWait(driver, 10).until(
        EC.url_to_be(LOGIN_URL)
    )

    assert driver.current_url == LOGIN_URL

def test_register_without_avatar(driver):
    """
    TC-REGISTER-002:
    Đăng ký khi không chọn ảnh đại diện.
    """

    register_page = RegisterPage(driver)

    register_page.open_page()

    register_page.register(
        VALID_FIRST_NAME,
        VALID_LAST_NAME,
        VALID_EMAIL,
        VALID_PHONE,
        VALID_USERNAME,
        VALID_PASSWORD,
        VALID_PASSWORD,
        None
    )

    assert (
        register_page.get_avatar_validation_message()
        != ""
    )

def test_register_without_first_name(driver):
    """
    TC-REGISTER-003:
    Đăng ký khi bỏ trống trường Họ.
    """

    register_page = RegisterPage(driver)

    register_page.open_page()


    register_page.register(
        "",
        VALID_LAST_NAME,
        VALID_EMAIL,
        VALID_PHONE,
        VALID_USERNAME,
        VALID_PASSWORD,
        VALID_PASSWORD,
        AVATAR_PATH
    )
    assert (
        register_page.get_first_name_validation_message()
        != ""
    )

def test_register_without_email(driver):
    """
    TC-REGISTER-005:
    Bỏ trống email.
    """
    register_page = RegisterPage(driver)

    register_page.open_page()

    register_page.register(
        VALID_FIRST_NAME,
        VALID_LAST_NAME,
        "",
        VALID_PHONE,
        VALID_USERNAME,
        VALID_PASSWORD,
        VALID_PASSWORD,
        AVATAR_PATH
    )
    assert (
        register_page.get_email_validation_message()
        != ""
    )

def test_register_with_invalid_email_format(driver):
    """
    TC-REGISTER-010:
    Đăng ký với email không đúng định dạng.
    """

    register_page = RegisterPage(driver)

    register_page.open_page()

    register_page.register(
        VALID_FIRST_NAME,
        VALID_LAST_NAME,
        "kimphunggmail.com",
        VALID_PHONE,
        VALID_USERNAME,
        VALID_PASSWORD,
        VALID_PASSWORD,
        AVATAR_PATH
    )
    assert (
        register_page.get_email_validation_message()
        != ""
    )

def test_register_with_invalid_phone(driver):
    """
    TC-REGISTER-011:
    Đăng ký với số điện thoại không đúng định dạng.
    """
    register_page = RegisterPage(driver)

    register_page.open_page()

    register_page.register(
        VALID_FIRST_NAME,
        VALID_LAST_NAME,
        VALID_EMAIL,
        "01234567899",
        VALID_USERNAME,
        VALID_PASSWORD,
        VALID_PASSWORD,
        AVATAR_PATH
    )
    assert (
        register_page.get_error_message()
        ==
        "Số điện thoại phải gồm đúng 10 chữ số"
    )

def test_register_with_password_confirmation_not_match(driver):
    """
    TC-REGISTER-012:
    Xác nhận mật khẩu không khớp với mật khẩu.
    """

    register_page = RegisterPage(driver)

    register_page.open_page()

    register_page.register(
        VALID_FIRST_NAME,
        VALID_LAST_NAME,
        VALID_EMAIL,
        VALID_PHONE,
        VALID_USERNAME,
        VALID_PASSWORD,
        "Abc@124",
        AVATAR_PATH
    )
    assert (
        register_page.get_error_message()
        ==
        "Mật khẩu xác nhận không khớp"
    )

def test_register_with_existing_username(driver):
    """
    TC-REGISTER-018:
    Đăng ký với tên đăng nhập đã tồn tại.
    """

    register_page = RegisterPage(driver)

    register_page.open_page()

    register_page.register(
        VALID_FIRST_NAME,
        VALID_LAST_NAME,
        "new_email_auto@gmail.com",
        "0912345678",
        "patient_an",
        VALID_PASSWORD,
        VALID_PASSWORD,
        AVATAR_PATH
    )
    assert (
        register_page.get_error_message()
        ==
        "Tên đăng nhập đã tồn tại."
    )

def test_register_with_existing_email(driver):
    """
    TC-REGISTER-019:
    Đăng ký với email đã tồn tại.
    """

    register_page = RegisterPage(driver)

    register_page.open_page()

    register_page.register(
        VALID_FIRST_NAME,
        VALID_LAST_NAME,
        "an@gmail.com",
        "0912345678",
        "new_username_auto_test",
        VALID_PASSWORD,
        VALID_PASSWORD,
        AVATAR_PATH
    )
    assert (
        register_page.get_error_message()
        ==
        "Email đã tồn tại."
    )