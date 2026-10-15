# API de Videojuegos - SQLModel + Alembic

API con FastAPI que usa **SQLModel** como ORM y **Alembic** para las migraciones.

- Modelos: `Estudio` y `VideoJuego` (relación 1 a N mediante la FK `videojuego.estudio_id → estudio.id`).
- Datos anidados: `GET /videojuegos` devuelve cada juego con su estudio y `GET /estudios` devuelve cada estudio con sus juegos.

## Cómo correrlo

```bash
python -m venv .venv
.venv\Scripts\activate          # en Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt

alembic upgrade head            # crea las tablas
uvicorn src.main:app --reload
```

Documentación interactiva: http://127.0.0.1:8000/docs

Al arrancar por primera vez se cargan algunos estudios y juegos de ejemplo.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/estudios/` | Lista de estudios con sus videojuegos |
| GET | `/estudios/{id}` | Un estudio con sus videojuegos |
| POST | `/estudios/` | Crea un estudio |
| PUT | `/estudios/{id}` | Modifica un estudio |
| DELETE | `/estudios/{id}` | Borra un estudio (solo si no tiene juegos) |
| GET | `/videojuegos/` | Lista de videojuegos con su estudio |
| GET | `/videojuegos/{id}` | Un videojuego con su estudio |
| POST | `/videojuegos/` | Crea un videojuego (`estudio_id` opcional) |
| PUT | `/videojuegos/{id}` | Modifica un videojuego |
| DELETE | `/videojuegos/{id}` | Borra un videojuego |

## Nueva migración

Después de cambiar un modelo en `src/models/juegos_models.py`:

```bash
alembic revision --autogenerate -m "descripcion del cambio"
alembic upgrade head
```
