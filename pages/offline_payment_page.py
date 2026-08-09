# pages/offline_payment_page.py
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class OfflinePaymentPage(BasePage):
    """Page Object for the Offline Payment module."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Inputs & Buttons
        self.search_input: Locator = page.locator("#txtUpicID")
        self.search_button: Locator = page.locator("#btnSearch")
        self.search_results_table_rows: Locator = page.locator("table tbody tr")

        # Dialogs & Loaders
        self.swal_popup: Locator = page.get_by_role("dialog")
        self.swal_ok_button: Locator = page.get_by_role("button", name="OK")
        self.loading_spinner: Locator = page.locator(".loader, #loader, .spinner, .loading-overlay")
        self.no_dues_message: Locator = page.locator("#lblTaxPaidMsg")

    def wait_for_ready_state(self) -> None:
        """Blocks execution until the UI loader is gone."""
        self.loading_spinner.wait_for(state="hidden")

    def search_property(self, search_value: str) -> None:
        """AAA: Act - Waits for readiness, then executes search."""
        self.wait_for_ready_state()
        self.search_input.fill(search_value)
        self.search_button.click()

    def trigger_empty_search(self) -> None:
        """Triggers search without filling input."""
        self.wait_for_ready_state()
        self.search_button.click()

    def get_property_id_label(self, property_id: str) -> Locator:
        """Dynamically locates the property ID text."""
        return self.page.get_by_text(property_id).first