import pytest

from tennis_scoreboard.exceptions.exceptions import (
    MethodDismatchToPathError,
    RouteDoesntExistsError,
)
from tennis_scoreboard.web.request import Request
from tennis_scoreboard.web.static import serve_static


def _request(method: str, path: str) -> Request:
    return Request(method=method, path=path, query={}, form={}, headers={})


def test_serve_css():
    response = serve_static(_request("GET", "/static/css/style.css"))

    assert response.status.value == 200
    assert ("Content-Type", "text/css; charset=utf-8") in response.headers
    assert response.body


@pytest.mark.parametrize(
    "path",
    [
        "/static/missing.css",
        "/static/../config.py",
    ],
)
def test_missing_or_unsafe_static_path(path):
    with pytest.raises(RouteDoesntExistsError):
        serve_static(_request("GET", path))


def test_static_post_is_not_allowed():
    with pytest.raises(MethodDismatchToPathError):
        serve_static(_request("POST", "/static/css/style.css"))
