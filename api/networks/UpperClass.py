from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from api.networks.RootClass import Root
import time
from datetime import datetime
import os
# from pprint import pprint


class Upper(Root):

    networkInfo = None
    browser = None
    mapStatus = {
        'Open': 1,
        'R': 2,
        'D': 2,
        'Confirmed': 3
    }

    def __init__(self, networkInfo):
        super().__init__()
        self.networkInfo = networkInfo

    def scrapTransactions(self):
        # raise Exception(self.networkInfo)
        # return [{'test': 'testing'}]
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

        # open login form
        driver.implicitly_wait(5)
        driver.find_element_by_id('inputPubEmail').send_keys(
            'affiliate-de@orangebuddies.com')
        driver.find_element_by_id(
            'inputPubPassword').send_keys('demedia2019!')
        driver.find_element_by_css_selector(
            '.btn.btn-lg.btn-primary.btn-block').click()

        # # basic navigation
        driver.implicitly_wait(5)
        driver.find_element_by_id('navigation_item_statistic').click()
        driver.find_element_by_xpath(
            '//*[@id="bs-example-navbar-collapse-1"]/ul/li[3]/ul/li[9]/a').click()

        # fetch transactions
        driver.implicitly_wait(5)
        transactionsTable = driver.find_elements_by_css_selector(
            '#datacontent tr')
        transactionsList = []
        for (idx, transaction) in enumerate(transactionsTable):
            transactionObject = {}
            details = transaction.find_elements_by_tag_name('td')[3].text
            if details:
                transactionObject[self.csvHeader[1]] = details

            clickref = transaction.find_elements_by_tag_name(
                'td')[4].find_elements_by_css_selector('span')
            if(len(clickref) > 0):
                clickref = clickref[0].text
                transactionObject[self.csvHeader[0]] = clickref
                transactionObject[self.csvHeader[9]] = clickref + \
                    self.networkInfo['culture']  # clickRefHash

            commission = transaction.find_elements_by_tag_name('td')[6].text
            if commission:
                transactionObject[self.csvHeader[2]
                                  ] = self.formatPrice(commission, '??')

            transactionObject[self.csvHeader[11]] = 0

            click_date = transaction.find_elements_by_tag_name(
                'td')[1].find_elements_by_tag_name('div')
            if len(click_date) > 0:
                # datetime.strptime(click_date,'%d/%m/%Y, %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                dt = click_date[0].text.strip()
                formatedDate = datetime.strptime(dt, '%d.%m.%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                transactionObject[self.csvHeader[4]] = formatedDate
                transactionObject[self.csvHeader[3]
                                  ] = formatedDate  # cwhen
                transactionObject[self.csvHeader[10]
                                  ] = formatedDate  # orddate

            status = transaction.find_elements_by_tag_name('td')[5].text
            if status:
                transactionObject[self.csvHeader[7]
                                  ] = self.mapStatus[status] if status in self.mapStatus else status

            if(transactionObject and len(transactionObject) > 0):
                transactionObject[self.csvHeader[5]] = ''  # reference_id
                transactionObject[self.csvHeader[6]] = ''  # unique_code

                transactionObject[self.csvHeader[8]] = __name__

                transactionObject[self.csvHeader[12]
                                  ] = time.strftime('%Y-%m-%d %H:%M:%S')

                transactionsList.append(transactionObject)

        driver.quit()
        return transactionsList


