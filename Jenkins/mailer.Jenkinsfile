
pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            dir 'mailer'
        }
    }
    parameters {
        string name: 'RECIPIENT_EMAIL'
        string name: 'ADDON_ENVIRONMENT'
        string name: 'TEMPLATE'
    }
    environment {
        MAIL_CONFIG = credentials('smtp')
    }
    stages {
        stage('build') {
            steps {
                dir('mailer') {
                    script {
                        sh "${params.ADDON_ENVIRONMENT} ./mailer.sh ${env.MAIL_CONFIG} ${params.RECIPIENT_EMAIL} ${params.TEMPLATE}"
                    }
                }
            }
        }
    }
}


