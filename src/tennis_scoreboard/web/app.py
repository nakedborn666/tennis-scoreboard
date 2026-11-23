from tennis_scoreboard.database import session_local
from tennis_scoreboard.web.request import Request
from tennis_scoreboard.web.router import Router
from tennis_scoreboard.web.controllers import *
from tennis_scoreboard.web.response import Response
from tennis_scoreboard.exceptions.exceptions import BadRequestError, RouteDoesntExistsError, MethodDismatchToPathError
from http import HTTPStatus
from tennis_scoreboard.web.exception_handler import error_response
router = Router()

router.register_route("GET", "/", main_page_controller)
router.register_route("GET", "/new-match", new_match_get_controller)
router.register_route("GET", "/match-score", match_score_get_controller)
router.register_route("GET", "/matches", matches_controller)
router.register_route("POST", "/match-score", match_score_post_controller)
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





