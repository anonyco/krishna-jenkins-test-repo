pipeline {
    agent { docker { 
		image 'gradle:7.4.2-jdk11-alpine' 
		args '-v /home/jack/code/krishna_git/build-server/repos:/root/repos:rw'
		} 
	}
    parameters {
        gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH_NAME', type: 'PT_BRANCH'
    }
    stages {
        stage('build') {
            steps {
		sh "ls /root/repos/"
		dir ("/root/repos/${BRANCH_NAME}"){
                    sh './gradlew build'
		}
            }
        }
    }
}
