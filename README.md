# Inventario API

API REST para inventario construida con FastAPI, SQLAlchemy y PostgreSQL. El proyecto cubre autenticación con JWT, autorización por roles, gestión de productos y movimientos de stock con reglas de negocio validadas y pruebas automatizadas.

Demo: [https://inventario-api-skyp.onrender.com/docs](https://inventario-api-skyp.onrender.com/docs)

## Qué demuestra este proyecto

- Diseño de una API backend con capas separadas: `routers`, `services`, `schemas`, `models`.
- Autenticación con JWT y autorización por rol (`admin`, `viewer`).
- Validaciones de negocio en inventario: stock insuficiente, soft delete, productos inactivos, categorías inexistentes.
- Persistencia versionada con Alembic.
- Testing con Pytest sobre flujos felices y casos de borde.
- Calidad automatizada en CI con tests y lint.

## Stack

- Python 3.11
- FastAPI
- SQLAlchemy 2
- PostgreSQL
- Alembic
- Pydantic v2
- Pytest
- Docker
- GitHub Actions

## Arquitectura

```text
app/
├── core/        # configuración, seguridad, dependencias, handlers
├── models/      # modelos SQLAlchemy
├── routers/     # endpoints HTTP
├── schemas/     # contratos de entrada/salida
├── services/    # reglas de negocio
├── database.py  # engine, session y Base
└── main.py      # app FastAPI y registro de routers
```

### Decisiones técnicas

- `services/` concentra lógica de negocio para evitar routers inflados.
- `Numeric(10,2)` y `Decimal` se usan para dinero en lugar de `float`.
- Los errores HTTP y de validación responden con un formato consistente.
- Los productos usan soft delete para conservar trazabilidad.
- Los movimientos validan cantidad positiva y bloquean stock negativo.

## Funcionalidades

### Auth

- `POST /auth/registro`
- `POST /auth/login`
- `GET /auth/me`

### Productos

- CRUD de productos
- CRUD básico de categorías
- filtros por categoría, activos y stock bajo
- paginación
- soft delete

### Inventario

- entradas y salidas de stock
- historial de movimientos por producto
- alertas de stock bajo

## Endpoints principales

| Método | Endpoint | Descripción | Auth |
| --- | --- | --- | --- |
| POST | `/auth/registro` | Registro de usuario | No |
| POST | `/auth/login` | Login con JWT | No |
| GET | `/auth/me` | Usuario autenticado | Sí |
| GET | `/productos/` | Listar productos | Sí |
| POST | `/productos/` | Crear producto | Admin |
| PATCH | `/productos/{id}` | Actualizar producto | Admin |
| DELETE | `/productos/{id}` | Desactivar producto | Admin |
| GET | `/productos/categorias` | Listar categorías | Sí |
| POST | `/productos/categorias` | Crear categoría | Admin |
| POST | `/inventario/movimiento` | Registrar movimiento | Sí |
| GET | `/inventario/movimientos/{id}` | Historial por producto | Sí |
| GET | `/inventario/alertas` | Stock bajo | Sí |

## Requisitos

- Python 3.11+
- Docker Desktop

## Ejecución local

```bash
git clone https://github.com/Vicente28CF/inventario-api.git
cd inventario-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements-dev.txt
copy .env.example .env
docker-compose up -d
alembic upgrade head
uvicorn app.main:app --reload
```

API disponible en `http://localhost:8000/docs`.

También puedes usar `start.bat` en Windows.

## Variables de entorno

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/inventario_db
SECRET_KEY=tu_secret_key_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
TESTING=false
```

## Calidad y testing

```bash
pytest
pytest --cov=app
ruff check .
```

La configuración de calidad vive en `pyproject.toml`.

## Migraciones

```bash
alembic upgrade head
alembic history
alembic revision -m "descripcion_del_cambio"
```

Migraciones relevantes:

- esquema inicial
- cambio de `precio` de `Float` a `Numeric(10,2)`

## CI

En GitHub Actions corren dos verificaciones en cada push y pull request:

- tests con SQLite y variables de entorno de CI
- lint con `ruff`

## Estado actual

- tests automatizados: `19 passed`
- autenticación con rate limiting
- documentación OpenAPI disponible en `/docs`
- deploy activo en Render

## Mejoras futuras

- refresh tokens
- búsqueda por nombre y ordenamiento
- auditoría más detallada de cambios
- cobertura de tests con métricas
- observabilidad con logging estructurado

## Autor

Vicente Cayetano  
[LinkedIn](https://www.linkedin.com/in/vicente-cayetano-3113322a9)  
[Portafolio](https://vcayetano-dev.lovable.app)
