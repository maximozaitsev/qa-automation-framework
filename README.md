# QA Automation Framework — Python · Pytest · Playwright · Allure

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Playwright](https://img.shields.io/badge/Playwright-UI%20Testing-green)
![Pytest](https://img.shields.io/badge/Pytest-Test%20Runner-yellow)
![Allure](https://img.shields.io/badge/Allure-Reporting-orange)
![CI](https://github.com/maximozaitsev/qa-automation-framework/actions/workflows/tests.yml/badge.svg)

A small, production-style test automation framework demonstrating the same
approach I use professionally: **Page Object Model** for UI, a thin **API
client** for backend testing, **Allure** for reporting, and a **CI pipeline**
that runs on every push.

This is a personal portfolio project. It tests two public demo services —
[SauceDemo](https://www.saucedemo.com) (UI) and [ReqRes](https://reqres.in)
(API) — so anyone can clone it and run it immediately, with no internal
credentials or NDA-covered code involved.

## Why this exists

Most of my day-to-day automation work lives in private company repos
(fintech / Web3 products under NDA). This project shows the same patterns —
structure, naming, reporting, CI — outside of any confidentiality constraints,
so it's easy for anyone to review.

## What it covers

- **UI tests** (`tests/ui`) — login flow (valid / invalid / locked-out users)
  and cart flow (add / remove items, badge count assertions), built on a
  Page Object Model (`pages/`).
- **API tests** (`tests/api`) — full CRUD coverage (GET / POST / PUT / DELETE)
  against a REST API, with status code and response-schema assertions.
- **Allure reporting** — every test step is wrapped in `allure.step(...)` so
  failures are readable at a glance, not just a stack trace.
- **CI** — GitHub Actions runs the full suite on every push and uploads
  Allure results as a build artifact.

## Project structure

```
qa-automation-framework/
├── pages/                  # Page Object Model
│   ├── base_page.py        # shared low-level Playwright helpers
│   ├── login_page.py
│   └── inventory_page.py
├── tests/
│   ├── ui/                 # Playwright UI tests
│   └── api/                # requests-based API tests
├── utils/
│   └── api_client.py       # thin wrapper over requests.Session
├── .github/workflows/tests.yml
├── conftest.py
├── pytest.ini
└── requirements.txt
```

## Running it locally

```bash
git clone https://github.com/maximozaitsev/qa-automation-framework.git
cd qa-automation-framework

# Python 3.12 is required — pinned Playwright 1.47 / pytest-playwright 0.5.2
python3.12 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

# Run everything
pytest

# Run only UI or only API tests
pytest tests/ui
pytest tests/api

# Run with Allure reporting
pytest --alluredir=allure-results
allure serve allure-results
```

## Design decisions worth noting

- **Page Object Model** keeps selectors and page logic out of test files —
  tests read like user stories, not CSS-selector soup.
- **`ApiClient`** is deliberately generic (base URL + verbs) so it can be
  pointed at any REST API by changing one constant — this is the same shape
  I use for real internal API suites.
- **Parametrized negative testing** (`test_login.py`) covers multiple invalid
  states with a single, readable test rather than copy-pasted variants.
- **CI runs on every push**, matching how I set up automation in production —
  a suite nobody runs isn't worth writing.

## About me

QA / Automation Engineer, 4+ years, specializing in Web3/DeFi products.
Built this framework's professional counterpart from scratch at my current
role, cutting regression testing time 6x and reaching 80% coverage on
critical flows.

- 📫 [t.me/mazajca](https://t.me/mazajca)
- ✉️ maximozaitsev@gmail.com
