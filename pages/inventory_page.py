"""Page Object for the SauceDemo inventory / cart flow."""
from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_LIST = ".inventory_list"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"

    def __init__(self, page: Page):
        super().__init__(page)

    def is_loaded(self) -> bool:
        return self.is_visible(self.INVENTORY_LIST)

    def add_item_to_cart(self, item_slug: str) -> None:
        """item_slug example: 'sauce-labs-backpack' -> button id add-to-cart-sauce-labs-backpack"""
        self.click(f"#add-to-cart-{item_slug}")

    def remove_item_from_cart(self, item_slug: str) -> None:
        self.click(f"#remove-{item_slug}")

    def cart_count(self) -> int:
        if not self.is_visible(self.CART_BADGE):
            return 0
        return int(self.text_of(self.CART_BADGE))

    def open_cart(self) -> None:
        self.click(self.CART_LINK)
