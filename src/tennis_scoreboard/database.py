from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tennis_scoreboard.config import url_config

engine = create_engine(url_config, echo=True)

session_local = sessionmaker(bind=engine)
