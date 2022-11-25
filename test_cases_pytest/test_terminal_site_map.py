import pytest
from test_cases_pytest.conftest import get_urls


URL_LIST = get_urls()


@pytest.mark.parametrize("url", URL_LIST)
def test_url(setup, url):
    bot = setup
    bot.url = url
    bot.run_url()


def test_debug(setup):
    url = 'some url'

    bot = setup
    bot.url = url
    bot.run_url()










