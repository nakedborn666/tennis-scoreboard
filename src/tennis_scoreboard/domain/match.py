from tennis_scoreboard.domain.set import Set
from tennis_scoreboard.exceptions.exceptions import MatchAlreadyEndedError

class Match:
    def __init__(self):
        self._sets = {1: 0,
                      2: 0}

        self._current_set = Set()
        self._ended_sets = []


    @classmethod
    def from_sets(cls, sets, current_set, ended_sets):
        match = cls()
        match._sets = {1: sets[0],
                       2: sets[1]}
        match._current_set = Set.from_games(current_set["games"], current_set["points"], current_set["tiebreak"])
        match._ended_sets = ended_sets
        return match


    @property
    def sets(self):
        return (self._sets[1], self._sets[2])


    @property
    def player1_sets(self) -> int:
        return self._sets[1]


    @property
    def player2_sets(self) -> int:
        return self._sets[2]

    @property
    def current_set(self):
        return self._current_set

    @property
    def current_set_data(self):
        return {"games": [self.current_set.player1_games, self.current_set.player2_games],
                "points": [self.current_set.current_game.player1_points, self.current_set.current_game.player2_points],
                "tiebreak": self.current_set.tiebreak}



    @property
    def ended_sets(self):
        return self._ended_sets


    def _is_match_ended(self) -> bool:
        return self.player2_sets == 2 or self.player1_sets == 2

    def winner(self) -> int | None:
        if self._is_match_ended():
            for key, value in self._sets.items():
                if value == 2:
                    return key
        return None


    def won_point(self, player_number):
        if player_number not in (1, 2):
            raise ValueError("Введите существующий номер игрока(1 или 2)")
        if self._is_match_ended():
            raise MatchAlreadyEndedError
        self._current_set.won_point(player_number)
        winner = self._current_set.winner()
        if winner is not None:
            self._sets[winner] += 1
            self._ended_sets.append([self._current_set.player1_games, self._current_set.player2_games])
            if not self._is_match_ended():
                self._current_set = Set()






