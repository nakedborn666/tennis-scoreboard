from domain.match import Match
import pytest
from exceptions.exceptions import MatchAlreadyEndedError


def test_new_match():
    match = Match()
    assert match._sets == {1: 0,
                           2: 0}


@pytest.mark.parametrize(
    "p1_sets, p2_sets, winner",
    [
        (1, 1, None),
        (1, 2, 2),
        (2, 1, 1),
        (2, 0, 1),
        (0, 2, 2)
    ]
)
def test_match_winner(p1_sets, p2_sets, winner):
    match = Match()
    match._sets = {1: p1_sets,
                   2: p2_sets}

    assert match.winner() == winner


def test_second_player_won_set():
    match = Match()
    match._sets = {1: 0,
                   2: 1}
    match._current_set._games = {1: 5,
                         2: 6}
    match._current_set._current_game._points = {1: 2,
                                                2: 3}
    match.won_point(2)
    assert match.winner() == 2


def test_one_point_to_games_not_to_sets():
    match = Match()
    match._current_set._games = {1: 1,
                                 2: 2}
    match._current_set._current_game._points = {1: 3,
                                                2: 1}

    match.won_point(1)
    assert match._current_set._games == {1: 2,
                                         2: 2}
    assert match._sets == {1: 0,
                           2: 0}


def test_new_set_create():
    match = Match()
    match._current_set._games = {1: 5,
                                 2: 4}
    match._current_set._current_game._points = {1: 3,
                                                2: 0}
    match.won_point(1)
    assert match._sets == {1: 1,
                           2: 0}
    assert match._current_set._games == {1: 0,
                                  2: 0}


def test_new_set_create_if_one_one_score():
    match = Match()
    match._sets = {1: 1,
                   2: 0}
    match._current_set._games = {1: 3,
                                 2: 5}
    match._current_set._current_game._points = {1: 1,
                                                2: 3}
    match.won_point(2)
    assert match._current_set._games == {1: 0,
                                         2: 0}


def test_match_already_ended_before_won_point():
    match = Match()
    match._sets = {1: 2,
                   2: 0}
    match._current_set._games = {1: 6,
                                 2: 2}
    match._current_set._current_game._points = {1: 4,
                                                2: 1}
    assert match._is_match_ended()
    assert match._current_set._games == {1: 6,
                                         2: 2}
    with pytest.raises(MatchAlreadyEndedError):
        match.won_point(player_number=1)


def test_one_point_change_current_game_points_not_sets_not_match():
    match = Match()

    match._current_set._games = {1: 2,
                                 2: 2}
    match._current_set._current_game._points = {1: 1,
                                                2: 1}
    match.won_point(1)
    assert match._current_set._current_game._points == {1: 2,
                                                2: 1}
    assert match._sets == {1: 0,
                           2: 0}
    assert match._current_set._games == {1: 2,
                                         2: 2}


def test_won_set_add_to_ended_sets():
    match = Match()

    match._current_set._games = {1: 5,
                                 2: 2}
    match._current_set._current_game._points = {1: 3,
                                                2: 1}
    match.won_point(1)
    assert match._ended_sets == [[6, 2]]


def test_one_one_score_and_new_set():
    match = Match()
    match._sets = {1: 0,
                   2: 1}

    match._current_set._games = {1: 5,
                                 2: 2}
    match._current_set._current_game._points = {1: 3,
                                                2: 1}
    match.won_point(1)

    assert match._sets == {1: 1,
                           2: 1}
    assert match._current_set._games == {1: 0,
                                         2: 0}


def test_tie_break_in_ended_sets():
    match = Match()
    match._sets = {1: 0,
                   2: 0}

    match._current_set._games = {1: 6,
                                 2: 6}
    match._current_set._tiebreak = {1: 6,
                                    2: 2}
    match._current_set._current_game._points = {1: 3,
                                                2: 1}
    match.won_point(1)

    assert match._ended_sets == [[7, 6]]


def test_final_set():
    match = Match()
    match._sets = {1: 1,
                   2: 1}
    match._ended_sets = [[6, 2]]

    match._current_set._games = {1: 5,
                                 2: 4}

    match._current_set._current_game._points = {1: 3,
                                                2: 0}
    match.won_point(1)

    assert match._sets == {1: 2,
                           2: 1}
    assert match._ended_sets == [[6, 2], [6, 4]]
    assert match._current_set._games == {1: 6,
                                         2: 4}


