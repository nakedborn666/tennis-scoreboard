from pathlib import Path

from tennis_scoreboard.exceptions.exceptions import (
    MethodDismatchToPathError,
    RouteDoesntExistsError,
)
from tennis_scoreboard.web.request import Request
from tennis_scoreboard.web.response import Response


STATIC_DIR = (Path(__file__).resolve().parent.parent / "static").resolve()

_CONTENT_TYPES = {
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
}


def serve_static(request: Request) -> Response:
    if request.method != "GET":
        raise MethodDismatchToPathError

    relative_path = request.path.removeprefix("/static/")
    if not relative_path:
        raise RouteDoesntExistsError

    file_path = (STATIC_DIR / relative_path).resolve()

    try:
        file_path.relative_to(STATIC_DIR)
    except ValueError:
        raise RouteDoesntExistsError

    if not file_path.is_file():
        raise RouteDoesntExistsError

    content_type = _CONTENT_TYPES.get(file_path.suffix.lower(), "application/octet-stream")
    return Response.bytes_helper(file_path.read_bytes(), content_type)
