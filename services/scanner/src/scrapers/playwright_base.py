import os
import re
from typing import Optional
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from src.scrapers.base import BaseScraper
from src.config import Config

class PlaywrightScraper(BaseScraper):
    def __init__(self, debug_dir: Optional[str] = None):
        self.cdp_url = Config.CHROME_CDP_URL
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.debug_dir = debug_dir

    def connect(self):
        """Connects to the remote browser via CDP."""
        if not self.playwright:
            self.playwright = sync_playwright().start()
        
        if not self.browser:
            print(f"Connecting to Chrome at {self.cdp_url}...")
            try:
                self.browser = self.playwright.chromium.connect_over_cdp(self.cdp_url)
                # Use the first context or create one if needed, but usually connect_over_cdp gives us the browser
                # We want to use the existing context if possible to share session
                if self.browser.contexts:
                    self.context = self.browser.contexts[0]
                else:
                    self.context = self.browser.new_context()
                
                self.page = self.context.new_page()
            except Exception as e:
                print(f"Failed to connect to CDP: {e}")
                raise

    def close(self):
        """Closes the connection (but not the browser itself)."""
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def navigate(self, url: str):
        if not self.page:
            self.connect()
        print(f"Navigating to {url}")
        self.page.goto(url)


    def save_page_html(self, name: str, strip_scripts: bool = True):
        if not self.page or not self.debug_dir:
            return
        
        os.makedirs(self.debug_dir, exist_ok=True)
        filepath = os.path.join(self.debug_dir, f"{name}.html")
        try:
            content = self.page.content()
            if strip_scripts:
                content = re.sub(r'<script.*?>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
                # Also remove meta redirects just in case
                content = re.sub(r'<meta httpequiv="refresh".*?>', '', content, flags=re.IGNORECASE)
                
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Saved HTML to {filepath} (scripts stripped: {strip_scripts})")
        except Exception as e:
            print(f"Failed to save HTML: {e}")
