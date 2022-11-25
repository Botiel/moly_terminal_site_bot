import pytest
import sys
import os
from playwright.sync_api import sync_playwright, Page
from test_cases_pytest.page_objects import *
from test_cases_pytest.utils import MAIN_FOLDER, FULL_TIMESTAMP


class Bot:

    def __init__(self, page: Page):
        self.page = page
        self.url = None
        self.error = None

    def run_url(self):
        try:
            AddToCart(page=self.page, url=self.url).run_page()
            CheckOut(page=self.page).run_page()
            PaymentPage(page=self.page).run_page()
        except Exception as e:
            self.error = e
            raise Exception

    def get_screenshot(self):
        shop = self.url.split("/")[-2]
        self.page.screenshot(path=f"{MAIN_FOLDER}/{shop}.png", full_page=True)


def get_urls() -> list[str]:

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
            page = browser.new_context().new_page()
            url_list = TerminalMap.get_urls(page=page)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit()

    return url_list


def pytest_cmdline_preparse(config):
    if not os.path.exists(MAIN_FOLDER):
        os.makedirs(MAIN_FOLDER)
    config.option.report = [f"{MAIN_FOLDER}/report_{FULL_TIMESTAMP}.html"]


@pytest.fixture(scope="function")
def setup(page):

    print("\n******** SETTING UP BOT ********")
    bot = Bot(page)

    yield bot

    print("\n******** TEARDOWN ********")
    if bot.error:
        bot.get_screenshot()
        print("\nScreenshot was created!")

    bot.page.close()


# def pytest_cmdline_main(config):
#     print(config.option)

