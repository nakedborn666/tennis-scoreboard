from dataclasses import dataclass
from urllib.parse import parse_qs
from exceptions.exceptions import BadRequestError


@dataclass
class Request:
    method: str
    path: str
    query: dict
    form: dict
    headers: dict


    @classmethod
    def from_environ(cls, environ: dict) -> "Request":
        method = environ["REQUEST_METHOD"]
        path = environ["PATH_INFO"]
        query_string = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=True)
        query = {k: v[0] for k, v in query_string.items()}
        form = cls.get_form(environ)
        headers = {"CONTENT_TYPE": environ.get("CONTENT_TYPE"),
                   "CONTENT_LENGTH": environ.get("CONTENT_LENGTH")}
        return cls(method=method, path=path, query=query, form=form, headers=headers)


    @staticmethod
    def get_form(environ: dict) -> dict:
        if environ["REQUEST_METHOD"] == "POST" and "application/x-www-form-urlencoded" in environ.get("CONTENT_TYPE", ""):
            try:
                length = int(environ.get("CONTENT_LENGTH") or 0)
            except (TypeError, ValueError):
                raise BadRequestError
            if length < 0:
                raise BadRequestError
            elif length == 0:
                return {}
            try:
                body = parse_qs((environ["wsgi.input"].read(length).decode("utf-8")), keep_blank_values=True)
            except (TypeError, ValueError):
                raise BadRequestError
            return {k: v[0] for k, v in body.items()}
        return {}


