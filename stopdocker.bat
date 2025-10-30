@echo off
call venv\Scripts\activate.bat
docker-compose -f docker-compose-dev.yml down 