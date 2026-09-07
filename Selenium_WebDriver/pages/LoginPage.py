from selenium.webdriver.common.by import By

from pages.BasePage import BasePage
class LoginPage(BasePage):
    """
    Page Object cho chức năng Đăng nhập / Đăng xuất.

    Mapping Test Case -> Method chính:

    TC-LOGIN-001, TC-LOGIN-002
    - Step 1: open_page()
    - Step 2: enter_username(), get_username_value()
    - Step 3: enter_password(), get_password_value()
    - Step 4: click_login()
    - Step 5: get_user_greeting(), is_logout_button_displayed()

    TC-LOGIN-003
    - Step 2: enter_username(), get_username_value()
    - Step 3: enter_password()
    - Step 4: click_login()
    - Step 5: get_username_validation_message(),
      is_logout_button_present()

    TC-LOGIN-004
    - Step 2: enter_username()
    - Step 3: enter_password(), get_password_value()
    - Step 4: click_login()
    - Step 5: get_password_validation_message(),
      is_logout_button_present()

    TC-LOGIN-005
    - Step 2-3: enter_username(), enter_password()
    - Step 4: click_login()
    - Step 5: get_username_validation_message(),
      get_password_validation_message(),
      is_logout_button_present()

    TC-LOGIN-006, TC-LOGIN-007
    - Step 2-3: enter_username(), enter_password()
    - Step 4: click_login()
    - Step 5: get_error_message(), is_logout_button_present()

    TC-LOGIN-008
    - Step 1: open_page(), enter_username(),
      enter_password(), click_login()
    - Step 2: logout()
    - Step 3: is_login_button_displayed(),
      is_logout_button_present()

    TC-LOGIN-009
    - Step 1: open_page(), is_logout_button_present()
    - Step 2: open()
    - Step 3: is_login_required_message_displayed(),
      is_login_nav_link_displayed()

    TC-LOGIN-010
    - Step 1: open_page(), enter_username(),
      enter_password(), click_login()
    - Step 2: logout()
    - Step 4: is_login_nav_link_displayed(),
      is_user_greeting_present(),
      is_logout_button_present()
    """

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

    def login(self, username, password):
        self.typing(
            *self.USERNAME_INPUT,
            username
        )

        self.typing(
            *self.PASSWORD_INPUT,
            password
        )

        self.click(
            *self.LOGIN_BUTTON
        )

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

    def is_logout_button_present(self):
        return len(self.finds(*self.LOGOUT_BUTTON)) > 0

    def is_user_greeting_present(self):
        return len(self.finds(*self.USER_GREETING)) > 0

    def is_login_required_message_displayed(self):
        return self.find(*self.LOGIN_REQUIRED_MESSAGE).is_displayed()

    def is_login_nav_link_displayed(self):
        return self.find(*self.LOGIN_NAV_LINK).is_displayed()

    def enter_username(self, username):
        self.typing(
            *self.USERNAME_INPUT,
            username
        )

    def enter_password(self, password):
        self.typing(
            *self.PASSWORD_INPUT,
            password
        )

    def click_login(self):
        self.click(
            *self.LOGIN_BUTTON
        )

    def is_login_nav_link_present(self):
        return len(
            self.finds(*self.LOGIN_NAV_LINK)
        ) > 0

    def get_username_value(self):
        return self.find(
            *self.USERNAME_INPUT
        ).get_attribute("value")

    def get_password_value(self):
        return self.find(
            *self.PASSWORD_INPUT
        ).get_attribute("value")