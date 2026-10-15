from typing import Optional
from sqlmodel import Field, SQLModel


class EstudioCreate(SQLModel):
  nombre: str = Field(min_length=1, description="Nombre del estudio")
  pais: str = Field(min_length=1, description="Pais del estudio")


class EstudioRead(EstudioCreate):
  id: int


class VideoJuegoCreate(SQLModel):
  nombre: str = Field(min_length=1, description="Nombre del videojuego")
  genero: str = Field(min_length=1, description="Genero del videojuego")
  puntuacion: int = Field(ge=0, le=10, description="Puntuacion del videojuego")
  estudio_id: Optional[int] = Field(
      default=None, gt=0, description="ID del estudio que lo desarrollo"
  )


class VideoJuegoRead(VideoJuegoCreate):
  id: int


class VideoJuegoReadWithEstudio(VideoJuegoRead):
  estudio: Optional[EstudioRead] = None  # ¡Dato anidado!


class EstudioReadWithVideojuegos(EstudioRead):
  videojuegos: list[VideoJuegoRead] = []  # ¡Dato anidado!
