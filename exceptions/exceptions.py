class GameAlreadyEnded(Exception):
    def __init__(self):
        self.message = "Гейм уже завершился"
        super().__init__(self.message)


class SetAlreadyEnded(Exception):
    def __init__(self):
        self.message = "Сет уже завершился"
        super().__init__(self.message)


class TieBreakAlreadyEnded(Exception):
    def __init__(self):
        self.message = "Тай-брейк уже завершился"
        super().__init__(self.message)


class TieBreakNotEnded(Exception):
    def __init__(self):
        self.message = "Тай-брейк еще не завершился"
        super().__init__(self.message)


class MatchAlreadyEnded(Exception):
    def __init__(self):
        self.message = "Матч уже завершился"
        super().__init__(self.message)


class MatchDoesntExists(Exception):
    def __init__(self):
        self.message = "Матч не существует"
        super().__init__(self.message)