
import waitress
from web.app import application


if __name__ == "__main__":
    waitress.serve(application, host="localhost", port=8000)