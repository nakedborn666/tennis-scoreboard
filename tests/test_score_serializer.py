from domain.match import Match
from domain.score_serializer import match_to_dict, match_from_dict
from domain.set import Set


def test_match_to_dict():
    match = Match()
    match._sets = {1: 1,
                   2: 1}
    match._current_set = Set.from_games([4, 3], [2, 1], None)
    match._ended_sets = [[6, 2], [3, 6]]

    assert match_to_dict(match) == {
                                    "sets": [1, 1],
                                    "ended_sets": [[6, 2], [3, 6]],
                                    "current_set": {
                                        "games": [4, 3],
                                        "points": [2, 1],
                                        "tiebreak": None
                                    },
    }


def test_match_from_dict():
    my_dict = {"sets": [1, 1],
            "ended_sets": [[6, 2], [3, 6]],
            "current_set": {"games": [4, 3],
                           "points": [2, 1],
                           "tiebreak": None}}
    match = match_from_dict(my_dict)
    assert match_to_dict(match) == my_dict