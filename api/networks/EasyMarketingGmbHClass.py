from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from api.networks.RootClass import Root
import time
from datetime import datetime
import os
# from pprint import pprint


class EasyMarketingGmbH(Root):

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
        try:
            # raise Exception(self.networkInfo)
            # print(self.networkInfo)
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument('--ignore-certificate-errors')
            chromeOptions.add_argument('--incognito')
            # chromeOptions.add_argument('--headless')

            if(self.env != 'dev'):  # run on production only
                chromeOptions.add_argument('--headless')
                chromeOptions.add_argument('--no-sandbox')
                chromeOptions.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(
                executable_path=self.ROOT_DIR + '/chromedriver', options=chromeOptions)
            driver.set_page_load_timeout(30)
            driver.get(self.networkInfo['loginlink'])

            # # pass login credentials
            # driver.implicitly_wait(5)
            driver.find_element_by_id(
                'inputPubEmail').send_keys(self.networkInfo['username'])
            driver.find_element_by_id(
                'inputPubPassword').send_keys(self.networkInfo['password'])
            driver.find_element_by_xpath(
                '//*[@id="main"]/div/div/div[2]/div/form/div[1]/div/button').click()

            # basic navigation
            driver.implicitly_wait(10)
            statsMenu = driver.find_element_by_id('navigation_item_statistic')
            statsMenu.click()

            driver.implicitly_wait(5)
            transactionsMenu = driver.find_element_by_xpath(
                '//*[@id="bs-example-navbar-collapse-1"]/ul/li[3]/ul/li[8]/a')
            transactionsMenu.click()

            driver.implicitly_wait(5)
            transactions = driver.find_element_by_css_selector(
                '#list table')

            driver.implicitly_wait(5)
            transactionsTable = transactions.find_elements_by_css_selector(
                'tbody tr')

            transactionsList = []
            for (idx, transaction) in enumerate(transactionsTable):
                transactionObject = {}

                details = transaction.find_elements_by_tag_name('td')[0].text
                if details:
                    transactionObject[self.csvHeader[1]] = details

                clickref = transaction.find_elements_by_tag_name('td')[3].text
                if clickref:
                    transactionObject[self.csvHeader[0]] = clickref
                    transactionObject[self.csvHeader[9]] = clickref + \
                        self.networkInfo['culture']  # clickRefHash

                commission = transaction.find_elements_by_tag_name('td')[
                    6].text
                if commission:
                    transactionObject[self.csvHeader[2]
                                      ] = self.formatPrice(commission, '£')

                orderValue = transaction.find_elements_by_tag_name('td')[
                    5].text
                if orderValue:
                    transactionObject[self.csvHeader[11]
                                      ] = self.formatPrice(orderValue, '£')

                click_date = transaction.find_elements_by_tag_name('td')[
                    7].text
                if click_date:
                    formatedDate = datetime.strptime(click_date,
                                                     '%d/%m/%Y, %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                    transactionObject[self.csvHeader[4]] = formatedDate
                    transactionObject[self.csvHeader[3]
                                      ] = formatedDate  # cwhen
                    transactionObject[self.csvHeader[10]
                                      ] = formatedDate  # orddate

                status = transactionsStatusArr[int(idx)]
                if status:
                    transactionObject[self.csvHeader[7]] = status

                if(len(transactionObject) > 0):
                    transactionObject[self.csvHeader[5]] = ''  # reference_id
                    transactionObject[self.csvHeader[6]] = ''  # unique_code

                    transactionObject[self.csvHeader[8]] = __name__

                    transactionObject[self.csvHeader[12]
                                      ] = time.strftime('%Y-%m-%d %H:%M:%S')

                    transactionsList.append(transactionObject)

            driver.quit()
            # transactionsList = [{"testing": '1'}]
            return transactionsList

        except:
            # driver.quit()
            return False

