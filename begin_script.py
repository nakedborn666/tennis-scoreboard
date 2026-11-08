
from database import session_local, engine
from services.match_service import MatchService

from sqlalchemy import inspect





if __name__ == "__main__":
    with session_local() as session:
        match_service_obj = MatchService(session)
        match = match_service_obj.create_match("броуди", "чувак")
        uuid = match.uuid
        while match.winner_id is None:
            match_service_obj.add_point(uuid, 1)
        session.commit()
        score = match.score
        winner = match.winner_id
        ended_matches_list = match_service_obj.ended_matches(0)
        ended_match_with_filter_and_page = match_service_obj.ended_matches(1, "броуди")
        print(uuid)
        print(score)
        print(winner)
        print("ended_matches:", ended_matches_list)
        print("ended_matches_with_filter_and_page", ended_match_with_filter_and_page)


        session.commit()


    with session_local() as session:
        match_service_obj = MatchService(session)
        match = match_service_obj.get_match_by_uuid(uuid)
        print(match.score)


        session.commit()


inspector = inspect(engine)
print(inspector.get_table_names())