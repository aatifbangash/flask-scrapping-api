from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from api.networks.RootClass import Root
import time
# from pprint import pprint


class Awin(Root):

    networkInfo = None
    browser = None
    mapStatus = {
        'pending': 1,
        'rejected': 2,
        'approved': 3
    }

    def __init__(self, networkInfo):
        super().__init__()
        self.networkInfo = networkInfo

    def scrapTransactions(self):
        # raise Exception(self.networkInfo)
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
        driver.get(self.networkInfo['loginlink'])

        # check privacy and cookie checkboxes
        driver.find_element_by_id('privacyCheckbox').click()
        driver.find_element_by_id('cookieCheckbox').click()
        driver.find_element_by_id('euContinueButton').click()

        # refresh page after checking privacy and cookie
        driver.refresh()

        # type username and passwork to login to dashboard
        driver.find_element_by_id('UserEmail').send_keys(
            self.networkInfo['username'])

        driver.find_element_by_id('UserPassword').send_keys(
            self.networkInfo['password'])

        driver.find_element_by_id('loginButton').click()

        # wait for the dashboard dom to load after login
        time.sleep(2)

        driver.find_element_by_xpath(
            '//*[@id="sidebar"]/div/nav/div[3]/a').click()  # hit report menu

        time.sleep(1)  # wait for transactions menu to load

        driver.find_element_by_xpath(
            '//*[@id="sidebar"]/div/nav/div[3]/ul/li[2]/a').click()  # hit transactions menu

        transactionsList = []
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.ui-jqgrid-view table tr')))  # wait for html table to load

        time.sleep(1)
        transactionsTable = driver.find_elements_by_css_selector(
            '.ui-jqgrid-view table tr')

        for (idx, tr) in enumerate(transactionsTable):
            transactionObject = {}
            if(idx == 0):  # skip the table header row
                continue

            click_date = tr.find_elements_by_css_selector('td')[0].text
            if click_date:
                transactionObject[self.csvHeader[4]] = click_date
                transactionObject[self.csvHeader[3]] = click_date  # cwhen
                transactionObject[self.csvHeader[10]] = click_date  # orderDate

            details = tr.find_elements_by_css_selector('td')[1].text
            if details:
                transactionObject[self.csvHeader[1]] = details

            status = tr.find_elements_by_css_selector('td')[2].text
            if status:
                transactionObject[self.csvHeader[7]] = self.mapStatus[status]

            commission = tr.find_elements_by_css_selector('td')[3].text
            if commission:
                transactionObject[self.csvHeader[2]
                                  ] = self.formatPrice(commission)
                transactionObject[self.csvHeader[11]] = self.formatPrice(
                    commission)  # ordValue

            reference_id = tr.find_elements_by_css_selector('td')[4].text
            if reference_id:
                transactionObject[self.csvHeader[5]] = reference_id

            clickref = tr.find_elements_by_css_selector('td')[5].text
            if clickref:
                transactionObject[self.csvHeader[0]] = clickref
                transactionObject[self.csvHeader[9]] = clickref + \
                    self.networkInfo['culture']  # clickRefHash

            if(len(transactionObject) > 0):
                # [6]networkClass
                transactionObject[self.csvHeader[6]] = ''

                # [8]networkClass
                transactionObject[self.csvHeader[8]] = __name__

                # [12] dateCreated
                transactionObject[self.csvHeader[12]
                                  ] = time.strftime('%Y-%m-%d %H:%M:%S')

                transactionsList.append(transactionObject)

        driver.quit()
        return transactionsList

