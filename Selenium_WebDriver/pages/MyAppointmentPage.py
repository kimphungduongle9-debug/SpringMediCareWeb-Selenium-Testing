from selenium.webdriver.common.by import By

from pages.BasePage import BasePage
from selenium.webdriver.support.ui import WebDriverWait

class MyAppointmentPage(BasePage):
    """
    Page Object cho chức năng Lịch hẹn của tôi của Patient.

    Mapping Test Case -> Step -> Method:

    TC-MYAPPOINTMENT-001
    - Step 5: Mở trang Lịch hẹn của tôi
      + open_page()
      + get_page_title()
    - Step 6: Tìm lịch hẹn vừa tạo
      + wait_for_appointment_by_note()
      + get_appointment_by_note()
    - Step 7-8: Kiểm tra Doctor, thời gian, ghi chú
      và trạng thái Chờ xác nhận
      + wait_for_appointment_by_note()

    TC-MYAPPOINTMENT-002
    - Step 7: Patient mở trang và tìm lịch
      vừa được Admin xác nhận
      + open_page()
      + wait_for_appointment_by_note()
    - Step 8: Kiểm tra thông tin và trạng thái Đã xác nhận
      + wait_for_appointment_by_note()

    TC-MYAPPOINTMENT-003
    - Step 7: Patient mở trang và tìm lịch
      vừa bị Admin hủy
      + open_page()
      + wait_for_appointment_by_note()
    - Step 8: Kiểm tra thông tin và trạng thái Đã hủy
      + wait_for_appointment_by_note()

    TC-MYAPPOINTMENT-004
    - Step 2: Kiểm tra lịch vừa tạo
      ở trạng thái Chờ xác nhận
      + open_page()
      + wait_for_appointment_by_note()
    - Step 8: Patient mở lại trang và tìm lịch
      sau khi Doctor hoàn thành khám
      + open_page()
      + wait_for_appointment_by_note()
    - Step 9: Kiểm tra trạng thái Đã hoàn thành
      và dữ liệu ban đầu không thay đổi
      + wait_for_appointment_by_note()

    TC-MYAPPOINTMENT-005
    - Step 8: Patient B mở Lịch hẹn của tôi
      và tìm lịch mới tại slot đã giải phóng
      + open_page()
      + wait_for_appointment_by_note()
    - Step 9: Kiểm tra lịch mới có ID khác
      và trạng thái Chờ xác nhận
      + wait_for_appointment_by_note()
    """

    URL = "http://localhost:3000/my-appointments"

    PAGE_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Lịch hẹn của tôi']"
    )

    APPOINTMENT_ROWS = (
        By.XPATH,
        "//table/tbody/tr"
    )

    EMPTY_MESSAGE = (
        By.XPATH,
        "//*[normalize-space()='Bạn chưa có lịch hẹn nào.']"
    )

    def open_page(self):
        self.open(self.URL)

    def get_page_title(self):
        return self.find(*self.PAGE_TITLE).text

    def get_appointment_by_note(self, note):
        rows = self.finds(
            *self.APPOINTMENT_ROWS
        )

        for row in rows:
            cells = row.find_elements(
                By.TAG_NAME,
                "td"
            )

            if len(cells) < 5:
                continue

            if cells[4].text == note:
                return {
                    "id": cells[0].text,
                    "doctor": cells[1].text,
                    "time": cells[2].text,
                    "status": cells[3].text,
                    "note": cells[4].text
                }

        return None

    def wait_for_appointment_by_note(self, note, timeout=10):
        def find_appointment(driver):
            appointment = self.get_appointment_by_note(note)

            if appointment is not None:
                return appointment

            return False

        return WebDriverWait(
            self.driver,
            timeout
        ).until(find_appointment)