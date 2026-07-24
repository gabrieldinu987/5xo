#!/bin/bash

set -e

echo
echo "==========================================="
echo " Deploying 5XO to Minikube"
echo "==========================================="
echo

echo "[1/5] Building Docker image..."

eval $(minikube docker-env)

docker build -t 5xo:latest .

echo
echo "[2/5] Creating namespace..."

kubectl apply -f k8s/namespace.yaml

echo
echo "[3/5] Deploying application..."

kubectl apply -f k8s/deployment.yaml

echo
echo "[4/5] Creating service..."

kubectl apply -f k8s/service.yaml

echo
echo "[5/5] Waiting for deployment..."

kubectl rollout status deployment/5xo -n 5xo

echo
echo "Pods:"
kubectl get pods -n 5xo

echo
echo "Services:"
kubectl get svc -n 5xo

echo
echo "Deployment finished successfully."

echo
echo "Application URL:"
minikube service 5xo-service -n 5xo --url