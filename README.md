# OrangeHRM Playwright Automation Framework
A hybrid Behavior-Driven Development (BDD) and Page Object Model (POM) test automation framework for OrangeHRM, built with Python, Pytest, and Playwright.
AUT: https://opensource-demo.orangehrmlive.com/

# 🚀 Features
BDD Support: Gherkin scenarios using pytest-bdd.
POM Architecture: Clean separation of page logic and test execution.
Multi-Browser: Custom support for Chrome, Firefox, and Edge.
Jenkins Ready: Integrated Playwright Tracing and HTML reporting.

# 🏗️ Project Structure
pages/: Page Object classes (Login, Dashboard, Attendance, etc.)

attendance.feature: Cucumber-Gherkin scenario definitions.

conftest.py: Global fixtures and browser configuration.

pytest.ini: Test runner configuration and markers.

test_attendance_bdd.py: BDD Runner

test_hrm_pom.py: Direct POM Runner 

# 🧪 Running Tests
You can run tests using the custom --browser_name flag. Tracing is enabled to record test execution for debugging.

# BDD Execution (Attendance Flow)
## Run in Firefox
pytest --browser firefox --tracing on --browser_name firefox test_attendance_bdd.py

# POM Execution (Direct Scripts)
## Run in Chrome with HTML Report
pytest --tracing on --html=report.html test_hrm_pom.py
