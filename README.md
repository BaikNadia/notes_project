
---

# 📝 Notes API - Менеджер личных заметок

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0.3-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15.1-red.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

REST API для управления личными заметками с поддержкой тегов, поиска и фильтрации. 
Создано на Django REST Framework с использованием PostgreSQL.

## ✨ Возможности

### Реализовано в текущей версии

| Функция | Описание |
|---------|----------|
| ✅ **Аутентификация** | JWT-токены для безопасного доступа |
| ✅ **CRUD заметок** | Создание, чтение, обновление и удаление заметок |
| ✅ **Теги** | Добавление тегов к заметкам (создаются автоматически) |
| ✅ **Поиск** | Полнотекстовый поиск по заголовку и содержимому |
| ✅ **Фильтрация** | Фильтр заметок по тегам |
| ✅ **Сортировка** | Сортировка по дате создания/обновления и заголовку |
| ✅ **Пагинация** | По 10 заметок на страницу |
| ✅ **Изоляция данных** | Пользователи видят только свои заметки |
| ✅ **Админ-панель** | Удобное управление через Django Admin |

### В ближайших планах

| Функция | Статус | Описание |
|---------|--------|----------|
| 🚀 **Избранное** | Запланировано | Отметка важных заметок |
| 🚀 **Архив** | Запланировано | Скрытие неактуальных заметок без удаления |
| 🚀 **Экспорт данных** | Запланировано | Выгрузка заметок в JSON/CSV |
| 🚀 **Статистика** | Запланировано | Аналитика по заметкам и тегам |
| 🚀 **Версионирование** | В будущем | История изменений заметок |
| 🚀 **Вложения** | В будущем | Загрузка файлов к заметкам |

## 🚀 Быстрый старт

### Требования

- Python 3.10+
- PostgreSQL 15+
- Git

### Установка

1. **Клонируйте репозиторий**
```bash
git clone https://github.com/BaikNadia/notes_project.git
cd notes-api
```

2. **Создайте виртуальное окружение**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Установите зависимости**
```bash
pip install -r requirements.txt
```

4. **Настройте переменные окружения**
Создайте файл `.env` в корне проекта:
```env
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
DB_NAME=ваша_db
DB_USER=postgres
DB_PASSWORD=ваш_пароль
DB_HOST=localhost
DB_PORT=5432
```

5. **Создайте базу данных PostgreSQL**
```sql
CREATE DATABASE ваша_db;
```

6. **Примените миграции**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Создайте суперпользователя**
```bash
python manage.py createsuperuser
```

8. **Запустите сервер**
```bash
python manage.py runserver
```

## 📚 API Документация

### Базовый URL
```
http://localhost:8000/api/
```

### Аутентификация

**Получение токена доступа**
```http
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

**Ответ:**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIs...",
    "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Обновление токена**
```http
POST /api/token/refresh/
{
    "refresh": "your_refresh_token"
}
```

### Эндпоинты

#### Заметки

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/notes/` | Список всех заметок |
| POST | `/api/notes/` | Создать заметку |
| GET | `/api/notes/{id}/` | Получить заметку |
| PUT | `/api/notes/{id}/` | Обновить заметку |
| PATCH | `/api/notes/{id}/` | Частично обновить |
| DELETE | `/api/notes/{id}/` | Удалить заметку |

**Параметры запроса (GET /notes/):**
- `?search=текст` - поиск по заголовку и содержимому
- `?tags__name=python` - фильтр по тегу
- `?ordering=-created_at` - сортировка (created_at, updated_at, title)

**Пример создания заметки:**
```http
POST /api/notes/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "title": "Изучаем DRF",
    "content": "Сегодня начал изучать Django REST Framework",
    "tag_names": ["python", "django", "learning"]
}
```

**Ответ:**
```json
{
    "id": 1,
    "title": "Изучаем DRF",
    "content": "Сегодня начал изучать Django REST Framework",
    "created_at": "2026-04-03T10:00:00Z",
    "updated_at": "2026-04-03T10:00:00Z",
    "author": "admin",
    "tags": [
        {"id": 1, "name": "python"},
        {"id": 2, "name": "django"},
        {"id": 3, "name": "learning"}
    ]
}
```

#### Теги

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/tags/` | Список тегов пользователя |
| GET | `/api/tags/{id}/` | Информация о теге |

## 💡 Варианты использования

### 1. 🧑‍💻 Для разработчиков

**Личная база знаний**
```bash
# Сохранить решение проблемы
curl -X POST http://localhost:8000/api/notes/ \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Фикс бага с миграциями",
    "content": "Решение: удалить все миграции и выполнить makemigrations заново",
    "tag_names": ["django", "debug", "solution"]
  }'

# Найти все решения по Django
curl -X GET "http://localhost:8000/api/notes/?search=решение&tags__name=django" \
  -H "Authorization: Bearer $TOKEN"
```

### 2. 📚 Для студентов

**Система конспектов**
```python
import requests

# Конспект лекции
note = {
    "title": "Лекция 5: SQL JOINs",
    "content": "INNER JOIN, LEFT JOIN, RIGHT JOIN - примеры использования...",
    "tag_names": ["sql", "database", "university", "2026"]
}
requests.post("http://localhost:8000/api/notes/", json=note, headers=headers)

