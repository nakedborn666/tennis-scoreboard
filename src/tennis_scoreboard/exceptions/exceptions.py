class GameAlreadyEndedError(Exception):
    def __init__(self):
        self.message = "Гейм уже завершился"
        super().__init__(self.message)


class SetAlreadyEndedError(Exception):
    def __init__(self):
        self.message = "Сет уже завершился"
        super().__init__(self.message)


class TieBreakAlreadyEndedError(Exception):
    def __init__(self):
        self.message = "Тай-брейк уже завершился"
        super().__init__(self.message)


class TieBreakNotEndedError(Exception):
    def __init__(self):
        self.message = "Тай-брейк еще не завершился"
        super().__init__(self.message)


class MatchAlreadyEndedError(Exception):
    def __init__(self):
        self.message = "Матч уже завершился"
        super().__init__(self.message)


class MatchDoesntExistsError(Exception):
    def __init__(self):
        self.message = "Матч не существует"
        super().__init__(self.message)


class RouteDoesntExistsError(Exception):
    def __init__(self):
        self.message = "Маршрут не найден"
        super().__init__(self.message)


class MethodDismatchToPathError(Exception):
    def __init__(self):
        self.message = "Неверный http-метод для маршрута"
        super().__init__(self.message)


class RouteAlreadyRegistredError(Exception):
    def __init__(self):
        self.message = "Данный маршрут уже зарегистрирован"
        super().__init__(self.message)


class BadRequestError(Exception):
    def __init__(self):
        self.message = "BadRequestError"
        super().__init__(self.message)


class MatchUuidDoesntExistError(Exception):
    def __init__(self):
        self.message = "несуществующий uuid матча"
        super().__init__(self.message)


class PageShouldBeNumberError(Exception):
    def __init__(self):
        self.message = "номер страницы должен быть положительным числом"
        super().__init__(self.message)