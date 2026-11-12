from __future__ import annotations

import json
import os
from typing import Any

import httpx

DEFAULT_BASE_URL = "http://localhost:8000"


class GreenwheelsApiError(Exception):
    """Readable API failure for MCP tool consumers."""

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


def format_detail(detail: Any) -> str:
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list):
        parts = []
        for item in detail:
            if isinstance(item, dict) and "msg" in item:
                parts.append(str(item["msg"]))
            else:
                parts.append(str(item))
        return "; ".join(parts) if parts else "Request failed"
    if isinstance(detail, dict):
        if "detail" in detail:
            return format_detail(detail["detail"])
        return json.dumps(detail)
    return "Request failed"


class ApiClient:
    def __init__(
        self,
        base_url: str | None = None,
        *,
        http_client: httpx.Client | None = None,
    ) -> None:
        raw = base_url if base_url is not None else os.environ.get("GREENWHEELS_API_URL", DEFAULT_BASE_URL)
        self.base_url = raw.rstrip("/")
        self._http_client = http_client

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
    ) -> Any:
        path = path if path.startswith("/") else f"/{path}"
        url = f"{self.base_url}{path}"
        try:
            if self._http_client is not None:
                response = self._http_client.request(method, url, json=json_body)
            else:
                with httpx.Client(timeout=30.0) as client:
                    response = client.request(method, url, json=json_body)
        except httpx.RequestError as exc:
            raise GreenwheelsApiError(f"Cannot reach API at {self.base_url}: {exc}") from exc

        if response.status_code == 204:
            return {"status": "ok"}

        try:
            payload = response.json() if response.content else None
        except json.JSONDecodeError:
            payload = None

        if response.is_error:
            detail = payload.get("detail") if isinstance(payload, dict) else response.text
            message = format_detail(detail) if detail else response.reason_phrase
            raise GreenwheelsApiError(message, status_code=response.status_code)

        return payload

    def get(self, path: str) -> Any:
        return self.request("GET", path)

    def post(self, path: str, json_body: dict[str, Any] | None = None) -> Any:
        return self.request("POST", path, json_body=json_body)

    def patch(self, path: str, json_body: dict[str, Any]) -> Any:
        return self.request("PATCH", path, json_body=json_body)

    def delete(self, path: str) -> Any:
        return self.request("DELETE", path)
