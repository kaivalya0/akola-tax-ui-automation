# tests/test_login.py
import pytest
from playwright.sync_api import Page, expect
from config.config import Config
from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.data_loader import DataLoader

# Load the login and invalid user data from your JSON file
data = DataLoader.load_json("property_tax_data.json")["property_tax"]


def test_valid_admin_login(page: Page) -> None:
    """Validates successful login with correct administrative credentials."""
    # AAA: Arrange
    login_page = LoginPage(page)
    login_page.navigate_to(data["url"])

    # AAA: Act
    login_page.perform_login(Config.VALID_USERNAME, Config.VALID_PASSWORD)

    # AAA: Assert
    home_page = HomePage(page)
    expect(page).to_have_url(home_page.expected_url, timeout=15000)


@pytest.mark.parametrize("invalid_case", data["invalid_users"])
def test_invalid_login_scenarios(page: Page, invalid_case) -> None:
    """Data-driven negative test suite for login error validations."""
    # AAA: Arrange
    login_page = LoginPage(page)
    login_page.navigate_to(data["url"])

    # AAA: Act
    login_page.perform_login(invalid_case["username"], invalid_case["password"])

    # AAA: Assert - Check that the expected error message is visible on the page
    error_banner = page.get_by_text(invalid_case["error"])
    expect(error_banner).to_be_visible(timeout=10000)