import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DjursboSpider(scrapy.Spider):
    name = 'djursbo_spider'
    start_urls = ['https://djursbo.dk/selskabs-og-afdelingshjemmesider/djursbo/afdelinger/tendrupvej-ballesvej/?StepBack=true']

    def parse(self, response):
        # Используем Selenium для получения полного HTML-кода страницы, включая динамический контент
        driver = webdriver.Chrome()  # Убедитесь, что у вас установлен драйвер Chrome и указан путь к нему
        driver.get(response.url)

        # Добавляем явное ожидание для элементов
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.section__title')))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.section__price')))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.section__description')))

        # Получаем полный HTML-код после загрузки всех элементов
        full_html = driver.page_source
        driver.quit()

        # Теперь парсим полученный полный HTML-код с помощью Scrapy
        response = scrapy.http.HtmlResponse(url=response.url, body=full_html, encoding='utf-8')

        # Извлекаем текст заголовка с помощью XPath-селектора
        title = response.xpath('//h1[@class="section__title"]/text()').get()
        # Извлекаем цену за жилье с помощью XPath-селектора
        price = response.xpath('//span[@class="section__price"]/text()').get()
        # Извлекаем описание с помощью XPath-селектора
        description = response.xpath('//div[@class="section__description"]/text()').get()

        # Выводим полученные данные в терминал
        print("Заголовок:", title)
        print("Цена:", price)
        print("Описание:", description)

# Создаем объект CrawlerProcess
process = CrawlerProcess()

# Добавляем паука в процесс
process.crawl(DjursboSpider)

# Запускаем процесс (блокирующий вызов, паук будет выполняться)
process.start()
