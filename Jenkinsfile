pipeline {
    agent { docker { image 'python:3.15.2-alpine3.24' } }
    stages {
        stage('Build') {
            steps {
                sh 'echo "Hello World"'
                sh '''
                    echo "Multiline shell steps works too"
                    ls -lah
                '''
            }
        }
        stage('Deploy') {
            steps {
                // Simule un déploiement instable : échoue 1 fois sur 2 au hasard
                timeout(time: 3, unit: 'MINUTES') {
                    retry(5) {
                        sh 'python -c "import random,sys; r=random.randint(0,1); print(\'tentative ->\', \'OK\' if r==0 else \'ECHEC\'); sys.exit(r)"'
                    }
                }
                timeout(time: 3, unit: 'MINUTES') {
                    sh 'sleep 5 && echo "Health check OK"'
                }
            }
        }
    }
    post {
        always   { echo 'This will always run' }
        success  { echo 'This will run only if successful' }
        failure  { echo 'This will run only if failed' }
        unstable { echo 'This will run only if the run was marked as unstable' }
        changed  { echo 'This will run only if the state of the Pipeline has changed' }
    }
}
