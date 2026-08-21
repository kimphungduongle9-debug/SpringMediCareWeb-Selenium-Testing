from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.BasePage import BasePage


class PrescriptionPage(BasePage):
    """
    Page Object cho chức năng kê đơn thuốc.

    TC-NOTIFICATION-006 sử dụng POM tại:
    - Step 6: Mở tab Đơn thuốc.
    - Step 7: Chọn thuốc, nhập số lượng, liều dùng,
      thêm thuốc vào đơn và lưu đơn thuốc.
    """

    # =========================
    # LOCATORS
    # =========================

    PRESCRIPTION_TAB = (
        By.XPATH,
        "//button[@role='tab' and normalize-space()='Đơn thuốc']"
    )

    PRESCRIPTION_FORM_TITLE = (
        By.XPATH,
        "//h4[normalize-space()='Kê đơn thuốc']"
    )

    DRUG_SELECT = (
        By.XPATH,
        "//h4[normalize-space()='Kê đơn thuốc']"
        "/ancestor::div[contains(@class, 'card')]"
        "//select"
    )

    QUANTITY_INPUT = (
        By.XPATH,
        "//h4[normalize-space()='Kê đơn thuốc']"
        "/ancestor::div[contains(@class, 'card')]"
        "//label[normalize-space()='Số lượng']"
        "/following::input[@type='number'][1]"
    )

    DOSAGE_INPUT = (
        By.XPATH,
        "//h4[normalize-space()='Kê đơn thuốc']"
        "/ancestor::div[contains(@class, 'card')]"
        "//input[@placeholder="
        "'Ví dụ: Ngày uống 2 lần, mỗi lần 1 viên sau ăn']"
    )

    ADD_TO_PRESCRIPTION_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Thêm vào đơn']"
    )

    SAVE_PRESCRIPTION_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Lưu đơn thuốc']"
    )

    PRESCRIPTION_SUCCESS_MESSAGE = (
        By.XPATH,
        "//div[contains(@class, 'alert') and "
        "contains(normalize-space(.), 'Kê đơn thuốc thành công.')]"
    )

    PRESCRIPTION_TABLE_ROWS = (
        By.XPATH,
        "//h4[normalize-space()='Kê đơn thuốc']"
        "/ancestor::div[contains(@class, 'card')]"
        "//tbody/tr"
    )

    # =========================
    # STEP 6 - POM
    # Mở chức năng kê đơn thuốc
    # =========================

    def open_prescription_tab(self):
        self.click(*self.PRESCRIPTION_TAB)

    def is_prescription_form_present(self):
        return len(self.finds(*self.PRESCRIPTION_FORM_TITLE)) > 0

    # =========================
    # STEP 7 - POM
    # Tạo và lưu đơn thuốc
    # =========================

    def select_drug_by_index(self, option_index):
        drug_select = Select(
            self.find(*self.DRUG_SELECT)
        )

        drug_select.select_by_index(
            int(option_index)
        )

        return (
            drug_select
            .first_selected_option
            .text
            .strip()
        )

    def enter_quantity(self, quantity):
        self.typing(
            *self.QUANTITY_INPUT,
            str(quantity)
        )

    def enter_dosage(self, dosage):
        self.typing(
            *self.DOSAGE_INPUT,
            dosage
        )

    def click_add_to_prescription(self):
        self.click(
            *self.ADD_TO_PRESCRIPTION_BUTTON
        )

    def get_prescription_item_count(self):
        return len(
            self.finds(*self.PRESCRIPTION_TABLE_ROWS)
        )

    def click_save_prescription(self):
        self.click(
            *self.SAVE_PRESCRIPTION_BUTTON
        )

    def get_prescription_success_message(self):
        return (
            self.find(
                *self.PRESCRIPTION_SUCCESS_MESSAGE
            )
            .text
            .strip()
        )

