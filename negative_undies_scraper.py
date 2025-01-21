import asyncio
from playwright.async_api import async_playwright
import pandas as pd

async def scrape_negative_underwear():
    # List to store scraped data
    scraped_data = []

    # Start Playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Change to False for debugging
        page = await browser.new_page()
        

        # Base URL
        base_url = "https://negativeunderwear.com/collections/womens-bras?page=2"
        current_page = 1

        while True:
            print(f"Scraping page {current_page}...")
            await page.goto(base_url)
            await page.wait_for_timeout(2000)  # Wait for content to load
            await page.screenshot(path="nonsense.png")
            # Select all product containers
            products = await page.query_selector_all('div[data-page="2"]')

            if not products:  # Break if no products are found
                print("No more products found. Exiting.")
                break

            for product in products:
                name = await product.query_selector('span[class="grid-product__title"]')
                price = await product.query_selector('span[class="grid-product__price"]')
                link = await product.query_selector('a')
                image = await product.query_selector('img[class="grid-product__image"]')
                color = await product.query_selector('div[class="products-in-family"]')
                scraped_data.append({
                    "name": (await name.inner_text()).strip() if name else None,
                    "price": (await price.inner_text()).strip() if price else None,
                    "link": await link.get_attribute('href') if link else None,
                    "image": await image.get_attribute('src') if image else None,
                    "Available colors": (await color.inner_text()).strip() if color else None
                })

            # Check if there's a next page
            next_page = await page.query_selector('a[class="pagination__next"]')
            if next_page:
                current_page += 1
            else:
                break

        # Close browser
        await browser.close()

    # Save data to CSV
    df = pd.DataFrame(scraped_data)
    df.to_csv("products.csv", index=False)
    print("Scraping complete. Data saved to products.csv")

    # Run the async function
await scrape_negative_underwear()

