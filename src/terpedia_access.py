"""Small optional client for authenticated Terpedia Knowledge API searches."""
from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_API_URL = "https://terpedia-knowledge-nanrsdlaoa-uc.a.run.app"

def search_tabular(query: str, *, source: str | None = None, limit: int = 8, timeout: float = 45.0) -> dict:
    """Search Terpedia's tabular Knowledge API; requires env-configured credentials.

    The API key is sent in the ``x-knowledge-key`` header and is never printed.
    """
    key = os.environ.get("TERPEDIA_KNOWLEDGE_API_KEY")
    if not key:
        raise RuntimeError("Set TERPEDIA_KNOWLEDGE_API_KEY in your local or hosted secret store.")
    base = os.environ.get("TERPEDIA_KB_API_URL", DEFAULT_API_URL).rstrip("/")
    payload = {"query": query, "limit": max(1, min(int(limit), 20))}
    if source:
        payload["source"] = source
    request = Request(
        f"{base}/v1/tabular/search",
        data=json.dumps(payload).encode("utf-8"),
        headers={"content-type": "application/json", "x-knowledge-key": key},
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"Terpedia Knowledge API returned HTTP {exc.code}.") from None
    except URLError as exc:
        raise RuntimeError(f"Terpedia Knowledge API request failed: {exc.reason}.") from None
