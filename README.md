# OrangeHRM Playwright Automation Framework
A hybrid Behavior-Driven Development (BDD) and Page Object Model (POM) test automation framework for OrangeHRM, built with Python, Pytest, and Playwright.
AUT: https://opensource-demo.orangehrmlive.com/

# 🚀 Features
BDD Support: Gherkin scenarios using pytest-bdd.

POM Architecture: Clean separation of page logic and test execution.

Multi-Browser: Custom support for Chrome, Firefox, and Edge.

Jenkins Ready: Automated pipeline with Jenkinsfile (Pipeline-as-Code). 

Artifact Reporting: Integrated Playwright Tracing and self-contained local HTML reporting.

# 🏗️ Project Structure
pages/: Page Object classes (Login, Dashboard, Attendance, etc.)

attendance.feature: Cucumber-Gherkin scenario definitions.

conftest.py: Global fixtures and browser configuration.

pytest.ini: Test runner configuration and markers.

test_attendance_bdd.py: BDD Runner

test_hrm_pom.py: Direct POM Runner 

Jenkinsfile: Pipeline definition for Docker-based CI execution.

# 🧪 Running Tests
You can run tests using the custom --browser_name flag. Tracing is enabled to record test execution for debugging.

# Jenkins Execution & Reporting
This project is configured to run automatically in Jenkins using a Pipeline-as-Code setup, executed within a Dockerized Playwright agent for environment consistency.

# BDD Execution (Attendance Flow)
## Run in Firefox
pytest --browser firefox --tracing on --browser_name firefox test_attendance_bdd.py

# POM Execution (Direct Scripts)
## Run in Chrome with HTML Report
pytest --tracing on --html=report.html test_hrm_pom.py
