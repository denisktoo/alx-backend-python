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

Here’s your **README.md** with only the commands and instructions — no code blocks for `Dockerfile`, `docker-compose.yml`, or `settings.py`:

---

# Messaging App – Docker & Docker Compose Setup

Containerizes a Django-based messaging application using Docker and Docker Compose with a **MySQL** database.

---

## **Prerequisites**

* Install Docker
* Install Docker Compose
* Create a `.env` file containing your MySQL credentials (DB name, user, password, host, port, and MySQL root password)

---

## **Task 0 – Set up a Docker Environment**

**Steps:**

* Create a `requirements.txt` with your dependencies
* Create a Dockerfile for the Django app
* Build & run container:

```bash
docker build -t messaging-app .
docker run -p 8000:8000 messaging-app
```

---

## **Task 1 – Use Docker Compose for Multi-Container Setup**

**Steps:**

* Create a `docker-compose.yml` with a `web` service for Django and a `db` service for MySQL
* Update Django settings to use MySQL environment variables
* Run the app:

```bash
docker-compose up --build
```

---

## **Task 2 – Persist Data Using Volumes**

**Steps:**

* Add a named volume for MySQL data in `docker-compose.yml`
* Mount the volume to persist database data between container restarts

---

## **Common Management Commands**

**Run migrations:**

```bash
docker-compose exec web python manage.py migrate
```

**Collect static files:**

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

---

## **Stopping and Cleaning Up**

Stop containers:

```bash
docker-compose down
```

Stop and remove all containers, networks, and volumes:

```bash
docker-compose down -v
```
---

# **Kubernetes Deployment**

### **Task 0 – Install Kubernetes & Set Up Local Cluster**

**Description:** Start a Minikube cluster and verify it is running.

**File:** messaging_app/messaging_app/kurbeScript

**Commands:**

```bash
chmod +x messaging_app/messaging_app/kurbeScript
./messaging_app/messaging_app/kurbeScript
```

---

### **Task 1 – Deploy Django Messaging App on Kubernetes**

**Description:** Create a Deployment and ClusterIP Service for the Django app.

**File:** messaging_app/messaging_app/deployment.yaml

**Commands:**

```bash
kubectl apply -f messaging_app/messaging_app/deployment.yaml
kubectl get pods -l app=messaging-app
kubectl logs <pod-name>
```

---

### **Task 2 – Scale the Django App**

**Description:** Increase the number of replicas for the Django Deployment to handle more traffic.

**File:** messaging_app/messaging_app/kubctl-0x01

**Commands:**

```bash
chmod +x messaging_app/messaging_app/kubctl-0x01
./messaging_app/messaging_app/kubctl-0x01
kubectl get pods -l app=messaging-app
kubectl top pods
```

---

### **Task 3 – Set Up Kubernetes Ingress**

**Description:** Route external traffic to the Django service via an Ingress controller.

**Files:**

* messaging_app/messaging_app/ingress.yaml
* messaging_app/commands.txt

**Commands:**

```bash
# Enable ingress and apply config
bash messaging_app/commands.txt
```

---

### **Task 4 – Blue–Green Deployment Strategy**

**Description:** Deploy two versions of the app (blue and green) and switch traffic gradually to achieve zero downtime.

**Files:**

* messaging_app/blue_deployment.yaml
* messaging_app/kubeservice.yaml
* messaging_app/kubctl-0x02
* messaging_app/messaging_app/green_deployment.yaml

**Commands:**

```bash
chmod +x messaging_app/kubctl-0x02
./messaging_app/kubctl-0x02
kubectl get pods
```

---

### **Task 5 – Rolling Update**

**Description:** Update the Django app gradually without downtime by updating the Docker image in the blue deployment.

**Files:**

* messaging_app/messaging_app/blue_deployment.yaml
* messaging_app/kubctl-0x03

**Commands:**

```bash
chmod +x messaging_app/kubctl-0x03
./messaging_app/kubctl-0x03
kubectl get pods -l app=messaging-app-blue
```
