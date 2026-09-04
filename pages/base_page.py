"""Base Page Object — shared helpers for all page objects.

Keeping common, low-level Playwright interactions here keeps individual
page objects focused on *what* they do, not *how* Playwright does it.
"""
from __future__ import annotations

from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str) -> None:
        self.page.goto(url)

    def click(self, selector: str) -> None:
        self.page.locator(selector).click()

    def fill(self, selector: str, text: str) -> None:
        self.page.locator(selector).fill(text)

    def text_of(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def expect_visible(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_visible()

    def expect_text(self, selector: str, text: str) -> None:
        expect(self.page.locator(selector)).to_contain_text(text)
