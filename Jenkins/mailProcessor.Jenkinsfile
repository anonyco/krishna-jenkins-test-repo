def statusCode = "0"
pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            dir 'mailer'
            args '-v /var/jenkins_home/:/var/jenkins_home/:rw,z'
        }
    }
    parameters {
        string name: 'INBOX'
        string name: 'messageNumber'
    }
    environment {
        MAIL_CONFIG = credentials('smtp')
    }
    stages {
        stage('Check Mail') {
            steps {
                dir('mailer') {
                    script {
                        statusCode = sh script:"./mailCredsLoader.sh ${env.MAIL_CONFIG} mailer.py checkMailForJobTrigger --imapInbox ${params.INBOX} --messageNumber ${params.messageNumber}", returnStatus:true
                        echo "${statusCode}"
                    }
                }
            }
        }
        stage('Trigger Patch') {
            when { expression { statusCode == 0 } }
            steps {
                dir('mailer') {
                    script {
                        branchName = sh(script:"./mailCredsLoader.sh ${env.MAIL_CONFIG} mailer.py checkMailForBranch --imapInbox ${params.INBOX} --messageNumber ${params.messageNumber}", returnStdout:true).trim()
                        if (branchName != "main") {
                            dir("/var/jenkins_home/repos/main/mailer"){
                                sh "./mailCredsLoader.sh ${env.MAIL_CONFIG} report.py create --reportForMailInBox ${params.INBOX} --reportForMailNumber ${params.messageNumber}"
                            }
                            build job: "jenkins_cloner", propagate: false, wait: false, parameters: [
                                gitParameter(name: "BRANCH_NAME", value: "${branchName}"),
                                string(name: "INBOX", value: "${params.INBOX}"),
                                string(name: "messageNumber", value: "${params.messageNumber}")
                                ]
                        } else {
                            dir("/var/jenkins_home/repos/main/mailer"){
                                sh "./mailCredsLoader.sh ${env.MAIL_CONFIG} mailer.py patchRejectionForBranch --imapInbox ${params.INBOX} --messageNumber ${params.messageNumber}"
                            }
                        }
                    }
                }
            }
        }
    }
}
