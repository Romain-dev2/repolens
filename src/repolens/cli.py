from __future__ import annotations

import argparse
import sys
from collections import Counter

from repolens.client.rest import GitHubClient
from repolens.exceptions import NotFoundError, RateLimitError, RepoLensError
from repolens.models.user import Repository, User


def format_profile(user: User, repos: list[Repository]) -> str:
    """Build a text summary of a profile (pure function, easy to test)."""
    own = [r for r in repos if not r.fork]
    languages = Counter(r.language for r in own if r.language)
    total = sum(languages.values())

    lines = [
        f"{user.name or user.login} (@{user.login})",
        f"Public repositories: {user.public_repos} | Followers: {user.followers}",
        f"Stars received (own repositories): {sum(r.stars for r in own)}",
    ]
    if total:
        lines.append("Top languages:")
        for language, count in languages.most_common(5):
            lines.append(f"  {language:<15} {count / total:>4.0%}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repolens", description="Analyze GitHub profiles and repositories."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    profile = sub.add_parser("profile", help="Show a summary of a GitHub profile")
    profile.add_argument("username", help="GitHub username")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    client = GitHubClient()
    try:
        user = client.get_user(args.username)
        repos = client.get_repositories(args.username)
    except NotFoundError:
        print(f"Error: user '{args.username}' not found.", file=sys.stderr)
        return 1
    except RateLimitError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except RepoLensError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(format_profile(user, repos))
    return 0