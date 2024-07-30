pipeline{
    agent any
    environment {
        DOCKER_IMAGE = 'service-user3'
        PORT_MAPPING = '8004:8004'
        CONTAINER_NAME = 'service-user3-container'
    }

    stages {
        stage('Stop Container and Remove') {
            steps {
                script {
                    def containerExists = sh(script: "docker ps -a --filter name=^/${CONTAINER_NAME}\$ --format '{{.Names}}'", returnStdout: true).trim()
                    if (containerExists == CONTAINER_NAME) {
                        sh "docker stop ${CONTAINER_NAME}"
                        sh "docker rm ${CONTAINER_NAME}"
                    }
                }
            }
        }

        stage('Build and Deploy') {
            steps {
                script {
                    def dockerImage = docker.build(DOCKER_IMAGE)
                }
            }
        }
    }
}