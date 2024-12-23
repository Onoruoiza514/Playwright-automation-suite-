

import asyncio
from playwright.async_api import async_playwright
from google.colab import files

class BrowserManager:
    def __init__(self):
        self.browser = None
        self.page = None
        self.pages = []



    async def start_browser(self):
        """this method is to launch the browser"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        print("Browser launched successfully!")


    async def close_browser(self):
        """this method closes the browser"""
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.page = None
            self.pages = []
            print("Browser closed successfully!")
        else:
            print("Browser not closed yet!")


    async def get_page(self):
        """this method returns the page"""
        return self.page


    async def get_browser(self):
        """this method returns the browser!"""
        return self.browser


    async def navigate_to_page(self, url: str = None):
        """Navigation to a specific oage with a known url"""
        await self.page.goto(url)
        #Lets take a screenshot of the damn page as evidence,haha😂
        shot_path = f"Evidnece_{url.replace('https://', '').replace('/', '_').replace('.', '_')}.webp"
        await self.page.screenshot(path=shot_path)
        files.download(shot_path)
        print(f"Navigated to the page {url} successfully and saved a copy as evidence or proof of visitation!")


    async def manage_tabs(self, url):
        """Open a new tab and navigate to a url"""
        #self.browser = await playwright.chromium.lauch(headless= False)
        if not self.browser:
            print("Browser is not initialised")
            return
        print("Opening a new tab....")
        if url is None:
            raise ValueError("URL required to open a new tab!")
        self.new_page = await self.browser.new_page()
        await self.new_page.goto(url)
        print(f"Navigated to a new tab for {url} successfully!")
        # Take a screenshot of the new tab
        screenshot_path = f"screenshot_{url.replace('https://', '').replace('/', '_').replace('.', '_')}.png"
        await self.new_page.screenshot(path=screenshot_path)
        files.download(screenshot_path)
        print(f"Screenshot of the new tab saved as {screenshot_path}")


    async def screenshot_page(self):
        """Take s screenshot of the current page"""
        #path = "screenshot.png"
        await self.page.screenshot(path= "screenshot.jpg")
        evidence = files.download("screenshot.jpg")
        if evidence == True:
            print("Screenshot taken successfully!")
        else:
            print("Visited but not downloaded!")


    async def emulate_device(self, device_name):
        """Simulate a specific device"""
        from playwright.async_api import devices
        device = devices[device_name]
        context = await self.browser.new_context(**device)
        self.page = await context.new_page()
        print(f"Emulated device {device_name} successfully!")

