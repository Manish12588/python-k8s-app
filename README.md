# python-k8s-app

A simple Python Flask app for Kubernetes practice.
Opens a webpage showing the tech stack and live system health of the pod.

## Tech Stack
- Python 3.11
- Flask 3.0
- Gunicorn (production server)
- psutil (system metrics)
- Port: 5000

## What the page shows
- Tech stack details
- Pod name, Pod IP, Namespace, Node name
- Memory usage with visual bar
- CPU usage percentage with visual bar
- Pod uptime

---

## Run locally

### Prerequisites
- Python 3.11+
- pip

```bash
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000

---

## Run with Docker

### Build
```bash
docker build -t YOUR_DOCKERHUB_USERNAME/python-k8s-app:latest .
```

### Run
```bash
docker run -p 5000:5000 YOUR_DOCKERHUB_USERNAME/python-k8s-app:latest
```
Open http://localhost:5000

### Push to Docker Hub
```bash
docker push YOUR_DOCKERHUB_USERNAME/python-k8s-app:latest
```

---

## Deploy to Kubernetes

### Step 1 — update image name
Open `k8s.yml` and replace `YOUR_DOCKERHUB_USERNAME` with your Docker Hub username.

### Step 2 — apply
```bash
kubectl apply -f k8s.yml
```

### Step 3 — verify
```bash
kubectl get pods
kubectl get svc
```

### Step 4 — access
```bash
kubectl port-forward service/python-app-service 5000:5000
```
Open http://localhost:5000

---

## Deploy in a namespace
```bash
kubectl create namespace dev
kubectl apply -f k8s.yml -n dev
kubectl port-forward service/python-app-service 5000:5000 -n dev
```

---

## Useful commands
```bash
kubectl logs python-app                  # view logs
kubectl describe pod python-app          # inspect pod
kubectl exec -it python-app -- sh        # shell into pod
kubectl delete -f k8s.yml               # delete pod and service
```
