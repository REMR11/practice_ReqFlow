from __future__ import annotations

from typing import Any

import pytest
import requests

from core.ai_proxy_client import AIProxyClient, AIProxyError


def test_client_is_unavailable_without_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AI_PROXY_URL", raising=False)
    monkeypatch.delenv("AI_PROXY_API_KEY", raising=False)

    client = AIProxyClient()
    assert client.is_available is False


def test_client_is_available_with_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_PROXY_URL", "https://proxy.example/v1")
    monkeypatch.setenv("AI_PROXY_API_KEY", "secret")

    client = AIProxyClient()
    assert client.is_available is True


def test_complete_returns_extracted_content(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, Any]:
            return {"choices": [{"message": {"content": "texto generado"}}]}

    def fake_post(url: str, headers: dict[str, str], json: dict[str, Any], timeout: float):
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = json
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(requests, "post", fake_post)

    client = AIProxyClient(
        proxy_url="https://proxy.example/v1",
        proxy_api_key="token",
        timeout=12.0,
    )
    output = client.complete("prompt", "mensaje", max_tokens=250)

    assert output == "texto generado"
    assert captured["url"] == "https://proxy.example/v1/chat"
    assert captured["headers"]["Authorization"] == "Bearer token"
    assert captured["json"]["messages"][0]["role"] == "system"
    assert captured["json"]["messages"][1]["role"] == "user"
    assert captured["json"]["max_tokens"] == 250
    assert captured["timeout"] == 12.0


def test_complete_raises_on_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeResponse:
        def raise_for_status(self) -> None:
            raise requests.HTTPError("boom")

    def fake_post(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(requests, "post", fake_post)

    client = AIProxyClient(proxy_url="https://proxy.example", proxy_api_key="token")

    with pytest.raises(AIProxyError):
        client.complete("prompt", "mensaje")


def test_complete_raises_on_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_post(*args, **kwargs):
        raise requests.Timeout("timeout")

    monkeypatch.setattr(requests, "post", fake_post)

    client = AIProxyClient(proxy_url="https://proxy.example", proxy_api_key="token")

    with pytest.raises(AIProxyError):
        client.complete("prompt", "mensaje")


def test_complete_raises_on_unexpected_response_shape(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, Any]:
            return {"foo": "bar"}

    def fake_post(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(requests, "post", fake_post)
    client = AIProxyClient(proxy_url="https://proxy.example", proxy_api_key="token")

    with pytest.raises(AIProxyError):
        client.complete("prompt", "mensaje")
