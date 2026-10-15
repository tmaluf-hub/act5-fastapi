from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Estudio(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  nombre: str = Field(index=True, unique=True)
  pais: str


  videojuegos: List["VideoJuego"] = Relationship(back_populates="estudio")



class VideoJuego(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  nombre: str
  genero: str
  puntuacion: int

  
  estudio_id: Optional[int] = Field(default=None, foreign_key="estudio.id")
  estudio: Optional[Estudio] = Relationship(back_populates="videojuegos")