from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for OneSolution Property Tax Login."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.username_input: Locator = page.get_by_placeholder("Username", exact=True)
        self.password_input: Locator = page.get_by_placeholder("Password", exact=True)
        self.login_button: Locator = page.get_by_role("button", name="Sign in")

        # Strict locator to prevent substring/tag conflicts
        self.dashboard_header: Locator = page.locator("strong").filter(has_text="Collection Dashboard")

    def perform_login(self, username: str, password: str) -> None:
        """Pure action method: Fills credentials and clicks Sign In without assuming success."""
        if username:
            self.fill_input(self.username_input, username)
        if password:
            self.fill_input(self.password_input, password)

        self.click_element(self.login_button)