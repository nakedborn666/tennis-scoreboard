from tennis_scoreboard.web.request import Request
import io
from tennis_scoreboard.exceptions.exceptions import BadRequestError
import pytest

def test_from_request_get():
    environ = {"REQUEST_METHOD": "GET",
               "PATH_INFO": "/matches",
               "QUERY_STRING": "page=2&filter_by_player_name=vadya",
               "wsgi.input": io.BytesIO(b"")}
    request = Request.from_environ(environ)
    assert request.method == "GET"
    assert request.path == "/matches"
    assert request.query == {"page": "2",
                             "filter_by_player_name": "vadya"}
    assert request.form == {}


def test_from_request_post_with_not_valid_length():
    environ = {"REQUEST_METHOD": "POST",
               "PATH_INFO": "/matches",
               "QUERY_STRING": "page=2&filter_by_player_name=vadya",
               "CONTENT_TYPE": "application/x-www-form-urlencoded",
               "CONTENT_LENGTH": "qwe",
               "wsgi.input": io.BytesIO(b"")}


    with pytest.raises(BadRequestError):
       Request.get_form(environ)

def test_from_request_post_with_body():
    body = "player1=Иван&player2=Пётр".encode("utf-8")
    environ = {"REQUEST_METHOD": "POST",
               "PATH_INFO": "/matches",
               "QUERY_STRING": "",
               "CONTENT_TYPE": "application/x-www-form-urlencoded",
               "CONTENT_LENGTH": str(len(body)),
               "wsgi.input": io.BytesIO(body)}
    request = Request.from_environ(environ)
    assert request.form == {"player1": "Иван",
                            "player2": "Пётр"}
