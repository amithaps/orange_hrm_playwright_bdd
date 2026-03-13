import re
from playwright.sync_api import Page, expect

def test_punch_in_crud(page: Page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    #context.tracing.start(screenshots=True, snapshots=True, sources=True)

    # Login
    expect(page.get_by_role("img", name="company-branding")).to_be_visible()
    page.get_by_role("textbox", name="Username").fill("Admin")
    page.get_by_role("textbox", name="Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    expect(page.get_by_role("heading", name ="Dashboard")).to_be_visible()

    # Widget Navigation
    (page.locator("div.orangehrm-dashboard-widget")
     .filter(has_text="Time at Work")
     .locator("button.orangehrm-attendance-card-action")
     .click())
    page.get_by_role("listitem").filter(has_text="Attendance").locator("i.bi-chevron-down").click()
    expect(page.get_by_role("menuitem", name="My Records")).to_be_visible()
    page.get_by_role("listitem").filter(has_text=re.compile(r"^My Records$")).click()

    no_records_msg = page.locator(".orangehrm-horizontal-padding").get_by_text("No Records Found")
    try:
        expect(no_records_msg).to_be_visible(timeout=5000)
        print("Confirmed: No existing records found. Proceeding to Create flow.")
    except:
        print("Records detected. Performing cleanup...")
        page.locator(".oxd-table-header-cell").get_by_role("checkbox").check(force=True)
        page.get_by_role("button", name=re.compile(r"Delete Selected")).click(force=True)
        page.get_by_role("button", name="Yes, Delete").click()
        try:
            page.locator(".oxd-loading-spinner").wait_for(state="hidden", timeout=15000)
        except Exception:
            pass  # If it was too fast to catch, just move on
        try:
            expect(no_records_msg).to_be_visible(timeout=10000)
            print("Confirmed: Table is empty. Proceeding.")
        except Exception as e:
            print(f"Final state check failed: {e}")



    # Punch In Flow - Create
    attendance_menu = page.get_by_role("listitem").filter(has_text="Attendance")
    if not page.get_by_role("menuitem", name="Punch In/Out").is_visible():
        attendance_menu.locator("i.bi-chevron-down").click()
    expect(page.get_by_role("menuitem", name="Punch In/Out")).to_be_visible()
    page.get_by_role("listitem").filter(has_text=re.compile(r"^Punch In/Out$")).click()
    expect(page.get_by_role("heading", name="Punch In")).to_be_visible()
    page.locator(".oxd-icon.bi-calendar").click()
    today_selector = ".oxd-calendar-date.--today"
    expect(page.locator(".oxd-date-input-calendar .oxd-calendar-dates-grid")).to_be_visible()
    page.locator(today_selector).click()
    page.get_by_role("textbox", name="Type here").fill("Starting Shift 101")
    page.get_by_role("button", name="In").click()
    page.evaluate("window.scrollTo(0, 0)")
    try:
        page.locator(".oxd-loading-spinner").wait_for(state="visible", timeout=2000)
    except:
        pass  # If it was too fast to catch, just move on
    page.locator(".oxd-loading-spinner").wait_for(state="hidden", timeout=15000)
    expect(page.get_by_role("heading", name="Punch Out")).to_be_visible()

    # Punch In Flow - Read & Update
    page.get_by_role("listitem").filter(has_text="Attendance").locator("i.bi-chevron-down").click()
    expect(page.get_by_role("menuitem", name="My Records")).to_be_visible()
    page.get_by_role("listitem").filter(has_text=re.compile(r"^My Records$")).click(timeout=10000)
    target_row = page.locator(".oxd-table-card").filter(has_text="Starting Shift 101")
    target_row.get_by_role("button").filter(has=page.locator(".bi-pencil-fill")).click()
    try:
        page.locator(".oxd-loading-spinner").wait_for(state="visible", timeout=2000)
    except:
        pass  # If it was too fast to catch, just move on
    page.locator(".oxd-loading-spinner").wait_for(state="hidden", timeout=15000)
    expect(page.get_by_text("Edit Attendance Records", exact=True)).to_be_visible()
    page.get_by_role("textbox", name="Type here").fill("Starting Shift 101 - Updated")
    page.get_by_role("button", name="Save").click()
    try:
        page.locator(".oxd-loading-spinner").wait_for(state="visible", timeout=2000)
    except:
        pass  # If it was too fast to catch, just move on
    page.locator(".oxd-loading-spinner").wait_for(state="hidden", timeout=15000)

    # Punch In Flow - Delete
    expect(page.get_by_text("Starting Shift 101 - Updated")).to_be_visible(timeout=5000)
    target_row = page.locator(".oxd-table-card").filter(has_text="Starting Shift 101 - Updated")
    target_row.get_by_role("button").filter(has=page.locator(".bi-trash")).click()
    page.get_by_role("button", name="Yes, Delete").click()
    try:
        page.locator(".oxd-loading-spinner").wait_for(state="visible", timeout=2000)
    except:
        pass  # If it was too fast to catch, just move on
    page.locator(".oxd-loading-spinner").wait_for(state="hidden", timeout=15000)
    expect(page.get_by_role("heading", name="My Attendance Records")).to_be_visible()
    expect(no_records_msg).to_be_visible(timeout=5000)

    # Logout
    page.locator(".oxd-userdropdown-tab").locator(".oxd-userdropdown-icon").click()
    expect(page.get_by_role("menuitem", name="Logout")).to_be_visible()
    page.get_by_role("menuitem", name="Logout").click()
    page.close()




