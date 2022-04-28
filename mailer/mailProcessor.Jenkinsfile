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
    }
    stages {
        stage('Check Mail') {
            steps {
                dir('mailer') {
                    script {
                        def statusCode = sh script:"./mailer.sh ${env.MAIL_CONFIG} checkMailForJobTrigger ${params.RECIPIENT_EMAIL} ${params.TEMPLATE}", returnStatus:true
                        echo "${statusCode}"
                    }
                }
            }
        }
    }
}
