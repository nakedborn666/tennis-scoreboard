# Tennis Scoreboard

Веб-приложение для ведения счёта теннисных матчей. 

## Возможности

- создание нового матча по именам двух игроков;
- подсчёт очков, геймов, сетов и тай-брейков;
- автоматическое определение победителя;
- просмотр текущего счёта матча;
- список завершённых матчей;
- фильтрация завершённых матчей по имени игрока;
- пагинация списка матчей;
- обработка ошибок с HTTP-статусами 400, 404, 405, 409 и 500;
- адаптивная HTML-вёрстка и статические ресурсы.

## Стек

- Python
- WSGI
- Waitress
- Jinja2
- SQLAlchemy
- Alembic
- MySQL
- pytest



## Локальный запуск

Необходимо склонировать репозиторий:

```bash
git clone https://github.com/nakedborn666/tennis-scoreboard.git
cd tennis-scoreboard
```

Создай виртуальное окружение и установи зависимости:

```bash
python -m venv .venv
```


```powershell
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip install -e .
```

## Настройка MySQL



- база: `tennis`;
- пользователь: `tennis`;
- пароль: `12345`.



Создай базу и пользователя:

```sql
CREATE DATABASE IF NOT EXISTS tennis
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'tennis'@'localhost'
    IDENTIFIED BY '12345';

ALTER USER 'tennis'@'localhost'
    IDENTIFIED BY '12345';

GRANT ALL PRIVILEGES ON tennis.* TO 'tennis'@'localhost';

FLUSH PRIVILEGES;
```

Строка подключения находится в `src/tennis_scoreboard/config.py`.

## Миграции

Применить миграции:


```powershell
.venv\Scripts\python.exe -m alembic upgrade head
```



## Запуск


```powershell
.venv\Scripts\python.exe run.py
```
