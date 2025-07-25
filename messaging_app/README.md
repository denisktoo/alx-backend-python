# 📨 Django Messaging API

A RESTful messaging API built with Django and Django REST Framework.

### ✅ Features

- JWT Authentication
- User Registration & Login
- User listing
- Conversations between users
- Message exchange within conversations
- Custom permissions (only participants can access)
- Pagination and Filtering

---

## 🚀 Getting Started

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🔌 API Endpoints

### 🔐 Auth

* `POST /api/register/`
  Example:

  ```json
  {
    "username": "Too",
    "email": "deniskiprotich746@gmail.com",
    "first_name": "Denis",
    "last_name": "Kiprotich",
    "password": "Too*#",
    "role": "guest"
  }
  ```

* `POST /api/token/`
  Example:

  ```json
  {
    "username": "Too",
    "password": "Too*#"
  }
  ```

* `POST /api/token/refresh/`

---

### 👤 Users

* `GET /api/users/`
  Returns a list of registered users.

---

### 💬 Conversations

* `GET /api/conversations/`
  Returns all conversations for the authenticated user.

* `POST /api/conversations/`
  Example:

  ```json
  {
    "participant_ids": [
      "bbf80c3b-84fc-4500-addc-ee1642c9d7e0",
      "52aefaed-a863-4078-80bf-3ace4029edf2"
    ]
  }
  ```

* `GET /api/conversations/<uuid:id>/`
  Example:
  `/api/conversations/600a1a2b-0daa-43d1-a32d-4315a6aac4d7/`

---

### 📨 Messages

* `GET /api/conversations/<uuid:conversation_id>/messages/`
  Example:
  `/api/conversations/600a1a2b-0daa-43d1-a32d-4315a6aac4d7/messages/`

* `POST /api/conversations/<uuid:conversation_id>/messages/`
  Example:

  ```json
  {
    "conversation": "206901b4-b389-4dd1-ad18-b16c24d1c929",
    "message_body": "Hey Denis, How are you?"
  }
  ```

---

## 🔒 Permissions

* Only participants of a conversation can:

  * View conversation details
  * Post messages
  * View messages

---

## 📚 Docs & References

* [Django REST Framework](https://www.django-rest-framework.org/)
* [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
* [DRF Pagination](https://www.django-rest-framework.org/api-guide/pagination/)
* [DRF Filtering](https://www.django-rest-framework.org/api-guide/filtering/)
* [DRF Permissions](https://www.django-rest-framework.org/api-guide/permissions/)

---
