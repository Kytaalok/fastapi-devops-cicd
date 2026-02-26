# fastapi-devops-cicd

Демо-проект на FastAPI в стиле DevOps: CI/CD, контейнеризация, security-проверки и манифесты Kubernetes.

[![CI](https://github.com/Kytaalok/fastapi-devops-cicd/actions/workflows/ci.yml/badge.svg)](https://github.com/Kytaalok/fastapi-devops-cicd/actions/workflows/ci.yml)
[![CD](https://github.com/Kytaalok/fastapi-devops-cicd/actions/workflows/cd.yml/badge.svg)](https://github.com/Kytaalok/fastapi-devops-cicd/actions/workflows/cd.yml)

## Стек

- FastAPI + pydantic-settings (конфигурация)
- Prometheus-метрики (prometheus-fastapi-instrumentator)
- Структурированные JSON-логи (python-json-logger)
- Pytest
- Ruff (линтер + форматтер)
- Docker / Docker Compose (с HEALTHCHECK)
- GitHub Actions (CI + CD)
- GHCR (GitHub Container Registry)
- Kubernetes (Minikube)

## Быстрый старт (5 минут)

### 1) Локальный запуск через Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

### 2) Открой эндпоинты

| Эндпоинт | URL |
|---|---|
| Swagger UI | `http://localhost:8000/docs` |
| Health | `http://localhost:8000/health` |
| Корень | `http://localhost:8000/` |
| Версия | `http://localhost:8000/version` |
| Prometheus-метрики | `http://localhost:8000/metrics` |

## Локальная разработка (без Docker)

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Linux/macOS:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

## Конфигурация

Настройки управляются через переменные окружения или файл `.env` (см. `.env.example`):

| Переменная | По умолчанию | Описание |
|---|---|---|
| `APP_VERSION` | `0.1.0` | Версия приложения (отдаётся на `/version`) |
| `LOG_LEVEL` | `INFO` | Уровень логирования (DEBUG, INFO, WARNING, ERROR) |

Конфигурация описана в `app/config.py` через `pydantic-settings` с валидацией типов.

## Логирование

Логи выводятся в формате JSON для автоматического парсинга в ELK, Loki, CloudWatch:

```json
{"asctime": "2026-02-25 12:00:00", "levelname": "INFO", "name": "fastapi-devops-cicd", "message": "Root endpoint called"}
```

## Мониторинг (Prometheus)

Эндпоинт `GET /metrics` отдаёт метрики в формате Prometheus:

- `http_requests_total` — счётчик запросов по методу, пути и статус-коду
- `http_request_duration_seconds` — гистограмма латенси
- `http_request_size_bytes` / `http_response_size_bytes` — размеры запросов и ответов

Готово к подключению в Prometheus + Grafana без дополнительной настройки.

## Проверки качества и тесты

```bash
ruff check .                    # линтер
ruff format --check .           # проверка форматирования
pytest -q                       # тесты
pip-audit -r requirements.txt   # аудит уязвимостей зависимостей
```

## CI pipeline (`.github/workflows/ci.yml`)

Запускается на `push` и `pull_request` в `main`:

1. Checkout репозитория
2. Установка Python
3. Установка зависимостей
4. Ruff lint + проверка форматирования
5. Pytest
6. `pip-audit`
7. Сборка Docker-образа
8. Trivy-сканирование уязвимостей

## CD pipeline (`.github/workflows/cd.yml`)

Запускается при `push` в `main` и при тегах `v*`:

1. Настройка Buildx
2. Логин в GHCR
3. Сборка и push образа
4. Trivy-сканирование опубликованного образа

Теги образов:

- `latest` (для default branch)
- `sha-<commit>`
- `v*` (git-теги, например `v0.1.0`)

## GHCR (важно)

Workflow использует `${{ secrets.GITHUB_TOKEN }}` с правами `packages: write`.
Если в требуется PAT, добавь секрет репозитория и замени `password` в `cd.yml`.

## Docker

Multi-stage сборка (`python:3.11-slim`), non-root пользователь `appuser`, встроенный `HEALTHCHECK`:

```bash
docker build -t fastapi-devops-cicd .
docker run -p 8000:8000 fastapi-devops-cicd
docker ps   # покажет статус healthy/unhealthy
```

## Деплой в Kubernetes (Minikube)

Перед применением манифестов проверь, что в `k8s/deployment.yaml` указан актуальный образ.

```bash
kubectl apply -f k8s/
kubectl get pods,svc
kubectl port-forward svc/fastapi-devops-cicd 8080:80
curl http://localhost:8080/health
```

Альтернатива через URL от Minikube:

```bash
minikube service fastapi-devops-cicd --url
```
