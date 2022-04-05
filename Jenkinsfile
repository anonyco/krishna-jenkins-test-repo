pipeline {
    agent { docker { 
		image 'gradle:7.4.2-jdk11-alpine' 
		args '-v /home/jack/code/krishna_git/build-server/repos:/app/repos:rw'
		} 
	}
    parameters {
        gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH_NAME', type: 'PT_BRANCH'
    }
    stages {
        stage('build') {
            steps {
		sh "ls /app/repos/"
		dir ("/app/repos/${BRANCH_NAME}"){
                    sh './gradlew build'
		}
            }
        }
    }
}
