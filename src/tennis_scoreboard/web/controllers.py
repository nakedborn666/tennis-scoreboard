
from tennis_scoreboard.services.match_service import MatchService
from tennis_scoreboard.exceptions.exceptions import MatchUuidDoesntExistError, PageShouldBeNumberError, BadRequestError
from tennis_scoreboard.web.response import Response
from tennis_scoreboard.web.templating import render_template



def main_page_controller(request, session):
    main_page = render_template("index.html")
    return Response.html_helper(main_page)


def new_match_get_controller(request, session):
    new_match_page = render_template("new-match.html")
    return Response.html_helper(new_match_page)



def new_match_post_controller(request, session):
    service = MatchService(session)
    p1 = request.form.get("player1_name", "").strip() or None
    p2 = request.form.get("player2_name", "").strip() or None
    if not p1 or not p2:
        raise BadRequestError
    match = service.create_match(p1, p2)
    return Response.redirect(f"/match-score?uuid={match.uuid}")


def match_score_get_controller(request, session):
    service = MatchService(session)
    uuid = request.query.get("uuid")
    if not uuid:
        raise MatchUuidDoesntExistError
    match_score_dto = service.get_match_score_dto_by_uuid(uuid)
    match_score_page = render_template("match-score.html",  match_score=match_score_dto)
    return Response.html_helper(match_score_page)



def match_score_post_controller(request, session):
    service = MatchService(session)
    uuid = request.query.get("uuid")
    if not uuid:
        raise MatchUuidDoesntExistError
    player_number = request.form.get("player_number")
    if player_number not in ("1", "2"):
        raise BadRequestError
    player_number = int(player_number)
    service.add_point(uuid, player_number)
    return Response.redirect(f"/match-score?uuid={uuid}")



def matches_controller(request, session):
    service = MatchService(session)
    page = request.query.get("page", 1)
    try:
        page = int(page)
        if page < 1:
            raise PageShouldBeNumberError
    except (ValueError, TypeError):
        raise PageShouldBeNumberError
    filter_by_player_name = request.query.get("filter_by_player_name") or None
    matches_page = service.ended_matches(page, filter_by_player_name)
    matches = render_template("matches.html", matches_page=matches_page, filter_by_player_name=filter_by_player_name)
    return Response.html_helper(matches)










