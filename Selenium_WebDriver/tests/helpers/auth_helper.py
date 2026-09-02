from selenium.webdriver.support.ui import WebDriverWait

from pages.LoginPage import LoginPage


HOME_URL = "http://localhost:3000/"


def login_user(driver, username, password):
    login_page = LoginPage(driver)

    login_page.open_page()
    login_page.login(
        username,
        password
    )

    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == HOME_URL
    )

    assert driver.current_url == HOME_URL, (
        "LOGIN FAILED | "
        f"Expected: {HOME_URL} | "
        f"Actual: {driver.current_url}"
    )