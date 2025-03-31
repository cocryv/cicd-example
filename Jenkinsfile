pipeline {
    agent any
    
    environment {
        // Pour Docker Hub, on utilise simplement le nom d'utilisateur comme préfixe
        DOCKER_REGISTRY_USER = 'valentincocry'  // Remplacez par votre utilisateur Docker Hub
        IMAGE_NAME = 'python-app'
        // Utilisation de BUILD_NUMBER uniquement si BRANCH_NAME n'est pas disponible
        IMAGE_TAG = "${env.BRANCH_NAME ?: 'main'}-${env.BUILD_NUMBER}"
    }
    
    stages {

        
        stage('Test') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root:root -v ${WORKSPACE}:/app -w /app'
                }
            }
            steps {
                sh 'pip install --no-cache-dir -r requirements.txt'
                sh 'python -m pytest tests/'
            }
        }
        
        
        stage('Build and Push Docker Image') {
            agent any
            steps {
                checkout scm
                script {
                    // Construire l'image avec le format correct
                    sh "docker build -t ${DOCKER_REGISTRY_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                    
                    // Vérification si nous sommes sur une branche qui nécessite un push
                    if (env.BRANCH_NAME == 'develop' || env.BRANCH_NAME == 'main' || env.BRANCH_NAME ==~ /release\/.*/) {
                        withCredentials([string(credentialsId: 'docker-registry-creds', variable: 'DOCKER_PWD')]) {
                            sh "echo ${DOCKER_PWD} | docker login -u ${DOCKER_REGISTRY_USER} --password-stdin"
                            sh "docker push ${DOCKER_REGISTRY_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                        }
                    }
                }
            }
        }
        
        stage('Deploy to Dev') {
            agent any
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
            agent any
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
            agent any
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
            node(null) {
                // Utiliser une approche plus sûre pour le nettoyage
                sh 'chmod -R 777 . || true'
                sh 'docker system prune -f || true'
                cleanWs() // Au lieu de deleteDir()
            }
        }
        success {
            echo 'Pipeline terminé avec succès!'
        }
        failure {
            echo 'Pipeline a échoué!'
        }
    }
}