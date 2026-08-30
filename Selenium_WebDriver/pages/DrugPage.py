from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.BasePage import BasePage
from pages.LoginPage import LoginPage
from selenium.webdriver.common.keys import Keys

class DrugPage(BasePage):

    BASE_URL = "http://localhost:3000"
    LIST_URL = "http://localhost:3000/admin-drugs"
    ADD_URL = "http://localhost:3000/drugs/add"

    PAGE_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Quản lý kho dược phẩm']"
    )

    ADD_PAGE_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Thêm thuốc']"
    )

    EDIT_PAGE_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Cập nhật thuốc']"
    )

    ADD_BUTTON = (
        By.XPATH,
        "//a[@href='/drugs/add' and contains(normalize-space(), 'Thêm thuốc')]"
    )

    CATEGORY_BUTTONS = (
        By.CSS_SELECTOR,
        ".mb-3 > button"
    )

    SEARCH_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='Nhập tên thuốc...']"
    )

    SEARCH_BUTTON = (
        By.XPATH,
        "//button[@type='submit' and normalize-space()='Tìm kiếm']"
    )

    TABLE_ROWS = (
        By.CSS_SELECTOR,
        "table tbody tr"
    )

    ALERT = (
        By.CSS_SELECTOR,
        ".alert"
    )

    SPINNER = (
        By.CSS_SELECTOR,
        ".spinner-border"
    )

    CATEGORY_SELECT = (
        By.NAME,
        "categoryId"
    )

    NAME_INPUT = (
        By.NAME,
        "name"
    )

    DESCRIPTION_INPUT = (
        By.NAME,
        "description"
    )

    PRICE_INPUT = (
        By.NAME,
        "price"
    )

    QUANTITY_INPUT = (
        By.NAME,
        "quantity"
    )

    MIN_QUANTITY_INPUT = (
        By.NAME,
        "minQuantity"
    )

    PRODUCTION_DATE_INPUT = (
        By.NAME,
        "productionDate"
    )

    EXPIRY_DATE_INPUT = (
        By.NAME,
        "expiryDate"
    )

    DOSAGE_FORM_INPUT = (
        By.NAME,
        "dosageForm"
    )

    UNIT_INPUT = (
        By.NAME,
        "unit"
    )

    STRENGTH_INPUT = (
        By.NAME,
        "strength"
    )

    MANUFACTURER_INPUT = (
        By.NAME,
        "manufacturer"
    )

    STATUS_SELECT = (
        By.NAME,
        "status"
    )

    IMAGE_INPUT = (
        By.NAME,
        "image"
    )

    SUBMIT_BUTTON = (
        By.CSS_SELECTOR,
        "form button[type='submit']"
    )

    def login_admin(self, username, password):
        login_page = LoginPage(self.driver)

        login_page.open_page()
        login_page.login(
            username,
            password,
            delay=0
        )

        self.wait.until(
            lambda driver:
            driver.current_url == self.BASE_URL + "/"
        )

    def wait_loading_finished(self):
        self.wait.until(
            lambda driver:
            len(driver.find_elements(*self.SPINNER)) == 0
        )

    def open_list(self):
        self.open(self.LIST_URL)

        self.wait.until(
            EC.visibility_of_element_located(
                self.PAGE_TITLE
            )
        )

        self.wait_loading_finished()

    def open_add(self):
        self.open(self.ADD_URL)

        self.wait.until(
            EC.visibility_of_element_located(
                self.ADD_PAGE_TITLE
            )
        )

        self.wait_loading_finished()

    def get_category_names(self):
        buttons = self.driver.find_elements(
            *self.CATEGORY_BUTTONS
        )

        return [
            button.text.strip()
            for button in buttons
            if button.text.strip()
        ]

    def select_category(self, category_name):
        button = self.wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//button[normalize-space()='{category_name}']"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        self.wait_loading_finished()

    def search_drug(self, keyword):
        field = self.find(
            *self.SEARCH_INPUT
        )

        field.clear()
        field.send_keys(keyword)

        self.click(
            *self.SEARCH_BUTTON
        )

        self.wait_loading_finished()

    def get_rows(self):
        return self.driver.find_elements(
            *self.TABLE_ROWS
        )

    def get_table_data(self):
        rows = self.get_rows()
        result = []

        for row in rows:
            cells = row.find_elements(
                By.TAG_NAME,
                "td"
            )

            if len(cells) < 10:
                continue

            result.append({
                "name": cells[2].text.strip(),
                "category": cells[3].text.strip(),
                "price": cells[4].text.strip(),
                "stock": cells[5].text.strip(),
                "production_date": cells[6].text.strip(),
                "expiry_date": cells[7].text.strip(),
                "status": cells[8].text.strip(),
            })

        return result

    def find_drug_row(self, drug_name):
        return self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//table//tbody//tr"
                f"[.//td//strong[normalize-space()='{drug_name}']]"
            ))
        )

    def click_edit_drug(self, drug_name):
        row = self.find_drug_row(
            drug_name
        )

        button = row.find_element(
            By.XPATH,
            ".//a[normalize-space()='Sửa']"
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        self.wait.until(
            EC.visibility_of_element_located(
                self.EDIT_PAGE_TITLE
            )
        )

    def click_delete_drug(self, drug_name):
        row = self.find_drug_row(
            drug_name
        )

        button = row.find_element(
            By.XPATH,
            ".//button[normalize-space()='Xóa']"
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

    def confirm_delete(self):
        alert = self.wait.until(
            EC.alert_is_present()
        )

        alert.accept()

        self.wait_loading_finished()

    def is_drug_present(self, drug_name):
        rows = self.get_table_data()

        return any(
            row["name"].split("\n")[0].strip().lower()
            == drug_name.strip().lower()
            for row in rows
        )

    def get_drug(self, drug_name):
        rows = self.get_table_data()

        for row in rows:
            actual_name = row["name"].split("\n")[0].strip()

            if actual_name.lower() == drug_name.strip().lower():
                return row

        return None

    def click_add_button(self):
        self.click(
            *self.ADD_BUTTON
        )

        self.wait.until(
            EC.visibility_of_element_located(
                self.ADD_PAGE_TITLE
            )
        )

    def select_form_category(self, category_name):
        element = self.find(
            *self.CATEGORY_SELECT
        )

        Select(element).select_by_visible_text(
            category_name
        )

    def select_status(self, status_value):
        element = self.find(
            *self.STATUS_SELECT
        )

        Select(element).select_by_value(
            status_value
        )

    def fill_form(
        self,
        category_name,
        name,
        price,
        quantity,
        min_quantity,
        production_date,
        expiry_date,
        dosage_form="",
        unit="",
        strength="",
        manufacturer="",
        status="available",
        image=""
    ):
        self.select_form_category(
            category_name
        )

        self.typing(
            *self.NAME_INPUT,
            name
        )

        self.typing(
            *self.PRICE_INPUT,
            str(price)
        )

        self.typing(
            *self.QUANTITY_INPUT,
            str(quantity)
        )

        self.typing(
            *self.MIN_QUANTITY_INPUT,
            str(min_quantity)
        )

        self.set_date(
            self.PRODUCTION_DATE_INPUT,
            production_date
        )

        self.set_date(
            self.EXPIRY_DATE_INPUT,
            expiry_date
        )
        if dosage_form:
            self.typing(
                *self.DOSAGE_FORM_INPUT,
                dosage_form
            )

        if unit:
            self.typing(
                *self.UNIT_INPUT,
                unit
            )

        if strength:
            self.typing(
                *self.STRENGTH_INPUT,
                strength
            )

        if manufacturer:
            self.typing(
                *self.MANUFACTURER_INPUT,
                manufacturer
            )

        self.select_status(
            status
        )

        if image:
            self.typing(
                *self.IMAGE_INPUT,
                image
            )

    def submit_form(self):
        self.click(
            *self.SUBMIT_BUTTON
        )

    def get_field_value(self, locator):
        return self.find(
            *locator
        ).get_attribute("value")

    def set_price(self, price):
        self.typing(
            *self.PRICE_INPUT,
            str(price)
        )

    def get_validation_message(self, locator):
        return self.find(
            *locator
        ).get_attribute(
            "validationMessage"
        )

    def is_on_list_page(self):
        return self.driver.current_url == self.LIST_URL

    def get_alert_text(self):
        alerts = self.driver.find_elements(
            *self.ALERT
        )

        if not alerts:
            return ""

        return alerts[0].text.strip()

    def set_date(self, locator, date_value):
        element = self.find(*locator)

        self.driver.execute_script(
            """
            const element = arguments[0];
            const value = arguments[1];

            const setter = Object.getOwnPropertyDescriptor(
                HTMLInputElement.prototype,
                'value'
            ).set;

            setter.call(element, value);

            element.dispatchEvent(
                new Event('input', { bubbles: true })
            );

            element.dispatchEvent(
                new Event('change', { bubbles: true })
            );
            """,
            element,
            date_value
        )

    def get_form_validation_errors(self):
        fields = {
            "categoryId": self.CATEGORY_SELECT,
            "name": self.NAME_INPUT,
            "price": self.PRICE_INPUT,
            "quantity": self.QUANTITY_INPUT,
            "minQuantity": self.MIN_QUANTITY_INPUT,
            "productionDate": self.PRODUCTION_DATE_INPUT,
            "expiryDate": self.EXPIRY_DATE_INPUT,
            "dosageForm": self.DOSAGE_FORM_INPUT,
            "unit": self.UNIT_INPUT,
            "strength": self.STRENGTH_INPUT,
            "manufacturer": self.MANUFACTURER_INPUT,
        }

        errors = {}

        for field_name, locator in fields.items():
            element = self.find(*locator)

            message = element.get_attribute(
                "validationMessage"
            )

            if message:
                errors[field_name] = message

        return errors