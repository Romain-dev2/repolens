import httpx
import pytest
import respx

from repolens.client.rest import API_URL, GitHubClient
from repolens.exceptions import NotFoundError, RateLimitError


@pytest.fixture
def client():
    return GitHubClient(token="")  # pas de token, pas de réseau


@respx.mock
def test_get_user(client):
    respx.get(f"{API_URL}/users/octocat").mock(
        return_value=httpx.Response(
            200, json={"login": "octocat", "name": "The Octocat", "public_repos": 8, "followers": 10}
        )
    )
    user = client.get_user("octocat")
    assert user.login == "octocat"
    assert user.public_repos == 8


@respx.mock
def test_user_not_found(client):
    respx.get(f"{API_URL}/users/ghost").mock(return_value=httpx.Response(404))
    with pytest.raises(NotFoundError):
        client.get_user("ghost")


@respx.mock
def test_rate_limit(client):
    respx.get(f"{API_URL}/users/octocat").mock(
        return_value=httpx.Response(
            403, headers={"x-ratelimit-remaining": "0", "x-ratelimit-reset": "1700000000"}
        )
    )
    with pytest.raises(RateLimitError) as exc:
        client.get_user("octocat")
    assert exc.value.reset_at == 1700000000


@respx.mock
def test_repositories_pagination(client):
    page1 = [{"name": f"r{i}", "language": "Python", "stargazers_count": 1} for i in range(100)]
    page2 = [{"name": "last", "language": None, "stargazers_count": 0}]
    route = respx.get(f"{API_URL}/users/octocat/repos")
    route.side_effect = [httpx.Response(200, json=page1), httpx.Response(200, json=page2)]
    repos = client.get_repositories("octocat")
    assert len(repos) == 101
    assert repos[-1].name == "last"