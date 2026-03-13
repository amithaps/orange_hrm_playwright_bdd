from playwright.sync_api import expect


class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username = page.get_by_role("textbox", name="Username")
        self.password = page.get_by_role("textbox", name="Password")
        self.login_btn = page.get_by_role("button", name="Login")


    def launch_app(self):
        self.page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    def submit_login_page(self, user_name, user_pwd):
        expect(self.page.get_by_role("img", name="company-branding")).to_be_visible()
        self.username.fill(user_name)
        self.password.fill(user_pwd)
        self.login_btn.click()
        expect(self.page.get_by_role("heading", name="Dashboard")).to_be_visible()

        from pages.dashboard_page import DashboardPage
        dashboard_pg = DashboardPage(self.page)
        return dashboard_pg