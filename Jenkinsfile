pipeline {

    agent any

    environment {

        APP_NAME   = "5xo"
        IMAGE_NAME = "5xo"
        IMAGE_TAG  = "latest"

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

        stage('Project Information') {

            steps {

                sh '''

                    echo "========================================"

                    echo "5XO CI/CD Pipeline"

                    echo "========================================"

                    echo

                    echo "Job..............: ${JOB_NAME}"

                    echo "Build............: ${BUILD_NUMBER}"

                    echo "Branch...........: ${BRANCH_NAME}"

                    echo "Workspace........: ${WORKSPACE}"

                    echo

                    git log -1 --oneline

                '''

            }

        }

        stage('Docker Build') {

            steps {

                sh '''

                    docker build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} .

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

        stage('Deploy Container') {

            steps {

                sh '''

                    docker rm -f ${APP_NAME} || true

                    docker run -d \
                        --name ${APP_NAME} \
                        --restart unless-stopped \
                        -p 5000:5000 \
                        ${IMAGE_NAME}:${IMAGE_TAG}

                '''

            }

        }

        stage('Health Check') {

            steps {

                sh '''

                    echo

                    echo "Waiting for application..."

                    for i in $(seq 1 20)

                    do

                        if curl -fs http://localhost:5000 >/dev/null

                        then

                            echo

                            echo "Application is UP."

                            exit 0

                        fi

                        sleep 2

                    done

                    echo

                    echo "Application failed to start."

                    docker logs ${APP_NAME}

                    exit 1

                '''

            }

        }

        stage('Docker Status') {

            steps {

                sh '''

                    echo

                    echo "Running Containers"

                    docker ps

                    echo

                    echo "Images"

                    docker images | grep 5xo || true

                    echo

                    echo "Disk Usage"

                    docker system df

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

                echo

                echo "Container Logs"

                docker logs ${APP_NAME} || true

            '''

        }

        always {

            sh '''

                docker image prune -f

            '''

            cleanWs()

        }

    }

}