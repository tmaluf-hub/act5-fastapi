from typing import Annotated, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlmodel import Session, select
from src.database import get_session
from src.models.juegos_models import Estudio
from src.schemas.videojuegos import (
    EstudioCreate,
    EstudioRead,
    EstudioReadWithVideojuegos,
)

router = APIRouter(prefix="/estudios", tags=["Estudios"])

EstudioId = Annotated[int, Path(gt=0)]


def buscar_estudio(id: int, session: Session) -> Estudio:
  estudio = session.get(Estudio, id)
  if not estudio:
    raise HTTPException(status_code=404, detail="Estudio no encontrado")
  return estudio


def validar_nombre_unico(
    nombre: str, session: Session, id_actual: Optional[int] = None
):
  existente = session.exec(select(Estudio).where(Estudio.nombre == nombre)).first()
  if existente and existente.id != id_actual:
    raise HTTPException(
        status_code=409, detail="Ya existe un estudio con ese nombre"
    )


@router.get("/", response_model=list[EstudioReadWithVideojuegos])
def obtener_estudios(session: Session = Depends(get_session)):
  return session.exec(select(Estudio)).all()


@router.get(
    "/{id}",
    response_model=EstudioReadWithVideojuegos,
    responses={404: {"description": "Estudio no encontrado"}},
)
def obtener_estudio_id(id: EstudioId, session: Session = Depends(get_session)):
  return buscar_estudio(id, session)


@router.post(
    "/",
    response_model=EstudioRead,
    status_code=201,
    responses={409: {"description": "Ya existe un estudio con ese nombre"}},
)
def crear_estudio(estudio: EstudioCreate, session: Session = Depends(get_session)):
  validar_nombre_unico(estudio.nombre, session)
  nuevo_estudio = Estudio.model_validate(estudio)
  session.add(nuevo_estudio)
  session.commit()
  session.refresh(nuevo_estudio)
  return nuevo_estudio


@router.put(
    "/{id}",
    response_model=EstudioRead,
    responses={
        404: {"description": "Estudio no encontrado"},
        409: {"description": "Ya existe un estudio con ese nombre"},
    },
)
def actualizar_estudio(
    id: EstudioId,
    estudio_actualizado: EstudioCreate = Body(),
    session: Session = Depends(get_session),
):
  estudio = buscar_estudio(id, session)
  validar_nombre_unico(estudio_actualizado.nombre, session, id_actual=id)

  estudio.sqlmodel_update(estudio_actualizado.model_dump())
  session.add(estudio)
  session.commit()
  session.refresh(estudio)
  return estudio


@router.delete(
    "/{id}",
    response_model=EstudioRead,
    responses={
        404: {"description": "Estudio no encontrado"},
        409: {"description": "El estudio tiene videojuegos asociados"},
    },
)
def eliminar_estudio(id: EstudioId, session: Session = Depends(get_session)):
  estudio = buscar_estudio(id, session)
  if estudio.videojuegos:
    raise HTTPException(
        status_code=409,
        detail="No se puede borrar un estudio con videojuegos asociados",
    )
  respuesta = EstudioRead.model_validate(estudio)

  session.delete(estudio)
  session.commit()
  return respuesta
