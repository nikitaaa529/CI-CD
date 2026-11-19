# Практическая работа №2 — локальный CI/CD

## Состав проекта
- `app.py` — учебный файловый менеджер на Flask.
- `tests/` — автоматические тесты.
- `Dockerfile` — многоступенчатая сборка Docker-образа; приложение работает от непривилегированного пользователя.
- `.github/workflows/main.yml` — конвейер Build → Test → SAST → Deploy.
- `requirements*.txt` — зависимости Python.

## Локальный запуск приложения
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements-dev.txt
py -m pytest -v --junitxml=test-results.xml
py app.py
```
Открыть в браузере: http://localhost:8080

## Сборка и запуск Docker
```powershell
docker build -t local-file-manager:latest .
docker run --rm -d --name local-file-manager -p 8080:8080 local-file-manager:latest
```
Остановить:
```powershell
docker stop local-file-manager
```

## Локальный запуск GitHub Actions через act
Для запуска workflow локально нужны Git, act и Docker Desktop с Linux containers.
После установки act открыть PowerShell в корне проекта:
```powershell
act -W .github/workflows/main.yml -P ubuntu-latest=catthehacker/ubuntu:act-latest
```
Если Docker CLI недоступен внутри runner-контейнера или Docker socket не подключён, локальная джоба Deploy может потребовать отдельной настройки act. Не считать успешный запуск отдельных jobs доказательством успешного Deploy.

## Важное замечание
Токены и пароли в проект не добавляются. Для этого учебного приложения секреты не требуются.
