import unicodedata

from selenium.webdriver.common.by import By
from pages.BasePage import BasePage
from selenium.common.exceptions import NoSuchElementException

class NotificationPage(BasePage):
    """
    Page Object cho chức năng Notification của Patient.

    Mapping Test Case -> Step -> Method:

    TC-NOTIFICATION-001
    - Step 5: Mở trang Thông báo
      + open_page()
      + get_page_title()

    - Step 6: Tìm thông báo của lịch vừa được Admin xác nhận
      + get_notification_by_appointment_id()

    - Step 7: Lấy loại, nội dung và thời gian thông báo để kiểm tra
      + get_notification_type()
      + get_notification_content()
      + get_notification_time()

    TC-NOTIFICATION-003
    - Step 8: Kiểm tra notification mới nhất sau khi Doctor lưu kết quả khám
      + get_latest_notification_by_type_and_keyword()

    TC-NOTIFICATION-005
    - Kiểm tra notification theo appointment ID
      + has_notification_by_appointment_id()

    - Lấy toàn bộ nội dung notification hiện có
      + get_all_notification_contents()
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

    # TC-NOTIFICATION-001 - Step 5
    # Mở trang Thông báo.
    def open_page(self):
        self.open(self.URL)

    # TC-NOTIFICATION-001 - Step 5
    # Lấy tiêu đề trang Thông báo.
    def get_page_title(self):
        return self.find(*self.PAGE_TITLE).text.strip()

    # TC-NOTIFICATION-001 - Step 6
    # Tìm đúng notification theo appointment ID.
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

    # TC-NOTIFICATION-001 - Step 7
    # Lấy loại notification.
    def get_notification_type(self, notification):
        return notification.find_element(
            *self.NOTIFICATION_TYPE
        ).text.strip()

    # TC-NOTIFICATION-001 - Step 7
    # Lấy nội dung notification.
    def get_notification_content(self, notification):
        return notification.find_element(
            *self.NOTIFICATION_CONTENT
        ).text.strip()

    # TC-NOTIFICATION-001 - Step 7
    # Lấy thời gian notification.
    def get_notification_time(self, notification):
        return notification.find_element(
            *self.NOTIFICATION_TIME
        ).text.strip()

    # Helper: Chuẩn hóa text để phục vụ kiểm tra nội dung notification.
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

    # TC-NOTIFICATION-003 - Step 8
    # Kiểm tra notification mới nhất theo type và keyword.
    def get_latest_notification_by_type_and_keyword(
            self,
            expected_type,
            expected_keyword):

        notifications = self.finds(
            *self.NOTIFICATION_ITEMS
        )

        if not notifications:
            raise AssertionError(
                "Patient không có notification nào."
            )

        normalized_expected = self.normalize_text(
            expected_keyword
        )

        for notification in notifications:
            try:
                notification_type = notification.find_element(
                    *self.NOTIFICATION_TYPE
                ).text.strip()

                notification_content = notification.find_element(
                    *self.NOTIFICATION_CONTENT
                ).text.strip()

            except NoSuchElementException:
                continue

            normalized_content = self.normalize_text(
                notification_content
            )

            if (
                    notification_type == expected_type
                    and normalized_expected in normalized_content
            ):
                return notification

        return None

    # TC-NOTIFICATION-005
    # Kiểm tra có tồn tại notification theo appointment ID hay không.
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

    # TC-NOTIFICATION-005
    # Lấy toàn bộ nội dung notification đang hiển thị.
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
