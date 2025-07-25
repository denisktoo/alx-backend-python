# 📨 Django Messaging API

A RESTful messaging API built with Django and Django REST Framework. Features include:

- JWT Authentication
- User Registration & Login
- Conversations between users
- Message exchange within conversations
- Custom permissions
- Pagination and filtering

---

## 🚀 Getting Started

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
````

---

## 🔌 API Endpoints

### Auth

* `POST /api/register/`
* `POST /api/token/`
* `POST /api/token/refresh/`

### Users

* `GET /api/users/`

### Conversations

* `GET/POST /api/conversations/`
* `GET /api/conversations/<id>/`

### Messages

* `GET/POST /api/conversations/<conversation_id>/messages/`

---

## 🔒 Permissions

Only conversation participants can view or send messages.

---

## 📚 Docs

* [Django REST Framework](https://www.django-rest-framework.org/)
* [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
* [DRF Pagination](https://www.django-rest-framework.org/api-guide/pagination/)
* [DRF Filtering](https://www.django-rest-framework.org/api-guide/filtering/)
* [DRF Permissions](https://www.django-rest-framework.org/api-guide/permissions/)

---
