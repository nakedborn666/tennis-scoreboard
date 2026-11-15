import json
import math
from uuid import uuid4
from models.match import MatchModel
from models.player import PlayerModel
from sqlalchemy.orm import aliased
from sqlalchemy import select, or_, func
from domain.match import Match
from services.player_service import PlayerService
from domain.score_serializer import match_to_dict, match_from_dict
from exceptions.exceptions import MatchDoesntExistsError, MatchAlreadyEndedError
from dto.match_dto import MatchDTO, MatchesPageDTO


_PAGE_SIZE = 5

class MatchService:
    def __init__(self, session):
        self.session = session
        self.player_service_obj = PlayerService(self.session)

    def create_match(self, player1_name, player2_name):
        player1 = self.player_service_obj.get_or_create_player(player1_name)
        player2 = self.player_service_obj.get_or_create_player(player2_name)
        domain_match = Match()
        match_dict = match_to_dict(domain_match)
        match_json = json.dumps(match_dict)
        match_uuid = str(uuid4())
        match_model = MatchModel(uuid=match_uuid, player1_id=player1.id, player2_id=player2.id, winner_id=None, score=match_json)

        self.session.add(match_model)
        self.session.flush()
        return match_model


    def get_match_score_by_uuid(self, uuid):
        match = self.get_match_by_uuid(uuid)
        return match.score


    def get_match_by_uuid(self, uuid):
        stmt = select(MatchModel).where(MatchModel.uuid==uuid)
        match = self.session.scalar(stmt)
        return match


    def add_point(self, uuid, player_number):
        match = self.get_match_by_uuid(uuid)
        if match is None:
            raise MatchDoesntExistsError

        if match.winner_id is not None:
            raise MatchAlreadyEndedError

        score = json.loads(match.score)
        domain_match = match_from_dict(score)
        domain_match.won_point(player_number)

        winner = domain_match.winner()
        if winner is not None:
            match.winner_id = match.player1_id if winner == 1 else match.player2_id

        match_json = json.dumps(match_to_dict(domain_match))
        match.score = match_json
        self.session.flush()

        return match


    @staticmethod
    def _build_ended_matches_stmts(name_filter):
        p1 = aliased(PlayerModel)
        p2 = aliased(PlayerModel)

        stmt = (select(MatchModel, p1.name, p2.name)
                .join(p1, MatchModel.player1_id == p1.id)
                .join(p2, MatchModel.player2_id == p2.id)
                .where(MatchModel.winner_id.is_not(None))
                )

        count_stmt = (select(func.count(MatchModel.id))
                      .join(p1, MatchModel.player1_id == p1.id)
                      .join(p2, MatchModel.player2_id == p2.id)
                      .where(MatchModel.winner_id.is_not(None)))

        if name_filter:
            stmt = stmt.where(
                or_(p1.name == name_filter, p2.name == name_filter)
            )

            count_stmt = count_stmt.where(
                or_(p1.name == name_filter, p2.name == name_filter)
            )

        return stmt, count_stmt


    @staticmethod
    def _page_pagination_helper(stmt, page):
        return (stmt.order_by(MatchModel.id.desc())
                .limit(_PAGE_SIZE)
                .offset(_PAGE_SIZE * (page - 1))
                )


    @staticmethod
    def _page_counter(matches_count):
        return math.ceil(matches_count / _PAGE_SIZE)


    def ended_matches(self, page: int, filter_by_player_name:str | None = None) -> MatchesPageDTO:
        if page < 1:
            page = 1

        stmt, count_stmt = self._build_ended_matches_stmts(filter_by_player_name)
        stmt = self._page_pagination_helper(stmt, page)
        ended_matches = self.session.execute(stmt).all()
        total_matches = self.session.scalar(count_stmt)
        total_pages = self._page_counter(total_matches)

        if total_pages == 0 or total_pages < page:
            ended_matches = []

        page_dto = MatchesPageDTO(matches=self._ended_matches_to_dto(ended_matches), current_page=page, total_pages=total_pages)

        return page_dto


    @staticmethod
    def _ended_matches_to_dto(matches):
        dto_list = []
        for match in matches:
            match_obj, p1_name, p2_name = match
            score_dict = json.loads(match_obj.score)
            score = score_dict["ended_sets"]
            match_dto = MatchDTO(uuid=match_obj.uuid, player1_name=p1_name, player2_name=p2_name, winner_name=p1_name if match_obj.winner_id == match_obj.player1_id else p2_name, score=score)
            dto_list.append(match_dto)
        return dto_list






