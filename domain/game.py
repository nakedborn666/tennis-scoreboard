
from exceptions.exceptions import GameAlreadyEndedError

_POINT_NAMES = {0: "0",
                1: "15",
                2: "30",
                3: "40"}

class Game:
    def __init__(self):
        self._points = {1: 0,
                        2: 0}

    @classmethod
    def from_points(cls, points):
        player1_points, player2_points = points
        game_obj = cls()
        game_obj._points = {1: player1_points,
                            2: player2_points}
        return game_obj


    @property
    def player1_points(self) -> int:
        return self._points[1]


    @property
    def player2_points(self)-> int:
        return self._points[2]


    def display(self) -> tuple:
        if self.player1_points == 3 and self.player2_points == 3:
            return "ровно", "ровно"
        if self.player1_points == 4 and self.player2_points == 3:
            return "больше", "40"
        if self.player2_points == 4 and self.player1_points == 3:
            return "40", "больше"

        return _POINT_NAMES[self.player1_points], _POINT_NAMES[self.player2_points]


    def __str__(self) -> str:
        winner = self.winner()
        if winner is None:
            player1_score, player2_score = self.display()
            return f"Текущий счет гейма: первый игрок - {player1_score}, второй игрок - {player2_score}"
        if winner == 1:
            return f"Гейм завершен, победу одержал первый игрок"
        else:
            return f"Гейм завершен, победу одержал второй игрок"


    def won_point(self, player_number: int) -> None:
        if player_number not in (1, 2):
            raise ValueError("Введите существующий номер игрока(1 или 2)")
        if self.winner() is not None:
            raise GameAlreadyEndedError
        self._points[player_number] += 1
        if (self.player1_points, self.player2_points) == (4, 4):
            self._points = {1: 3,
                            2: 3}


    def winner(self) -> int | None:
        if self.player1_points >= 4 and self.player2_points <= (self.player1_points - 2):
            return 1
        elif self.player2_points >= 4 and self.player1_points <= (self.player2_points - 2):
            return 2

        return None






        




