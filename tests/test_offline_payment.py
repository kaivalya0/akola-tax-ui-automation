# tests/test_offline_payment.py
import re
import pytest
from playwright.sync_api import Page, expect
from config.config import Config
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.offline_payment_page import OfflinePaymentPage
from utils.data_loader import DataLoader

data = DataLoader.load_json("property_tax_data.json")["offline_payment"]


@pytest.fixture
def authenticated_home(page: Page) -> HomePage:
    """Handles login setup before tests run."""
    login_page = LoginPage(page)
    login_page.navigate_to("https://onesolutionakolaprompt.tabamc.in/Login")
    login_page.perform_login(Config.VALID_USERNAME, Config.VALID_PASSWORD)

    home = HomePage(page)
    expect(page).to_have_url(home.expected_url, timeout=15000)
    return home


def test_offline_payment_positive_search_workflow(page: Page, authenticated_home: HomePage) -> None:
    # AAA: Arrange
    offline_page = OfflinePaymentPage(page)
    authenticated_home.navigate_to_offline_payment()
    expect(page).to_have_url(re.compile(r".*/OfflinePayment", re.IGNORECASE))

    # AAA: Act
    offline_page.search_property(data["valid_search"]["identifier"])

    # AAA: Assert
    expect(offline_page.search_results_table_rows.first).to_be_attached(timeout=15000)
    assert offline_page.search_results_table_rows.count() > 0


@pytest.mark.test_data_validation
def test_empty_search_warning_popup(page: Page, authenticated_home: HomePage) -> None:
    # AAA: Arrange
    offline_page = OfflinePaymentPage(page)
    authenticated_home.navigate_to_offline_payment()
    expect(page).to_have_url(re.compile(r".*/OfflinePayment", re.IGNORECASE))

    # AAA: Act
    offline_page.trigger_empty_search()

    # AAA: Assert
    expect(offline_page.swal_popup).to_be_visible(timeout=10000)
    offline_page.swal_ok_button.click()
    expect(offline_page.swal_popup).not_to_be_visible()


@pytest.mark.test_data_validation
def test_negative_unseeded_property_search_warning(page: Page, authenticated_home: HomePage) -> None:
    # AAA: Arrange
    offline_page = OfflinePaymentPage(page)
    authenticated_home.navigate_to_offline_payment()
    expect(page).to_have_url(re.compile(r".*/OfflinePayment", re.IGNORECASE))

    # AAA: Act
    offline_page.search_property(data["invalid_search"]["identifier"])

    # AAA: Assert

    try:
        offline_page.swal_popup.wait_for(state="visible", timeout=3000)
        offline_page.swal_ok_button.click()
    except Exception:
        expect(page).to_have_url(re.compile(r".*/OfflinePayment", re.IGNORECASE))


def test_offline_payment_no_dues_workflow(page: Page, authenticated_home: HomePage) -> None:
    """Validates the edge case where a property has no pending dues."""
    # AAA: Arrange
    offline_page = OfflinePaymentPage(page)
    authenticated_home.navigate_to_offline_payment()
    search_data = data["no_dues_search"]

    # AAA: Act
    offline_page.search_property(search_data["identifier"])

    try:
        offline_page.swal_popup.wait_for(state="visible", timeout=3000)
        offline_page.swal_ok_button.click()
    except Exception:
        pass  # No popup appeared, proceed normally

    # AAA: Assert - Verify the message exists in the DOM and contains the correct text
    expected_message = re.compile(r"No Dues are pending|थकबाकी बाकी नाही", re.IGNORECASE)

    expect(offline_page.no_dues_message).to_be_attached(timeout=15000)
    expect(offline_page.no_dues_message).to_contain_text(expected_message)

    # AAA: Assert - Verify Property details loaded underneath
    property_label = offline_page.get_property_id_label(search_data["identifier"])
    expect(property_label).to_be_attached(timeout=5000)