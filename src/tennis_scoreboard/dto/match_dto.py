from dataclasses import dataclass

@dataclass
class MatchDTO:
    uuid: str
    player1_name: str
    player2_name: str
    winner_name: str
    score: list


@dataclass
class MatchesPageDTO:
    matches: list[MatchDTO]
    current_page: int
    total_pages: int

