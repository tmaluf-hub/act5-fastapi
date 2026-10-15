from typing import Annotated, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlmodel import Session, select
from src.database import get_session
from src.models.juegos_models import Estudio, VideoJuego
from src.schemas.videojuegos import VideoJuegoCreate, VideoJuegoReadWithEstudio

router = APIRouter(prefix="/videojuegos", tags=["Videojuegos"])

VideojuegoId = Annotated[int, Path(gt=0)]


def buscar_videojuego(id: int, session: Session) -> VideoJuego:
  videojuego = session.get(VideoJuego, id)
  if not videojuego:
    raise HTTPException(status_code=404, detail="Videojuego no encontrado")
  return videojuego


def validar_estudio(estudio_id: Optional[int], session: Session):
  if estudio_id is not None and not session.get(Estudio, estudio_id):
    raise HTTPException(status_code=404, detail="Estudio no encontrado")


@router.get("/", response_model=list[VideoJuegoReadWithEstudio])
def obtener_videojuegos(session: Session = Depends(get_session)):
  return session.exec(select(VideoJuego)).all()


@router.get(
    "/{id}",
    response_model=VideoJuegoReadWithEstudio,
    responses={404: {"description": "Videojuego no encontrado"}},
)
def obtener_videojuego_id(
    id: VideojuegoId, session: Session = Depends(get_session)
):
  return buscar_videojuego(id, session)


@router.post(
    "/",
    response_model=VideoJuegoReadWithEstudio,
    status_code=201,
    responses={404: {"description": "Estudio no encontrado"}},
)
def crear_videojuego(
    videojuego: VideoJuegoCreate, session: Session = Depends(get_session)
):
  validar_estudio(videojuego.estudio_id, session)
  nuevo_videojuego = VideoJuego.model_validate(videojuego)
  session.add(nuevo_videojuego)
  session.commit()
  session.refresh(nuevo_videojuego)
  return nuevo_videojuego


@router.put(
    "/{id}",
    response_model=VideoJuegoReadWithEstudio,
    responses={404: {"description": "Videojuego o estudio no encontrado"}},
)
def actualizar_videojuego(
    id: VideojuegoId,
    videojuego_actualizado: VideoJuegoCreate = Body(),
    session: Session = Depends(get_session),
):
  videojuego = buscar_videojuego(id, session)
  validar_estudio(videojuego_actualizado.estudio_id, session)

  videojuego.sqlmodel_update(videojuego_actualizado.model_dump())
  session.add(videojuego)
  session.commit()
  session.refresh(videojuego)
  return videojuego


@router.delete(
    "/{id}",
    response_model=VideoJuegoReadWithEstudio,
    responses={404: {"description": "Videojuego no encontrado"}},
)
def eliminar_videojuego(
    id: VideojuegoId, session: Session = Depends(get_session)
):
  videojuego = buscar_videojuego(id, session)
  # Se arma la respuesta antes de borrar, porque despues del commit
  # el objeto ya no se puede leer (ni su estudio anidado).
  respuesta = VideoJuegoReadWithEstudio.model_validate(videojuego)

  session.delete(videojuego)
  session.commit()
  return respuesta
