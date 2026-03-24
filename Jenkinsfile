pipeline {
    agent {
        // Using a custom Dockerfile defined in the repo
        // This 'bakes' the environment instead of installing at runtime
        dockerfile {
            filename 'Dockerfile'
            args '--ipc=host --user root'
        }
    }

    environment {
        ORANGE_HRM_CREDS = credentials('orange-hrm-creds')
        CI = 'true'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Verify Environment') {
            steps {
                sh 'pip --version'
                sh 'playwright --version'
            }
        }

        stage('Run Playwright Tests') {
            steps {
                sh 'pytest --tracing retain-on-failure --browser_name chrome --html=report.html --self-contained-html test_attendance_bdd.py'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'report.html, test-results/**/*.zip', allowEmptyArchive: true
        }
    }
}
//pipeline {
//    agent {
//        docker {
//            // Official Microsoft Playwright image
//            image 'mcr.microsoft.com/playwright/python:v1.40.0-jammy'
//            args '--ipc=host --user root'
//        }
//    }
//
//    environment {
//        // This makes the credentials available as environment variables in Python
//        ORANGE_HRM_CREDS = credentials('orange-hrm-creds')
//        // It tells your conftest.py to run in 'headless' mode automatically.
//        CI = 'true'
//    }
//
//    stages {
//        stage('Checkout Code') {
//            steps {
//                checkout scm
//            }
//        }
//
//        stage('Install Dependencies') {
//            steps {
//                sh '''
//                    pip install --upgrade pip
//                    pip install -r requirements.txt
//
//                    # we must install the actual branded Google Chrome binary.
//                    # 'playwright install' alone installs Chromium, Firefox, and WebKit.
//                    # 'playwright install chrome' specifically adds the Google Chrome stable build.
//                    playwright install chrome
//                '''
//            }
//        }
//
//        stage('Run Playwright Tests') {
//            steps {
//                // This command matches conftest.py choices and logic.
//                sh 'pytest --tracing retain-on-failure --browser_name chrome --html=report.html --self-contained-html test_attendance_bdd.py'
//            }
//        }
//    }
//
//    post {
//        always {
//            // Archive the HTML report and the Playwright traces
//            archiveArtifacts artifacts: 'report.html, test-results/**/*.zip', allowEmptyArchive: true
//        }
//    }
//}