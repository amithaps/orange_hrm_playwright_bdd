class DashboardPage:
    def __init__(self, page):
        self.page = page
        self.time_at_work_widget = page.locator("div.orangehrm-dashboard-widget").filter(has_text="Time at Work")
        self.clock_icon = self.time_at_work_widget.locator("button.orangehrm-attendance-card-action")

    def click_clock_icon(self):
        self.clock_icon.click()
        from pages.attendance_page import AttendancePage
        attendance_pg = AttendancePage(self.page)
        return attendance_pg