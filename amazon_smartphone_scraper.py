async def login_amazon_account():
    with open("cooks.json", 'r') as file:
        cookies_data = json.load(file)

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)
        context =  await browser.new_context()
        await context.add_cookies(cookies_data)
        page = await context.new_page()
        await page.goto("https://www.amazon.com")
        print("Navigated to amazon successfully, Now locating the sign up botton")
        await page.screenshot(path= "nice_one.png")
        print("Screenshoted the bastard")
        print("Clicked the sign up botton successfully,Tryimg you fill in the email")

        search_box= page.locator('input[id="twotabsearchtextbox"]')
        await search_box.fill("smartphones")
        search_bar = page.locator('input[id="nav-search-submit-button"]')
        await search_bar.click()

        await page.wait_for_selector('h2[class="a-size-medium-plus a-spacing-none a-color-base a-text-bold"]')
        print("Search results and varieties of smartphones with yheir specifications Consoled brother")
        await page.screenshot(path="results.png")

        with open("amazon_smartphones.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Product Name", "Price", "Rating", "Number of Reviews","Amount of products sold out", "Product Link", "Actual listed price"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            while True:

                #Locate product elements
                products = page.locator('div[class="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"]')
                product_count = await products.count()
                for i in range(product_count):
                    try:
                        #Extract products details
                        name = await products.nth(i).locator('h2[class="a-size-medium a-spacing-none a-color-base a-text-normal"]').inner_text() if await products.nth(i).locator('h2[class="a-size-medium a-spacing-none a-color-base a-text-normal"]').count() > 0 else "N/A"
                        price = await products.nth(i).locator('span[class="a-price-whole"]').inner_text() if await products.nth(i).locator('span[class="a-price-whole"]').count() > 0 else "N/A"
                        reviews = await products.nth(i).locator('span[class="a-size-small puis-normal-weight-text s-underline-text"]').inner_text() if await products.nth(i).locator('span[class="a-size-small puis-normal-weight-text s-underline-text"]').count() > 0 else "N/A"
                        rating = await products.nth(i).locator('span[class="a-icon-alt"]').inner_text() if await products.nth(i).locator('span[class="a-icon-alt"]').count() > 0 else "N/A"
                        link = await products.nth(i).locator('a[class="a-link-normal s-line-clamp-2 s-link-style a-text-normal"]').get_attribute("href") if await products.nth(i).locator('a[class="a-link-normal s-line-clamp-2 s-link-style a-text-normal"]').count() > 0 else "N/A"
                        sold = await products.nth(i).locator('div[class="a-row a-size-base"]').inner_text() if await products.nth(i).locator('div[class="a-row a-size-base"]').count() > 0 else "N/A"
                        list_price = await products.nth(i).locator('span[class="a-price a-text-price"] span[class="a-offscreen"]').inner_text() if await products.nth(i).locator('span[class="a-price a-text-price"] span[class="a-offscreen"]').count() > 0 else "N/A"

                        writer.writerow({
                            "Product Name": name,
                            "Price": price,
                            "Rating": rating,
                            "Number of Reviews": reviews,
                            "Amount of products sold out": sold,
                            "Product Link": f"https://www.amazon.com{link}" if link != "N/A" else "N/A", #this wounf render a complete clickable link
                            "Actual listed price": list_price
                                    })
                    except Exception as e:
                        print(f"Error scraping product {i+1}: {e}")

                # Check for "Next" button within a present pave
                next_button = page.locator('a[class="s-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator"]')
                if await next_button.is_visible():
                    print("Navigating to the next page...")
                    await next_button.click()
                    await asyncio.sleep(5)  # Wait for the next page to load for about 5secs
                else:
                    print("No more pages to scrape")
                    break

        # Close the browser
        await browser.close()
        print("Scraping completed. Data saved to 'amazon_smartphones.csv'")



if __name__ == "__main__":
    await login_amazon_account()

