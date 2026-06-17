from playwright.sync_api import sync_playwright
from Sneaker import Sneaker
import csv


def close_popup(page):
    btn = page.get_by_label("Close pop-up")
    if btn.count() > 0:
        btn.click()


def get_info_product(page):
    products = []
    elements = page.locator("figure")
    print(elements.count())
    for i in range(elements.count()):
        product = elements.nth(i)
        href = product.locator("a.product-card__link-overlay").get_attribute("href")
        name = product.locator("a.product-card__link-overlay").text_content()
        price = product.locator("div.product-price").text_content().replace(',','.')
        img = product.locator("img.product-card__hero-image").get_attribute("src")
        products.append(
            Sneaker(name, price, href, img, None, [])
        )
    return products


def write_to_csv(writer, product):
    writer.writerow(product.__dict__)


def nike_search():
    #Start playwright
    with sync_playwright() as p:
        # Launch browser (headless=False means you'll see the browser)
        browser = p.chromium.launch(headless=False)

        # Create a new context (like incognito window)
        context = browser.new_context()
        page = context.new_page()

        # page.goto("https://www.nike.com/lu/en/w/new-mens-basketball-shoes-3glsmz3n82yznik1zy7ok")
        page.goto("https://www.nike.com/lu/en/w/mens-shoes-nik1zy7ok")

        page.wait_for_load_state("load")          # Default - page fully loaded

        close_popup(page)

        products = get_info_product(page)

        csvfile = open("nike_shoes.csv", 'w', newline='', encoding='utf-8')
        fieldnames = [
            "name"
            , "price"
            , "url"
            , "image"
            , "description"
            , "color"
            , "sizes"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        counter = 1
        n = len(products)
        try:
            for pr in products:
                print(f"{counter} of {n}")
                page_product = context.new_page()
                page_product.goto(pr.url)
                page_product.wait_for_load_state("load")          # Default - page fully loaded
                close_popup(page_product)
                elements = page_product.query_selector_all('[data-testid="pdp-grid-selector-item"]')
                for element in elements:
                # Get the text from the label inside
                    label = element.query_selector('label')
                    if label:
                        size_text = label.inner_text()
                        pr.sizes.append(size_text)
                desc = page_product.locator("h2#pdp_product_subtitle").text_content()
                col = page_product.locator('[data-testid="product-description-color-description"]').text_content()
                pr.description = desc
                pr.color = col
                write_to_csv(writer, pr)
                page_product.close()
                counter += 1
        except Exception as e:
            print(e)
        finally:
            # Always close the file
            if csvfile and not csvfile.closed:
                csvfile.close()
                print("File closed successfully")

        # Or use input to keep browser open until you press Enter
        # input("Press Enter to close the browser...")
        # for pr in products:
        #     print(pr)

        browser.close()
        return products


if __name__ == "__main__":
    nike_search()