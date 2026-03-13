import re
from playwright.sync_api import expect, Page


class LogoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.profile_dropdown = page.locator(".oxd-userdropdown-tab").locator(".oxd-userdropdown-icon")
        self.logout_menuitem = page.get_by_role("menuitem", name="Logout")


    def logout_app(self):
        self.profile_dropdown.click()
        expect(self.logout_menuitem).to_be_visible()
        self.logout_menuitem.click()
        return self.page