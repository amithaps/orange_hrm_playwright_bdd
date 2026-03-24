import pytest
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def user_creds():
    """
    Fixture to provide credentials.
    Uses Jenkins environment variables. From local refers to local Env Vars.
    """
    # user = os.getenv('ORANGE_HRM_CREDS_USR', 'Admin')
    # pw = os.getenv('ORANGE_HRM_CREDS_PSW', 'admin123')
    user = os.getenv('ORANGE_HRM_CREDS_USR')
    pw = os.getenv('ORANGE_HRM_CREDS_PSW')

    if not user or not pw:
        pytest.exit("\n[ERROR] Credentials not found! Check your Jenkins Vault or local Env Vars.")

    return {"user_name": user, "user_pwd": pw}

# @pytest.fixture(scope="session")
# def fixture_user_creds(request):
#     return request.param

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name",
        action="store",
        default="chrome",
        help="browser option: chrome or firefox or edge",
        choices = ("chrome", "firefox", "edge")
    )

# Sample implementation but overrides default page. Explicit close(). Command line Traces wont be possible.

# @pytest.fixture()
# def select_browser(playwright, request):
#     browser_name = request.config.getoption("browser_name")
#     if browser_name == "chrome":
#         browser = playwright.chromium.launch(headless=False)
#     elif browser_name == "firefox":
#         browser = playwright.firefox.launch(headless=False)
#     # ADDED: Support for Microsoft Edge
#     elif browser_name == "edge":
#         # We use playwright.chromium because Edge is a Chromium-based browser,
#         # but we specify the 'msedge' channel to launch the branded version.
#         browser = playwright.chromium.launch(channel="msedge", headless=False)
#
#     context = browser.new_context()
#     page = context.new_page()
#     yield page
#     context.close()
#     browser.close()

@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig):
    """
    This tells Playwright WHICH brand to launch.
    This is the ONLY place 'channel' is allowed.
    """
    browser_name = pytestconfig.getoption("browser_name")
    # 1. Fetch environment variable and normalize to lowercase string
    ci_env_str = os.getenv("CI", "false").lower()
    # 2. Compare string to "true" to create a REAL Boolean (True or False)
    is_ci_boolean = (ci_env_str == "true")
    # 3. Assign the Boolean result to headless. headless=False for local runs (or True for Jenkins)
    launch_args = {"headless": is_ci_boolean}

    if browser_name == "edge":
        launch_args["channel"] = "msedge"
    elif browser_name == "chrome":
        launch_args["channel"] = "chrome"
    # Firefox has no channel, so it just gets {"headless": False}
    return launch_args


