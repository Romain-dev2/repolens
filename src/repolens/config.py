import os


def get_token() -> str | None:
    """Return the GitHub token from the environment, if any."""
    return os.environ.get("GITHUB_TOKEN") or None