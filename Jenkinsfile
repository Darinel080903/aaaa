pipeline{
    agent any

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