# Expense Tracker on Kubernetes

This repository contains my submission for `CSG527 Cloud Computing - Lab Assignment 4` at BITS Pilani, Hyderabad Campus. The project demonstrates how a simple Python Flask application can be containerized, deployed, scaled, and managed on Kubernetes, with bonus work covering Ingress, ConfigMaps, Secrets, a multi-tier setup, and Jenkins-based CI/CD pipeline integration.

## Assignment Objective

The goal of this assignment is to design, deploy, and manage a scalable containerized application using Kubernetes. For this submission, the chosen application is an `Expense Tracker` built with Flask. It supports:

- Adding an expense with title, amount, and category
- Viewing the current expense list
- Deleting an expense entry

Because the app uses in-memory storage, it is simple, lightweight, and suitable for demonstrating container orchestration concepts such as replica management, rolling updates, and service exposure.

## Project Architecture

The final implementation uses a multi-tier structure:

- `Flask backend` serves the application logic and HTML templates on port `5000`
- `NGINX frontend` acts as a reverse proxy and exposes the application on port `80`
- `Kubernetes` manages deployments, services, ingress, configuration, and scaling

Request flow:

`User -> Ingress -> frontend-service (NGINX) -> expense-service (Flask backend)`

## Technologies Used

- `Python Flask` for the application
- `Docker` for containerization
- `Kubernetes` for orchestration
- `Minikube` or Docker Desktop Kubernetes for local cluster execution
- `kubectl` for cluster management
- `NGINX` for frontend reverse proxy
- `Jenkins` for CI/CD pipeline demonstration

## Repository Structure

- `app.py` - Flask application
- `templates/` - HTML template(s)
- `static/` - CSS assets
- `Dockerfile` - backend container image definition
- `requirements.txt` - Python dependencies
- `deployment.yaml` - backend deployment with `5` replicas
- `service.yaml` - backend ClusterIP service
- `configmap.yaml` - app configuration values
- `secret.yaml` - secret-based environment values
- `ingress.yaml` - Ingress routing to the frontend
- `nginx-frontend/` - NGINX frontend image and Kubernetes manifest

## Assignment Coverage

This repository reflects the final runnable setup submitted for the assignment. Across the implementation and report, the following phases and bonus tasks were completed:

### Core Assignment Phases

1. Environment setup using Docker, `kubectl`, and Kubernetes/Minikube
2. Application containerization using Docker
3. Kubernetes deployment using manifests
4. Service exposure for application access
5. Scaling and rolling updates
6. Documentation and analysis

### Bonus Tasks Completed

- `Ingress` configuration for hostname-based access
- `ConfigMaps and Secrets` for runtime configuration injection
- `Multi-tier deployment` using Flask backend + NGINX frontend
- `CI/CD pipeline integration using Jenkins`

## Local Application Run

To run the Flask app directly without Docker or Kubernetes:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open:

`http://127.0.0.1:5000`

## Docker Build

### Build backend image

```powershell
docker build -t expense-tracker:v3 .
```

### Build frontend image

```powershell
docker build -t nginx-frontend:v1 .\nginx-frontend
```

## Kubernetes Deployment

This final version uses locally built image tags:

- `expense-tracker:v3`
- `nginx-frontend:v1`

Build these images before applying the manifests.

### Apply manifests

```powershell
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f .\nginx-frontend\frontend-deployment.yaml
kubectl apply -f ingress.yaml
```

### Verify resources

```powershell
kubectl get pods
kubectl get services
kubectl get ingress
```

### If your cluster cannot see local Docker images

For `Minikube`:

```powershell
minikube image load expense-tracker:v3
minikube image load nginx-frontend:v1
```

For `kind`:

```powershell
kind load docker-image expense-tracker:v3
kind load docker-image nginx-frontend:v1
```

If pods enter `ErrImageNeverPull`, rebuild or load the images into the same runtime used by the cluster, then restart the deployments:

```powershell
kubectl rollout restart deployment expense-deployment
kubectl rollout restart deployment frontend-deployment
kubectl get pods
```

## Ingress Access

This project uses an NGINX Ingress controller and the host:

`expense.local`

If you are using Minikube:

```powershell
minikube addons enable ingress
minikube tunnel
```

Add this entry to your Windows hosts file if needed:

```text
127.0.0.1 expense.local
```

Then open:

`http://expense.local`

## Configuration Management

The application demonstrates Kubernetes configuration injection using:

- `ConfigMap` for `APP_TITLE`
- `Secret` for `ADMIN_EMAIL`

These values are injected into the Flask container as environment variables during deployment.

## Scaling and Updates

The backend deployment is configured with:

- `5 replicas` in `deployment.yaml`
- Kubernetes-managed rolling restarts through `kubectl rollout restart`

This supports the assignment requirement of demonstrating scalability and update management on Kubernetes.

## Jenkins CI/CD Integration

As documented in the accompanying report, the project also includes a Jenkins CI/CD pipeline implementation as a bonus task. The pipeline was configured in Jenkins as a `Declarative Pipeline` with three stages:

- `Build` - simulate Docker image build
- `Test` - simulate smoke or readiness testing
- `Deploy` - simulate Kubernetes deployment/update

The report records Jenkins running in Docker and executing a `Build -> Test -> Deploy` workflow successfully. This demonstrates how the Expense Tracker can be integrated into a basic automated delivery pipeline for containerized Kubernetes deployments.

## Report Reference

Additional implementation details, screenshots, and Jenkins pipeline evidence are included in:

`LA4_Final_Report_with_Jenkins.pdf`

## Notes

- This repository represents the final working state of the assignment
- The app uses in-memory storage, so data is not persisted across pod restarts
- The Jenkins CI/CD work is documented in the report and complements the Kubernetes deployment workflow shown in this repository
