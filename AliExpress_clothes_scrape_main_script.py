import asyncio
import csv
from playwright.async_api import async_playwright

async def scrape_AliExpress():
    start_url = "https://www.aliexpress.com/category/100003109/women-clothing.html"

    async with async_playwright() as p:
        # Launch browser with timeout settings
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Set default timeout to 3 minutes
        page.set_default_timeout(180000)

        await page.goto(start_url)
        print("Navigated to AliExpress clothing store successfully")

        # Open CSV file for writing
        with open("scraped_ali_express_clothes_women_products.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["id", "title", "price", "original_price", "sold", "store_name", "store_link", "product_link"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            product_id = 1

            async def scroll_to_load_more(page, selector):
                previous_count = 0
                while True:
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await asyncio.sleep(3)  # Wait for new content
                    current_count = await page.locator(selector).count()
                    if current_count == previous_count:
                        break
                    previous_count = current_count

            selectors = {
                "title": "h3[class=\"multi--titleText--nXeOvyr\"]",
                "price": 'div[class="multi--price-sale--U-S0jtj"]',
                "original_price": 'span[style="text-decoration: line-through; color: rgb(153, 153, 153);"]',
                "sold": 'span[class="multi--trade--Ktbl2jB"]',
                "store": 'span[class="cards--store--3GyJcot"] a',
                "product_link": 'a[class*="cards--storeLink--"]',
                "next_button": 'span[class="comet-icon comet-icon-arrowleftrtl32 "]'
            }

            while True:
                await scroll_to_load_more(page, selectors["title"])
                print("Finished scrolling on the current page")

                await page.wait_for_selector(selectors["title"], timeout=180000)

                product_titles = page.locator(selectors["title"])
                product_prices = page.locator(selectors["price"])
                product_original_prices = page.locator(selectors["original_price"])
                product_sold = page.locator(selectors["sold"])
                product_stores = page.locator(selectors["store"])
                product_links = page.locator(selectors["product_link"])

                product_count = await product_titles.count()
                for i in range(product_count):
                    try:
                        title = await product_titles.nth(i).inner_text()
                        price = await product_prices.nth(i).inner_text() if await product_prices.count() > i else "N/A"
                        original_price = await product_original_prices.nth(i).inner_text() if await product_original_prices.count() > i else "N/A"
                        sold = await product_sold.nth(i).inner_text() if await product_sold.count() > i else "N/A"
                        store_name = await product_stores.nth(i).inner_text() if await product_stores.count() > i else "N/A"
                        store_link = await product_stores.nth(i).get_attribute('href') if await product_stores.count() > i else "N/A"
                        product_link = await product_links.nth(i).get_attribute('href') if await product_links.count() > i else "N/A"

                        writer.writerow({
                            "id": product_id,
                            "title": title,
                            "price": price,
                            "original_price": original_price,
                            "sold": sold,
                            "store_name": store_name,
                            "store_link": store_link,
                            "product_link": product_link
                        })
                        print(f"Scraped product {product_id}: {title}")
                        product_id += 1
                    except Exception as e:
                        print(f"Error extracting details for product {product_id}: {e}")

                next_button = page.locator(selectors["next_button"])
                if await next_button.is_visible() and next_button.is_enabled():
                    print("Navigating to the next page...")
                    await next_button.first.click()
                    await asyncio.sleep(5)
                else:
                    print("No more pages to scrape")
                    break

        await browser.close()
        print(f"Scraping completed. Data saved to 'scraped_ali_express_clothes_women_products.csv'")

await scrape_AliExpress()
      
