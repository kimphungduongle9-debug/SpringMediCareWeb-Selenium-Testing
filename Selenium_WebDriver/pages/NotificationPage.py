from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class NotificationPage(BasePage):
    """
    Page Object cho trang Thông báo của Patient.

    TC-NOTIFICATION-001 sử dụng Page Object này cho:
    - Step 5: Mở trang Thông báo.
    - Step 6: Tìm thông báo của lịch vừa được Admin xác nhận.
    - Step 7: Lấy loại, nội dung và thời gian thông báo để kiểm tra.
    """

    URL = "http://localhost:3000/notifications"

    PAGE_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Thông báo của tôi']"
    )

    NOTIFICATION_ITEMS = (
        By.CSS_SELECTOR,
        "div.notification-item"
    )

    NOTIFICATION_TYPE = (
        By.TAG_NAME,
        "strong"
    )

    NOTIFICATION_CONTENT = (
        By.TAG_NAME,
        "p"
    )

    NOTIFICATION_TIME = (
        By.TAG_NAME,
        "span"
    )

    # Step 5:
    # Patient mở trang Thông báo.
    def open_page(self):
        self.open(self.URL)

    def get_page_title(self):
        return self.find(*self.PAGE_TITLE).text.strip()

    # Step 6:
    # Tìm đúng thông báo dựa trên ID của lịch vừa được xác nhận.
    # Ví dụ appointment_id = 119 thì tìm notification có "#119".
    def get_notification_by_appointment_id(self, appointment_id):
        expected_id = f"#{appointment_id}"

        notifications = self.finds(
            *self.NOTIFICATION_ITEMS
        )

        for notification in notifications:
            content = notification.find_element(
                *self.NOTIFICATION_CONTENT
            ).text

            if expected_id in content:
                return notification

        raise AssertionError(
            "Không tìm thấy thông báo của lịch hẹn "
            f"{expected_id}."
        )

    # Step 7:
    # Lấy loại thông báo, ví dụ: [Lịch hẹn].
    def get_notification_type(self, notification):
        return notification.find_element(
            *self.NOTIFICATION_TYPE
        ).text.strip()

    # Step 7:
    # Lấy toàn bộ nội dung của notification.
    def get_notification_content(self, notification):
        return notification.find_element(
            *self.NOTIFICATION_CONTENT
        ).text.strip()

    # Step 7:
    # Lấy thời gian notification hiển thị.
    def get_notification_time(self, notification):
        return notification.find_element(
            *self.NOTIFICATION_TIME
        ).text.strip()