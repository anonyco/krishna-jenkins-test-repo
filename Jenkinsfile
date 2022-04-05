pipeline {
    agent { docker { image 'maven:3.6.3-openjdk-17-slim' } }
    stages {
        stage('build') {
            steps {
                sh 'mvn --version'
            }
        }
    }
}
