from __future__ import annotations

import urllib.error
import urllib.request
from urllib.parse import urlparse

from .models import FetchResult


class PublicGetClient:
    """Public HTTPS GET-only client. No live order/transaction write method exists."""

    def __init__(self, timeout: float = 8.0, max_bytes: int = 512_000):
        self.timeout = timeout
        self.max_bytes = max_bytes

    def get(self, url: str) -> FetchResult:
        if urlparse(url).scheme != "https":
            return FetchResult(url=url, ok=False, status_code=None, error="only_https_allowed")
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "airdrop-agent-engine/0.2 public-read-only"},
            method="GET",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read(self.max_bytes)
                charset = response.headers.get_content_charset() or "utf-8"
                code = int(response.status)
                return FetchResult(
                    url=url,
                    ok=200 <= code < 400,
                    status_code=code,
                    text=body.decode(charset, errors="replace"),
                )
        except urllib.error.HTTPError as exc:
            return FetchResult(url=url, ok=False, status_code=exc.code, error=f"http_{exc.code}")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            return FetchResult(url=url, ok=False, status_code=None, error=type(exc).__name__)

    def fetch(self, url: str) -> FetchResult:
        """Legacy v0.1 alias for old PreflightEvaluator tests/callers."""
        return self.get(url)


UrlReader = PublicGetClient
