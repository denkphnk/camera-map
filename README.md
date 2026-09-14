# 🎥 Camera Map

Система управления камерами видеонаблюдения и загруженными видео.

---

## 🚀 Быстрый старт

```bash
git clone git@github.com:denkphnk/camera-map.git
cd camera-map
docker compose up -d
docker compose exec api python3 scripts/seed_cameras.py
docker compose exec api alembic upgrade head
```

**Frontend:** http://localhost:5173

**Backend API:** http://localhost:8000/docs

---

## 🛠 Стек

### Backend

* Python 3.12
* FastAPI
* SQLAlchemy 2.0
* PostgreSQL 16
* Alembic
* Pydantic v2
* JWT Authentication
* Redis
* MinIO (S3)

### Frontend

* React
* TypeScript
* Vite
* Mantine UI
* React Query
* React Router
* Mapbox GL

### Infrastructure

* Docker
* Docker Compose

---

## 📊 Основные сущности

```
User (1)
 └─── (N) Video

Camera (1)
 └─── (N) Video
```

### User

* Регистрация
* Авторизация
* JWT + Refresh Token
* Личный кабинет

### Camera

* Карта камер
* GeoJSON представление
* Поиск и фильтрация
* Привязка видео

### Video

* Загрузка MP4
* Валидация файла
* Хранение в MinIO
* Автоматическое создание превью
* Просмотр и удаление

---

## 🗺 Основной функционал

### Авторизация

* Регистрация пользователя
* Вход по email и паролю
* JWT Access Token
* Refresh Token

### Карта камер

* Отображение камер на карте Mapbox
* GeoJSON формат данных
* Поиск по названию и адресу
* Фильтрация по:

  * модели камеры
  * типу камеры
  * классу камеры
  * количеству видео

### Видео

* Загрузка видео для выбранной камеры
* Проверка формата MP4
* Сохранение видео в MinIO
* Сохранение первого кадра как превью
* Просмотр видео через стриминг
* Удаление видео

### Личный кабинет

* Информация о пользователе
* Мои видео
* Все видео системы
* Поиск по названию видео
* Поиск по пользователю

### Кэширование

* Хранение GeoJSON камер в Redis
* Автоматическая инвалидация кэша после изменения данных

---

## 🔌 Основные эндпоинты

### Auth

| Метод | Эндпоинт         |
| ----- | ---------------- |
| POST  | `/auth/register` |
| POST  | `/auth/login`    |
| POST  | `/auth/refresh`  |

### Users

| Метод | Эндпоинт    |
| ----- | ----------- |
| GET   | `/users/me` |

### Cameras

| Метод | Эндпоинт           |
| ----- | ------------------ |
| GET   | `/cameras`         |
| GET   | `/cameras/geojson` |
| GET   | `/cameras/{id}`    |

### Videos

| Метод  | Эндпоинт               |
| ------ | ---------------------- |
| POST   | `/videos/upload`       |
| GET    | `/videos/me`           |
| GET    | `/videos`              |
| GET    | `/videos/{id}/stream`  |
| GET    | `/videos/{id}/preview` |
| DELETE | `/videos/{id}`         |

📖 **Полная документация:** `/docs`

---

## 🐳 Сервисы

| Сервис        | Порт |
| ------------- | ---- |
| API           | 8000 |
| Frontend      | 5173 |
| PostgreSQL    | 5432 |
| Redis         | 6379 |
| MinIO API     | 9000 |
| MinIO Console | 9001 |

---

## 🗄 Хранилище

### PostgreSQL

Хранит:

* пользователей
* камеры
* видео
* refresh-токены

### Redis

Хранит:

* GeoJSON камер
* кэш часто используемых данных

### MinIO

Хранит:

* исходные видеофайлы
* превью первого кадра

---

## 🔐 Безопасность

* Хранение паролей в виде хеша
* JWT Access Token
* Refresh Token
* Проверка прав на удаление видео
* Валидация загружаемых файлов

```
