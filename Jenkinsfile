pipeline {
    agent { docker { image 'python:3.15.2-alpine3.24' } }

    options {
        skipStagesAfterUnstable()   // pas de déploiement si les tests échouent
    }

    environment {
        APP_NAME = 'jenkins-tp'
    }

    stages {
        stage('Build') {
            steps {
                sh '''
                    python -m venv .venv
                    . .venv/bin/activate
                    pip install --no-cache-dir pytest
                    mkdir -p dist
                    cp app.py dist/
                    echo "Build ${BUILD_NUMBER}" > dist/version.txt
                '''
            }
        }
        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest --junitxml=reports/results.xml || true
                '''
                junit 'reports/*.xml'
            }
        }
        stage('Deploy - Staging') {
            steps {
                sh 'echo "Déploiement de ${APP_NAME} (build ${BUILD_NUMBER}) en STAGING..."'
                sh 'echo "Smoke tests OK"'
            }
        }
        stage('Sanity check') {
            steps {
                input "Does the staging environment look ok?"
            }
        }
        stage('Deploy - Production') {
            steps {
                timeout(time: 3, unit: 'MINUTES') {
                    retry(3) {
                        sh 'echo "Déploiement de ${APP_NAME} en PRODUCTION..."'
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'dist/**', fingerprint: true, allowEmptyArchive: true
            echo 'One way or another, I have finished'
            deleteDir()
        }
        success  { echo 'I succeeded!' }
        unstable { echo 'I am unstable :/' }
        failure  { echo 'I failed :(' }
        changed  { echo 'Things were different before...' }
    }
}
