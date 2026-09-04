"""Page Object for the SauceDemo login page (https://www.saucedemo.com)."""
from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage

URL = "https://www.saucedemo.com/"


class LoginPage(BasePage):
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self) -> "LoginPage":
        self.goto(URL)
        return self

    def login(self, username: str, password: str) -> None:
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def error_text(self) -> str:
        return self.text_of(self.ERROR_MESSAGE)

    def has_error(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE)
