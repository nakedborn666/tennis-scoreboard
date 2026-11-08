from domain.game import Game
from exceptions.exceptions import SetAlreadyEnded, TieBreakAlreadyEnded, TieBreakNotEnded


class Set:
    def __init__(self):
        self._games = {1: 0,
                       2: 0}

        self._current_game = Game()

        self._tiebreak = {1: 0,
                          2: 0}


    @classmethod
    def from_games(cls, games, current_game_points, tiebreak):
        set_obj = cls()
        set_obj._games = {1: games[0],
                          2: games[1]}
        set_obj._current_game = Game.from_points(current_game_points)
        set_obj._tiebreak = {1: 0,
                             2: 0} if tiebreak is None else {1: tiebreak[0],
                                                             2: tiebreak[1]}
        return set_obj


    @property
    def player1_games(self) -> int:
        return self._games[1]


    @property
    def player2_games(self) -> int:
        return self._games[2]


    @property
    def current_game(self):
        return self._current_game


    @property
    def tiebreak(self):
        if self._is_it_tiebreak():
            return [self._tiebreak[1], self._tiebreak[2]]
        return None

    def _is_it_tiebreak(self) -> bool:
        if (self.player1_games, self.player2_games) == (6, 6):
            return True
        return False


    def won_tiebreak_point(self, player: int) -> None:
        if player not in (1, 2):
            raise ValueError("Введите существующий номер игрока(1 или 2)")
        if self.tiebreak_winner() is not None:
            raise TieBreakAlreadyEnded
        self._tiebreak[player] += 1


    def _is_tiebreak_ended(self) -> bool:
        if self.tiebreak_winner():
            return True
        return False


    def won_tiebreak(self):
        if self._is_tiebreak_ended():
            self._games[self.tiebreak_winner()] += 1
            self._tiebreak = {1: 0,
                              2: 0}
        else:
            raise TieBreakNotEnded


    def tiebreak_winner(self) -> int | None:
        tiebreak_p1 = self._tiebreak[1]
        tiebreak_p2 = self._tiebreak[2]
        if tiebreak_p1 >= 7 and tiebreak_p2 <= (tiebreak_p1  - 2):
            return 1
        elif tiebreak_p2 >= 7 and tiebreak_p1 <= (tiebreak_p2 - 2):
            return 2
        return None


    def winner(self):
        if not self._is_it_tiebreak():
            if self.player1_games >= 6 and self.player2_games <= (self.player1_games - 2):
                return 1
            elif self.player2_games >= 6 and self.player1_games <= (self.player2_games - 2):
                return 2
            elif self._games == {1: 7,
                                 2: 6}:
                return 1
            elif self._games == {1: 6,
                                 2: 7}:
                return 2
            return None
        else:
            if self._is_tiebreak_ended():
                return self.tiebreak_winner()
            else:
                return None


    def won_point(self, player_number):
        if player_number not in (1, 2):
            raise ValueError("Введите существующий номер игрока(1 или 2)")
        if self.winner() is not None:
            raise SetAlreadyEnded
        if not self._is_it_tiebreak():
            self._current_game.won_point(player_number)
            winner = self._current_game.winner()
            if winner:
                self._games[winner] += 1
                if self.winner() is None:
                    self._current_game = Game()
        else:
            if self._is_tiebreak_ended():
                raise SetAlreadyEnded
            else:
                self.won_tiebreak_point(player_number)
                if self._is_tiebreak_ended():
                    self.won_tiebreak()







