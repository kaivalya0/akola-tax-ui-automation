# conftest.py
from typing import Generator
import pytest
from playwright.sync_api import BrowserContext, Page
from pages.login_page import LoginPage

@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    new_page = context.new_page()
    new_page.set_default_navigation_timeout(60000)
    new_page.set_default_timeout(30000)
    yield new_page
    new_page.close()

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Forces explicit viewport and locale to prevent CI responsive collapse and language toggles."""
    return {
        **browser_context_args,
        "locale": "en-US",
        "timezone_id": "Asia/Kolkata",
        "ignore_https_errors": True,
        "viewport": {
            "width": 1920,
            "height": 1080,
        }
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Chromium-level arguments to eliminate browser-level overlays."""
    return {
        **browser_type_launch_args,
        "args": [
            "--disable-save-password-bubble",
            "--disable-autofill-keyboard-accessory-view",
            "--disable-single-click-autofill",
            "--disable-infobars"
        ]
    }