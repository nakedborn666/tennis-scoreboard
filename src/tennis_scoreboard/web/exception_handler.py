import logging

from tennis_scoreboard.exceptions.exceptions import BadRequestError, RouteDoesntExistsError, MethodDismatchToPathError, MatchUuidDoesntExistError, MatchDoesntExistsError, PageShouldBeNumberError, MatchAlreadyEndedError
from tennis_scoreboard.web.response import Response
from http import HTTPStatus

logger = logging.getLogger(__name__)


_HTTP_EXCEPTIONS = {
    BadRequestError: ("<h1>Некорректный запрос</h1>", HTTPStatus.BAD_REQUEST),
    RouteDoesntExistsError: ("<h1>Страница не найдена</h1>", HTTPStatus.NOT_FOUND),
    MethodDismatchToPathError: ("<h1>Метод не поддерживается</h1>", HTTPStatus.METHOD_NOT_ALLOWED),
    MatchUuidDoesntExistError: ("<h1>Uuid матча не передан</h1>", HTTPStatus.BAD_REQUEST),
    MatchDoesntExistsError: ("<h1>Матч не найден</h1>", HTTPStatus.NOT_FOUND),
    PageShouldBeNumberError: ("<h1>Номер страницы должен быть положительным числом</h1>", HTTPStatus.BAD_REQUEST),
    MatchAlreadyEndedError: ("<h1>Матч уже завершен</h1>", HTTPStatus.CONFLICT)
    }

def error_response(error):
    if type(error) in _HTTP_EXCEPTIONS:
        message, code = _HTTP_EXCEPTIONS[type(error)]
        return Response.html_helper(message, code)
    else:
        logger.exception("Необработанная ошибка: %s", type(error).__name__)
        return Response.html_helper("<h1>Ошибка сервера</h1>", HTTPStatus.INTERNAL_SERVER_ERROR)
