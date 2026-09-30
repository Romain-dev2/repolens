# RepoLens

Python command-line tool that analyzes GitHub profiles and repositories using the official GitHub REST API.

![CI](https://github.com/Romain-dev2/repolens/actions/workflows/ci.yml/badge.svg)

## Description

RepoLens fetches public data about a GitHub user (profile, repositories, languages, stars) and summarizes it in the terminal. It was built as a personal project to practice clean Python architecture, API consumption (pagination, error handling, rate limits) and a pull-request-based workflow.

## Features

- Fetch a GitHub user profile (name, followers, number of public repositories)
- List all public repositories of a user, with automatic pagination
- Compute the language distribution and the total number of stars (forks are excluded)
- Clear error messages for unknown users, network errors and rate limits
- Works without authentication on public endpoints; optional token for higher limits
- Fully tested offline (no network access needed to run the test suite)

## Architecture

```
repolens/
├── src/repolens/
│   ├── cli.py            # command-line interface (argparse)
│   ├── config.py         # reads GITHUB_TOKEN from the environment
│   ├── exceptions.py     # RepoLensError, NotFoundError, RateLimitError
│   ├── client/
│   │   └── rest.py       # GitHub REST client (pagination, error handling)
│   └── models/
│       └── user.py       # User and Repository dataclasses
├── tests/                # pytest + respx (mocked HTTP)
└── .github/workflows/    # CI: ruff + pytest
```

The code is split in layers: the **client** handles network I/O, the **models** are typed data objects, and the **CLI** formats results. Formatting is a pure function (`format_profile`), which makes it easy to test.

## Technologies

- Python 3.10+
- [httpx](https://www.python-httpx.org/) for HTTP requests
- [pytest](https://pytest.org/) and [respx](https://lundberg.github.io/respx/) for tests
- [ruff](https://docs.astral.sh/ruff/) for linting
- GitHub Actions for continuous integration

## GitHub API

RepoLens uses the official [GitHub REST API](https://docs.github.com/en/rest). It currently calls:

- `GET /users/{username}`
- `GET /users/{username}/repos` (paginated, 100 items per page)

Without a token, GitHub applies a low rate limit to unauthenticated requests. See the [official rate limit documentation](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api) for current values. RepoLens raises a dedicated `RateLimitError` when the limit is reached.

## Installation

```bash
git clone https://github.com/Romain-dev2/repolens.git
cd repolens
python -m venv .venv
```

Activate the virtual environment:

```powershell
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
source .venv/bin/activate
```

Then install the dependencies and the package:

```bash
pip install -r requirements.txt
pip install -e .
```

## Configuration

A token is optional. To use one, set the `GITHUB_TOKEN` environment variable. The token is never stored in the code or in the repository.

```powershell
# Windows (PowerShell), current session only
$env:GITHUB_TOKEN = "your_token_here"
```

```bash
# Linux / macOS
export GITHUB_TOKEN="your_token_here"
```

## Usage

```bash
repolens profile <username>
# or
python -m repolens profile <username>
```

Example of output format (values depend on the user):

```
Name (@username)
Public repositories: 12 | Followers: 34
Stars received (own repositories): 5
Top languages:
  Python           60%
  JavaScript       30%
  HTML             10%
```

Exit codes: `0` on success, `1` for a missing user or an API error, `2` when the rate limit is reached.

## Tests

```bash
pytest
ruff check .
```

All tests use recorded or mocked responses and do not require network access. The same checks run automatically on every pull request through GitHub Actions.

## Roadmap

- [x] REST client with pagination and error handling
- [x] `profile` command
- [x] Continuous integration
- [ ] `--top N` and `--json` options for `profile`
- [ ] Repository analysis (activity, freshness, size)
- [ ] Issues and pull requests analytics
- [ ] Markdown and JSON reports
- [ ] ETag-based caching
- [ ] Repository comparison
- [ ] Optional GraphQL support for the contribution calendar (token required)

Progress is tracked in the [Issues](https://github.com/Romain-dev2/repolens/issues) tab.

## Contributing

Contributions are welcome.

1. Open or pick an issue (look for `good first issue`).
2. Create a branch: `feature/short-description` or `fix/short-description`.
3. Write code and tests, then run `pytest` and `ruff check .`.
4. Open a pull request that references the issue (`Closes #N`).
5. Address the review comments, then the PR is merged.

## License

Released under the [MIT License](LICENSE).

## Support

For bugs or questions, open an [issue](https://github.com/Romain-dev2/repolens/issues) or start a discussion in the [Discussions](https://github.com/Romain-dev2/repolens/discussions) tab.