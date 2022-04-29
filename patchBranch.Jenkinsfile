pipeline {
    agent any
    options {
        lock(extra: [[resource: "jenkins_pipeline_${params.BRANCH_NAME}"]])
    }
    parameters {
        string name: "messageNumber"
        string name: "INBOX"
        gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH_NAME', type: 'PT_BRANCH'
    }
    environment {
        MAIL_CONFIG = credentials('smtp')
    }
    stages {
        stage('Download Patches') {
            agent {
                dockerfile {
                    filename 'Dockerfile'
                    dir 'mailer'
                    customWorkspace "/var/jenkins_home/repos/${params.BRANCH_NAME}"
                }
            }
            steps {
                dir("mailer") {
                    script {
                        sh "./mailer.sh ${env.MAIL_CONFIG} downloadReFormat ../incoming ${params.messageNumber} ${params.INBOX}"
                    }
                }
            }
        }
        stage('Apply Patch') {
            agent {
                dockerfile {
                    filename 'Dockerfile'
                    dir 'mailer'
                    customWorkspace "/var/jenkins_home/repos/${params.BRANCH_NAME}"
                }
            }
            steps {
                script {
                    sh "git am incoming/*"
                }
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'gradle:7.4.2-jdk11-alpine'
                    customWorkspace "/var/jenkins_home/repos/${params.BRANCH_NAME}"
                }
            }
            steps {
                script {
                    sh "./gradlew build"
                }
            }
        }
        stage('Push') {
            agent {
                dockerfile {
                    filename 'Dockerfile'
                    dir 'mailer'
                    customWorkspace "/var/jenkins_home/repos/${params.BRANCH_NAME}"
                }
            }
            steps {
                script {
                    sh "git push origin ${params.BRANCH_NAME}"
                }
            }
        }
    }
}
