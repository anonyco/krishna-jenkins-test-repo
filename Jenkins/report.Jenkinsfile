
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
        stage('build') {
            steps {
                dir('mailer') {
                    script {
                        sh "./mailCredsLoader.sh ${env.MAIL_CONFIG} report.py update --reportForMailInBox ${params.INBOX} --reportForMailNumber ${params.messageNumber} --updateWithText '${params.BRANCH_NAME} Was Cloned or Updated Successfully'"
                    }
                }
            }
        }
    }
}