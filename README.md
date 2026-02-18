# GCP Web Application

A full-stack, cloud-native web application for user authentication and document management, deployed on **Google Cloud Platform (GCP)** using **Kubernetes (GKE)** and **Cloud Build CI/CD**.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Local Development](#local-development)
- [Docker Setup](#docker-setup)
- [GCP Deployment](#gcp-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [API Reference](#api-reference)
- [Known Issues & Future Improvements](#known-issues--future-improvements)

---

## Overview

This application provides a web-based platform where users can register, log in, upload documents, and view their stored files. The backend is powered by **Flask (Python)**, the frontend is served via **Node.js/Express**, and documents are stored in **Google Cloud Storage**. User data is persisted in a **MySQL** database.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        GKE Cluster                          │
│                                                             │
│  ┌───────────────────┐         ┌────────────────────────┐   │
│  │  frontend-ns      │         │  backend-ns            │   │
│  │                   │         │                        │   │
│  │  Node.js/Express  │──HTTP──▶│  Flask REST API        │   │
│  │  (LoadBalancer)   │         │  (NodePort :5000)      │   │
│  │  Port: 3000       │         │                        │   │
│  └───────────────────┘         └──────────┬─────────────┘   │
│                                           │                 │
└───────────────────────────────────────────┼─────────────────┘
                                            │
                         ┌──────────────────|
                         │                  │        
                  ┌──────▼──────┐   ┌───────▼───────┐
                  │   MySQL DB  │   │  GCS Bucket   │
                  │  (Users)    │   │  (Documents)  │
                  └─────────────┘   └───────────────┘
```

- **Frontend** (Node.js) is exposed via a `LoadBalancer` service and acts as a proxy to the backend.
- **Backend** (Flask) handles all business logic and is exposed internally via `NodePort`.
- **MySQL** stores user credentials.
- **Google Cloud Storage** stores user-uploaded documents, organized by user email.

---

## Tech Stack

| Layer        | Technology                              |
|--------------|-----------------------------------------|
| Frontend     | HTML, CSS, JavaScript, Node.js, Express |
| Backend      | Python 3.12, Flask, Flask-CORS          |
| Database     | MySQL (`mysql-connector-python`)        |
| Storage      | Google Cloud Storage                    |
| Auth         | GCP Service Account (JSON key)          |
| Containers   | Docker (Python 3.12, Node.js 20)        |
| Orchestration| Kubernetes (GKE)                        |
| CI/CD        | Google Cloud Build                      |
| Registry     | Google Container Registry (GCR)         |

---

## Features

- User registration with name, email, and password
- User login with credential validation
- File/document upload to GCP Cloud Storage (per-user folder)
- List uploaded documents per user
- Dockerized frontend and backend
- Kubernetes deployment with separate namespaces
- Automated CI/CD via Google Cloud Build

---

## Project Structure

```
gcp-web-application/
├── backend/
│   ├── app.py                    # Flask application & API routes
│   ├── Dockerfile                # Backend container definition
│   ├── cloudbuild.yaml           # Backend CI/CD pipeline
│   ├── requirements.txt          # Python dependencies
│   ├── k8s-manifests/
│   │   └── deployment.yaml       # Backend K8s Deployment & Service
│   └── utils/
│       └── database.py           # MySQL helper functions
│
├── frontend/
│   ├── server.js                 # Express server & proxy to Flask
│   ├── Dockerfile                # Frontend container definition
│   ├── cloudbuild.yaml           # Frontend CI/CD pipeline
│   ├── package.json              # Node.js dependencies
│   ├── index.html                # Login page
│   ├── register.html             # Registration page
│   ├── dashboard.html            # Dashboard page
│   ├── js/
│   │   └── dashboard.js          # Dashboard frontend logic
│   ├── css/
│   │   ├── styles-login.css
│   │   ├── styles-register.css
│   │   └── styles-dashboard.css
│   └── k8s-manifests/
│       └── deployment.yaml       # Frontend K8s Deployment & Service
│
└── README.md
```

---

## Prerequisites

- [Python 3.12+](https://www.python.org/)
- [Node.js 20+](https://nodejs.org/)
- [Docker](https://www.docker.com/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Google Cloud SDK (`gcloud`)](https://cloud.google.com/sdk/docs/install)
- A **GCP Project** with the following enabled:
  - Google Kubernetes Engine (GKE) API
  - Google Cloud Storage API
  - Google Container Registry (GCR) API
  - Cloud Build API
- A **MySQL** database (Cloud SQL or self-hosted)
- A **GCP Service Account** with Storage Admin permissions (JSON key file)

---

## Environment Variables

### Backend (`.env` in `/backend`)

| Variable                        | Description                                  |
|----------------------------------|---------------------------------------------|
| `MYSQL_HOST`                    | MySQL host address                           |
| `MYSQL_USER`                    | MySQL username                               |
| `MYSQL_PASSWORD`                | MySQL password                               |
| `MYSQL_DB`                      | MySQL database name                          |
| `GOOGLE_APPLICATION_CREDENTIALS`| Path to GCP service account JSON key file    |
| `GCP_BUCKET_NAME`               | Name of the GCS bucket for document storage  |

**Example:**
```env
MYSQL_HOST=127.0.0.1
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DB=webapp_db
GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json
GCP_BUCKET_NAME=your-gcs-bucket-name
```

### Frontend (Environment variable / `.env`)

| Variable           | Description                                                 |
|--------------------|-------------------------------------------------------------|
| `FLASK_SERVER_URL` | URL of the Flask backend (default: `http://localhost:5000`) |
| `PORT`             | Port for the Node.js server (default: `3000`)               |

---

## Local Development

### 1. Clone the repository
```bash
git clone https://github.com/your-username/gcp-web-application.git
cd gcp-web-application
```

### 2. Set up the Backend
```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create your .env file with the required variables (see above)
cp .env.example .env

# Run the Flask server
python app.py
```
Flask will start at `http://localhost:5000`.

### 3. Set up the Frontend
```bash
cd frontend

# Install dependencies
npm install

# Set the backend URL (optional, defaults to localhost:5000)
export FLASK_SERVER_URL=http://localhost:5000

# Start the server
node server.js
```
The frontend will be available at `http://localhost:3000`.

---

## Docker Setup

### Build and run the backend
```bash
cd backend
docker build -t gcp-webapp-backend .
docker run -p 5000:5000 --env-file .env gcp-webapp-backend
```

### Build and run the frontend
```bash
cd frontend
docker build -t gcp-webapp-frontend .
docker run -p 3000:3000 -e FLASK_SERVER_URL=http://host.docker.internal:5000 gcp-webapp-frontend
```

---

## GCP Deployment

### 1. Authenticate with GCP
```bash
gcloud auth login
gcloud config set project flask-app-436123
```

### 2. Configure kubectl for GKE
```bash
gcloud container clusters get-credentials web-app-cluster --zone us-central1
```

### 3. Build and push Docker images to GCR
```bash
# Backend
docker build -t gcr.io/flask-app-436123/backend ./backend/
docker push gcr.io/flask-app-436123/backend

# Frontend
docker build -t gcr.io/flask-app-436123/frontend ./frontend/
docker push gcr.io/flask-app-436123/frontend
```

### 4. Deploy to Kubernetes
```bash
# Deploy backend
kubectl apply -f backend/k8s-manifests/deployment.yaml

# Deploy frontend
kubectl apply -f frontend/k8s-manifests/deployment.yaml
```

### 5. Verify deployments
```bash
kubectl get pods -n backend-ns
kubectl get pods -n frontend-ns

# Get the external IP of the frontend
kubectl get service node-frontend-service -n frontend-ns
```

Once the `EXTERNAL-IP` is assigned, open it in a browser on port `3000`.

---

## CI/CD Pipeline

CI/CD is handled by **Google Cloud Build**. Each service has its own `cloudbuild.yaml`.

### Backend Pipeline (`backend/cloudbuild.yaml`)
1. **Build** the Docker image tagged with the commit SHA
2. **Push** the image to GCR
3. **Deploy** by updating the Kubernetes deployment image

### Frontend Pipeline (`frontend/cloudbuild.yaml`)
1. **Build** the Docker image
2. **Push** to GCR
3. **Deploy** to the GKE frontend namespace

### Trigger Setup
Connect your GitHub repository to Cloud Build via the GCP Console:
1. Go to **Cloud Build → Triggers**
2. Create a trigger linked to your GitHub repo
3. Set the build configuration to the respective `cloudbuild.yaml`

Logs are stored in the `gs://gcp-app-logs` GCS bucket.

---

## API Reference

All API routes are served by the Flask backend on port `5000`.

### `POST /register`
Register a new user.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "yourpassword"
}
```
**Responses:**
- `200 OK` — `{ "message": "Successfully registered" }`
- `400 Bad Request` — Missing fields
- `500 Internal Server Error` — Registration failed

---

### `POST /login`
Authenticate an existing user.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "yourpassword"
}
```
**Responses:**
- `200 OK` — `{ "message": "Login successful" }`
- `401 Unauthorized` — `{ "message": "Invalid username or password" }`

---

### `POST /upload-document`
Upload a file to GCS for a specific user. Accepts `multipart/form-data`.

**Form Data:**
- `file` — The file to upload
- `email` — The user's email (used as the folder prefix in GCS)

**Responses:**
- `200 OK` — `{ "message": "File uploaded successfully" }`
- `400 Bad Request` — Missing file or email
- `500 Internal Server Error` — Upload failed

---

### `POST /list-documents`
List all documents uploaded by a user.

**Request Body:**
```json
{
  "email": "john@example.com"
}
```
**Response:**
```json
["document1.pdf", "report.docx", "image.png"]
```

---

## Known Issues & Future Improvements

| Issue | Recommended Fix |
|-------|-----------------|
| 🔴 Passwords stored in plain text | Implement password hashing with `bcrypt` |
| 🔴 No session/token management | Implement JWT-based authentication |
| 🟡 Email passed via URL query param | Use secure HTTP-only cookies or session tokens |
| 🟡 No input validation on API routes | Add schema validation (e.g., `marshmallow` or `pydantic`) |
| 🟡 GCS credentials loaded from JSON file | Use GKE Workload Identity instead of service account key files |
| 🟠 No HTTPS | Configure an Ingress with TLS termination |
| 🟠 Single replica deployments | Configure Horizontal Pod Autoscaler (HPA) |
| 🟢 No logging/monitoring | Integrate Google Cloud Logging and Monitoring |

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
