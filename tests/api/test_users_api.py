"""API tests against https://reqres.in — a public mock REST API.

Demonstrates: positive & negative CRUD coverage, status code and schema
assertions, and Allure reporting for API-level tests.
"""
import allure
import pytest

from utils.api_client import ApiClient

BASE_URL = "https://reqres.in/api"


@pytest.fixture(scope="module")
def api():
    return ApiClient(BASE_URL)


@allure.epic("Public API")
@allure.feature("Users")
class TestUsersApi:

    @allure.title("GET single user returns 200 and the expected schema")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_single_user(self, api):
        """
        Fetching an existing user (id=2) should return HTTP 200 with a
        payload containing the required fields and a matching id.
        """
        with allure.step("Request user with id=2"):
            response = api.get("/users/2")

        with allure.step("Verify status code and response schema"):
            assert response.status_code == 200
            body = response.json()["data"]
            for field in ("id", "email", "first_name", "last_name"):
                assert field in body, f"Missing field '{field}' in response"
            assert body["id"] == 2

    @allure.title("GET user list returns 200 with pagination metadata")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_list(self, api):
        """
        Fetching page=2 of the user list should return HTTP 200, contain
        at least one user, and report pagination metadata consistent
        with the requested page.
        """
        with allure.step("Request the second page of users"):
            response = api.get("/users", params={"page": 2})

        with allure.step("Verify status code and list metadata"):
            assert response.status_code == 200
            body = response.json()
            assert body["page"] == 2
            assert len(body["data"]) > 0
            assert body["total_pages"] >= body["page"]

    @allure.title("GET a non-existent user returns 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_not_found(self, api):
        with allure.step("Request a user id that does not exist"):
            response = api.get("/users/9999")

        with allure.step("Verify 404 is returned"):
            assert response.status_code == 404

    @allure.title("POST creates a new user and returns 201 with an id")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user(self, api):
        payload = {"name": "Maksim Zaitsev", "job": "QA Automation Engineer"}

        with allure.step("Create a new user"):
            response = api.post("/users", json=payload)

        with allure.step("Verify 201 and echoed fields"):
            assert response.status_code == 201
            body = response.json()
            assert body["name"] == payload["name"]
            assert body["job"] == payload["job"]
            assert "id" in body and "createdAt" in body

    @allure.title("PUT updates an existing user and returns 200")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user(self, api):
        payload = {"name": "Maksim Zaitsev", "job": "Senior QA Engineer"}

        with allure.step("Update user id=2"):
            response = api.put("/users/2", json=payload)

        with allure.step("Verify 200 and updated field"):
            assert response.status_code == 200
            assert response.json()["job"] == "Senior QA Engineer"

    @allure.title("DELETE removes a user and returns 204")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user(self, api):
        with allure.step("Delete user id=2"):
            response = api.delete("/users/2")

        with allure.step("Verify 204 No Content"):
            assert response.status_code == 204

    @allure.title("[DEMO] Intentional failure to showcase Allure error reporting")
    @allure.severity(allure.severity_level.MINOR)
    def test_intentional_failure_demo(self, api):
        """Deliberately broken test kept on purpose — makes the Allure report
        demonstrate how failures are visualized (stack trace + step history).
        """
        with allure.step("Request a known endpoint"):
            response = api.get("/users/2")

        with allure.step("Failing assertion on purpose"):
            assert response.status_code == 418, "This test intentionally fails (expect 418)"
