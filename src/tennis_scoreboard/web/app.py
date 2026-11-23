from tennis_scoreboard.database import session_local
from tennis_scoreboard.web.request import Request
from tennis_scoreboard.web.router import Router
from tennis_scoreboard.web.controllers import *

from tennis_scoreboard.web.static import serve_static

from tennis_scoreboard.web.exception_handler import error_response
router = Router()

router.register_route("GET", "/", main_page_controller)
router.register_route("GET", "/new-match", new_match_get_controller)
router.register_route("GET", "/match-score", match_score_get_controller)
router.register_route("GET", "/matches", matches_controller)
router.register_route("POST", "/match-score", match_score_post_controller)
router.register_route("POST", "/new-match", new_match_post_controller)


def application(environ, start_response):
    try:
        request = Request.from_environ(environ)
        if request.path.startswith("/static/"):
            response = serve_static(request)
        else:
            with session_local() as session:
                controller = router.find_controller(request.method, request.path)
                response = controller(request, session)
                session.commit()
    except Exception as error:
        response = error_response(error)
    status = f'{response.status.value} {response.status.phrase}'
    start_response(status, response.headers)
    return [response.body]





