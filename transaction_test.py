
from models.player import PlayerModel
from database import session_local

from services.player_service import PlayerService
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError





if __name__ == "__main__":
    with session_local() as session:
        player_service_obj = PlayerService(session)
        new_player = player_service_obj.get_or_create_player("ляля")
        session.commit()

        next_player = PlayerModel(name="ляля")
        try:
            session.add(next_player)
            session.commit()
        except IntegrityError as error:
            print(type(error).__name__, error)
            try:
                stmt = select(PlayerModel.name)
                players_name = session.scalars(stmt).all()
                print(players_name)
            except Exception as e:
                print(type(e).__name__, e)

            session.rollback()
            stmt = select(PlayerModel.name)
            players_name = session.scalars(stmt).all()
            print(players_name)

    with session_local() as session:
        new_playa = PlayerModel(name="голый666")
        session.add(new_playa)
        session.flush()


    with session_local() as session:
        find_playa = select(PlayerModel).where(PlayerModel.name == "голый666")
        found = session.scalar(find_playa)
        print(found)
