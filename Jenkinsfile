pipeline {

    agent any

    environment {

        IMAGE_NAME = "5xo"
        IMAGE_TAG  = "latest"

        K8S_NAMESPACE = "5xo"

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

                echo "========== KUBERNETES =========="

                kubectl config current-context
                kubectl get nodes

                '''

            }

        }

        stage('Install Dependencies') {

            steps {

                sh '''

                python3 -m pip install --upgrade pip

                pip3 install -r requirements.txt

                '''

            }

        }

        stage('Run Tests') {

            steps {

                sh '''

                pytest -v

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

        stage('Load Image into Minikube') {

            steps {

                sh '''

                minikube image load ${IMAGE_NAME}:${IMAGE_TAG}

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
                    -n ${K8S_NAMESPACE}

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
                echo "========== SERVICES =========="

                kubectl get svc \
                    -n ${K8S_NAMESPACE}

                echo
                echo "========== DEPLOYMENTS =========="

                kubectl get deployments \
                    -n ${K8S_NAMESPACE}

                '''

            }

        }

    }

    post {

        success {

            echo '======================================'
            echo 'Pipeline completed successfully!'
            echo 'Application deployed to Kubernetes.'
            echo '======================================'

        }

        failure {

            sh '''

            echo
            echo "========== DEBUG =========="

            kubectl get all -n ${K8S_NAMESPACE} || true

            kubectl describe pods -n ${K8S_NAMESPACE} || true

            '''

            echo 'Pipeline failed.'

        }

        always {

            cleanWs()

        }

    }

}