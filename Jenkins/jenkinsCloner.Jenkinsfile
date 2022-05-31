pipeline {
    agent {
        docker {
            image 'gradle:7.4.2-jdk11-alpine'
            args '-v /var/jenkins_home/:/var/jenkins_home/:rw,z'
        }
    }
    options {
        lock(extra: [[resource: 'jenkins_git_cloner'], [resource: "jenkins_pipeline_${params.BRANCH_NAME}"]])
    }
    parameters {
        gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH_NAME', type: 'PT_BRANCH'
        string name: "messageNumber"
        string name: "INBOX"
    }
    stages {
        stage('clone') {
            steps {
                ws("/var/jenkins_home/repos"){
                    script {
                        if (fileExists("${params.BRANCH_NAME}")) {
                            echo "Folder found, not cloning again, but instead pull the latest code"
                            dir("${params.BRANCH_NAME}") {
                                retry(2) {
                                    sh "git reset --hard origin/${params.BRANCH_NAME}"
                                    sh "git checkout origin/${params.BRANCH_NAME}"
                                    sh "git pull origin ${params.BRANCH_NAME}"
                                    sh "git checkout origin/${params.BRANCH_NAME}"
                                }
                            }
                        }
                        else {
                            echo "folder not found, cloning it"
                            withCredentials([usernameColonPassword(credentialsId: 'github', variable: 'GIT_CREDS')]) {
                                sh "git clone -b ${params.BRANCH_NAME} 'https://${GIT_CREDS}@github.com/anonyco/krishna-jenkins-test-repo' ${params.BRANCH_NAME}"
                            }
                        }
                    }
                }
            }
        }
        stage('trigger build') {
            steps {
                build job: "patchBranch", propagate: false, wait: false, parameters: [
                            gitParameter(name: "BRANCH_NAME", value: "${params.BRANCH_NAME}"),
			    string(name: "INBOX", value: "${params.INBOX}"),
			    string(name: "messageNumber", value: "${params.messageNumber}")
                            ]

            }
        }
    }
    post {
        success {
            ws("/var/jenkins_home/repos/main/mailer"){
                sh "pwd && ls && ./mailCredsLoader.sh ${env.MAIL_CONFIG} report.py update --reportForMailInBox ${params.INBOX} --reportForMailNumber ${params.messageNumber} --updateWithText \"${params.BRANCH_NAME} Was Cloned or Updated Successfully\""
            }
        }

        failure {
            dir("/var/jenkins_home/repos/main/mailer"){
                sh "./mailCredsLoader.sh ${env.MAIL_CONFIG} report.py update --reportForMailInBox ${params.INBOX} --reportForMailNumber ${params.messageNumber} --updateWithText \"Cloning ${params.BRANCH_NAME} Failed\""
                sh "./mailCredsLoader.sh ${env.MAIL_CONFIG} report.py send --reportForMailInBox ${params.INBOX} --reportForMailNumber ${params.messageNumber}"
            }
        }
    }
}
