"""Conexão com o banco.

- No computador: SQLite em backend/acoust.db.
- Na Vercel com banco configurado (DATABASE_URL ou POSTGRES_URL): Postgres. É o
  único jeito de contas e histórico sobreviverem entre um acesso e outro.
- Na Vercel sem banco configurado: SQLite em /tmp, a única pasta gravável lá.
  A calculadora funciona, mas contas e histórico somem quando a função reinicia.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


def _url_do_banco() -> str:
    url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")
    if url:
        # Os provedores entregam "postgres://"; o SQLAlchemy 2 com psycopg 3
        # espera "postgresql+psycopg://".
        for prefixo in ("postgres://", "postgresql://"):
            if url.startswith(prefixo):
                return "postgresql+psycopg://" + url[len(prefixo):]
        return url
    if os.getenv("VERCEL"):
        return "sqlite:////tmp/acoust.db"
    return "sqlite:///" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "acoust.db")


DATABASE_URL = _url_do_banco()
_sqlite = DATABASE_URL.startswith("sqlite")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if _sqlite else {},
    # o Postgres gerenciado derruba conexões ociosas; testa antes de reaproveitar
    pool_pre_ping=not _sqlite,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
