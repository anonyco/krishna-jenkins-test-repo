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
	string name: 'TEMPLATE'
    }
    environment {
        MAIL_CONFIG = credentials('smtp')
        SKIP = 0
    }
    stages {
        stage('Check Mail') {
            steps {
                dir('mailer') {
                    script {
                        def statusCode = sh script:"./mailer.sh ${env.MAIL_CONFIG} checkMailForJobTrigger ${params.INBOX} ${params.messageNumber}", returnStatus:true
                        env.SKIP = statusCode
                    }
                }
            }
        }
        stage('Trigger Patch') {
            when ( env.SKIP == 0)
            steps {
                dir('mailer') {
                    script {
                        def statusCode = sh script:"./mailer.sh ${env.MAIL_CONFIG} checkMailForJobTrigger ${params.INBOX} ${params.messageNumber}", returnStatus:true
                        env.SKIP = statusCode
                    }
                }
            }
        }
    }
}
