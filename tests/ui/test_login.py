"""UI tests for the SauceDemo login flow.

Demonstrates: Page Object Model, parametrized negative testing,
Allure step reporting, and Playwright's auto-waiting assertions.
"""
import allure
import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"


@allure.epic("SauceDemo")
@allure.feature("Authentication")
class TestLogin:

    @allure.title("Standard user can log in and lands on the inventory page")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login(self, page):
        """
        As a standard user, when I enter valid credentials and click Login,
        the inventory page should be displayed.
        """
        with allure.step("Open login page"):
            login_page = LoginPage(page).open()

        with allure.step("Log in with a valid standard user"):
            login_page.login(VALID_USER, VALID_PASSWORD)

        with allure.step("Verify inventory page is loaded"):
            inventory_page = InventoryPage(page)
            assert inventory_page.is_loaded(), "Inventory list did not load after login"

    @allure.title("Locked-out user sees an explicit error message")
    @allure.severity(allure.severity_level.NORMAL)
    def test_locked_out_user(self, page):
        """
        A locked-out user should be blocked from logging in and receive
        an error message mentioning the account is locked out.
        """
        with allure.step("Attempt login with a locked-out account"):
            login_page = LoginPage(page).open()
            login_page.login("locked_out_user", VALID_PASSWORD)

        with allure.step("Verify a locked-out error is shown"):
            assert login_page.has_error()
            assert "locked out" in login_page.error_text().lower()

    @allure.title("Invalid credentials are rejected: {username}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "username,password",
        [
            ("standard_user", "wrong_password"),
            ("not_a_real_user", "secret_sauce"),
            ("", ""),
        ],
    )
    def test_invalid_login_is_rejected(self, page, username, password):
        """
        Invalid credentials (wrong password, non-existent user, or empty
        fields) must always be rejected with an error message.
        """
        with allure.step(f"Attempt login with username='{username}'"):
            login_page = LoginPage(page).open()
            login_page.login(username, password)

        with allure.step("Verify an error message is displayed"):
            assert login_page.has_error(), "Expected an error for invalid credentials"
