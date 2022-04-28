pipeline {
    agent {
        docker {
            image 'gradle:7.4.2-jdk11-alpine'
            args ''
        }
    }
    options {
        lock(extra: [[resource: "jenkins_pipeline_master"]])
    }
    parameters {
	string name: "messageNumber"
	string name: "INBOX"
	gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH_NAME', type: 'PT_BRANCH'
    }
    stages {
        stage('build') {
            steps {
		sh "echo ${params.FROM}"
		sh "cat ${params.CONTENT_FILE}"
                    sh './gradlew build'
		sh "rm ${params.FROM}"
            }
        }
    }
}
