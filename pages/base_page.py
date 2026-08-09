from playwright.sync_api import Locator, Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate_to(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    @staticmethod
    def click_element(locator: Locator) -> None:
        locator.wait_for(state="visible")
        locator.click()

    @staticmethod
    def fill_input(locator: Locator, text: str) -> None:
        locator.wait_for(state="visible")
        locator.fill(text)