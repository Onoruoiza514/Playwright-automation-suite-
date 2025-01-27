from playwright.async_api import async_playwright
import pandas as pd

async def scrape_company_list():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to the FMCSA page
        await page.goto("https://safer.fmcsa.dot.gov/keywordx.asp?searchstring=%2AAN%2A&SEARCHTYPE=")
        await page.screenshot(path="example.png")
        # Wait for the page to load
        await page.wait_for_selector("tr")

        # Extract data
        rows = await page.query_selector_all("tr")
        data = []

        for row in rows:
            try:
                # Extract company name, location, and href
                company_element = await row.query_selector("th > b > a")
                location_element = await row.query_selector("td > b")

                company_name = await company_element.inner_text() if company_element else "N/A"
                location = await location_element.inner_text() if location_element else "N/A"
                link = await company_element.get_attribute("href") if company_element else "N/A"

                # Add to the data list
                data.append({
                    "Company Name": company_name.strip(),
                    "Location": location.strip(),
                    "Link": f"https://safer.fmcsa.dot.gov/{link.strip()}" if link != "N/A" else "N/A"
                })
            except Exception as e:
                print(f"Error processing row: {e}")

        # Save to CSV
        df = pd.DataFrame(data)
        df.to_csv("company_data.csv", index=False)

        await browser.close()
        print("Scraping complete. Data saved to 'company_data.csv'.")

# Run the script
import asyncio
await scrape_company_list()
