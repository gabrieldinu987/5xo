#!/bin/bash

set -e

echo "Deploying 5XO..."

kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml

echo "Deployment finished."

kubectl get pods
kubectl get svc