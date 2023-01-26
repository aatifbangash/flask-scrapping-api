from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from api.networks.RootClass import Root
import time
from datetime import datetime
import os
# from pprint import pprint


class Tradetracker(Root):

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
            driver.find_element_by_id('open-close-login').click()

            # pass login credentials
            driver.implicitly_wait(5)
            driver.implicitly_wait(5)
            driver.find_element_by_id(
                'control-affiliate-username').send_keys('orangebuddiesuk')
            driver.find_element_by_id(
                'control-affiliate-password').send_keys('ukTT19!')
            driver.find_element_by_id('affiliate-login').submit()

            # basic navigation
            driver.implicitly_wait(10)
            reportMenu = driver.find_element_by_xpath(
                '//*[@id="wrapper-affiliate"]/div[2]/div[1]/ul[1]/li[4]/a')
            reportMenu.click()

            driver.implicitly_wait(5)
            transactionsMenu = driver.find_element_by_xpath(
                '//*[@id="wrapper-affiliate"]/div[2]/div[1]/ul[1]/li[4]/ul/li[5]/a')
            transactionsMenu.click()

            driver.implicitly_wait(5)
            salesTransactionsMenu = driver.find_element_by_xpath(
                '//*[@id="wrapper-affiliate"]/div[2]/div[1]/ul[1]/li[4]/ul/li[5]/ul/li[2]/a')
            salesTransactionsMenu.click()

            driver.implicitly_wait(5)
            selectAllTransLink = driver.find_element_by_css_selector(
                '.list-view-filter-item-all a')
            selectAllTransLink.click()
            driver.implicitly_wait(5)

            driver.find_element_by_id('s2id_predefined-periods-p').click()

            driver.implicitly_wait(1)
            driver.find_element_by_xpath(  # this month
                '//*[@id="select2-result-label-16"]').click()

            driver.implicitly_wait(5)
            transactions = driver.find_elements_by_css_selector(
                '#list-view-27')[1]

            driver.implicitly_wait(5)
            transactionsStatusArr = []
            transactionsStatus = driver.find_elements_by_css_selector(
                '#list-view-27')[0]
            for transaction in transactionsStatus.find_elements_by_css_selector('tbody tr'):
                status = os.path.basename(transaction.find_elements_by_tag_name('td img')[
                                          0].get_attribute('src'))
                transactionsStatusArr.append(
                    status.replace('.png', ''))  # status

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
            return transactionsList

        except:
            # driver.quit()
            return False


