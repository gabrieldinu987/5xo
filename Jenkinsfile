pipeline {

    agent any

    environment {
        APP_NAME   = "5xo"
        IMAGE_NAME = "5xo"
        IMAGE_TAG  = "latest"
    }

    options {
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Project Info') {
            steps {
                sh '''
                    echo "=================================="
                    echo "5XO CI/CD PIPELINE"
                    echo "=================================="

                    echo "JOB       : $JOB_NAME"
                    echo "BUILD     : $BUILD_NUMBER"
                    echo "WORKSPACE : $WORKSPACE"

                    echo
                    echo "Last commit:"
                    git log -1 --oneline

                    echo
                    docker --version
                    python3 --version
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    docker run --rm \
                        ${IMAGE_NAME}:${IMAGE_TAG} \
                        python -m pytest -v
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    docker rm -f ${APP_NAME} 2>/dev/null || true

                    docker run -d \
                    --name ${APP_NAME} \
                    --network host \
                    ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Docker Status') {
            steps {
                sh '''
                    echo
                    echo "Running containers"
                    docker ps

                    echo
                    echo "Images"
                    docker images
                '''
            }
        }
    }

    post {

        success {
            echo 'Pipeline finished successfully.'
        }

        failure {
            sh '''
                docker logs ${APP_NAME} || true
            '''
        }

        always {
            sh '''
                docker image prune -f || true
            '''

            cleanWs()
        }
    }
}