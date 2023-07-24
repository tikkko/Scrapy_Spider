import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DjursboSpider(scrapy.Spider):
    name = 'djursbo_spider'
    start_urls = [
        'https://djursbo.dk/selskabs-og-afdelingshjemmesider/djursbo/afdelinger/tendrupvej-ballesvej/?StepBack=true']

    def parse(self, response):
        driver = webdriver.Chrome()
        driver.get(response.url)

        # Adding explicit waits for elements
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.section__title')))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.section__price')))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.section__description')))

        # Fetching the full HTML code after all elements are loaded
        full_html = driver.page_source
        driver.quit()

        # Now parsing the received full HTML code using Scrapy
        response = scrapy.http.HtmlResponse(url=response.url, body=full_html, encoding='utf-8')

        # Extracting the title text, property price, and description using XPath selectors
        title = response.xpath('//h1[@class="section__title"]/text()').get()
        price = response.xpath('//span[@class="section__price"]/text()').get()
        description = response.xpath('//div[@class="section__description"]/text()').get()

        print("Title:", title)
        print("Price:", price)
        print("Description:", description)


process = CrawlerProcess()

process.crawl(DjursboSpider)

process.start()
