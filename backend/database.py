"""
Conexão com o banco de dados (MySQL) usado pelo backend FastAPI.
"""
import os

from sqlmodel import Session, create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:20071607@localhost:3306/pethope",
)

engine = create_engine(DATABASE_URL, echo=False)


def get_session():
    """Dependency do FastAPI: injeta uma sessão do banco por requisição."""
    with Session(engine) as session:
        yield session
