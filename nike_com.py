from playwright.sync_api import sync_playwright
from Sneaker import Sneaker
from WriterCSV import WriterCSV


def close_popup(page):
    btn = page.get_by_label("Close pop-up")
    if btn.count() > 0:
        btn.click()


def get_info_products(page):
    products = []
    elements = page.locator("figure")
    print(elements.count())
    for i in range(elements.count()):
        product = elements.nth(i)
        href = product.locator("a.product-card__link-overlay").get_attribute("href")
        name = product.locator("a.product-card__link-overlay").text_content()
        price = product.locator("div.product-price").first.text_content().replace(',','.')
        img = product.locator("img.product-card__hero-image").get_attribute("src")
        products.append(
            Sneaker(name, price, href, img, None, [])
        )
    return products

def scroll_to_load_all(page, max_scrolls=50, wait_time=1000):
    """Scroll down until page height doesn't change"""
    previous_height = 0
    scroll_position = 0

    for i in range(max_scrolls):
        # Get current height
        current_height = page.evaluate("document.body.scrollHeight")

        print(f"Scroll {i+1}: Height = {current_height}px")

        # If height hasn't changed, we're done
        if current_height == previous_height and i > 0:
            print(f"Height stable at {current_height}px. Stopping.")
            break

        for i in range(50):
            scroll_position += 200
            page.evaluate(f"window.scrollTo(0, {scroll_position})")
            page.wait_for_timeout(wait_time)

        previous_height = current_height

    print(f"Final height: {page.evaluate('document.body.scrollHeight')}px")


def nike_search():
    #Start playwright
    with sync_playwright() as p:
        # Launch browser (headless=False means you'll see the browser)
        browser = p.chromium.launch(headless=False)

        # Create a new context (like incognito window)
        context = browser.new_context()
        page = context.new_page()

        # page.goto("https://www.nike.com/lu/en/w/new-mens-basketball-shoes-3glsmz3n82yznik1zy7ok")
        # page.goto("https://www.nike.com/lu/en/w/mens-shoes-nik1zy7ok")
        page.goto("https://www.nike.com/lu/en/w/mens-road-running-shoes-3qxw3znik1zy7ok")

        page.wait_for_load_state("load")          # Default - page fully loaded
        close_popup(page)

        scroll_to_load_all(page, 50, 300)
        # get all products from page
        products = get_info_products(page)

        writercsv = WriterCSV("nike_shoes.csv")
        writercsv.open()

        counter = 1
        n = len(products)
        try:
            for sneaker in products:
                print(f"{counter} of {n}")
                page_product = context.new_page()
                page_product.goto(sneaker.url)
                page_product.wait_for_load_state("load")          # Default - page fully loaded
                close_popup(page_product)
                elements = page_product.query_selector_all('[data-testid="pdp-grid-selector-item"]')
                for element in elements:
                    # Get the text from the label inside
                    label = element.query_selector('label')
                    if label:
                        size_text = label.inner_text()
                        sneaker.sizes.append(size_text)
                desc = page_product.locator("h2#pdp_product_subtitle").text_content()
                col = page_product.locator('[data-testid="product-description-color-description"]').text_content()
                sneaker.description = desc
                sneaker.color = col
                writercsv.write_sneaker(sneaker)
                page_product.close()
                counter += 1
        except Exception as e:
            print(e)
        finally:
            # Always close the file
            writercsv.close()

        # Or use input to keep browser open until you press Enter
        # input("Press Enter to close the browser...")
        # for pr in products:
        #     print(pr)

        browser.close()
        return products


if __name__ == "__main__":
    nike_search()