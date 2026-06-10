from playwright.sync_api import sync_playwright
from dataclasses import dataclass, field
from typing import List

@dataclass
class Sneaker:
    name: str
    price: str
    url: str
    image: str
    sizes: List[str] = field(default_factory=list)  # ✅ Fixed

    def __str__(self):
        return (
            f"{self.name}: {self.price}\n"
            f"{self.url}\n"
            f"{self.image}\n"
            f"Sizes: {', '.join(self.sizes) if self.sizes else 'No sizes'}"
        )



def close_popup(page):
    btn = page.get_by_label("Close pop-up")
    if btn.count() > 0:
        btn.click()


def get_urls(page):
    products = []
    elements = page.locator("figure")
    print(elements.count())
    for i in range(elements.count()):
        product = elements.nth(i)
        href = product.locator("a.product-card__link-overlay").get_attribute("href")
        name = product.locator("a.product-card__link-overlay").text_content()
        price = product.locator("div.product-price.lu__styling.is--current-price.css-196r7ux").text_content()
        img = product.locator("img.product-card__hero-image.css-ocqh9").get_attribute("src")
        products.append(
            Sneaker(name, price, href, img, [])
        )
    return products


def nike_search():
    #Start playwright
    with sync_playwright() as p:
        # Launch browser (headless=False means you'll see the browser)
        browser = p.chromium.launch(headless=False)

        # Create a new context (like incognito window)
        context = browser.new_context()

        page = context.new_page()

        page.goto("https://www.nike.com/lu/en/w/new-mens-basketball-shoes-3glsmz3n82yznik1zy7ok")

        page.wait_for_load_state("load")          # Default - page fully loaded

        close_popup(page)

        products = get_urls(page)

        for pr in products:
            page_product = context.new_page()
            page_product.goto(pr.url)
            page_product.wait_for_load_state("load")          # Default - page fully loaded
            close_popup(page_product)
            elements = page_product.locator("label.u-full-width.u-full-height.d-sm-flx.flx-jc-sm-c.flx-ai-sm-c")
            for i in range(elements.count()):
                pr.sizes.append(elements.nth(i).text_content())
            page_product.close()
        # Or use input to keep browser open until you press Enter
        # input("Press Enter to close the browser...")
        for pr in products:
            print(pr)

        browser.close()

if __name__ == "__main__":
    nike_search()