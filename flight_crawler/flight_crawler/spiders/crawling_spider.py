import os
import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http.response import Response
from playwright.async_api import Page
from urllib.parse import urlparse
from scrapy.link import Link
from scrapy import Request
from pathlib import Path


class FlightCrawler(CrawlSpider):
    name = "flight_crawler"
    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "firefox",
        "PLAYWRIGHT_MAX_CONTEXTS": 4,
        "PLAYWRIGHT_MAX_PAGES_PER_CONTEXT": 2,
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "timeout": 20 * 1000,
            "headless": True,
        },
        "DOWNLOAD_HANDLERS": {
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
    }
    allowed_domains = ["flightradar24.com"]
    rules = (Rule(LinkExtractor(), callback="parse"),)
    links = set()

    def start_requests(self):
        """Start requests method.
        We do override this method to use Playwright to load js.

        Yields:
            Request: Request object.
        """
        yield Request(
            url="https://www.flightradar24.com",
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_goto_kwargs": {
                    "wait_until": "networkidle",
                },
            },
            callback=self.parse_home_page,
        )

    async def parse_home_page(self, response: Response):
        """Home page parsing method.
        As the website is dynamic, we need to use Playwright to load js,
        and we also have to click on the hamburger menu to load the navigation.

        Args:
            response (Response): Response object.

        Yields:
            Request: Request object.
        """
        page: Page = response.meta["playwright_page"]
        await page.click("button[id='hamburger-menu-button']")
        aside = await page.query_selector("aside[id='aside-main-menu']")
        nav = await aside.query_selector("nav")
        nav_items = await nav.query_selector_all("div[class='pb-1']")
        for div in nav_items:
            anchor = await div.query_selector("a")
            if await anchor.get_attribute("href") != "#":
                continue

            await div.click()
            sub_links = await div.query_selector_all("a")
            for data_link in sub_links:
                link = await data_link.get_attribute("href")
                if link.startswith("https://www.flightradar24.com/data"):
                    self.links.add(await data_link.get_attribute("href"))

        for link in self.links:
            yield Request(link, callback=self.parse_navigation, meta={"playwright": True})

    async def parse_navigation(self, response: Response):
        """Navigation parsing method.

        Args:
            response (Response): Response object.

        Yields:
            Request: Request object.
        """
        print("we are in parse_navigation, url:", response.url)
        if not response.url.startswith("https://www.flightradar24.com/data"):
            # We are only interested in data.
            # In a real world scenario we would probably want to crawl the whole website.
            # But here to avoid getting blocked we only crawl the data section.
            # In case you want to crawl the whole website, just remove this if statement.
            #
            # middlewares.py is aimed to catch erros regarding anti-bot measures.
            # For now it only catches error and does not do anything with them except logging.
            return

        if response.xpath("//h1[@class='airport-name']"):
            if not os.path.exists("results"):
                os.makedirs("results", exist_ok=True)
            json_data = {
                "url": response.url,
                "data": response.text,
            }
            file_path = Path("results", "data.json")
            with open(file_path, "a") as f:
                f.write(json.dumps(json_data) + "\n")

        links = LinkExtractor(allow_domains="flightradar24.com", unique=True).extract_links(response)
        for link in links:
            parsed_url = urlparse(link.url)
            path = parsed_url.path
            domain = parsed_url.netloc
            if "#" in path:
                path = path.split("#")[0]
            link_to_verify = f"{domain}{path}"
            if link_to_verify not in self.links:
                yield Request(url=link.url, callback=self.parse_navigation, meta={"playwright": True})

        new_links = set()
        link_obj: Link
        for link_obj in links:
            url: str = link_obj.url
            parse_url = urlparse(url)
            path = parse_url.path
            domain = parse_url.netloc
            if "#" in path:
                path = path.split("#")[0]

            link_to_add = f"{domain}{path}"
            new_links.add(link_to_add)

        self.links.update(new_links)
