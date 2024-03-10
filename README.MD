## Приложение для учета рабочего времени сотрудников
### Описание
Приложение для учета рабочего времени сотрудников. Позволяет вести учет рабочего времени сотрудников, а также просматривать отчеты по рабочему времени.
### Технологии
- Python 3.10
- Django 5.0
- PostgreSQL 13
- Docker
- Docker-compose
- Git

### Установка
1. Склонировать репозиторий
2. Перейти в папку проекта
3. Создать файл .env, образец файл `example_env` и заполнить его необходимыми данными  
3.1. Для работы отправки писем через почтовый сервер, необходимо заполнить переменные `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
4. Запустить проект командой (предворительно установив Docker и Docker compose):  
4.1. При первом запуске будут созданы базы данных и применены миграции автоматически, а также создан суперпользователь. Изменить этот функционал можно в файле `entrypoint.sh`
```bash
docker compose up -d --build
```
5. Для остановки проекта выполнить команду:
```bash
docker compose down
```