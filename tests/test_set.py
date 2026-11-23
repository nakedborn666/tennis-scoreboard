from tennis_scoreboard.domain.set import Set
import pytest
from tennis_scoreboard.exceptions.exceptions import SetAlreadyEndedError, TieBreakAlreadyEndedError
from tennis_scoreboard.domain.game import Game


def test_new_set():
    match_set = Set()
    assert match_set._games == {1: 0,
                                2: 0}


def test_first_player_zero_games():
    match_set = Set()
    assert match_set.player1_games == 0


def test_second_player_zero_games():
    match_set = Set()
    assert match_set.player2_games == 0


@pytest.mark.parametrize(
    "p1_games, p2_games, winner",
    [
        (7, 5, 1),
        (1, 7, 2),
        (6, 5, None),
        (7, 6, 1),
        (4, 3, None),
        (6, 7, 2)
    ]
)
def test_set_winner(p1_games,p2_games,winner):
    match_set = Set()
    match_set._games = {1: p1_games,
                  2: p2_games}
    assert match_set.winner() == winner


def test_second_player_won_point():
    match_set = Set()
    match_set._games = {1: 1,
                        2: 1}
    match_set._current_game = Game()
    match_set._current_game._points = {1: 2,
                               2: 3}
    match_set.won_point(2)
    assert match_set._games == {1: 1,
                         2: 2}


def test_first_player_won_point():
    match_set = Set()
    match_set._games = {1: 1,
                        2: 1}
    match_set._current_game = Game()
    match_set._current_game._points = {1: 3,
                                       2: 2}
    match_set.won_point(1)
    assert match_set._games == {1: 2,
                                2: 1}


def test_set_already_ended_before_won_point():
    match_set = Set()
    match_set._current_game = Game()
    match_set._current_game._points = {1: 4,
                                       2: 2}
    match_set._games = {1: 7,
                        2: 5}
    with pytest.raises(SetAlreadyEndedError):
        match_set.won_point(1)


def test_is_tiebreak():
    match_set = Set()
    match_set._games = {1: 6,
                        2: 6}
    assert match_set._is_it_tiebreak()


def test_is_not_tiebreak():
    match_set = Set()
    match_set._games = {1: 7,
                        2: 5}
    assert not match_set._is_it_tiebreak()


def test_first_player_won_tiebreak_point():
    match_set = Set()
    match_set._games = {1: 6,
                        2: 6}
    match_set.won_tiebreak_point(1)
    assert match_set._tiebreak == {1: 1,
                                   2: 0}


def test_second_player_won_tiebreak_point():
    match_set = Set()
    match_set._games = {1: 6,
                        2: 6}
    match_set._tiebreak = {1: 4,
                           2: 5}
    match_set.won_tiebreak_point(2)
    assert match_set._tiebreak == {1: 4,
                                   2: 6}


def test_first_player_tiebreak_winner():
    match_set = Set()
    match_set._games = {1: 6,
                        2: 6}

    match_set._tiebreak = {1: 7,
                           2: 5}
    assert match_set.tiebreak_winner() == 1


def test_tie_break_already_ended():
    match_set = Set()
    match_set._games = {1: 6,
                        2: 6}
    match_set._tiebreak = {1: 7,
                           2: 5}
    with pytest.raises(TieBreakAlreadyEndedError):
        match_set.won_tiebreak_point(1)


def test_set_winner_with_tiebreak():
    match_set = Set()
    match_set._games = {1: 6,
                       2: 6}
    match_set._tiebreak = {1: 5,
                           2: 6}
    match_set.won_point(2)
    assert match_set.winner() == 2




def test_won_point_not_game():
    match_set = Set()
    match_set.won_point(1)
    assert match_set._current_game._points == {1: 1,
                                       2: 0}
    assert match_set._games == {1: 0,
                         2: 0}


def test_if_set_won_new_game_doesnt_create():
    match_set = Set()
    match_set._games = {1: 5,
                        2: 4}
    match_set._current_game._points = {1: 3,
                               2: 0}
    match_set.won_point(1)
    assert match_set._games == {1: 6,
                                2: 4}
    assert match_set._current_game._points == {1: 4,
                                               2: 0}
    assert match_set.winner() == 1


def test_second_player_won_point_and_test_winner():
    match_set = Set()
    match_set._games = {1: 4,
                        2: 5}
    match_set._current_game._points = {1: 0,
                                       2: 3}
    match_set.won_point(2)
    assert match_set._games == {1: 4,
                                2: 6}
    assert match_set.winner() == 2


def test_set_already_ended_after_won_point():
    set_match = Set()
    set_match._games = {1: 6,
                        2: 2}

    with pytest.raises(SetAlreadyEndedError):
        set_match.won_point(1)


def test_tiebreak_logic():
    set_match = Set()
    set_match._games = {1: 6,
                        2: 6}
    set_match._tiebreak = {1: 6,
                           2: 3}
    set_match.won_point(1)
    assert set_match._games == {1: 7,
                                2: 6}
    assert set_match._tiebreak == {1: 0,
                                   2: 0}
    assert set_match.winner() == 1