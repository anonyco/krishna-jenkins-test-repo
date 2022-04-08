pipeline {
    agent { docker { 
		image 'gradle:7.4.2-jdk11-alpine'
		args '-v /home/jack/code/krishna_git/build-server/repos:/repos:rw --rm=true'
		}
	}
    parameters {
        gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH_NAME', type: 'PT_BRANCH'
    }
    stages {
        stage('clone') {
            steps {
		script {
sh "ls -aslh"
		sh "ln -sf repos /repos"
		}
		dir("repos/") {
			script {
sh "ls -aslh"
			}
		}
            }
        }
        stage('build') {
            steps {
                sh "ls /repos/"
                dir ("/repos/${BRANCH_NAME}"){
                    sh './gradlew build'
                }
            }
        }
    }
}
