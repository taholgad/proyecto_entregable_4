# Task Manager API - Entregable 4

## Descripcion
Task Manager es una API y aplicacion web para gestionar historias de usuario y tareas con soporte de generacion asistida por IA.

El proyecto fue desarrollado en entregables previos con FastAPI, SQLAlchemy, MySQL y Pydantic. En este Entregable 4 se incorpora contenerizacion con Docker y CI/CD con GitHub Actions sin modificar la logica de negocio.

## Nota sobre la adaptacion del enunciado
El enunciado original menciona Flask y puerto 5000. Este proyecto reutiliza FastAPI, por lo que se utiliza Uvicorn y puerto 8000, manteniendo equivalencia funcional con lo solicitado.

## Arquitectura
~~~text
task_manager_app/
├── app/
│   ├── controllers/
│   ├── database/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── api/
├── prompts/
├── schemas/
├── services/
├── templates/
├── tests/
├── .github/workflows/docker.yml
├── Dockerfile
├── .dockerignore
├── requirements.txt
└── README.md
~~~

## Requisitos previos
- Python 3.12+
- MySQL 8+
- Docker Desktop (para build y run local de contenedor)
- Cuenta Docker Hub (para publicacion)
- Repositorio GitHub (para pipeline)

## Variables de entorno
Crear archivo .env en la raiz de task_manager_app:

~~~env
# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=task_manager

# Azure OpenAI
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://your-resource.openai.azure.com
OPENAI_API_VERSION=2024-10-21
OPENAI_MODEL=gpt-4-mini

# Debug
DEBUG=True
~~~

## Ejecucion local sin Docker
~~~bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
~~~

API en: http://localhost:8000

## Construccion y ejecucion con Docker
### Build de imagen
~~~bash
docker build -t task-manager-app:local .
~~~

### Run del contenedor
~~~bash
docker run --rm -p 8000:8000 --env-file .env task-manager-app:local
~~~

### Validacion
Abrir:
- http://localhost:8000/docs

## Pipeline CI/CD (GitHub Actions)
Archivo: .github/workflows/docker.yml

El pipeline ejecuta:
1. Test
- Instala dependencias
- Ejecuta pytest -v

2. Build and Push
- Construye imagen Docker
- Publica en Docker Hub en eventos push (no en pull_request)
- Etiquetas:
  - latest
  - sha del commit

## Secrets requeridos en GitHub
Configurar en Settings > Secrets and variables > Actions:
- DOCKER_USERNAME
- DOCKER_PASSWORD (token recomendado)

## Publicacion en Docker Hub (Fase 5)
1. Crear repositorio en Docker Hub, por ejemplo: task-manager-app
2. Verificar que IMAGE_NAME en workflow coincide con el repositorio
3. Hacer push a main/master para disparar build y push automatico

## Pruebas automaticas (Fase 4)
Suite ejecutable en local:
~~~bash
pytest -v
~~~

Cobertura funcional incluida:
- GET de comprobacion de API
- CRUD de tareas
- CRUD de historias de usuario
- Generacion de historias y tareas mediante IA con mocks

Resultado validado localmente:
- 35 pruebas pasadas

## Validacion completa (Fase 6)
Estado actual:
- Build correcto en entorno Python local: OK
- Tests superados: OK (35 passed)
- Imagen publicada: pendiente de ejecutar en GitHub Actions con Docker Hub secrets
- Aplicacion accesible en contenedor: pendiente en este entorno (Docker CLI no disponible en la maquina durante la verificacion)
- Swagger, CRUD y generacion IA: validados por pruebas automatizadas

## Endpoints principales
### Historias de usuario
- GET /api/user-stories/
- GET /api/user-stories/{id}
- POST /api/user-stories/
- PUT /api/user-stories/{id}
- DELETE /api/user-stories/{id}
- POST /api/user-stories/generate

### Tareas
- GET /api/tasks/
- GET /api/tasks/{id}
- POST /api/tasks/
- PUT /api/tasks/{id}
- DELETE /api/tasks/{id}
- POST /api/tasks/user-stories/{story_id}/generate-tasks

## Enlaces del entregable
- Repositorio GitHub: https://github.com/USUARIO/REPOSITORIO
- Imagen Docker Hub: https://hub.docker.com/r/USUARIO/task-manager-app

Sustituir USUARIO/REPOSITORIO por los valores reales del proyecto.
