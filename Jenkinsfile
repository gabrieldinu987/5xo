pipeline {
    agent any

    environment {
        APP_NAME   = "5xo"
        IMAGE_NAME = "5xo"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    options {
        timestamps()
        ansiColor('xterm')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      -t ${IMAGE_NAME}:${IMAGE_TAG} \
                      .
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    docker run --rm \
                        ${IMAGE_NAME}:${IMAGE_TAG} \
                        python3 -m unittest discover tests
                '''
            }
        }

        stage('Replace Running Container') {
            steps {
                sh '''
                    docker rm -f ${APP_NAME} || true

                    docker run -d \
                        --restart unless-stopped \
                        --name ${APP_NAME} \
                        -p 5000:5000 \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    echo "Waiting for application..."

                    for i in $(seq 1 20)
                    do
                        if curl -fs http://localhost:5000 >/dev/null
                        then
                            echo "Application started successfully."
                            exit 0
                        fi

                        sleep 2
                    done

                    docker logs ${APP_NAME}

                    exit 1
                '''
            }
        }

        stage('Docker Status') {
            steps {
                sh '''
                    echo
                    echo "===== RUNNING CONTAINERS ====="
                    docker ps

                    echo
                    echo "===== DOCKER IMAGES ====="
                    docker images | grep 5xo || true

                    echo
                    echo "===== DISK USAGE ====="
                    docker system df
                '''
            }
        }

    }

    post {

        success {

            echo "Build completed successfully."

            sh '''
                docker image prune -f
            '''
        }

        failure {

            echo "Build failed."

            sh '''
                docker ps -a
            '''
        }

        always {

            cleanWs()
        }
    }
}