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
                        build job: "report", propagate: true, wait: true, parameters: [
                                    string(name: "INBOX", value: "${params.INBOX}"),
                                    string(name: "messageNumber", value: "${params.messageNumber}"),
                                    string(name: "task", value: "create")
                                    ]
                        echo "${branchName}"
                        if (branchName != "main") {
                            build job: "jenkins_cloner", propagate: false, wait: false, parameters: [
                                gitParameter(name: "BRANCH_NAME", value: "${branchName}"),
                                string(name: "INBOX", value: "${params.INBOX}"),
                                string(name: "messageNumber", value: "${params.messageNumber}")
                                ]
                            build job: "report", propagate: true, wait: true, parameters: [
                                        string(name: "INBOX", value: "${params.INBOX}"),
                                        string(name: "messageNumber", value: "${params.messageNumber}"),
                                        string(name: "task", value: "update"),
                                        string(name: "message", value: "Patch Accepted")
                                        ]
                        } else {
                            build job: "report", propagate: true, wait: true, parameters: [
                                        string(name: "INBOX", value: "${params.INBOX}"),
                                        string(name: "messageNumber", value: "${params.messageNumber}"),
                                        string(name: "task", value: "update"),
                                        string(name: "message", value: "Patch Rejected, \r\n Reason: Main is a Restricted Branch")
                                        ]
                            build job: "report", propagate: true, wait: true, parameters: [
                                        string(name: "INBOX", value: "${params.INBOX}"),
                                        string(name: "messageNumber", value: "${params.messageNumber}"),
                                        string(name: "task", value: "send")
                                        ]
                        }
                    }
                }
            }
        }
    }
}
