from selenium import webdriver
from api.networks.RootClass import Root


class Test(Root):

    networkInfo = None
    browser = None

    def __init__(self, networkInfo):
        super().__init__()
        self.networkInfo = networkInfo

    def scrap(self):

        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--ignore-certificate-errors')
        chromeOptions.add_argument('--incognito')

        chromeOptions.add_argument('--headless')

        if(self.env != 'dev'):  # run on production only
            chromeOptions.add_argument('--headless')
            chromeOptions.add_argument('--no-sandbox')
            chromeOptions.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(
            executable_path=self.ROOT_DIR + '/chromedriver', options=chromeOptions)

        driver.set_page_load_timeout(30)
        driver.get('https://onlineustaad.com/blog/')
        articles = driver.find_elements_by_css_selector('.content-inner')
        resultArr = []
        for article in articles:
            obj = {}
            obj['title'] = article.find_elements_by_css_selector(
                '.entry-content .entry-header')[0].text
            obj['src'] = article.find_elements_by_css_selector(
                'img')[0].get_attribute('data-lazy-src')
            obj['link'] = article.find_elements_by_css_selector(
                'a.post-image')[0].get_attribute('href')
            obj['desc'] = article.find_elements_by_css_selector(
                '.entry-content .entry-summary p')[0].text

            resultArr.append(obj)

        driver.quit()
        return resultArr