# Подготовка к экзамену - собрать все по SQL
notes = requests.get(
    "http://localhost:8000/api/notes/?search=SQL&ordering=title",
    headers=headers
).json()
```

### 3. 📝 Для блогеров и писателей

**Контент-план**
```bash
# Идея для статьи
POST /api/notes/
{
    "title": "10 ошибок начинающего Django разработчика",
    "content": "1. Неправильная настройка settings.py\n2. Игнорирование миграций...",
    "tag_names": ["blog", "draft", "article", "python"]
}

# Готовые статьи к публикации
GET /api/notes/?search=ready&ordering=-updated_at
```

### 4. 🏢 Для менеджеров проектов

**Управление задачами**
```json
// Протокол встречи
{
    "title": "Спринт-ретроспектива 15.04",
    "content": "Что сделано хорошо:\n- Закрыли 15 багов\nЧто улучшить:\n- Больше тестов",
    "tag_names": ["sprint", "retro", "team"]
}

// To-Do лист
{
    "title": "Задачи на неделю",
    "content": "☐ Согласовать бюджет\n☐ Провести 1-1 с командой\n☐ Подготовить отчёт",
    "tag_names": ["todo", "work", "urgent"]
}
```

### 5. 🏠 Для домашнего использования

**Кулинарная книга**
```python
# Рецепт
recipe = {
    "title": "Паста Карбонара",
    "content": "Ингредиенты:\n- Спагетти 200г\n- Панчетта 100г\n- Яйца 2шт\n- Пармезан 50г",
    "tag_names": ["recipe", "italian", "dinner", "quick"]
}
```

**Список покупок**
```bash
GET /api/notes/?search=купить&ordering=-created_at
```

### 6. 🔌 Интеграция с другими сервисами

**Telegram бот** (пример)
```python
# Можно обернуть API в телеграм-бота
@bot.message_handler(commands=['note'])
def save_note(message):
    response = requests.post(
        "http://api.example.com/notes/",
        json={"title": message.text, "tag_names": ["telegram"]},
        headers={"Authorization": f"Bearer {token}"}
    )
```

## 🛠 Технологии

- **Backend:** Django 5.0.3, Django REST Framework 3.15.1
- **База данных:** PostgreSQL
- **Аутентификация:** JWT (Simple JWT)
- **Фильтрация:** Django Filter
- **Язык:** Python 3.10+

## 📁 Структура проекта

```
notes-api/
├── notes_project/          # Основная конфигурация проекта
│   ├── settings.py        # Настройки Django
│   ├── urls.py            # Главные URL-маршруты
│   └── wsgi.py            # WSGI конфигурация
├── notes_api/              # Основное приложение
│   ├── models.py          # Модели данных
│   ├── serializers.py     # Сериализаторы DRF
│   ├── views.py           # API вьюхи
│   ├── urls.py            # API маршруты
│   └── admin.py           # Настройка админки
├── .env                   # Переменные окружения
├── requirements.txt       # Зависимости
└── manage.py             # Django management скрипт
```

## 🧪 Тестирование API (примеры с curl)

### Получить токен
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Создать заметку
```bash
curl -X POST http://localhost:8000/api/notes/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Идея для приложения",
    "content": "Создать менеджер паролей",
    "tag_names": ["idea", "project"]
  }'
```

### Поиск заметок
```bash
# Найти по слову
curl -X GET "http://localhost:8000/api/notes/?search=идея" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Отфильтровать по тегу
curl -X GET "http://localhost:8000/api/notes/?tags__name=python" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Комбинированный запрос
curl -X GET "http://localhost:8000/api/notes/?search=django&ordering=-created_at" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔄 Дорожная карта улучшений

### Этап 1: Улучшение пользовательского опыта (2-3 дня)
- [ ] Добавить избранное (`is_favorite` поле)
- [ ] Добавить архив (`is_archived` поле)
- [ ] Массовое удаление заметок
- [ ] Копирование заметок

### Этап 2: Расширенный функционал (3-5 дней)
- [ ] Экспорт заметок в JSON/CSV
- [ ] Статистика использования (количество заметок по тегам)
- [ ] Отображение популярных тегов
- [ ] Автосохранение черновиков

### Этап 3: Интеграции и автоматизация (5-7 дней)
- [ ] Регистрация пользователей (djoser)
- [ ] Восстановление пароля по email
- [ ] Webhook уведомления при создании заметки
- [ ] Telegram бот для заметок

### Этап 4: Производительность и масштабирование (неделя)
- [ ] Кэширование (Redis)
- [ ] Пагинация с курсорами для больших объемов
- [ ] Полнотекстовый поиск (PostgreSQL Search)
- [ ] Rate limiting для API

### Этап 5: Дополнительные возможности (по мере необходимости)
- [ ] Версионирование заметок (история изменений)
- [ ] Вложения (файлы, изображения)
- [ ] Шаблоны заметок
- [ ] Совместный доступ к заметкам
- [ ] API версионирование (v1, v2)

## 🤝 Вклад в проект

Приветствуются pull requests и issues!

1. Форкните репозиторий
2. Создайте ветку для фичи (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Запушьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📄 Лицензия

MIT License - свободно используйте, модифицируйте и распространяйте.

## 🙏 Благодарности

- Django и DRF команде за отличные инструменты
- PostgreSQL за надежную базу данных
- Всем, кто тестирует и улучшает проект

## 📞 Контакты

- Автор: BaikNadia
- GitHub: https://github.com/BaikNadia
- Проект: https://github.com/BaikNadia/notes_project



---

**⭐ Поставьте звезду проекту, если он вам полезен!**

---
