from database import session_local
from web.request import Request
from web.router import Router
from web.controllers import *
from web.response import Response
from exceptions.exceptions import BadRequestError, RouteDoesntExistsError, MethodDismatchToPathError
from http import HTTPStatus
from web.exception_handler import error_response
router = Router()

router.register_route("GET", "/", main_page_controller)
router.register_route("GET", "/new-match", new_match_get_controller)
router.register_route("POST", "/new-match", new_match_post_controller)


def application(environ, start_response):
    with session_local() as session:
        try:
            request = Request.from_environ(environ)
            controller = router.find_controller(request.method, request.path)
            response = controller(request, session)
            session.commit()
        except Exception as error:
            response = error_response(error)
        status = f'{response.status.value} {response.status.phrase}'
        start_response(status, response.headers)
        return [response.body]





