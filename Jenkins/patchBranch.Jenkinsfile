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
                    args '-v /var/jenkins_home/:/var/jenkins_home/:rw,z'
                }
            }
            steps {
                dir("/var/jenkins_home/repos/${params.BRANCH_NAME}") {
                    script {
                        dir("/var/jenkins_home/repos/main/mailer"){
                            sh "./mailCredsLoader.sh ${env.MAIL_CONFIG} mailer.py downloadReFormat --path /var/jenkins_home/repos/${params.BRANCH_NAME}/incoming --messageNumber ${params.messageNumber} --imapInbox ${params.INBOX}"
                        }
                    }
                }
            }
        }
        stage('Apply Patch') {
            agent {
                dockerfile {
                    filename 'Dockerfile'
                    dir 'mailer'
                    args '-v /var/jenkins_home/:/var/jenkins_home/:rw,z'
                }
            }
            steps {
                dir("/var/jenkins_home/repos/${params.BRANCH_NAME}"){
                    script {
                        sh "git config user.email 'you@example.com'"
                        sh "git config user.name 'Your Name'"
                        try {
                            sh "git am incoming/*"
                        } catch (Exception e) {
                            echo 'Exception occurred: ' + e.toString()
                            sh "git am --show-current-patch > bad.patch"
                            sh "git am --abort"
                            dir("/var/jenkins_home/repos/main/mailer"){
                                sh "./mailCredsLoader.sh ${env.MAIL_CONFIG} mailer.py failedPatchMail --badPatchPath /var/jenkins_home/repos/${params.BRANCH_NAME}/bad.patch"
                            }
                            error e
                        }
                    }
                }
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'gradle:7.4.2-jdk11-alpine'
                    args '-v /var/jenkins_home/:/var/jenkins_home/:rw,z'
                }
            }
            steps {
                dir("/var/jenkins_home/repos/${params.BRANCH_NAME}"){
                    script {
                        sh "./gradlew build"
                    }
                }
            }
        }
        stage('Push') {
            agent {
                dockerfile {
                    filename 'Dockerfile'
                    dir 'mailer'
                    args '-v /var/jenkins_home/:/var/jenkins_home/:rw,z'
                }
            }
            steps {
                dir("/var/jenkins_home/repos/${params.BRANCH_NAME}"){
                    script {
                        withCredentials([usernameColonPassword(credentialsId: 'github', variable: 'GIT_CREDS')]) {
                            sh "git push origin HEAD:${params.BRANCH_NAME}"
                        }
                    }
                }
            }
        }
    }
}
