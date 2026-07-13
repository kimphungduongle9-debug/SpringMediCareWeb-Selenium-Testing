from selenium.webdriver.common.by import By

from pages.BasePage import BasePage

import time

class LoginPage(BasePage):
    URL = "http://localhost:3000/login"

    USERNAME_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='Nhập tên đăng nhập hoặc email']"
    )

    PASSWORD_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='Nhập mật khẩu']"
    )

    LOGIN_BUTTON = (
        By.CSS_SELECTOR,
        "button.login-big-btn[type='submit']"
    )

    USER_GREETING = (
        By.XPATH,
        "//nav[contains(@class, 'main-nav')]"
        "//span[contains(normalize-space(.), 'Xin chào')]"
    )

    LOGOUT_BUTTON = (
        By.XPATH,
        "//button[@type='button' and normalize-space()='Đăng xuất']"
    )

    ERROR_MESSAGE = (
        By.CLASS_NAME,
        "login-error-text"
    )
    LOGIN_REQUIRED_MESSAGE = (
        By.XPATH,
        "//div[contains(text(),'Vui lòng đăng nhập để xem lịch hẹn.')]"
    )

    LOGIN_NAV_LINK = (
        By.XPATH,
        "//a[@href='/login']"
    )
    def open_page(self):
        self.open(self.URL)

    def login(self, username, password, delay=1.5):
        time.sleep(delay)

        self.typing(*self.USERNAME_INPUT, username)
        time.sleep(delay)

        self.typing(*self.PASSWORD_INPUT, password)
        time.sleep(delay)

        self.click(*self.LOGIN_BUTTON)

    def get_user_greeting(self):
        return self.find(*self.USER_GREETING).text

    def is_logout_button_displayed(self):
        return self.find(*self.LOGOUT_BUTTON).is_displayed()

    def get_error_message(self):
        return self.find(*self.ERROR_MESSAGE).text

    def get_username_validation_message(self):
        return self.find(
            *self.USERNAME_INPUT
        ).get_attribute("validationMessage")

    def get_password_validation_message(self):
        return self.find(
            *self.PASSWORD_INPUT
        ).get_attribute("validationMessage")

    def logout(self):
        self.click(*self.LOGOUT_BUTTON)

    def is_login_button_displayed(self):
        return self.find(*self.LOGIN_BUTTON).is_displayed()
    #
    # def is_login_nav_link_displayed(self):
    #     return self.find(*self.LOGIN_NAV_LINK).is_displayed()

    def is_logout_button_present(self):
        return len(self.finds(*self.LOGOUT_BUTTON)) > 0

    def is_user_greeting_present(self):
        return len(self.finds(*self.USER_GREETING)) > 0

    def is_login_required_message_displayed(self):
        return self.find(*self.LOGIN_REQUIRED_MESSAGE).is_displayed()

    def is_login_nav_link_displayed(self):
        return self.find(*self.LOGIN_NAV_LINK).is_displayed()



