pipeline {
    agent none
    
    environment {
        DOCKER_REGISTRY = 'https://hub.docker.com/'
        IMAGE_NAME = 'python-app'
        IMAGE_TAG = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Test') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root:root'  // Exécuter en tant que root pour éviter les problèmes de permissions
                }
            }
            steps {
                checkout scm
                sh 'pip install --no-cache-dir -r requirements.txt'
                sh 'python -m pytest tests/'
            }
        }
        
        stage('Build and Push Docker Image') {
            agent any  // Utilise un nœud Jenkins avec Docker installé
            steps {
                checkout scm
                script {
                    // Construire l'image
                    sh "docker build -t ${env.DOCKER_REGISTRY}/${env.IMAGE_NAME}:${env.IMAGE_TAG} ."
                    
                    // Pousser l'image si on est sur les branches concernées
                    if (env.BRANCH_NAME == 'develop' || env.BRANCH_NAME == 'main' || env.BRANCH_NAME ==~ /release\/.*/) {
                        withCredentials([string(credentialsId: 'docker-registry-creds', variable: 'DOCKER_PWD')]) {
                            sh "echo ${DOCKER_PWD} | docker login ${env.DOCKER_REGISTRY} -u user --password-stdin"
                            sh "docker push ${env.DOCKER_REGISTRY}/${env.IMAGE_NAME}:${env.IMAGE_TAG}"
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
                sh 'docker system prune -f || true'
                deleteDir()
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