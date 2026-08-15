from selenium.webdriver.common.by import By

from pages.BasePage import BasePage
from datetime import datetime

class DoctorWorkSchedulePage(BasePage):

    URL = "http://localhost:3000/doctor-work-schedule"

    PAGE_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Lịch làm việc của tôi']"
    )

    DOCTOR_INFO = (
        By.XPATH,
        "//h2[normalize-space()='Lịch làm việc của tôi']/following-sibling::p"
    )

    PREVIOUS_WEEK_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='← Tuần trước']"
    )

    NEXT_WEEK_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Tuần sau →']"
    )

    WEEK_RANGE = (
        By.XPATH,
        "//button[normalize-space()='← Tuần trước']/following-sibling::div[1]"
    )

    SCHEDULE_LIST_TABLE = (
        By.XPATH,
        "//h3[normalize-space()='Danh sách lịch làm việc']/following::table[1]"
    )

    DOCTOR_NAME = (
        By.XPATH,
        "//h2[normalize-space()='Lịch làm việc của tôi']"
        "/following-sibling::p[1]//strong[1]"
    )

    SPECIALTY = (
        By.XPATH,
        "//h2[normalize-space()='Lịch làm việc của tôi']"
        "/following-sibling::p[1]//strong[2]"
    )

    WEEK_TABLE = (
        By.XPATH,
        "//h3[normalize-space()='Lịch làm việc theo tuần']"
        "/following::table[1]"
    )

    WEEK_HEADER_DATES = (
        By.XPATH,
        "//h3[normalize-space()='Lịch làm việc theo tuần']"
        "/following::table[1]/thead/tr/th[position()>1]/small"
    )

    WEEK_SHIFT_ROWS = (
        By.XPATH,
        "//h3[normalize-space()='Lịch làm việc theo tuần']"
        "/following::table[1]/tbody/tr"
    )

    EMPTY_CELLS = (
        By.XPATH,
        "//h3[normalize-space()='Lịch làm việc theo tuần']"
        "/following::table[1]//span[normalize-space()='Trống']"
    )

    WEEK_DOCTOR_NAMES = (
        By.XPATH,
        "//h3[normalize-space()='Lịch làm việc theo tuần']"
        "/following::table[1]/tbody//strong"
    )
    SCHEDULE_LIST_ROWS = (
        By.XPATH,
        "//h3[normalize-space()='Danh sách lịch làm việc']"
        "/following::table[1]/tbody/tr"
    )
    SCHEDULE_LIST_TITLE = (
        By.XPATH,
        "//h3[normalize-space()='Danh sách lịch làm việc']"
    )
    def open_page(self):
        self.open(self.URL)

    def get_page_title(self):
        return self.find(*self.PAGE_TITLE).text

    def get_doctor_info(self):
        return self.find(*self.DOCTOR_INFO).text

    def get_week_range(self):
        return self.find(*self.WEEK_RANGE).text

    def click_previous_week(self):
        self.click(*self.PREVIOUS_WEEK_BUTTON)

    def click_next_week(self):
        self.click(*self.NEXT_WEEK_BUTTON)

    def get_doctor_name(self):
        return self.find(*self.DOCTOR_NAME).text

    def get_specialty(self):
        return self.find(*self.SPECIALTY).text

    def get_week_header_dates(self):
        elements = self.finds(*self.WEEK_HEADER_DATES)
        return [element.text for element in elements]

    def get_week_shift_rows(self):
        elements = self.finds(*self.WEEK_SHIFT_ROWS)
        return [element.text for element in elements]

    def get_empty_cell_count(self):
        return len(self.finds(*self.EMPTY_CELLS))

    def get_week_doctor_names(self):
        elements = self.finds(*self.WEEK_DOCTOR_NAMES)
        return [element.text for element in elements]

    def get_week_schedule_records(self):
        dates = self.get_week_header_dates()

        rows = self.finds(*self.WEEK_SHIFT_ROWS)

        records = []

        for row in rows:
            shift_info = row.find_element(
                By.TAG_NAME,
                "th"
            ).text.splitlines()

            shift_name = shift_info[0]

            start_time, end_time = (
                shift_info[1].split(" - ")
            )

            cells = row.find_elements(
                By.TAG_NAME,
                "td"
            )

            for index, cell in enumerate(cells):

                if "Trống" in cell.text:
                    continue

                cards = cell.find_elements(
                    By.XPATH,
                    "./div"
                )

                for card in cards:
                    doctor_name = (
                        card.find_element(
                            By.TAG_NAME,
                            "strong"
                        ).text
                    )

                    formatted_date = datetime.strptime(
                        dates[index],
                        "%d/%m/%Y"
                    ).strftime("%d/%m/%Y")

                    records.append({
                        "doctor": doctor_name,
                        "date": formatted_date,
                        "shift": shift_name,
                        "start": start_time,
                        "end": end_time
                    })

        return records

    def has_schedule_in_week(self):
        return len(
            self.finds(*self.WEEK_DOCTOR_NAMES)
        ) > 0

    def scroll_to_schedule_list(self):
        self.scroll_to_element(
            *self.SCHEDULE_LIST_TITLE
        )

    def get_schedule_list_records(self):
        rows = self.finds(
            *self.SCHEDULE_LIST_ROWS
        )

        records = []

        for row in rows:
            cells = row.find_elements(
                By.TAG_NAME,
                "td"
            )

            if len(cells) < 7:
                continue

            records.append({
                "doctor": cells[1].text,
                "date": cells[2].text,
                "shift": cells[3].text,
                "start": cells[4].text,
                "end": cells[5].text
            })

        return records

    def get_schedule_list_doctor_names(self):
        rows = self.finds(
            *self.SCHEDULE_LIST_ROWS
        )

        doctor_names = []

        for row in rows:
            cells = row.find_elements(
                By.TAG_NAME,
                "td"
            )

            if len(cells) < 8:
                continue

            doctor_names.append(
                cells[1].text
            )

        return doctor_names