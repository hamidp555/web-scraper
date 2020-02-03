
from importlib import import_module
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumDownloaderMiddleware(object):

    def __init__(self, crawler):
        driver_name = crawler.settings.get('SELENIUM_DRIVER_NAME')
        driver_executable_path = crawler.settings.get(
            'SELENIUM_DRIVER_EXECUTABLE_PATH')
        browser_executable_path = crawler.settings.get(
            'SELENIUM_BROWSER_EXECUTABLE_PATH')
        driver_arguments = crawler.settings.get('SELENIUM_DRIVER_ARGUMENTS')

        if not driver_name or not driver_executable_path:
            raise NotConfigured(
                'SELENIUM_DRIVER_NAME and SELENIUM_DRIVER_EXECUTABLE_PATH must be set'
            )

        webdriver_base_path = f'selenium.webdriver.{driver_name}'

        driver_clazz_module = import_module(f'{webdriver_base_path}.webdriver')
        driver_clazz = getattr(driver_clazz_module, 'WebDriver')

        driver_options_module = import_module(f'{webdriver_base_path}.options')
        driver_options_clazz = getattr(driver_options_module, 'Options')
        driver_options = driver_options_clazz()

        if browser_executable_path:
            driver_options.binary_location = browser_executable_path

        for argument in driver_arguments:
            driver_options.add_argument(argument)

        driver_kwargs = {
            'executable_path': driver_executable_path,
            f'{driver_name}_options': driver_options
        }

        self.driver = driver_clazz(**driver_kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        webdriver_settings = request.meta.get('webdriver_settings', None)
        if not webdriver_settings:
            spider.logger.debug(
                'will not use selenium webdriver passing it to another downloader')
            return None

        # get webdriver settings
        wait_time = webdriver_settings.get('wait_time', None)
        wait_until = webdriver_settings.get('wait_until', None)
        cookies = webdriver_settings.get('cookies', None)
        screenshot = webdriver_settings.get('screenshot', None)
        script = webdriver_settings.get('script', None)

        self.driver.get(request.url)

        if wait_until and wait_time:
            spider.logger.debug(
                'waiting for {} seconds for expected condition'.format(wait_time))
            WebDriverWait(self.driver, wait_time).until(wait_until)

            if(isinstance(wait_until, EC.frame_to_be_available_and_switch_to_it)):
                iframe_body = str.encode(self.driver.page_source)
                request.meta.update(iframe_body=iframe_body)
                self.driver.switch_to_default_content()

        if cookies:
            for cookie_name, cookie_value in cookies.items():
                self.driver.add_cookie(
                    {
                        'name': cookie_name,
                        'value': cookie_value
                    }
                )

        if screenshot:
            spider.logger.debug('taking screen a shot')
            request.meta['screenshot'] = self.driver.get_screenshot_as_png()

        if hasattr(request, 'script'):
            spider.logger.debug('executing a script')
            self.driver.execute_script(script)

        body = str.encode(self.driver.page_source)
        spider.logger.debug('recieved page source from webderiver')

        # Expose the driver via the "meta" attribute
        request.meta.update(webdriver=self.driver)
        spider.logger.debug('added webdervier to request meta')

        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_closed(self, spider):
        spider.logger.info('Spider closed (selenium): %s' % spider.name)
        self.driver.quit()

    def spider_opened(self, spider):
        spider.logger.info('Spider opened (selenium): %s' % spider.name)
