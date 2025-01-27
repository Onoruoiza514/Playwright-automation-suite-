import asyncio
import csv
from playwright.async_api import async_playwright

async def scrape_company_data(input_csv, output_csv):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # List to store scraped data
        scraped_data = []

        # Read URLs from the input CSV file
        urls = read_urls_from_csv(input_csv) #We would create a helper function that would go onto our earlier scraped file and

        # Iterate through each URL
        for index, url in enumerate(urls, start=1):
            try:
                # Visit the URL
                await page.goto(url, timeout=30000)
                await page.screenshot(path="Test_photo.png")
                print("Navigated to the page..........")

                # Check if the page contains the expected table
                table_exists = page.locator('table[border="1" width="70%" bordercolor="SILVER" cellspacing="0" cellpadding="4" summary="For formatting purpose"]')
                if not table_exists:
                    print(f"Link number {index} is not available.")
                    scraped_data.append({
                        "Entity Type": "N/A",
                        "USDOT Status": "N/A",
                        "USDOT Number":"N/A",
                        "MCS-150 Mileage Year":"N/A",
                        "MCS-150 Form Date":"N/A",
                        "Legal Name":"N/A",
                        "DBA Name":"N/A",
                        "Physical Address":"N/A",
                        "Phone":"N/A",
                        "Mailing Address":"N/A",
                        "URL":url,
                        "Error": f"Link Number {index} not available......."
                    })
                    continue

                # Scrape data from the table
                data = {
                    "Entity Type": await extract_text(page, "th:has-text('Entity Type:') + td"),
                    "USDOT Status": await extract_text(page, "th:has-text('USDOT Status:') + td"),
                    "USDOT Number": await extract_text(page, "th:has-text('USDOT Number:') + td"),
                    "MCS-150 Mileage Year": await extract_text(page, "th:has-text('MCS-150 Mileage (Year):') + td"),
                    "MCS-150 Form Date": await extract_text(page, "th:has-text('MCS-150 Form Date:') + td"),
                    "Legal Name": await extract_text(page, "th:has-text('Legal Name:') + td"),
                    "DBA Name": await extract_text(page, "th:has-text('DBA Name:') + td"),
                    "Physical Address": await extract_text(page, "th:has-text('Physical Address:') + td"),
                    "Phone": await extract_text(page, "th:has-text('Phone:') + td"),
                    "Mailing Address": await extract_text(page, "th:has-text('Mailing Address:') + td"),
                    "URL": url,
                    "Error": "N/A"
                }

                scraped_data.append(data)

            except Exception as e:
                print(f"Error scraping link number {index}: {e}")
                scraped_data.append({
                    "Entity Type": "N/A",
                    "USDOT Status":"N/A",
                    "USDOT Number": "N/A",
                    "MCS-150 Mileage Year": "N/A",
                    "MCS-150 Form Date": "N/A",
                    "Legal Name":"N/A",
                    "DBA Name" : "N/A",
                    "Physical Address": "N/A",
                    "Phone" : "N/A",
                    "Mailing Address": "N/A",
                    "URL": url,
                    "Error": f"Error scraping link number {index}: {e}"
                })

        # Save data to the output CSV file
        save_to_csv(scraped_data, output_csv) #We would also create am additional functions to sace our scraped datas

        await browser.close()

def read_urls_from_csv(filename):
    """Read URLs from a CSV file."""
    urls = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            urls.append(row['Link'])
            #Print we got the links successfully
    return urls

def save_to_csv(data, filename):
    """Save data to a CSV file."""
    fieldnames = ["Entity Type","USDOT Number","USDOT Status","MCS-150 Mileage Year","MCS-150 Form Date","Legal Name","DBA Name","Physical Address","Phone","Mailing Address","URL","Error"]

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

async def extract_text(page, selector):
    """Extract text from a selector."""
    element = await page.query_selector(selector)
    return await element.inner_text() if element else "N/A"

# Example usage
input_csv = "company_data.csv"  # CSV file containing the URLs inq a column named 'URL'
output_csv = "scraped_data.csv"

# Run the scraper
await scrape_company_data(input_csv, output_csv)
