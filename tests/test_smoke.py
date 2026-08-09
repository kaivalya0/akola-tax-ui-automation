# test_smoke.py
from playwright.sync_api import Page, expect


def test_google_accessibility(page: Page) -> None:
    # Act: Attempt to navigate to an external site
    page.goto("https://www.google.com")

    # Assert: Verify the browser loaded the page successfully
    expect(page).to_have_title("Google")