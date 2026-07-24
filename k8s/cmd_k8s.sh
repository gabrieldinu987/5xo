#1 Creaza namespace-ul pentru aplicatie
kubectl apply -f k8s/namespace.yaml

#2 Creaza deployment-ul pentru aplicatie
kubectl apply -f k8s/deployment.yaml

#3 Creaza service-ul pentru aplicatie
kubectl apply -f k8s/service.yaml