import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.attendance_page import AttendancePage
from pages.logout_page import LogoutPage

# pytest --headed --tracing on --browser_name edge test_attendance_bdd.py

scenarios('attendance.feature')
class ScenarioContext:
    def __init__(self):
        self.login_page: LoginPage | None = None
        self.dashboard_page: DashboardPage | None = None
        self.attendance_page: AttendancePage | None = None
        self.logout_page: LogoutPage | None = None
        self.initial_note: str = ""
        self.updated_note: str = ""

@pytest.fixture
def test_step_context():
    return ScenarioContext()

@given("I am on the OrangeHRM login page")
#def launch_hrm(test_step_context, select_browser):
def launch_hrm(test_step_context, page):
    test_step_context.login_page = LoginPage(page)
    test_step_context.login_page.launch_app()

@when(parsers.parse("I login with credentials"))
def login_hrm(test_step_context, user_creds):
    test_step_context.dashboard_page = test_step_context.login_page.submit_login_page(user_creds["user_name"],
                                                                                      user_creds["user_pwd"])

@when("I navigate to the Attendance section")
def navigate_to_attendance(test_step_context):
    test_step_context.attendance_page = test_step_context.dashboard_page.click_clock_icon()

@when("I ensure a clean state by removing existing records")
def cleanup_preexisting_records(test_step_context):
    test_step_context.attendance_page = test_step_context.attendance_page.cleanup_records()

@when(parsers.parse("I create a Punch-in record with note {initial_note}"))
def create_punch_in_record(test_step_context, initial_note):
    test_step_context.initial_note = initial_note
    test_step_context.attendance_page = test_step_context.attendance_page.create_attendance_record(note=test_step_context.initial_note)

@when(parsers.parse("I update the record note to {updated_note}"))
def update_punch_in_record(test_step_context, updated_note):
    test_step_context.updated_note = updated_note
    test_step_context.attendance_page = test_step_context.attendance_page.update_attendance_record(old_note=test_step_context.initial_note,
        new_note=test_step_context.updated_note)

@then(parsers.parse("I delete the record with note {updated_note}"))
def delete_punch_in_record(test_step_context, updated_note):
    test_step_context.updated_note = updated_note
    test_step_context.logout_page = test_step_context.attendance_page.delete_attendance_record(note=test_step_context.updated_note)

@then("I log out of the application")
def logout_hrm(test_step_context):
    test_step_context.logout_page.logout_app()