import waitress

from tennis_scoreboard.web.app import application


def main() -> None:
    waitress.serve(application, host="localhost", port=8000)


if __name__ == "__main__":
    main()
