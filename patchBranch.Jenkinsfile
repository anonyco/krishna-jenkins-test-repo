pipeline {
    agent {
        node {
            name "built-in node"
            customWorkspace "/var/jenkins_home/repos/{params.BRANCH_NAME}"
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
            agent {
                dockerfile {
                    filename 'Dockerfile'
                    dir 'mailer'
                }
            }
            steps {
                script {
                    sh "ls && pwd"
                }
            }
        }
        stage('Apply Patch') {
            agent {
                dockerfile {
                    filename 'Dockerfile'
                    dir 'mailer'
                }
            }
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
            agent {
                dockerfile {
                    filename 'Dockerfile'
                    dir 'mailer'
                }
            }
            steps {
                script {
                    sh "ls && pwd"
                }
            }
        }
    }
}
