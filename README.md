# Mini CRM

Небольшое full-stack приложение для учёта клиентских заявок. Проект сделан на Django и подходит как стартовый кейс для портфолио: есть интерфейс менеджера, форма создания заявки и простое API.

## Что умеет проект

- создание заявок через веб-форму;
- просмотр заявок в общей таблице;
- фильтрация по статусу;
- поиск по имени и телефону;
- обновление статуса заявки;
- JSON API для списка заявок и изменения статуса.

## Стек

- Python 3.11+
- Django 5
- SQLite
- HTML / CSS / Bootstrap 5

## Быстрый запуск на Windows 10 через VS Code

### 1. Открой проект в VS Code

Распакуй архив и открой папку `mini_crm_vscode_windows`.

### 2. Создай виртуальное окружение

Открой терминал PowerShell в VS Code и выполни команды:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Если PowerShell ругается на выполнение скриптов:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

После этого снова выполни:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Примени миграции

```powershell
python manage.py migrate
```

### 4. Запусти проект

```powershell
python manage.py runserver
```

Открой в браузере:

```text
http://127.0.0.1:8000/
```

## Создание администратора

Если хочешь работать через Django Admin:

```powershell
python manage.py createsuperuser
```

После этого панель будет доступна по адресу:

```text
http://127.0.0.1:8000/admin/
```

## API

### Получить список заявок

```http
GET /api/leads/
```

### Получить одну заявку

```http
GET /api/leads/1/
```

### Создать заявку

```http
POST /api/leads/
Content-Type: application/json
```

Пример тела:

```json
{
  "full_name": "Иван Петров",
  "phone": "+7 999 123-45-67",
  "email": "ivan@example.com",
  "company": "Alpha Studio",
  "source": "telegram",
  "budget": 60000,
  "comment": "Нужен сайт под ключ"
}
```

### Обновить статус

```http
PATCH /api/leads/1/
Content-Type: application/json
```

Пример тела:

```json
{
  "status": "in_progress"
}
```

## Возможные доработки

- авторизация менеджеров;
- отдельные карточки клиентов;
- экспорт в Excel;
- подключение PostgreSQL;
- Docker-сборка;
- комментарии по этапам сделки.

## Как оформить проект на GitHub

- добавь 2–3 скриншота интерфейса;
- напиши в описании репозитория: `Мини-CRM для обработки входящих заявок`;
- укажи стек: `Django, SQLite, Bootstrap, REST API`.
# Mini-CRM
