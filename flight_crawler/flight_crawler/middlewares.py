# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.exceptions import CloseSpider
from time import sleep


class FlightCrawlerSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.

        # Here we can check if the response is valid or not
        # and return a new request if we want to retry
        # valid conditions are:
        # - if no captcha or other anti-bot mechanism (like cloudflare)
        # -> recaptcha-token or hcaptcha present in the html
        # - if no "you are blocked" message or anything similar
        # -> "you are blocked" "ip blocked" present in the html
        blocked_messages = [
            "you are blocked",
            "ip blocked",
            "access denied",
            "access from your network has been temporarily restricted",
            "access to this page has been denied",
        ]
        if any(message in response.text.lower() for message in blocked_messages):
            # We are blocked, we should abort the request
            raise CloseSpider("Blocked by anti-bot mechanism")

        if response.xpath("//div[@class='g-recaptcha']"):
            # We are blocked by a captcha, we should abort the request
            raise CloseSpider("Blocked by captcha")

        if "dn-cgi/challenge-platform" in response.headers.get("Location", b""):
            # We are blocked by cloudflare, we should abort the request and terminate the process
            raise CloseSpider("Blocked by cloudflare")

        if response.status == 429:
            # We are blocked by cloudflare, we should try again later (headers["Retry-After"])
            sleep(int(response.headers["Retry-After"]))

        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class FlightCrawlerDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
