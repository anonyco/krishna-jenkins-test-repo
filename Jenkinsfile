pipeline {
    agent { docker { image 'gradle:7.4.2-jdk11-alpine' } }
    parameters {
        gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH_NAME', type: 'PT_BRANCH'
    }
    stages {
        stage('build') {
            steps {
		dir ("/home/jenkins/repos/${BRANCH_NAME}"){
                    sh './gradlew build'
		}
            }
        }
    }
}
