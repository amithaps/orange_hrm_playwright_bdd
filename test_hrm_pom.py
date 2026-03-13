import pytest
from playwright.sync_api import Page, sync_playwright
# classes are in a folder named 'pages'
from pages.login_page import LoginPage

@pytest.mark.smoke
@pytest.mark.regression
def test_orange_hrm_attendance_flow(page: Page):
    # 1. Initialize and Login
    # The login method should return a DashboardPage instance
    login_page = LoginPage(page)
    login_page.launch_app()
    dashboard_page = login_page.submit_login_page("Admin", "admin123")

    # 2. Navigate to Attendance
    # The dashboard method should return an AttendancePage instance
    attendance_page = dashboard_page.click_clock_icon()

    # 3. Cleanup and CRUD Flow
    # Note: methods returning 'self' allow you to update the same variable
    attendance_page = attendance_page.cleanup_records()
    attendance_page = attendance_page.create_attendance_record()
    attendance_page = attendance_page.update_attendance_record()

    # 4. Final step and Logout
    # delete_attendance_record returns the LogoutPage (or UserMenu) instance
    logout_page = attendance_page.delete_attendance_record()
    logout_page.logout_app()

    # Final browser cleanup
    #page.close()