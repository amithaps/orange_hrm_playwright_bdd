import pytest

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

    # Start with headless=False (or True for Jenkins)
    launch_args = {"headless": True}

    if browser_name == "edge":
        launch_args["channel"] = "msedge"
    elif browser_name == "chrome":
        launch_args["channel"] = "chrome"

    # Firefox has no channel, so it just gets {"headless": False}
    return launch_args


