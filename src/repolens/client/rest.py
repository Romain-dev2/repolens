from __future__ import annotations

import httpx

from repolens.config import get_token
from repolens.exceptions import NotFoundError, RateLimitError, RepoLensError
from repolens.models.user import Repository, User

API_URL = "https://api.github.com"
PER_PAGE = 100


class GitHubClient:
    def __init__(self, token: str | None = None, base_url: str = API_URL):
        token = token if token is not None else get_token()
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "repolens",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self._http = httpx.Client(base_url=base_url, headers=headers, timeout=10.0)

    def _get(self, path: str, params: dict | None = None) -> httpx.Response:
        try:
            response = self._http.get(path, params=params)
        except httpx.HTTPError as exc:
            raise RepoLensError(f"Network error: {exc}") from exc
        self._check(response, path)
        return response

    @staticmethod
    def _check(response: httpx.Response, path: str) -> None:
        if response.status_code == 404:
            raise NotFoundError(f"Not found: {path}")
        if response.status_code in (403, 429) and response.headers.get("x-ratelimit-remaining") == "0":
            reset = response.headers.get("x-ratelimit-reset")
            raise RateLimitError(int(reset) if reset else None)
        if response.is_error:
            raise RepoLensError(f"GitHub API error {response.status_code} on {path}")

    def get_user(self, username: str) -> User:
        return User.from_api(self._get(f"/users/{username}").json())

    def get_repositories(self, username: str) -> list[Repository]:
        repos: list[Repository] = []
        page = 1
        while True:
            data = self._get(
                f"/users/{username}/repos", params={"per_page": PER_PAGE, "page": page}
            ).json()
            repos.extend(Repository.from_api(item) for item in data)
            if len(data) < PER_PAGE:
                return repos
            page += 1