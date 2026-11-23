from dataclasses import dataclass


@dataclass
class PlayerScoreDTO:
    name: str
    sets: int
    games: int
    points: str
    tiebreak: int | None


@dataclass
class MatchScoreDTO:
    uuid: str
    player1: PlayerScoreDTO
    player2: PlayerScoreDTO
    is_finished: bool
    winner_name: str | None

