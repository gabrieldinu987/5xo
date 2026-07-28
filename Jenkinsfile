pipeline {

    agent any

    environment {

    IMAGE_NAME = "5xo"
    IMAGE_TAG = "latest"
    K8S_NAMESPACE = "fivexo"

    }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment') {
            steps {
                sh '''
                set -e

                echo "========== USER =========="
                whoami
                pwd

                echo
                echo "========== TOOLS =========="
                docker --version
                kubectl version --client
                git --version
                python3 --version

                echo
                echo "========== KUBERNETES =========="
                kubectl config current-context
                kubectl cluster-info
                kubectl get nodes
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                set -e

                docker build \
                    -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Load Image into Minikube') {
            steps {
                sh '''
                set -e

                echo "Importing image into Minikube..."

                docker save ${IMAGE_NAME}:${IMAGE_TAG} | \
                docker exec -i minikube ctr -n=k8s.io images import -

                echo "Verifying image..."

                docker exec minikube ctr -n=k8s.io images ls | grep ${IMAGE_NAME}
                '''
            }
        }

        stage('Deploy Namespace') {
            steps {
                sh '''
                kubectl apply -f k8s/namespace.yaml
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                '''
            }
        }

        stage('Restart Deployment') {
            steps {
                sh '''
                kubectl rollout restart deployment/${DEPLOYMENT} -n ${NAMESPACE}

                kubectl rollout status deployment/${DEPLOYMENT} \
                    -n ${NAMESPACE} \
                    --timeout=180s
                '''
            }
        }

        stage('Cluster Status') {
            steps {
                sh '''
                echo
                echo "========== NODES =========="
                kubectl get nodes

                echo
                echo "========== DEPLOYMENTS =========="
                kubectl get deployment -n ${NAMESPACE}

                echo
                echo "========== PODS =========="
                kubectl get pods -n ${NAMESPACE} -o wide

                echo
                echo "========== SERVICES =========="
                kubectl get svc -n ${NAMESPACE}

                echo
                echo "========== EVENTS =========="
                kubectl get events -n ${NAMESPACE} --sort-by=.metadata.creationTimestamp
                '''
            }
        }

    }

    post {

        success {

            echo '''
==========================================
Deployment completed successfully
==========================================
'''
        }

        failure {

            sh '''
            echo
            echo "========== DEBUG =========="

            kubectl get all -n ${NAMESPACE} || true

            echo
            kubectl describe deployment ${DEPLOYMENT} -n ${NAMESPACE} || true

            echo
            kubectl describe pods -n ${NAMESPACE} || true

            echo
            kubectl logs -n ${NAMESPACE} -l app=5xo --all-containers=true || true

            echo
            kubectl get events -n ${NAMESPACE} --sort-by=.metadata.creationTimestamp || true
            '''
        }

        always {

            cleanWs()
        }
    }
}