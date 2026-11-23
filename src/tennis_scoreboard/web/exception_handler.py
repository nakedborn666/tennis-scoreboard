import logging

from tennis_scoreboard.exceptions.exceptions import (
    BadRequestError,
    MatchAlreadyEndedError,
    MatchDoesntExistsError,
    MethodDismatchToPathError,
    MatchUuidDoesntExistError,
    PageShouldBeNumberError,
    RouteDoesntExistsError,
)
from tennis_scoreboard.web.response import Response
from tennis_scoreboard.web.templating import render_template
from http import HTTPStatus

logger = logging.getLogger(__name__)


_HTTP_EXCEPTIONS = {
    BadRequestError: ("Некорректный запрос", HTTPStatus.BAD_REQUEST),
    RouteDoesntExistsError: ("Страница не найдена", HTTPStatus.NOT_FOUND),
    MethodDismatchToPathError: ("Метод не поддерживается", HTTPStatus.METHOD_NOT_ALLOWED),
    MatchUuidDoesntExistError: ("UUID матча не передан", HTTPStatus.BAD_REQUEST),
    MatchDoesntExistsError: ("Матч не найден", HTTPStatus.NOT_FOUND),
    PageShouldBeNumberError: ("Номер страницы должен быть положительным числом", HTTPStatus.BAD_REQUEST),
    MatchAlreadyEndedError: ("Матч уже завершён", HTTPStatus.CONFLICT),
}

def error_response(error):
    response_spec = _HTTP_EXCEPTIONS.get(type(error))
    if response_spec is not None:
        message, code = response_spec
        return Response.html_helper(render_template("error.html", message=message), code)
    else:
        logger.exception("Необработанная ошибка: %s", type(error).__name__)
        message = "Ошибка сервера"
        return Response.html_helper(render_template("error.html", message=message), HTTPStatus.INTERNAL_SERVER_ERROR)
