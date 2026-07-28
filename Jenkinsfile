pipeline {

    agent any

    environment {

        IMAGE_NAME = "5xo"
        IMAGE_TAG = "latest"

        K8S_NAMESPACE = "5xo"

        HOME = "/home/gabriel"
        MINIKUBE_HOME = "/home/gabriel/.minikube"
        KUBECONFIG = "/home/gabriel/.kube/config"
    }

    options {
        timestamps()
        disableConcurrentBuilds()

        buildDiscarder(logRotator(
            numToKeepStr: '10'
        ))
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment Info') {

            steps {

                sh '''
                echo "========== SYSTEM =========="

                whoami
                pwd

                echo
                echo "========== TOOLS =========="

                docker --version
                git --version
                python3 --version
                kubectl version --client
                minikube version

                echo
                echo "========== ENVIRONMENT =========="

                echo "HOME=$HOME"
                echo "MINIKUBE_HOME=$MINIKUBE_HOME"
                echo "KUBECONFIG=$KUBECONFIG"

                echo
                echo "========== CLUSTER =========="

                kubectl cluster-info

                echo
                kubectl get nodes

                echo
                docker images | grep ${IMAGE_NAME} || true
                '''
            }
        }

        stage('Build Docker Image') {

            steps {

                sh '''
                docker build \
                    -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Deploy to Kubernetes') {

            steps {

                sh '''

                kubectl apply -f k8s/namespace.yaml

                kubectl apply -f k8s/deployment.yaml

                kubectl apply -f k8s/service.yaml

                '''
            }
        }

        stage('Wait for Deployment') {

            steps {

                sh '''

                kubectl rollout status \
                    deployment/5xo \
                    -n ${K8S_NAMESPACE} \
                    --timeout=180s

                '''
            }
        }

        stage('Cluster Status') {

            steps {

                sh '''

                echo
                echo "========== PODS =========="

                kubectl get pods \
                    -n ${K8S_NAMESPACE} \
                    -o wide

                echo
                echo "========== DEPLOYMENTS =========="

                kubectl get deployments \
                    -n ${K8S_NAMESPACE}

                echo
                echo "========== SERVICES =========="

                kubectl get svc \
                    -n ${K8S_NAMESPACE}

                echo
                echo "========== EVENTS =========="

                kubectl get events \
                    -n ${K8S_NAMESPACE} \
                    --sort-by=.lastTimestamp

                '''
            }
        }

    }

    post {

        success {

            echo '''
==========================================
Pipeline completed successfully!
Application deployed to Kubernetes.
==========================================
'''
        }

        failure {

            sh '''

            echo
            echo "========== DEBUG =========="

            kubectl get all -n ${K8S_NAMESPACE} || true

            echo
            echo "========== POD DESCRIBE =========="

            kubectl describe pods \
                -n ${K8S_NAMESPACE} || true

            echo
            echo "========== POD LOGS =========="

            POD=$(kubectl get pods -n ${K8S_NAMESPACE} -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

            if [ ! -z "$POD" ]; then
                kubectl logs "$POD" -n ${K8S_NAMESPACE} || true
            fi

            '''

            echo 'Pipeline failed.'
        }

        always {

            cleanWs()

        }

    }

}