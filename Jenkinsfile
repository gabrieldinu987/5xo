pipeline {

    agent any

    stages {

        stage('Checkout') {

            steps {

                checkout scm

            }

        }

        stage('Python Environment') {

            steps {

                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }

        }

        stage('Run Tests') {

            steps {

                sh '''
                    . venv/bin/activate

                    pytest \
                        --junitxml=report.xml \
                        --cov=game \
                        --cov-report=xml \
                        --cov-report=html
                '''
            }

        }

        stage('Docker Build') {

            steps {

                sh '''
                    docker build \
                        -t 5xo:${BUILD_NUMBER} \
                        -t 5xo:latest .
                '''
            }

        }

    }

    post {

        always {

            junit 'report.xml'

            archiveArtifacts artifacts: '''
                report.xml,
                coverage.xml,
                htmlcov/**
            ''', fingerprint: true

        }

    }

}