"""Thin wrapper around requests.Session so tests read like business logic,
not raw HTTP calls — swap base_url to point this framework at any REST API.
"""
from __future__ import annotations

import requests


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.session.get(f"{self.base_url}{path}", **kwargs)
        return self.session.post(f"{self.base_url}{path}", json=json, **kwargs)

    def put(self, path: str, json: dict, **kwargs) -> requests.Response:
        return self.session.put(f"{self.base_url}{path}", json=json, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.session.delete(f"{self.base_url}{path}", **kwargs)
