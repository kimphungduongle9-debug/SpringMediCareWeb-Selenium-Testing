from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class PatientMedicalHistoryPage(BasePage):

    URL = "http://localhost:3000/patient-medical-history"

    PAGE_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Lịch sử khám bệnh']"
    )

    RECORD_ROWS = (
        By.CSS_SELECTOR,
        "table tbody tr"
    )

    RECORD_ID_CELLS = (
        By.CSS_SELECTOR,
        "table tbody tr td:first-child"
    )

    EMPTY_MESSAGE = (
        By.XPATH,
        "//div[contains(@class, 'alert') "
        "and contains(normalize-space(.), "
        "'Bạn chưa có hồ sơ khám bệnh nào.')]"
    )

    VIEW_DETAIL_BUTTONS = (
        By.XPATH,
        "//table//button[normalize-space()='Xem chi tiết']"
    )

    def open_page(self):
        self.open(self.URL)

    def get_page_title(self):
        return self.find(
            *self.PAGE_TITLE
        ).text

    def get_record_count(self):
        return len(
            self.finds(*self.RECORD_ROWS)
        )

    def get_record_ids(self):
        return [
            element.text.strip()
            for element in self.finds(
                *self.RECORD_ID_CELLS
            )
        ]

    def is_empty_message_present(self):
        return len(
            self.finds(*self.EMPTY_MESSAGE)
        ) > 0

    def get_first_record_id(self):
        record_ids = self.get_record_ids()

        assert record_ids, (
            "Expected: Patient có ít nhất một Medical Record | "
            "Actual: Không có Medical Record nào"
        )

        return record_ids[0]

    def click_view_detail_by_record_id(self, record_id):
        button = (
            By.XPATH,
            f"//table//tr[td[1][normalize-space()='{record_id}']]"
            "//button[normalize-space()='Xem chi tiết']"
        )

        self.click(*button)