from selenium.webdriver.common.by import By

from pages.BasePage import BasePage

class RegisterPage(BasePage):
    """
    Page Object cho chức năng Đăng ký tài khoản.

    Mapping Test Case -> Method chính:

    TC-REGISTER-001
    - Step 1: open_page()
    - Step 2: enter_first_name(), enter_last_name(),
      enter_email(), enter_phone(), enter_username(),
      enter_password(), enter_confirm_password()
    - Step 3: upload_avatar()
    - Step 4: click_register()

    TC-REGISTER-002 -> TC-REGISTER-009
    - Nhập các trường hợp lệ:
      + enter_first_name()
      + enter_last_name()
      + enter_email()
      + enter_phone()
      + enter_username()
      + enter_password()
      + enter_confirm_password()
      + upload_avatar()
    - Thực hiện đăng ký:
      + click_register()
    - Kiểm tra required validation:
      + get_avatar_validation_message()
      + get_first_name_validation_message()
      + get_last_name_validation_message()
      + get_email_validation_message()
      + get_phone_validation_message()
      + get_username_validation_message()
      + get_password_validation_message()
      + get_confirm_password_validation_message()

    TC-REGISTER-010 -> TC-REGISTER-017
    - Nhập dữ liệu validation bằng các method enter_*()
    - upload_avatar()
    - click_register()
    - Kiểm tra:
      + get_email_validation_message()
      + get_error_message()

    TC-REGISTER-018 -> TC-REGISTER-019
    - Nhập username/email đã tồn tại bằng enter_*()
    - upload_avatar()
    - click_register()
    - Kiểm tra lỗi bằng get_error_message()
    """

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

    def enter_first_name(self, first_name):
        self.typing(*self.FIRST_NAME_INPUT, first_name)

    def enter_last_name(self, last_name):
        self.typing(*self.LAST_NAME_INPUT, last_name)

    def enter_email(self, email):
        self.typing(*self.EMAIL_INPUT, email)

    def enter_phone(self, phone):
        self.typing(*self.PHONE_INPUT, phone)

    def enter_username(self, username):
        self.typing(*self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.typing(*self.PASSWORD_INPUT, password)

    def enter_confirm_password(self, confirm_password):
        self.typing(*self.CONFIRM_PASSWORD_INPUT, confirm_password)

    def upload_avatar(self, avatar_path):
        self.find(*self.AVATAR_INPUT).send_keys(avatar_path)

    def click_register(self):
        self.click(*self.REGISTER_BUTTON)

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
            avatar_path
    ):
        self.typing(
            *self.FIRST_NAME_INPUT,
            first_name
        )

        self.typing(
            *self.LAST_NAME_INPUT,
            last_name
        )

        self.typing(
            *self.EMAIL_INPUT,
            email
        )

        self.typing(
            *self.PHONE_INPUT,
            phone
        )

        self.typing(
            *self.USERNAME_INPUT,
            username
        )

        self.typing(
            *self.PASSWORD_INPUT,
            password
        )

        self.typing(
            *self.CONFIRM_PASSWORD_INPUT,
            confirm_password
        )

        if avatar_path:
            self.find(
                *self.AVATAR_INPUT
            ).send_keys(avatar_path)

        self.click(
            *self.REGISTER_BUTTON
        )

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

    def get_last_name_validation_message(self):
        return self.find(*self.LAST_NAME_INPUT).get_attribute(
            "validationMessage"
        )

    def get_phone_validation_message(self):
        return self.find(*self.PHONE_INPUT).get_attribute(
            "validationMessage"
        )

    def get_username_validation_message(self):
        return self.find(*self.USERNAME_INPUT).get_attribute(
            "validationMessage"
        )

    def get_password_validation_message(self):
        return self.find(*self.PASSWORD_INPUT).get_attribute(
            "validationMessage"
        )

    def get_confirm_password_validation_message(self):
        return self.find(
            *self.CONFIRM_PASSWORD_INPUT
        ).get_attribute("validationMessage")