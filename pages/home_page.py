# pages/home_page.py
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.offline_payment_page import OfflinePaymentPage


class HomePage(BasePage):
    """Page Object for the post-login Home/Dashboard page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.expected_url = "https://onesolutionakolaprompt.tabamc.in/PropertyTax/Home"

    def navigate_to_offline_payment(self) -> OfflinePaymentPage:
        """Teleports directly to the target URL, bypassing the brittle dynamic sidebar completely."""


        self.page.goto("https://onesolutionakolaprompt.tabamc.in/propertyTax/OfflinePayment")
        self.page.wait_for_load_state("domcontentloaded")

        return OfflinePaymentPage(self.page)