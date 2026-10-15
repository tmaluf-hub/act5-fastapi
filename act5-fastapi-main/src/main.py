from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from src.database import engine
from src.models.juegos_models import Estudio, VideoJuego
from src.routers.estudios import router as estudios_router
from src.routers.videojuegos import router as videojuegos_router

# Las tablas NO se crean aca: las crea Alembic con `alembic upgrade head`.


def seed_datos():
  with Session(engine) as session:
    hay_datos = session.exec(select(Estudio)).first() or session.exec(
        select(VideoJuego)
    ).first()
    if hay_datos:
      return

    rockstar = Estudio(nombre="Rockstar Games", pais="Estados Unidos")
    riot = Estudio(nombre="Riot Games", pais="Estados Unidos")
    activision = Estudio(nombre="Activision", pais="Estados Unidos")
    roblox = Estudio(nombre="Roblox Corporation", pais="Estados Unidos")
    mojang = Estudio(nombre="Mojang Studios", pais="Suecia")

    juegos_iniciales = [
        VideoJuego(
            nombre="GTA V", genero="Mundo Abierto", puntuacion=10, estudio=rockstar
        ),
        VideoJuego(
            nombre="League of Legends", genero="MOBA", puntuacion=7, estudio=riot
        ),
        VideoJuego(
            nombre="Call of Duty", genero="Disparos", puntuacion=8, estudio=activision
        ),
        VideoJuego(nombre="Roblox", genero="MMO", puntuacion=4, estudio=roblox),
        VideoJuego(nombre="Minecraft", genero="Sandbox", puntuacion=1, estudio=mojang),
    ]
    session.add_all(juegos_iniciales)
    session.commit()
    print("¡Estudios y juegos iniciales cargados con éxito!")


@asynccontextmanager
async def lifespan(app: FastAPI):
  seed_datos()
  yield


app = FastAPI(title="API de Videojuegos - SQLModel", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(estudios_router)
app.include_router(videojuegos_router)
