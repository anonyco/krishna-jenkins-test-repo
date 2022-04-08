pipeline {
    agent { docker { 
		image 'gradle:7.4.2-jdk11-alpine'
		args '-v /home/jack/code/krishna_git/build-server/repos:/repos:rw'
		}
	}
    parameters {
        gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH_NAME', type: 'PT_BRANCH'
    }
    stages {
        stage('clone') {
            steps {
		script {
		sh "ls -aslh / && id"
		sh "ls -aslh /repos/ && pwd && ls -aslh"
		}
		dir("/repos/") {
			script {
			folder_state = sh(script: "test -d ${params.BRANCH_NAME} && echo '1' || echo '0', returnStdout: true")
			if (folder_state=='0') {
				echo "new Branch, cloning it now"
			}
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
