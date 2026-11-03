pipeline {
    agent { docker { image 'python:3.15.2-alpine3.24' } }
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
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'dist/**', fingerprint: true
            junit 'reports/*.xml'
            echo 'One way or another, I have finished'
            deleteDir() /* clean up our workspace */
        }
        success  { echo 'I succeeded!' }
        unstable { echo 'I am unstable :/' }
        failure  { echo 'I failed :(' }
        changed  { echo 'Things were different before...' }
    }
}
