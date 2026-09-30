class RepoLensError(Exception):
    """Base error for RepoLens."""


class NotFoundError(RepoLensError):
    """The requested GitHub resource does not exist."""


class RateLimitError(RepoLensError):
    """The GitHub API rate limit has been reached."""

    def __init__(self, reset_at: int | None = None):
        self.reset_at = reset_at
        super().__init__("GitHub API rate limit exceeded. Set GITHUB_TOKEN to raise the limit.")