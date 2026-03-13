@echo off
call venv\Scripts\activate
docker-compose up -d
uvicorn app.main:app --reload