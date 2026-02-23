# fastapi-devops-cicd

Демо-проект на FastAPI в стиле DevOps: CI/CD, контейнеризация, security-проверки и манифесты Kubernetes.

[![CI](https://github.com/Kytaalok/fastapi-devops-cicd/actions/workflows/ci.yml/badge.svg)](https://github.com/Kytaalok/fastapi-devops-cicd/actions/workflows/ci.yml)
[![CD](https://github.com/Kytaalok/fastapi-devops-cicd/actions/workflows/cd.yml/badge.svg)](https://github.com/Kytaalok/fastapi-devops-cicd/actions/workflows/cd.yml)

## Стек

- FastAPI
- Pytest
- Ruff
- Docker / Docker Compose
- GitHub Actions
- GHCR
- Kubernetes (Minikube)

## Быстрый старт (5 минут)

### 1) Локальный запуск через Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

### 2) Открой эндпоинты

- Swagger UI: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`
- Корень: `http://localhost:8000/`
- Версия: `http://localhost:8000/version`

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

## Проверки качества и тесты

```bash
ruff check .
ruff format --check .
pytest -q
pip-audit -r requirements.txt
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
Если в твоей организации требуется PAT, добавь секрет репозитория и замени `password` в `cd.yml`.

## Деплой в Kubernetes (Minikube)

Проверь, что образ в `k8s/deployment.yaml` указывает на твой GHCR (`ghcr.io/kytaalok/fastapi-devops-cicd:latest`), затем:

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
