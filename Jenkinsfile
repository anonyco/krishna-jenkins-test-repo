pipeline {
    agent { 
        docker {
            image 'gradle:7.4.2-jdk11-alpine'
            args '--rm=true'
        }
    }
    options {
	lock(extra: [[resource: 'jenkins_git_cloner'], [resource: "jenkins_pipeline_${params.BRANCH_NAME}"]])
    }
    parameters {
        gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH_NAME', type: 'PT_BRANCH'
    }
    stages {
        stage('clone') {
            steps {
ws("/var/jenkins_home/repos"){
                    script {
sleep 30
                        sh "ls -aslh && printenv"
                        if (fileExists("${params.BRANCH_NAME}")) {
                            echo "Folder found, not cloning again, but instead pull the latest code"
			    dir("${params.BRANCH_NAME}") {
				sh "git reset --hard origin/${params.BRANCH_NAME}"
				sh "git pull origin ${params.BRANCH_NAME}"
			    }
                        }
                        else {
                            echo "folder not found, cloning it"
                            withCredentials([usernameColonPassword(credentialsId: 'github', variable: 'GIT_CREDS')]) {
				sh "id && ls -aslh && pwd"
                                sh "git clone -b ${params.BRANCH_NAME} https://${GIT_CREDS}@github.com/anonyco/krishna-jenkins-test-repo ${params.BRANCH_NAME}"
                            }

                        }
                    }
}
            }
        }

    }
}
