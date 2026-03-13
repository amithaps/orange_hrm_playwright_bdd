import re
from playwright.sync_api import expect, Page

class AttendancePage:
    def __init__(self, page: Page):
        self.page = page
        self.list_item_attendance_dropdown = page.get_by_role("listitem").filter(has_text="Attendance").locator("i.bi-chevron-down")
        self.menu_item_my_records = page.get_by_role("menuitem", name="My Records")
        self.menu_item_my_records2 = page.get_by_role("listitem").filter(has_text=re.compile(r"^My Records$"))
        self.no_records_msg = page.locator(".orangehrm-horizontal-padding").get_by_text("No Records Found")
        self.check_box_header = page.locator(".oxd-table-header-cell").get_by_role("checkbox")
        self.button_delete_all = page.get_by_role("button", name=re.compile(r"Delete Selected"))
        self.button_delete_confirmation = page.get_by_role("button", name="Yes, Delete")
        self.loading_spinner = page.locator(".oxd-loading-spinner")
        self.punch_in_out_dropdown = page.get_by_role("menuitem", name="Punch In/Out")
        self.punch_in_out_dropdown2 = page.get_by_role("listitem").filter(has_text=re.compile(r"^Punch In/Out$"))
        self.punch_in_heading = page.get_by_role("heading", name="Punch In")
        self.calendar_button = page.locator(".oxd-icon.bi-calendar")
        self.calendar_popup = page.locator(".oxd-date-input-calendar .oxd-calendar-dates-grid")
        self.today_selector = page.locator(".oxd-calendar-date.--today")
        self.punch_in_note = page.get_by_role("textbox", name="Type here")
        self.submit_punch_in_button = page.get_by_role("button", name="In")
        self.punch_out_heading = page.get_by_role("heading", name="Punch Out")
        self.scroll_up = page.evaluate("window.scrollTo(0, 0)")
        #self.target_attendance_row = page.locator(".oxd-table-card").filter(has_text="Starting Shift 101")
        #self.edit_button = self.target_attendance_row.get_by_role("button").filter(has=self.page.locator(".bi-pencil-fill"))
        self.edit_attendance_text = page.get_by_text("Edit Attendance Records", exact=True)
        self.submit_edit_punch_in_button = page.get_by_role("button", name="Save")
        #self.find_updated_row = page.get_by_text("Starting Shift 101 - Updated")
        #self.target_att_updated_row = page.locator(".oxd-table-card").filter(has_text="Starting Shift 101 - Updated")
        #self.delete_row_button = self.target_att_updated_row.get_by_role("button").filter(has=self.page.locator(".bi-trash"))
        self.delete_row_confirmation = page.get_by_role("button", name="Yes, Delete")
        self.page_text_for_validation = page.get_by_role("heading", name="My Attendance Records")


    def cleanup_records(self):
        self.list_item_attendance_dropdown.click()
        expect(self.menu_item_my_records).to_be_visible()
        self.menu_item_my_records2.click()

        try:
            expect(self.no_records_msg).to_be_visible(timeout=5000)
            print("Confirmed: No existing records found. Proceeding to Create flow.")
        except:
            print("Records detected. Performing cleanup...")
            self.check_box_header.check(force=True)
            self.button_delete_all.click(force=True)
            self.button_delete_confirmation.click()
        try:
            self.loading_spinner.wait_for(state="hidden", timeout=15000)
        except Exception:
            pass  # If it was too fast to catch, just move on
        try:
            expect(self.no_records_msg).to_be_visible(timeout=10000)
            print("Confirmed: Table is empty. Proceeding.")
        except Exception as e:
            print(f"Final state check failed: {e}")
        return self

    def create_attendance_record(self, note="Starting Shift 101"):
        # Punch In Flow - Create
        if not self.punch_in_out_dropdown.is_visible():
            self.list_item_attendance_dropdown.click()
        expect(self.punch_in_out_dropdown).to_be_visible()
        self.punch_in_out_dropdown2.click()
        expect(self.punch_in_heading).to_be_visible()

        self.calendar_button.click()
        expect(self.calendar_popup).to_be_visible()
        self.today_selector.click()
        self.punch_in_note.fill(note)
        self.submit_punch_in_button.click()
        self.scroll_up
        try:
            self.loading_spinner.wait_for(state="visible", timeout=2000)
        except:
            pass  # If it was too fast to catch, just move on
        self.loading_spinner.wait_for(state="hidden", timeout=15000)
        expect(self.punch_out_heading).to_be_visible()
        return self

    def update_attendance_record(self, old_note="Starting Shift 101", new_note="Starting Shift 101 - Updated"):
        # Punch In Flow - Read & Update
        self.list_item_attendance_dropdown.click()
        expect(self.menu_item_my_records).to_be_visible()
        self.menu_item_my_records2.click(timeout=10000)

        target_attendance_row = self.page.locator(".oxd-table-card").filter(has_text=old_note)
        edit_button = target_attendance_row.get_by_role("button").filter(has=self.page.locator(".bi-pencil-fill"))
        edit_button.click()

        try:
            self.loading_spinner.wait_for(state="visible", timeout=2000)
        except:
            pass  # If it was too fast to catch, just move on

        self.loading_spinner.wait_for(state="hidden", timeout=15000)
        expect(self.edit_attendance_text).to_be_visible()
        self.punch_in_note.fill(new_note)
        self.submit_edit_punch_in_button.click()

        try:
            self.loading_spinner.wait_for(state="visible", timeout=2000)
        except:
            pass  # If it was too fast to catch, just move on
        self.loading_spinner.wait_for(state="hidden", timeout=15000)
        return self

    def delete_attendance_record(self, note="Starting Shift 101 - Updated"):
        # Punch In Flow - Delete
        find_updated_row = self.page.get_by_text(note)
        expect(find_updated_row).to_be_visible(timeout=5000)

        target_att_updated_row = self.page.locator(".oxd-table-card").filter(has_text=note)
        delete_row_button = target_att_updated_row.get_by_role("button").filter(has=self.page.locator(".bi-trash"))
        delete_row_button.click()
        self.delete_row_confirmation.click()
        try:
            self.loading_spinner.wait_for(state="visible", timeout=2000)
        except:
            pass  # If it was too fast to catch, just move on
        self.loading_spinner.wait_for(state="hidden", timeout=15000)

        expect(self.page_text_for_validation).to_be_visible()
        expect(self.no_records_msg).to_be_visible(timeout=5000)

        from pages.logout_page import LogoutPage
        logout_pg = LogoutPage(self.page)
        return logout_pg