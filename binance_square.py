from __future__ import annotations

import os
import requests


ENDPOINT = "https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add"


class BinanceSquareError(RuntimeError):
    pass


def publish_text(text: str) -> tuple[str | None, str | None]:
    api_key = os.getenv("BINANCE_SQUARE_OPENAPI_KEY")
    if not api_key:
        raise BinanceSquareError("Missing BINANCE_SQUARE_OPENAPI_KEY")

    headers = {
        "X-Square-OpenAPI-Key": api_key,
        "Content-Type": "application/json",
        "clienttype": "binanceSkill",
    }
    payload = {"bodyTextOnly": text}

    try:
        response = requests.post(
            ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30,
        )
    except requests.RequestException as exc:
        raise BinanceSquareError(f"Network error: {exc}") from exc

    # Binance may return useful JSON even on non-2xx.
    try:
        data = response.json()
    except ValueError:
        raise BinanceSquareError(
            f"HTTP {response.status_code}: non-JSON response"
        )

    code = str(data.get("code", ""))
    message = data.get("message")

    if code != "000000":
        raise BinanceSquareError(
            f"Binance Square API error code={code}, message={message}"
        )

    content_id = ((data.get("data") or {}).get("id"))
    link = (
        f"https://www.binance.com/square/post/{content_id}"
        if content_id
        else None
    )
    return content_id, link
