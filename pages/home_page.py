from playwright.sync_api import Locator, Page
from pages.base_page import BasePage
from pages.offline_payment_page import OfflinePaymentPage


class HomePage(BasePage):
    """Page Object for the post-login Home/Dashboard page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.expected_url = "https://onesolutionakolaprompt.tabamc.in/PropertyTax/Home"

        self.transaction_menu: Locator = page.locator("a:has-text('Transaction')").first
        self.offline_payment_menu: Locator = page.locator("a[href*='/propertyTax/OfflinePayment']")

    def navigate_to_offline_payment(self) -> OfflinePaymentPage:
        """Idempotent navigation: Bypasses shifting sidebar animations via JS injection."""

        if self.offline_payment_menu.is_hidden():
            self.transaction_menu.click(force=True)

        self.offline_payment_menu.wait_for(state="attached", timeout=3000)

        self.offline_payment_menu.evaluate("element => element.click()")

        return OfflinePaymentPage(self.page)