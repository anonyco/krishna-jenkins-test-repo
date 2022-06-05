
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
        string name: 'task'
        string name: 'message'
        File name: 'messageFile'
    }
    environment {
        MAIL_CONFIG = credentials('smtp')
    }
    stages {
        stage('create') {
            when {
                expression { params.task == "create" }
            }
            steps {
                dir('mailer') {
                    script {
                        sh "./mailCredsLoader.sh ${env.MAIL_CONFIG} report.py create --reportForMailInBox ${params.INBOX} --reportForMailNumber ${params.messageNumber}"
                    }
                }
            }
        }
        stage('update') {
            when {
                expression { params.task == "update" }
            }
            steps {
                dir('mailer') {
                    script {
                        sh "./mailCredsLoader.sh ${env.MAIL_CONFIG} report.py update --reportForMailInBox ${params.INBOX} --reportForMailNumber ${params.messageNumber} --updateWithText '${params.message}'"
                    }
                }
            }
        }
        stage('send') {
            when {
                expression { params.task == "send" }
            }
            steps {
                dir('mailer') {
                    script {
                        sh "./mailCredsLoader.sh ${env.MAIL_CONFIG} report.py send --reportForMailInBox ${params.INBOX} --reportForMailNumber ${params.messageNumber}"
                    }
                }
            }
        }
    }
}