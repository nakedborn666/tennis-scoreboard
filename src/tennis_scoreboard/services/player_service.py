from sqlalchemy import select
from tennis_scoreboard.models.player import PlayerModel

class PlayerService:
    def __init__(self, session):
        self.session = session

    def get_or_create_player(self, name):
        new_player = PlayerModel(name=name)
        player = self.get_player_by_name(name)
        if player:
            return player

        self.session.add(new_player)
        self.session.flush()
        return new_player


    def get_player_by_name(self, name):
        stmt = select(PlayerModel).where(PlayerModel.name == name)
        player = self.session.scalar(stmt)
        return player


    def get_player_name_by_id(self, player_id):
        if player_id is None:
            return None
        player = self.session.get(PlayerModel, player_id)
        if player is None:
            return None
        return player.name


