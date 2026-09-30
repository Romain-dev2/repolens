from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    login: str
    name: str | None
    public_repos: int
    followers: int

    @classmethod
    def from_api(cls, data: dict) -> User:
        return cls(
            login=data["login"],
            name=data.get("name"),
            public_repos=data.get("public_repos", 0),
            followers=data.get("followers", 0),
        )


@dataclass(frozen=True)
class Repository:
    name: str
    language: str | None
    stars: int
    forks: int
    fork: bool

    @classmethod
    def from_api(cls, data: dict) -> Repository:
        return cls(
            name=data["name"],
            language=data.get("language"),
            stars=data.get("stargazers_count", 0),
            forks=data.get("forks_count", 0),
            fork=data.get("fork", False),
        )