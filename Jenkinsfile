pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    .venv/bin/python -m pytest
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                              -Dsonar.projectKey=autodeploy-ai \
                              -Dsonar.projectName="AutoDeploy AI" \
                              -Dsonar.sources=app \
                              -Dsonar.tests=tests \
                              -Dsonar.python.version=3.12
                        """
                    }
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build -t autodeploy-ai:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                    trivy image \
                      --severity HIGH,CRITICAL \
                      --ignore-unfixed \
                      --exit-code 1 \
                      autodeploy-ai:${BUILD_NUMBER}
                '''
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-autodeploy',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                          -u "$DOCKER_USERNAME" \
                          --password-stdin

                        docker tag autodeploy-ai:${BUILD_NUMBER} \
                          tmdd224/autodeploy-ai:${BUILD_NUMBER}

                        docker push \
                          tmdd224/autodeploy-ai:${BUILD_NUMBER}

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker pull tmdd224/autodeploy-ai:${BUILD_NUMBER}

                    docker stop autodeploy-api || true
                    docker rm autodeploy-api || true

                    docker run -d \
                      --name autodeploy-api \
                      -p 8000:8000 \
                      tmdd224/autodeploy-ai:${BUILD_NUMBER}

                    sleep 5

                    curl -f http://localhost:8000/health
                '''
            }
        }
    }

    post {
        success {
            echo 'AutoDeploy AI : pipeline réussi !'
        }

        failure {
            echo 'AutoDeploy AI : pipeline échoué.'
        }
    }
}


