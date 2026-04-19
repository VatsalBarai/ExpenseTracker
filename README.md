# Expense Tracker

This repository contains coursework for the Kubernetes assignment.

This repository is organized around one final runnable setup:

- Flask backend in the project root
- NGINX frontend reverse proxy in `nginx-frontend/`
- Kubernetes manifests in the project root and `nginx-frontend/`

## Basic run flow

### Backend image

```powershell
docker build -t expense-tracker:v3 .
```

### Frontend image

```powershell
docker build -t nginx-frontend:v1 .\nginx-frontend
```

### Local Python run without Kubernetes

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`

## Kubernetes notes

This project uses local image tags in the manifests:

- `expense-tracker:v3`
- `nginx-frontend:v1`

Build those images before applying the manifests.

If your cluster is not using the same container runtime as your local Docker build, load the images into the cluster first.

### Docker Desktop Kubernetes

Usually the two `docker build` commands are enough.

### Minikube

```powershell
minikube image load expense-tracker:v3
minikube image load nginx-frontend:v1
```

### kind

```powershell
kind load docker-image expense-tracker:v3
kind load docker-image nginx-frontend:v1
```

### Kubernetes apply

```powershell
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f .\nginx-frontend\frontend-deployment.yaml
kubectl apply -f ingress.yaml
```

If pods show `ErrImageNeverPull`, build the images first in the same container runtime used by your Kubernetes cluster, then restart the deployments.

```powershell
kubectl rollout restart deployment expense-deployment
kubectl rollout restart deployment frontend-deployment
kubectl get pods
```

## Ingress access

Make sure an NGINX ingress controller is installed in your cluster.

If you are using Minikube:

```powershell
minikube addons enable ingress
minikube tunnel
```

Then add this entry to your Windows hosts file if needed:

```text
127.0.0.1 expense.local
```

Open `http://expense.local`

## Final structure

- `app.py`, `templates/`, `static/`: application code
- `Dockerfile`, `requirements.txt`: backend image build
- `deployment.yaml`, `service.yaml`, `configmap.yaml`, `secret.yaml`, `ingress.yaml`: Kubernetes resources
- `nginx-frontend/`: frontend image and service/deployment manifest
