pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            dir 'mailer'
        }
    }
    options {
        lock(extra: [[resource: "jenkins_pipeline_${params.BRANCH_NAME}"]])
    }
    parameters {
        string name: "messageNumber"
        string name: "INBOX"
        gitParameter branchFilter: 'origin/(.*)', name: 'BRANCH_NAME', type: 'PT_BRANCH'
    }
    stages {
        stage('Download Patches') {
            steps {
                script {
                    sh "ls && pwd"
                }
            }
        }
        stage('Apply Patch') {
            steps {
                script {
                    sh "ls && pwd"
                }
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'gradle:7.4.2-jdk11-alpine'
                }
            }
            steps {
                script {
                    sh "ls && pwd"
                }
            }
        }
        stage('Push') {
            steps {
                script {
                    sh "ls && pwd"
                }
            }
        }
    }
}
