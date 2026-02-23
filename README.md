# fastapi-devops-cicd

DevOps-style FastAPI project with CI/CD, containerization, security checks, and Kubernetes manifests.

[![CI](https://github.com/your-github-username/fastapi-devops-cicd/actions/workflows/ci.yml/badge.svg)](https://github.com/your-github-username/fastapi-devops-cicd/actions/workflows/ci.yml)
[![CD](https://github.com/your-github-username/fastapi-devops-cicd/actions/workflows/cd.yml/badge.svg)](https://github.com/your-github-username/fastapi-devops-cicd/actions/workflows/cd.yml)

## Stack

- FastAPI
- Pytest
- Ruff
- Docker / Docker Compose
- GitHub Actions
- GHCR
- Kubernetes (Minikube)

## Quick Start (5 minutes)

### 1) Run locally with Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

### 2) Open endpoints

- Swagger UI: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`
- Root: `http://localhost:8000/`
- Version: `http://localhost:8000/version`

## Local development (without Docker)

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

## Test and quality checks

```bash
ruff check .
ruff format --check .
pytest -q
pip-audit -r requirements.txt
```

## CI pipeline (`.github/workflows/ci.yml`)

Runs on push/PR to `main`:

1. Checkout
2. Setup Python
3. Install deps
4. Ruff lint + format check
5. Pytest
6. `pip-audit`
7. Docker image build
8. Trivy scan

## CD pipeline (`.github/workflows/cd.yml`)

Runs on push to `main` and tags `v*`:

1. Buildx setup
2. Login to GHCR
3. Build and push image
4. Trivy scan for pushed image

Image tags:

- `latest` (default branch)
- `sha-<commit>`
- `v*` (git tags, for example `v0.1.0`)

## GHCR notes

Workflow uses `${{ secrets.GITHUB_TOKEN }}` with `packages: write` permission.
If your organization requires PAT, add a repo secret and replace `password` in `cd.yml`.

## Kubernetes (Minikube) deploy

Update image in `k8s/deployment.yaml` to your GHCR path, then:

```bash
kubectl apply -f k8s/
kubectl get pods,svc
kubectl port-forward svc/fastapi-devops-cicd 8080:80
curl http://localhost:8080/health
```

Alternative with Minikube service URL:

```bash
minikube service fastapi-devops-cicd --url
```

