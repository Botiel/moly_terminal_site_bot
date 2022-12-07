import pytest
from test_cases_pytest.conftest import get_urls


URL_LIST = get_urls()[:5]


@pytest.mark.parametrize("url", URL_LIST)
def test_url(setup, url):
    bot = setup
    bot.url = url + '?x'
    bot.run_url()












