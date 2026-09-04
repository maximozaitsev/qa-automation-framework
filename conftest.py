"""Root conftest — ensures the project root is on sys.path so that
`from pages...` / `from utils...` imports work regardless of where
pytest is invoked from, and centralizes any shared fixtures.
"""
import sys
from pathlib import Path

import allure
import pytest
from _pytest.python import Function

ROOT_DIR = Path(__file__).parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# Attach all Allure-relevant pytest markers as dynamic tags so they show up
# in the report without each test having to call allure.dynamic.tag(...).
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_setup(item: Function) -> None:
    for marker in item.iter_markers():
        allure.dynamic.tag(marker.name)
    yield


# On UI test failures, attach a full-page screenshot so failures are
# immediately actionable from the Allure report.
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Function, call) -> None:
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page is not None and hasattr(page, "screenshot"):
            allure.attach(
                page.screenshot(full_page=True),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )
