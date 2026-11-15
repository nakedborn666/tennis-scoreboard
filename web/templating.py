from jinja2 import Environment, FileSystemLoader
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=True,
)
def render_template(name, **context):
    template = env.get_template(name)
    return template.render(**context)



#@dataclass
#class Stats:
#    level: int
#    wins: int
#
#
#@dataclass
#class Player:
#    name: str
#    score: int
#    stats: Stats
#
#players = [
#    Player(name="Аня", score=1200, stats=Stats(level=7, wins=12)),
#    Player(name="Дима", score=300, stats=Stats(level=5, wins=7)),
#    Player(name="Олег", score=40, stats=Stats(level=2, wins=3)),
#]
#
#env = Environment(autoescape=True)
#
#template = env.from_string(
#    "Игроки:\n"
#    "{% for player in players %}"
#    "{{ loop.index }}. {{ player.name }} — "
#    "уровень {{ player.stats.level }}, "
#    "победы {{ player.stats.wins }}"
#    "{% if player.stats.wins >=10 %} [ветеран]{% endif %}\n"
#    "{% else %}"
#    "Список игроков пуст\n"
#    "{% endfor %}"
#)
#
#
#
#
#result = template.render(players=players)
#
#print(result)