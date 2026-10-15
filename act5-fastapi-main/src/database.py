from sqlmodel import Session, create_engine

DATABASE_URL = "sqlite:///./db_juegos_sqlmodel.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def get_session():
  with Session(engine) as session:
    yield session
