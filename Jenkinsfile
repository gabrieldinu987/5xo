pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('System Information') {
            steps {
                sh 'whoami'
                sh 'pwd'
                sh 'python3 --version'
                sh 'git --version'
                sh 'docker --version'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    python --version
                '''
            }
        }

    }

}