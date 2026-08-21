import unicodedata

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

    @staticmethod
    def normalize_text(text):
        """
        Chuẩn hóa chuỗi để so sánh nội dung notification:
        - Chuyển về chữ thường.
        - Loại bỏ dấu tiếng Việt.
        - Chuyển đ/Đ thành d/D.
        """
        text = text.replace("đ", "d").replace("Đ", "D")

        text = unicodedata.normalize(
            "NFD",
            text
        )

        text = "".join(
            character
            for character in text
            if unicodedata.category(character) != "Mn"
        )

        return text.lower().strip()

    def get_latest_notification_by_type_and_keyword(
            self,
            expected_type,
            expected_keyword):
        """
        TC-NOTIFICATION-003 - Step 8:
        Lấy notification mới nhất và kiểm tra
        notification vừa phát sinh sau khi Doctor lưu kết quả khám.
        """

        notifications = self.finds(
            *self.NOTIFICATION_ITEMS
        )

        if not notifications:
            raise AssertionError(
                "Patient không có notification nào."
            )

        # Notification mới nhất được hiển thị đầu danh sách.
        latest_notification = notifications[0]

        notification_type = latest_notification.find_element(
            *self.NOTIFICATION_TYPE
        ).text.strip()

        notification_content = latest_notification.find_element(
            *self.NOTIFICATION_CONTENT
        ).text.strip()

        assert notification_type == expected_type, (
            "Notification mới nhất không đúng loại. "
            f"Expected: '{expected_type}', "
            f"Actual: '{notification_type}'."
        )

        normalized_expected = self.normalize_text(
            expected_keyword
        )

        normalized_actual = self.normalize_text(
            notification_content
        )

        assert normalized_expected in normalized_actual, (
            "Notification mới nhất không có nội dung mong đợi. "
            f"Expected keyword: '{expected_keyword}', "
            f"Actual: '{notification_content}'."
        )

        return latest_notification

    def has_notification_by_appointment_id(
            self,
            appointment_id):

        expected_id = f"#{appointment_id}"

        notifications = self.finds(
            *self.NOTIFICATION_ITEMS
        )

        for notification in notifications:
            content = notification.find_element(
                *self.NOTIFICATION_CONTENT
            ).text

            if expected_id in content:
                return True

        return False

    def get_all_notification_contents(self):
        """
        TC-NOTIFICATION-005:
        Lấy toàn bộ nội dung notification đang hiển thị
        của Patient hiện tại.
        """

        notifications = self.finds(
            *self.NOTIFICATION_ITEMS
        )

        return [
            notification.find_element(
                *self.NOTIFICATION_CONTENT
            ).text.strip()
            for notification in notifications
        ]
