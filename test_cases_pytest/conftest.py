import pytest
import sys
import os
from playwright.sync_api import sync_playwright, Page
from test_cases_pytest.page_objects import *
from test_cases_pytest.utils import MAIN_FOLDER, FULL_TIMESTAMP


class Bot:

    def __init__(self, page: Page):
        self.page = page
        self.url = ""
        self.shop_folder = ""

    def create_shop_log_folder(self) -> None:
        shop = self.url.split("/")[-2]
        self.shop_folder = f"{MAIN_FOLDER}/{shop}"
        if not os.path.exists(self.shop_folder):
            os.makedirs(self.shop_folder)

    def write_to_log(self, msg) -> None:
        with open(f"{self.shop_folder}/log.log", "a") as f:
            f.writelines(f"{msg.type}: {msg.text}\n")

    def take_screenshot(self, index: str) -> None:

        shop = self.url.split("/")[-2]
        self.page.screenshot(path=f"{self.shop_folder}/{shop}_{index}.png", full_page=True)
        print(f"\n{index} screenshot was created!\n")

    def run_url(self) -> None:

        self.create_shop_log_folder()

        self.page.on("console", lambda msg: self.write_to_log(msg))
        print("Creating console log file...\n")

        try:
            self.page.goto(self.url)

            self.take_screenshot(index="store page")
            AddToCart(page=self.page).run_page()

            self.take_screenshot(index="checkout page")
            CheckOut(page=self.page).run_page()

            PaymentPage(page=self.page).run_page()
            self.take_screenshot(index="payment page")

        except Exception as e:
            self.take_screenshot(index="error")
            raise Exception(e)


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

    print("\n******** SETTING UP BOT ********\n")
    page.set_viewport_size({"width": 1600, "height": 900})
    bot = Bot(page)

    yield bot

    print("\n******** TEARDOWN ********")
    bot.page.close()
    print("Page closed...")


# def pytest_cmdline_main(config):
#     print(config.option)

