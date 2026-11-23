from tennis_scoreboard.domain.match import Match


def match_to_dict(match_obj: Match) -> dict:
    sets = [match_obj.player1_sets, match_obj.player2_sets]
    current_set = match_obj.current_set_data
    ended_sets = match_obj.ended_sets
    return {"sets": sets,
            "ended_sets": ended_sets,
            "current_set": current_set}


def match_from_dict(data):
    current_set = data["current_set"]
    sets = data["sets"]
    ended_sets = data["ended_sets"]
    return Match.from_sets(sets, current_set,ended_sets)
