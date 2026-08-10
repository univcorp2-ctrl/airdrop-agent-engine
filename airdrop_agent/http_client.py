from __future__ import annotations

import html
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .models import FetchResult

_TAG_RE = re.compile(r"<[^>]+>")
_SPACE_RE = re.compile(r"\s+")


class UrlReader:
    def __init__(self, timeout: float = 15.0) -> None:
        self.timeout = timeout

    def fetch(self, url: str) -> FetchResult:
        req = Request(
            url,
            headers={
                "User-Agent": "airdrop-agent-engine/0.1 (+read-only preflight)",
                "Accept": "text/html,application/json,text/plain;q=0.9,*/*;q=0.8",
            },
        )
        try:
            with urlopen(req, timeout=self.timeout) as response:
                raw = response.read(2_000_000)
                charset = response.headers.get_content_charset() or "utf-8"
                text = raw.decode(charset, errors="replace")
                cleaned = self._normalize(text)
                return FetchResult(url, True, response.status, cleaned)
        except HTTPError as exc:
            return FetchResult(url, False, exc.code, error=f"HTTPError: {exc.reason}")
        except URLError as exc:
            return FetchResult(url, False, None, error=f"URLError: {exc.reason}")
        except Exception as exc:  # defensive: the runner must fail closed
            return FetchResult(url, False, None, error=f"{type(exc).__name__}: {exc}")

    @staticmethod
    def _normalize(text: str) -> str:
        text = _TAG_RE.sub(" ", text)
        text = html.unescape(text)
        return _SPACE_RE.sub(" ", text).strip()
