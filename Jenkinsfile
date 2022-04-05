pipeline {
    agent { docker { 
		image 'gradle:7.4.2-jdk11-alpine' 
		args '-v /home/jack/code/krishna_git/build-server/repos:/root/repos'
		} 
	}
    parameters {
        gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH_NAME', type: 'PT_BRANCH'
    }
    stages {
        stage('build') {
            steps {
		dir ("/root/repos/${BRANCH_NAME}"){
                    sh './gradlew build'
		}
            }
        }
    }
}
