from selenium.webdriver.common.by import By

from pages.BasePage import BasePage

import time


class RegisterPage(BasePage):

    URL = "http://localhost:3000/register"


    FIRST_NAME_INPUT = (
        By.XPATH,
        "//label[text()='Họ']/following-sibling::input"
    )

    LAST_NAME_INPUT = (
        By.XPATH,
        "//label[text()='Tên']/following-sibling::input"
    )

    EMAIL_INPUT = (
        By.XPATH,
        "//label[text()='Email']/following-sibling::input"
    )

    PHONE_INPUT = (
        By.XPATH,
        "//label[text()='Số điện thoại']/following-sibling::input"
    )

    USERNAME_INPUT = (
        By.XPATH,
        "//label[text()='Tên đăng nhập']/following-sibling::input"
    )

    PASSWORD_INPUT = (
        By.XPATH,
        "//label[text()='Mật khẩu']/following-sibling::input"
    )

    CONFIRM_PASSWORD_INPUT = (
        By.XPATH,
        "//label[text()='Xác nhận mật khẩu']/following-sibling::input"
    )

    AVATAR_INPUT = (
        By.XPATH,
        "//label[text()='Ảnh đại diện']/following-sibling::input"
    )

    REGISTER_BUTTON = (
        By.CSS_SELECTOR,
        "button.register-big-btn[type='submit']"
    )

    AVATAR = (
        By.CSS_SELECTOR,
        "input[type='file']"
    )

    ERROR_MESSAGE = (
        By.CLASS_NAME,
        "register-error-text"
    )

    def open_page(self):
        self.open(self.URL)

    def get_avatar_validation_message(self):
        return self.find(
            *self.AVATAR
        ).get_attribute("validationMessage")

    def register(
            self,
            first_name,
            last_name,
            email,
            phone,
            username,
            password,
            confirm_password,
            avatar_path,
            delay=1.5
    ):

        time.sleep(delay)

        self.typing(
            *self.FIRST_NAME_INPUT,
            first_name
        )

        time.sleep(delay)

        self.typing(*self.LAST_NAME_INPUT,last_name)

        time.sleep(delay)

        self.typing(*self.EMAIL_INPUT,email)

        time.sleep(delay)

        self.typing(*self.PHONE_INPUT,phone)

        time.sleep(delay)

        self.typing(*self.USERNAME_INPUT,username)

        time.sleep(delay)

        self.typing(*self.PASSWORD_INPUT,password)

        time.sleep(delay)

        self.typing(*self.CONFIRM_PASSWORD_INPUT,confirm_password)

        time.sleep(delay)

        if avatar_path:
            self.find(*self.AVATAR_INPUT).send_keys(avatar_path)

        time.sleep(delay)

        self.click(*self.REGISTER_BUTTON)

    def get_first_name_validation_message(self):
        return self.find(
            *self.FIRST_NAME_INPUT
        ).get_attribute("validationMessage")

    def get_email_validation_message(self):
        return self.find(
            *self.EMAIL_INPUT
        ).get_attribute("validationMessage")

    def get_error_message(self):
        element = self.scroll_to_element(
            *self.ERROR_MESSAGE
        )

        return element.text