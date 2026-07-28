pipeline {

    agent any

    environment {

    IMAGE_NAME      = "5xo"
    IMAGE_TAG       = "latest"

    APP_NAME        = "fivexo"
    K8S_NAMESPACE   = "fivexo"

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
                script {
                    sh """
                        set -e

                        kubectl rollout restart deployment/fivexo -n fivexo

                        kubectl rollout status deployment/fivexo \
                            -n fivexo \
                            --timeout=180s
                    """
                }
            }
        }

        stage('Cluster Status') {
            steps {

                steps {
                    sh """
                        echo "========== PODS =========="
                        kubectl get pods -n fivexo -o wide

                        echo
                        echo "========== SERVICES =========="
                        kubectl get svc -n fivexo

                        echo
                        echo "========== DEPLOYMENTS =========="
                        kubectl get deployments -n fivexo

                        echo
                        echo "========== EVENTS =========="
                        kubectl get events -n fivexo \
                            --sort-by=.metadata.creationTimestamp
                    """
                }

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

            sh """
                echo
                echo "========== DEBUG =========="

                kubectl get all -n fivexo || true

                echo
                echo "========== DEPLOYMENT =========="
                kubectl describe deployment fivexo -n fivexo || true

                echo
                echo "========== PODS =========="
                kubectl describe pods -n fivexo || true

                echo
                echo "========== LOGS =========="
                kubectl logs \
                    -n fivexo \
                    -l app=fivexo \
                    --all-containers=true || true

                echo
                echo "========== EVENTS =========="
                kubectl get events \
                    -n fivexo \
                    --sort-by=.metadata.creationTimestamp || true
            """

            echo 'Pipeline failed.'
        }

        always {
            cleanWs()
        }
    }
}