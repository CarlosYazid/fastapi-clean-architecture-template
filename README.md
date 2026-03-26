# FastAPI Clean Architecture

Template base de FastAPI con arquitectura limpia, lista para producción y actualizada a las dependencias modernas.

> Fork y refactorización de [fastapi-clean-architecture](https://github.com/jujumilk3/fastapi-clean-architecture), adaptado para funcionar con el ecosistema Python actual.

![openapi-docs](./doc/images/openapi-docs-v1.png)

---

## Principios de diseño

1. **Funcionalidad mínima** — sólo lo esencial, sin sobreingeniería.
2. **Arquitectura convincente** — separación clara de responsabilidades.
3. **Fácil de leer** — código limpio, predecible y navegable.
4. **Compatibilidad** — funciona con las dependencias más recientes.
5. **Versatilidad** — base extensible para proyectos reales.

---

## Stack tecnológico

| Categoría | Tecnología |
|-----------|-----------|
| Runtime | Python 3.13+ |
| Framework | FastAPI 0.135+ |
| ORM | SQLModel + SQLAlchemy 2.0 (async) |
| Base de datos | PostgreSQL (asyncpg) |
| Migraciones | Alembic |
| Inyección de dependencias | dependency-injector |
| Autenticación | JWT (PyJWT + argon2) |
| Paginación | fastapi-pagination |
| Gestor de paquetes | uv |
| Linter/Formatter | ruff |
| Tests | pytest + pytest-asyncio |
| Servidor | Uvicorn / Gunicorn |
| Container | Docker |

---

## Modelos base

- **user** — entidad principal

---

## Estructura del proyecto

```
.
├── migrations/              # Migraciones Alembic
│   └── versions/
├── src/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/   # Routers: auth, user, ...
│   │       └── routes.py
│   ├── core/
│   │   ├── container.py     # Contenedor de DI
│   │   ├── database.py      # Sesiones async SQLAlchemy
│   │   ├── dependencies.py  # Guards de autenticación
│   │   ├── exceptions.py    # Excepciones HTTP tipadas
│   │   ├── security.py      # JWTBearer
│   │   └── settings.py      # Config via pydantic-settings
│   ├── model/               # Modelos SQLModel (tabla)
│   ├── repository/          # Patrón repositorio (CRUD base + especializaciones)
│   ├── schema/              # Schemas Pydantic (request/response)
│   ├── services/            # Lógica de negocio
│   └── util/                # Utilidades (auth, etc.)
├── tests/
│   ├── integration_tests/
│   ├── unit_tests/
│   └── test_data/
├── alembic.ini
└── pyproject.toml
```

---

## Entorno requerido

Crea un archivo `.env` en la raíz del proyecto:

```dotenv
# PostgreSQL
ENV=dev
DB=postgresql
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
DB_URI_MIGRATIONS=postgresql://tu_usuario:tu_password@localhost:5432/dev-fca

# Auth (opcional, tiene default)
SECRET_KEY=cambia-esto-en-produccion
```

> Los nombres de base de datos se resuelven automáticamente según `ENV`:
> `prod` → `fca`, `stage` → `stage-fca`, `dev` → `dev-fca`, `test` → `test-fca`

---

## Instalación y ejecución

### Docker
Este proyecto tiene 2 imagenes en [docker hub](https://hub.docker.com/r/carlosyazid/fastapi-clean-architecture-template):
- **Dev**: `docker pull carlosyazid/fastapi-clean-architecture-template:dev`
- **Prod**: `docker pull carlosyazid/fastapi-clean-architecture-template:prod`

### Local
Este proyecto usa [uv](https://github.com/astral-sh/uv) como gestor de paquetes.

```bash
cd src

# Instalar dependencias
uv sync --dev

# Levantar el servidor de desarrollo
uv run uvicorn app.main:app --reload

# Opciones adicionales
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Base de datos y migraciones (Alembic)

Todos los comandos se ejecutan desde la **raíz del proyecto**.

```bash
# Aplicar todas las migraciones
uv run alembic upgrade head

# Revertir todas las migraciones
uv run alembic downgrade base

# Generar nueva migración a partir de los modelos
uv run alembic -x ENV=dev revision --autogenerate -m "nombre_de_la_revision"

# Ver historial de revisiones
uv run alembic history
```

### Flujo para crear o modificar modelos

1. Crea o edita los modelos en `src/model/*.py`
2. Genera la migración: `uv run alembic -x ENV=dev revision --autogenerate -m "descripcion"`
3. Revisa el archivo generado en `migrations/versions/`
4. Aplica la migración: `uv run alembic -x ENV=dev upgrade head`

> Si no se especifica `ENV`, se aplica al entorno `test`.

---

## Tests

```bash
cd src

# Instalar dependencias
uv sync --group dev

# Ejecutar todos los tests
uv run pytest

# Con reporte de cobertura en consola
uv run pytest --cov=app --cov-report=term-missing

# Con reporte de cobertura en HTML
uv run pytest --cov=app --cov-report=html
```

Los tests de integración usan una base de datos PostgreSQL real. La variable `ENV=test` se establece automáticamente en el `conftest.py` y apunta a la base de datos `test-fca`.

---

## Linting y formateo

```bash
cd src

# Instalar dependencias
uv sync --group dev

# Formatear código
uv run ruff format . --line-length 120

# Revisar y corregir issues
uv run ruff check . --fix --line-length 120
```

El pipeline de CI aplica `ruff` automáticamente en cada push a `main` y hace commit de las correcciones.

---

## Autenticación

La autenticación se basa en JWT con roles:

| Endpoint | Acceso |
|----------|--------|
| `POST /api/v1/auth/sign-up` | Público |
| `POST /api/v1/auth/sign-in` | Público |
| `GET /api/v1/auth/me` | Usuario activo |
| `GET /api/v1/user` | Superusuario |
| `POST /api/v1/user` | Superusuario |
| `PATCH /api/v1/user` | Superusuario |
| `DELETE /api/v1/user/{id}` | Superusuario |

Los tokens se pasan como `Bearer` en el header `Authorization`.

---

## CI/CD (GitHub Actions)

| Workflow | Trigger | Descripción |
|----------|---------|-------------|
| `pytest.yml` | push a `main` | Ejecuta tests contra PostgreSQL real |
| `formatter.yml` | push a `main` | Aplica `ruff` y hace commit automático de fixes |

---

## Referencias

- [FastAPI — Documentación oficial](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Alembic — Tutorial oficial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Dependency Injector](https://python-dependency-injector.ets-labs.org/)
- [uv — Gestor de paquetes](https://github.com/astral-sh/uv)
- [Uvicorn](https://uvicorn.dev/)
- [Pytest](https://docs.pytest.org/en/stable/)
- [Docker](https://docs.docker.com/)
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/)