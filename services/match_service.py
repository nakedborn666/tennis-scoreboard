import json
from uuid import uuid4
from models.match import MatchModel
from models.player import PlayerModel
from sqlalchemy.orm import aliased
from sqlalchemy import select
from domain.match import Match
from services.player_service import PlayerService
from domain.score_serializer import match_to_dict, match_from_dict
from exceptions.exceptions import MatchDoesntExists, MatchAlreadyEnded
from dto.match_dto import MatchDTO


class MatchService:
    def __init__(self, session):
        self.session = session
        self.player_service_obj = PlayerService(self.session)

    def create_match(self, player1_name, player2_name):
        player1 = self.player_service_obj.get_or_create_player(player1_name)
        player2 = self.player_service_obj.get_or_create_player(player2_name)
        new_match_model = Match()
        match_dict = match_to_dict(new_match_model)
        match_json = json.dumps(match_dict)
        match_uuid = str(uuid4())
        match_obj = MatchModel(uuid=match_uuid, player1_id=player1.id, player2_id=player2.id, winner_id=None, score=match_json)

        self.session.add(match_obj)
        self.session.flush()
        return match_obj


    def get_match_by_uuid(self, uuid):
        stmt = select(MatchModel).where(MatchModel.uuid==uuid)
        match = self.session.scalar(stmt)
        return match


    def add_point(self, uuid, player_number):
        match = self.get_match_by_uuid(uuid)
        if match is None:
            raise MatchDoesntExists
        if match.winner_id is not None:
            raise MatchAlreadyEnded
        score = json.loads(match.score)
        domain_match = match_from_dict(score)
        domain_match.won_point(player_number)
        if domain_match.winner() is not None:
            match.winner_id = match.player1_id if domain_match.winner() == 1 else match.player2_id
        match_json = json.dumps(match_to_dict(domain_match))
        match.score = match_json
        self.session.flush()
        return match


    def ended_matches(self, page=1, filter_by_player_name=None):
        p1 = aliased(PlayerModel)
        p2 = aliased(PlayerModel)
        stmt = (select(MatchModel, p1.name, p2.name).where(MatchModel.winner_id.is_not(None))
                .join(p1, MatchModel.player1_id == p1.id)
                .join(p2, MatchModel.player2_id == p2.id))
        ended_matches = self.session.execute(stmt).all()
        return ended_matches


    def ended_matches_to_dto(self, matches):
        dto_list = []
        for match in matches:
            match_obj, p1_name, p2_name = match
            score_dict = json.loads(match_obj.score)
            score = score_dict["ended_sets"]
            match_dto = MatchDTO(uuid=match_obj.uuid, player1_name=p1_name, player2_name=p2_name, winner_name=p1_name if match_obj.winner_id == match_obj.player1_id else p2_name, score=score)
            dto_list.append(match_dto)
        return dto_list







