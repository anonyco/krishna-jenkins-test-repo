pipeline {
    agent { 
        docker {
            image 'gradle:7.4.2-jdk11-alpine'
            args '--rm=true'
        }
    }
    options {
        lock(extra: [[resource: "jenkins_pipeline_${params.BRANCH_NAME}"]])
    }
    parameters {
        gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH_NAME', type: 'PT_BRANCH'
    }
    stages {
        stage('build') {
            steps {
                sh "ls -aslh repos/"
                dir (""){
ws("/var/jenkins_home/repos/${BRANCH_NAME}"){
                    sh './gradlew build'
}
                }
            }
        }
    }
}
