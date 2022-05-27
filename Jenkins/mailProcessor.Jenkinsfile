def statusCode = "0"
pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            dir 'mailer'
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
                        statusCode = sh script:"./mailer.sh ${env.MAIL_CONFIG} checkMailForJobTrigger ${params.INBOX} ${params.messageNumber}", returnStatus:true
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
                        branchName = sh(script:"./mailer.sh ${env.MAIL_CONFIG} checkMailForBranch ${params.INBOX} ${params.messageNumber}", returnStdout:true).trim()
                        if (branchName != "main") {
                            build job: "jenkins_cloner", propagate: false, wait: false, parameters: [
                                gitParameter(name: "BRANCH_NAME", value: "${branchName}"),
                                string(name: "INBOX", value: "${params.INBOX}"),
                                string(name: "messageNumber", value: "${params.messageNumber}")
                                ]
                        } else {
                            sh "./mailer.sh ${env.MAIL_CONFIG} patchRejectionForBranch ${params.INBOX} ${params.messageNumber}"
                        }
                    }
                }
            }
        }
    }
}