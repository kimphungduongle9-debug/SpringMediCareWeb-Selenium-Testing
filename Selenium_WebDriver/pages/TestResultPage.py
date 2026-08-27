from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class TestResultPage(BasePage):
    __test__ = False
    """
    Page Object cho chức năng Xét nghiệm
    trong Chi tiết hồ sơ bệnh án.

    TC-NOTIFICATION-007 sử dụng POM tại:
    - Step 4: Chuyển đến phần Xét nghiệm.
    - Step 5: Nhập kết quả xét nghiệm hợp lệ.
    - Step 6: Lưu kết quả xét nghiệm.
    """

    # ============================================================
    # LOCATORS
    # ============================================================

    TEST_RESULT_TAB = (
        By.XPATH,
        "//button[@role='tab' and normalize-space()='Xét nghiệm']"
    )

    TEST_RESULT_FORM_TITLE = (
        By.XPATH,
        "//h4[normalize-space()='Thêm kết quả xét nghiệm']"
    )

    TEST_NAME_INPUT = (
        By.XPATH,
        "//h4[normalize-space()='Thêm kết quả xét nghiệm']"
        "/ancestor::div[contains(@class,'card')]"
        "//label[normalize-space()='Tên xét nghiệm']"
        "/following-sibling::input"
    )

    TEST_RESULT_TEXTAREA = (
        By.XPATH,
        "//h4[normalize-space()='Thêm kết quả xét nghiệm']"
        "/ancestor::div[contains(@class,'card')]"
        "//label[normalize-space()='Kết quả']"
        "/following-sibling::textarea"
    )

    SAVE_TEST_RESULT_BUTTON = (
        By.XPATH,
        "//h4[normalize-space()='Thêm kết quả xét nghiệm']"
        "/ancestor::div[contains(@class,'card')]"
        "//button[normalize-space()='Lưu kết quả']"
    )

    TEST_RESULT_SUCCESS_MESSAGE = (
        By.XPATH,
        "//div[contains(@class,'alert') "
        "and contains(normalize-space(.), "
        "'Thêm kết quả xét nghiệm thành công.')]"
    )

    TEST_RESULT_ROWS = (
        By.XPATH,
        "//h4[normalize-space()='Kết quả xét nghiệm']"
        "/ancestor::div[contains(@class,'card')]"
        "//tbody/tr"
    )

    # ============================================================
    # Step 4 - POM
    # Chuyển đến tab Xét nghiệm.
    # ============================================================

    def open_test_result_tab(self):
        self.click(
            *self.TEST_RESULT_TAB
        )

    def is_test_result_form_present(self):
        return len(
            self.finds(
                *self.TEST_RESULT_FORM_TITLE
            )
        ) > 0

    # ============================================================
    # Step 5 - POM
    # Nhập thông tin kết quả xét nghiệm.
    # ============================================================

    def enter_test_name(self, test_name):
        self.typing(
            *self.TEST_NAME_INPUT,
            test_name
        )

    def enter_test_result(self, result):
        self.typing(
            *self.TEST_RESULT_TEXTAREA,
            result
        )

    # ============================================================
    # Step 6 - POM
    # Lưu kết quả xét nghiệm.
    # ============================================================

    def click_save_test_result(self):
        self.click(
            *self.SAVE_TEST_RESULT_BUTTON
        )

    def get_success_message(self):
        return (
            self.find(
                *self.TEST_RESULT_SUCCESS_MESSAGE
            )
            .text
            .strip()
        )

    def has_test_result(self, test_name, result):
        rows = self.finds(
            *self.TEST_RESULT_ROWS
        )

        for row in rows:
            row_text = row.text.strip()

            if (
                test_name in row_text
                and result in row_text
            ):
                return True

        return False