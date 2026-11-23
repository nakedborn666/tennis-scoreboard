from http import HTTPStatus
from dataclasses import dataclass

@dataclass
class Response:
    status: HTTPStatus
    headers: list[tuple[str, str]]
    body: bytes

    @classmethod
    def html_helper(cls, html, status=HTTPStatus.OK):
        body = html.encode("utf-8")
        headers = [("Content-Type", "text/html; charset=utf-8"),
                   ("Content-Length", str(len(body)))]

        return cls(status=status, headers=headers, body=body)


    @classmethod
    def bytes_helper(cls, body: bytes, content_type: str, status=HTTPStatus.OK):
        headers = [("Content-Type", content_type),
                   ("Content-Length", str(len(body))),
                   ("Cache-Control", "public, max-age=3600")]

        return cls(status=status, headers=headers, body=body)


    @classmethod
    def redirect(cls, location):
        return cls(status=HTTPStatus.SEE_OTHER,
                   headers=[("Location", location), ("Content-Length", "0")],
                   body=b"",
        )

