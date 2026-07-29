kubectl port-forward svc/fivexo-service 5000:5000 -n fivexo

kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090 -n monitoring

kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80 