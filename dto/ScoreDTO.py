from dataclasses import dataclass


@dataclass
class MatchScoreDTO:
    uuid: str
    player1_name: str
    player2_name: str
    
    sets: str
    current_set: str
    current_game: str
    tiebreak: str
    is_finished: str
    winner: str | None


