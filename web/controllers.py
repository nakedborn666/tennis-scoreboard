from http import HTTPStatus

from services.match_service import MatchService

from web.response import Response
from web.templating import render_template



def main_page_controller(request, session):
    main_page = render_template("index.html")
    return Response.html_helper(main_page)


def new_match_get_controller(request, session):

    new_match_page = render_template("new-match.html")
    return Response.html_helper(new_match_page)



def new_match_post_controller(request, session):
    service = MatchService(session)
    p1, p2 = request.form["player1_name"], request.form["player2_name"]
    match = service.create_match(p1, p2)
    return Response.redirect(f"/match-score?uuid={match.uuid}")


def match_score_controller(request, session):
    service = MatchService(session)
    uuid = request.form["uuid"]
    return service.get_match_score_by_uuid(uuid)


def matches_controller(request, session):
    service = MatchService(session)
    page, filter = request.query
    return service.ended_matches(page, filter)




