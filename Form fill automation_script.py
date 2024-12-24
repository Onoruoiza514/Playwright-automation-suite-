#We install dependencies
!pip install playwright
from playwright.async_api import async_playwright
import asyncio
# Install Playwright
#!pip install playwright

# Install the required browsers
!python3 -m playwright install




#Them the main script 
async def fill_form(page, label, value):
    """Fills a form field based on its label."""
    field = page.get_by_label(label)
    await field.fill(value)


#Amother function
async def implement():
    """Implements the form filling process"""
    url = "https://docs.google.com/forms/d/e/1FAIpQLScV0DvomCjJGqGo6bJvAlcJiYp5GYFxjLojszsszUmxdkTmew/viewform?usp=dialog"

    async with async_playwright() as p:  # Properly use async context management
        browser = await p.chromium.launch(headless=True, slow_mo=200)
        page = await browser.new_page() # Properly use async context management
        # Navigate to the form page
        await page.goto(url)


        # Fill the form fields
        await fill_form(page, "FirstName", "Abdulfaatihi")
        await fill_form(page, "LastName", "Onoruoiza")
        await fill_form(page, "PhoneNumber", "08077235670")
        await fill_form(page, "Email", "abdulonoruoiza410@gmail.com")
        await fill_form(page, "HomeAddress", "House number 66B, Zone 9, Lugbe, Airport Road, Abuja")
        await fill_form(page, "FeedbackMessage", "Blah blah blah blah")

        # Submit the form
        submit_button = page.get_by_role("button", name="submit")
        await submit_button.click()
        print(f"Form to {url} submitted successfull!")

        await browser.close()
        await page.close()
        print("Everything done and closed men")

if __name__ == "__main__":
    await implement()
