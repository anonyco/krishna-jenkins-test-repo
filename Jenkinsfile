pipeline {
    agent { 
        docker {
            image 'gradle:7.4.2-jdk11-alpine'
            args '--rm=true'
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
                        if (! fileExists("${env.WORKSPACE}/repos")) {
                            echo "Creating a folder for all Repos"
                            sh "mkdir \"$WORKSPACE/repos\""
                        }
                }

                dir("${env.WORKSPACE}/repos/") {
ws("/var/jenkins_home/workspace/test-jenkins/"){
                    script {
                        sh "ls -aslh && printenv"
                        if (fileExists("${params.BRANCH_NAME}")) {
                            echo "Folder found, not cloning again, but instead pull the latest code"
			    dir("${env.WORKSPACE}/repos/${params.BRANCH_NAME}") {
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
        stage('build') {
            steps {
                sh "ls -aslh repos/"
                dir ("${env.WORKSPACE}/repos/${BRANCH_NAME}"){
ws("/var/jenkins_home/workspace/test-jenkins/repos/${BRANCH_NAME}"){
                    sh './gradlew build'
}
                }
            }
        }
    }
}
