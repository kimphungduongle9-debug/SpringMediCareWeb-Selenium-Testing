from selenium.webdriver.support.ui import WebDriverWait

from pages.LoginPage import LoginPage


HOME_URL = "http://localhost:3000/"
LOGIN_URL = "http://localhost:3000/login"


def login_doctor(driver, username, password):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login(username, password)

    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == HOME_URL
    )

    assert driver.current_url == HOME_URL, (
        "LOGIN FAILED | "
        f"Expected: {HOME_URL} | Actual: {driver.current_url}"
    )


def logout_current_user(driver):
    login_page = LoginPage(driver)
    login_page.logout()

    WebDriverWait(driver, 10).until(
        lambda d: "/login" in d.current_url
    )

    assert "/login" in driver.current_url, (
        "LOGOUT FAILED | "
        f"Expected URL chứa /login | Actual: {driver.current_url}"
    )