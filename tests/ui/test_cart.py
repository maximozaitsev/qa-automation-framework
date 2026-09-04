"""UI tests for the SauceDemo cart flow — demonstrates a multi-page-object
flow (login -> inventory -> cart) and state assertions via the cart badge.
"""
import allure

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"
BACKPACK = "sauce-labs-backpack"
BIKE_LIGHT = "sauce-labs-bike-light"


def _login(page) -> InventoryPage:
    LoginPage(page).open().login(VALID_USER, VALID_PASSWORD)
    return InventoryPage(page)


@allure.epic("SauceDemo")
@allure.feature("Cart")
class TestCart:

    @allure.title("Adding an item updates the cart badge count")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_item_updates_badge(self, page):
        inventory = _login(page)

        with allure.step("Cart starts empty"):
            assert inventory.cart_count() == 0

        with allure.step(f"Add '{BACKPACK}' to the cart"):
            inventory.add_item_to_cart(BACKPACK)

        with allure.step("Cart badge shows 1 item"):
            assert inventory.cart_count() == 1

    @allure.title("Adding two items and removing one leaves the correct count")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_and_remove_items(self, page):
        inventory = _login(page)

        with allure.step("Add two different items"):
            inventory.add_item_to_cart(BACKPACK)
            inventory.add_item_to_cart(BIKE_LIGHT)
            assert inventory.cart_count() == 2

        with allure.step("Remove one item"):
            inventory.remove_item_from_cart(BACKPACK)

        with allure.step("Cart badge reflects the remaining item"):
            assert inventory.cart_count() == 1
