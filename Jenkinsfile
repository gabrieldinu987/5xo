pipeline {

    agent any

    environment {
        IMAGE_NAME = "5xo"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv

                    . venv/bin/activate

                    pip install --upgrade pip

                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    . venv/bin/activate

                    pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                        -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                        -t ${IMAGE_NAME}:latest \
                        .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {

                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                            -u "$DOCKER_USER" \
                            --password-stdin

                        docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${DOCKER_USER}/${IMAGE_NAME}:${BUILD_NUMBER}
                        docker tag ${IMAGE_NAME}:latest ${DOCKER_USER}/${IMAGE_NAME}:latest

                        docker push ${DOCKER_USER}/${IMAGE_NAME}:${BUILD_NUMBER}
                        docker push ${DOCKER_USER}/${IMAGE_NAME}:latest

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    cd infrastructure/deployment
                    docker compose up -d --pull always
                '''
            }
        }
    }

    post {

        success {
            echo "Build #${BUILD_NUMBER} completed successfully."
        }

        failure {
            echo "Build #${BUILD_NUMBER} failed."
        }

        always {
            cleanWs()
        }
    }
}