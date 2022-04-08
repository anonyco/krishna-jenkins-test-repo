pipeline {
    agent { docker { 
		image 'gradle:7.4.2-jdk11-alpine'
		args '-v /home/jack/code/krishna_git/build-server/repos:/var/jenkins_home/workspace/test-sanity/repos:rw --rm=true'
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
		}
		dir("repos/") {
			script {
sh "ls -aslh && printenv"
    if (fileExists("${env.WORKSPACE}/repos/branch2")) {
        echo "Folder found, not cloning again but rather pulling latest code on the branch"
dir("repos/${params.BRANCH_NAME}") {
sh "git pull"
}

    }
else {
echo "folder not found, cloning it"
withCredentials([usernameColonPassword(credentialsId: 'github', variable: 'GIT_CREDS')]) {
    sh "git clone -b ${params.BRANCH_NAME} https://${GIT_CREDS}@github.com/anonyco/krishna-jenkins-test-repo ${params.BRANCH_NAME}"
}
}
			}
		}
            }
        }
        stage('build') {
            steps {
                sh "ls -aslh /repos/"
sleep 600
                dir ("repos/${BRANCH_NAME}"){
                    sh './gradlew build'
                }
            }
        }
    }


}
