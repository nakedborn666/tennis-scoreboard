import pytest
from domain.game import Game
from exceptions.exceptions import GameAlreadyEndedError

def test_new_game():
    game = Game()
    assert game._points == {1: 0,
                            2: 0}

def test_first_point_goes_to_player_1():
    game = Game()
    game.won_point(1)
    assert game._points == {1: 1, 2: 0}


def test_first_points_goes_to_player_2():
    game = Game()
    game.won_point(2)
    assert game._points == {1: 0,
                            2: 1}

@pytest.mark.parametrize(
    "p1_points, p2_points, winner",
    [
        (4, 0, 1),
        (2, 0, None),
        (3, 1, None),
        (4, 2, 1),
        (4, 3, None),
        (0, 4, 2)
    ]
)
def test_winner(p1_points,p2_points,winner):
    game = Game()
    game._points = {1: p1_points,
                    2: p2_points}
    assert game.winner() == winner



def test_game_already_ended_before_won_point():
    game = Game()
    game._points = {1: 4,
                    2: 2}
    with pytest.raises(GameAlreadyEndedError):
        game.won_point(player_number=1)




def test_more_or_equal_fourth_point_for_first_player_with_no_win():
    game = Game()
    game._points = {1: 3,
                    2: 3}

    game.won_point(1)
    assert game.winner() is None and game._points == {1: 4,
                                                      2: 3}

def test_more_or_equal_fourth_point_for_second_player_to_equal_points():
    game = Game()
    game._points = {1: 4,
                    2: 3}
    game.won_point(2)
    assert game.winner() is None and game._points == {1: 3,
                                                      2: 3}


def test_more_or_equal_fourth_point_for_first_player_to_win():
    game = Game()
    game._points = {1: 4,
                    2: 3}
    game.won_point(1)
    assert game.winner() == 1 and game._points == {1: 5,
                                                   2: 3}





@pytest.mark.parametrize(
    "p1_points, p2_points, score",
    [
        (2, 1, "Текущий счет гейма: первый игрок - 30, второй игрок - 15"),
        (2, 0, "Текущий счет гейма: первый игрок - 30, второй игрок - 0"),
        (3, 1, "Текущий счет гейма: первый игрок - 40, второй игрок - 15"),
        (3, 3, "Текущий счет гейма: первый игрок - ровно, второй игрок - ровно"),
        (4, 3, "Текущий счет гейма: первый игрок - больше, второй игрок - 40"),
        (3, 4, "Текущий счет гейма: первый игрок - 40, второй игрок - больше"),
        (5, 3, "Гейм завершен, победу одержал первый игрок"),
        (1, 4, "Гейм завершен, победу одержал второй игрок")
    ]
)
def test_display(p1_points, p2_points, score):
    game = Game()
    game._points = {1: p1_points,
                    2: p2_points}

    assert str(game) == score


def test_str_does_not_change_points():
    game = Game()
    game._points = {1: 3,
                    2: 1}

    str(game)

    assert game._points == {1: 3,
                            2: 1}

    assert game.winner() is None