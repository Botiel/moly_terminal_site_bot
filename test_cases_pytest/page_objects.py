from playwright.sync_api import Page, expect
from test_cases_pytest.config import TERMINAL_SITE_MAP


class TerminalMap:
    site_url = "//tr/td/a"

    @classmethod
    def get_urls(cls, page: Page) -> list[str]:
        page.goto(TERMINAL_SITE_MAP)
        all_urls = page.query_selector_all(cls.site_url)

        url_list = [url.get_attribute("href") for url in all_urls]
        print(f"\nSite Map Quantity: {len(url_list)}\n")
        page.close()
        return url_list


class AddToCart:
    add_to_cart_button = '//a[text()="הוספה לסל"]'
    pagination = '//*[text()="הבא →"]'
    pagination2 = '//ul[@class="dokan-pagination"]/li[last()]/a'
    cart_loading = '//div[@class="xoo-wsc-basket active"]'
    cart_not_loading = '//div[@class="xoo-wsc-basket"]'
    checkout_btn = '//a[@class="xoo-wsc-ft-btn xoo-wsc-cart "]'
    checkout_url = "https://ashdod.shop/checkout/"

    def __init__(self, page: Page):
        self.page = page

    def search_for_add_button(self):

        while True:
            add_buttons = self.page.query_selector_all(self.add_to_cart_button)
            if add_buttons:
                add_buttons[0].click()
                return
            else:
                try:
                    self.page.locator(self.pagination).click(timeout=3000)
                except Exception as e:
                    print(f"Error:{e}\n\nmessage: No -add to cart- button")
                    raise Exception
                else:
                    continue

    def go_to_checkout(self):
        self.page.wait_for_selector(self.cart_loading, timeout=5000)
        self.page.wait_for_selector(self.cart_not_loading, timeout=5000)

        # self.page.query_selector_all(self.cart_not_loading)[0].click()
        # self.page.wait_for_selector(self.checkout_btn, timeout=3000)
        # self.page.query_selector_all(self.checkout_btn)[0].click()

        self.page.goto(self.checkout_url)

    def run_page(self):
        self.search_for_add_button()
        self.go_to_checkout()


class CheckOut:
    checkout_url = "https://ashdod.shop/checkout/"
    h3_order_details = '//h3[@id="order_review_heading"]'

    # ===== Details =======
    first_name = '//*[@name="billing_first_name"]'
    last_name = '//*[@name="billing_last_name"]'
    address = '//*[@name="billing_address_1"]'
    city = '//*[@name="billing_city"]'
    phone = '//*[@name="billing_phone"]'
    email = '//*[@name="billing_email"]'
    checkout_form_element = '//table[@class="shop_table woocommerce-checkout-review-order-table"]'
    terms = '//input[@id="terms"]'
    store_terms = '//input[@id="store-terms"]'
    shipping = '//input[@class="shipping_method"]'
    submit = '//*[@id="place_order_desktop"]'

    def __init__(self, page: Page):
        self.page = page

    def assert_page(self):
        expect(self.page).to_have_url(self.checkout_url)
        self.page.wait_for_selector(self.h3_order_details, timeout=20000)
        expect(self.page.locator(self.h3_order_details)).to_have_text("פרטי ההזמנה")

    def fill_form(self):
        self.page.fill(self.first_name, "test")
        self.page.fill(self.last_name, "test")
        self.page.fill(self.address, "test")
        self.page.fill(self.city, "test")
        self.page.fill(self.phone, "0584444444")
        self.page.fill(self.email, "test@test.io")

        self.page.wait_for_selector(self.checkout_form_element, timeout=3000)
        try:
            # Shipping method
            locator = self.page.query_selector_all(self.shipping)
            locator[0].click(timeout=3000)
        except Exception:
            pass

        self.page.locator(self.terms).click()
        self.page.locator(self.store_terms).click()
        self.page.locator(self.submit).click()

    def run_page(self):
        self.assert_page()
        self.fill_form()


class PaymentPage:
    payment_tag = '//*[text()="תשלום באשראי"]'
    submit = "submit_btn"

    def __init__(self, page: Page):
        self.page = page

    def run_page(self):
        self.page.wait_for_selector(self.payment_tag, timeout=10000)
        self.page.reload()
        frame = self.page.frame("chekout_frame")

        try:
            frame.get_by_role("button").click(timeout=2000)
        except Exception as e:
            print(f"error: {e}\n\nmessage: Payment Page Error!")
            raise Exception
