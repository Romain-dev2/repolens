import httpx
import respx

from repolens.cli import main
from repolens.client.rest import API_URL


@respx.mock
def test_profile_command(capsys, monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    respx.get(f"{API_URL}/users/octocat").mock(
        return_value=httpx.Response(
            200, json={"login": "octocat", "name": "The Octocat", "public_repos": 2, "followers": 5}
        )
    )
    respx.get(f"{API_URL}/users/octocat/repos").mock(
        return_value=httpx.Response(
            200,
            json=[
                {"name": "a", "language": "Python", "stargazers_count": 3, "fork": False},
                {"name": "b", "language": "Go", "stargazers_count": 1, "fork": True},
            ],
        )
    )
    assert main(["profile", "octocat"]) == 0
    out = capsys.readouterr().out
    assert "@octocat" in out
    assert "Python" in out
    assert "Go" not in out  # forks are excluded from the language stats


@respx.mock
def test_profile_unknown_user(capsys, monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    respx.get(f"{API_URL}/users/ghost").mock(return_value=httpx.Response(404))
    assert main(["profile", "ghost"]) == 1
    assert "not found" in capsys.readouterr().err