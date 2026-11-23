from tennis_scoreboard.exceptions.exceptions import RouteDoesntExistsError, MethodDismatchToPathError, RouteAlreadyRegistredError
from collections.abc import Callable

class Router:
    def __init__(self):
        self._routes = {}

    @staticmethod
    def normalize_route(method: str, path: str | None) -> tuple:
        method = method.upper()
        if path is None:
            path = ""
        path = "/" + path.strip("/")
        return method, path


    def register_route(self, method: str, path: str, controller: Callable) -> None:
        method, path = self.normalize_route(method, path)
        existed_methods = self._routes.get(path, {})
        if method in existed_methods:
            raise RouteAlreadyRegistredError
        self._routes.setdefault(path, {})[method] = controller


    def find_controller(self, method, path):
        method, path = self.normalize_route(method, path)
        if path not in self._routes:
            raise RouteDoesntExistsError
        if method not in self._routes[path]:
            raise MethodDismatchToPathError
        return self._routes[path][method]



