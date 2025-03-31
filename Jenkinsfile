pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
        }
    }
    
    environment {
        DOCKER_REGISTRY = 'https://hub.docker.com/'
        IMAGE_NAME = 'python-app'
        IMAGE_TAG = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'sudo pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                sh 'python -m pytest tests/'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    app = docker.build("${env.DOCKER_REGISTRY}/${env.IMAGE_NAME}:${env.IMAGE_TAG}")
                }
            }
        }
        
        stage('Push Docker Image') {
            when {
                anyOf {
                    branch 'develop';
                    branch 'main';
                    branch pattern: 'release/*', comparator: 'REGEXP'
                }
            }
            steps {
                withCredentials([string(credentialsId: 'docker-registry-creds', variable: 'DOCKER_PWD')]) {
                    sh "echo ${DOCKER_PWD} | docker login ${env.DOCKER_REGISTRY} -u user --password-stdin"
                    sh "docker push ${env.DOCKER_REGISTRY}/${env.IMAGE_NAME}:${env.IMAGE_TAG}"
                }
            }
        }
        
        stage('Deploy to Dev') {
            when {
                branch 'develop'
            }
            steps {
                sh '''
                echo "Deploying to DEV environment"
                # Ici vous pouvez ajouter les commandes pour déployer sur dev
                # Exemple avec kubectl:
                # kubectl set image deployment/app app=${env.DOCKER_REGISTRY}/${env.IMAGE_NAME}:${env.IMAGE_TAG} --namespace=dev
                '''
            }
        }
        
        stage('Deploy to Test') {
            when {
                branch pattern: 'release/*', comparator: 'REGEXP'
            }
            steps {
                sh '''
                echo "Deploying to TEST environment"
                # Ici vous pouvez ajouter les commandes pour déployer sur test
                '''
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                // Ajoutez une étape d'approbation manuelle pour la prod
                input message: 'Déployer en production?', ok: 'Oui'
                
                sh '''
                echo "Deploying to PRODUCTION environment"
                # Ici vous pouvez ajouter les commandes pour déployer sur prod
                '''
            }
        }
    }
    
    post {
        always {
            // Nettoyage
            sh 'docker system prune -f'
            deleteDir()
        }
        success {
            echo 'Pipeline terminé avec succès!'
        }
        failure {
            echo 'Pipeline a échoué!'
        }
    }
}