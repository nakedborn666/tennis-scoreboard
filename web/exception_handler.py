import logging

from exceptions.exceptions import BadRequestError, RouteDoesntExistsError, MethodDismatchToPathError
from web.response import Response
from http import HTTPStatus

logger = logging.getLogger(__name__)

def error_response(error):
    if isinstance(error, BadRequestError):
        return Response.html_helper("<h1>Некорректный запрос</h1>", HTTPStatus.BAD_REQUEST)
    elif isinstance(error, RouteDoesntExistsError):
        return Response.html_helper("<h1>Страница не найдена</h1>", HTTPStatus.NOT_FOUND)
    elif isinstance(error, MethodDismatchToPathError):
        return Response.html_helper("<h1>Метод не поддерживается</h1>", HTTPStatus.METHOD_NOT_ALLOWED)
    else:
        logger.exception("Необработанная ошибка: %s", type(error).__name__)
        return Response.html_helper("<h1>Ошибка сервера</h1>", HTTPStatus.INTERNAL_SERVER_ERROR)

