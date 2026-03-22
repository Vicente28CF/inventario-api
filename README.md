# Inventario API

API REST para gestión de inventario empresarial construida con FastAPI y PostgreSQL. Cubre autenticación JWT, autorización por roles, gestión de productos con reglas de negocio validadas, movimientos de stock y pruebas automatizadas.

🌐 **Demo en vivo:** [https://inventario-api-skyp.onrender.com/docs](https://inventario-api-skyp.onrender.com/docs)

---

## Stack

**Backend**
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)

**Base de datos**
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white)

**Testing**
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)

**DevOps & Deploy**
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=white)

**Herramientas**
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)

---

## Qué demuestra este proyecto

- Diseño de API backend con capas separadas: `routers`, `services`, `schemas`, `models`.
- Autenticación con JWT y autorización por rol (`admin`, `viewer`).
- Validaciones de negocio: stock insuficiente, soft delete, productos inactivos, categorías inexistentes.
- Persistencia versionada con Alembic.
- Testing con Pytest sobre flujos felices y casos de borde.
- Calidad automatizada en CI con tests y lint.

---

## Arquitectura

```
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

- `services/` concentra la lógica de negocio para evitar routers inflados.
- `Numeric(10,2)` y `Decimal` se usan para dinero en lugar de `float`.
- Los errores HTTP y de validación responden con un formato consistente.
- Los productos usan soft delete para conservar trazabilidad.
- Los movimientos validan cantidad positiva y bloquean stock negativo.

---

## Funcionalidades

**Autenticación**

- Registro y login de usuarios
- Tokens JWT con access token y rate limiting
- Roles: `admin` y `viewer`
- Endpoints protegidos por rol

**Productos**

- CRUD completo de productos
- Gestión de categorías
- Filtros por categoría, estado y stock
- Paginación de resultados
- Soft delete (desactivar sin borrar)

**Inventario**

- Registro de entradas y salidas de stock
- Historial completo de movimientos por producto
- Alertas automáticas de stock bajo
- Validación de stock insuficiente en salidas

---

## Endpoints

| Método | Endpoint                       | Descripción              | Auth  |
| ------ | ------------------------------ | ------------------------ | ----- |
| POST   | `/auth/registro`               | Registrar usuario        | No    |
| POST   | `/auth/login`                  | Login, retorna JWT       | No    |
| GET    | `/auth/me`                     | Datos del usuario actual | Sí    |
| GET    | `/productos/`                  | Listar productos         | Sí    |
| POST   | `/productos/`                  | Crear producto           | Admin |
| GET    | `/productos/{id}`              | Obtener producto         | Sí    |
| PATCH  | `/productos/{id}`              | Actualizar producto      | Admin |
| DELETE | `/productos/{id}`              | Desactivar producto      | Admin |
| GET    | `/productos/categorias`        | Listar categorías        | Sí    |
| POST   | `/productos/categorias`        | Crear categoría          | Admin |
| POST   | `/inventario/movimiento`       | Registrar movimiento     | Sí    |
| GET    | `/inventario/movimientos/{id}` | Historial de producto    | Sí    |
| GET    | `/inventario/alertas`          | Productos con stock bajo | Sí    |

---

## Correr localmente

**Requisitos:** Python 3.11+, Docker Desktop

```bash
# Clona el repo
git clone https://github.com/Vicente28CF/inventario-api.git
cd inventario-api

# Crea el entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Instala dependencias
pip install -r requirements-dev.txt

# Configura variables de entorno
cp .env.example .env
# Edita .env con tus credenciales

# Levanta PostgreSQL con Docker
docker-compose up -d

# Aplica migraciones
alembic upgrade head

# Corre el servidor
uvicorn app.main:app --reload
```

> En Windows también puedes usar `start.bat` para los últimos tres pasos.

API disponible en `http://localhost:8000/docs`

---

## Variables de entorno

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/inventario_db
SECRET_KEY=tu_secret_key_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
TESTING=false
```

---

## Tests

```bash
pytest
pytest --cov=app
```

```
tests/test_auth.py::test_registro_exitoso PASSED
tests/test_auth.py::test_registro_email_duplicado PASSED
tests/test_auth.py::test_login_exitoso PASSED
tests/test_auth.py::test_login_credenciales_incorrectas PASSED
tests/test_auth.py::test_me_autenticado PASSED
tests/test_auth.py::test_me_sin_token PASSED
tests/test_productos.py::test_crear_producto_como_admin PASSED
tests/test_productos.py::test_crear_producto_sin_permiso PASSED
tests/test_productos.py::test_listar_productos PASSED
tests/test_productos.py::test_obtener_producto_no_existe PASSED
tests/test_productos.py::test_crear_categoria_como_admin PASSED
tests/test_productos.py::test_movimiento_entrada PASSED
tests/test_productos.py::test_movimiento_salida_stock_insuficiente PASSED

19 passed
```

---

## Migraciones

```bash
# Aplicar migraciones pendientes
alembic upgrade head

# Crear nueva migración
alembic revision -m "descripcion_del_cambio"

# Ver historial
alembic history
```

Migraciones relevantes:

- esquema inicial
- cambio de `precio` de `Float` a `Numeric(10,2)`

---

## CI/CD

Cada push activa automáticamente GitHub Actions:

- **test** — corre los 19 tests con SQLite en memoria
- **lint** — verifica calidad del código con `ruff`

Los merges a `main` y `develop` requieren que todos los checks pasen.

---

## Estructura del proyecto

```
inventario-api/
├── app/
│   ├── core/
│   │   ├── config.py       ← variables de entorno
│   │   ├── security.py     ← JWT y hashing
│   │   └── deps.py         ← dependencias de auth
│   ├── models/
│   │   ├── usuario.py
│   │   ├── producto.py
│   │   └── movimiento.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── productos.py
│   │   └── inventario.py
│   ├── schemas/
│   │   ├── usuario.py
│   │   └── producto.py
│   ├── services/           ← reglas de negocio
│   ├── database.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_productos.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── requirements.txt
```

---

## Mejoras futuras

- Refresh tokens
- Búsqueda por nombre y ordenamiento
- Auditoría detallada de cambios
- Cobertura de tests con métricas
- Observabilidad con logging estructurado

---

## Autor

**Vicente Cayetano** — [LinkedIn](https://www.linkedin.com/in/vicente-cayetano-3113322a9) · [Portafolio](https://vcayetano-dev.lovable.app)
