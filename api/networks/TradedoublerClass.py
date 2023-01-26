from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from api.networks.RootClass import Root
import time
from datetime import datetime
import os
# from pprint import pprint


class Tradedoubler(Root):

    networkInfo = None
    browser = None
    mapStatus = {
        'P': 1,
        'R': 2,
        'D': 2,
        'A': 3
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
            driver.implicitly_wait(10)
            driver.execute_script(
                "document.querySelector('#menu-item-58867 a').click()")
            driver.implicitly_wait(10)
            driver.switch_to.window(driver.window_handles[1])
            driver.implicitly_wait(3)

            # pass login credentials
            driver.find_element_by_id(
                'userLoginFormUsername').send_keys('orangebuddiesuk')
            driver.find_element_by_id(
                'userLoginFormPassword').send_keys('UKTrade19!')
            driver.find_element_by_css_selector(
                'button[type="submit"]').click()

            # basic navigation
            driver.implicitly_wait(10)
            if(chromeOptions.headless):  # if headless
                element = driver.find_element_by_css_selector(".li123456 a")
                driver.execute_script("arguments[0].click();", element)
            else:
                print('non head')
                driver.find_element_by_class_name('li123456').click()

            driver.find_element_by_link_text('Leads - Sales activity').click()
            driver.implicitly_wait(10)

            # close main tab
            driver.switch_to.window(driver.window_handles[0])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            driver.implicitly_wait(10)
            driver.execute_script(
                "document.querySelector('input[name=\"transactionSearchForm[period]\"]').click()")
            driver.execute_script(
                "document.querySelector('.ranges li:nth-child(4)').click()")
            driver.find_element_by_css_selector(
                'button[type="submit"]').click()
            driver.implicitly_wait(10)

            transactionsTable = driver.find_elements_by_css_selector(
                '#DataTables_Table_1 tbody tr')

            transactionsList = []
            for (idx, transaction) in enumerate(transactionsTable):
                transactionObject = {}
                details = transaction.find_elements_by_tag_name('td')[5].text
                if details:
                    transactionObject[self.csvHeader[1]] = details

                clickref = transaction.find_elements_by_tag_name('td')[10].text
                if clickref:
                    transactionObject[self.csvHeader[0]] = clickref
                    transactionObject[self.csvHeader[9]] = clickref + \
                        self.networkInfo['culture']  # clickRefHash

                commission = transaction.find_elements_by_tag_name('td')[
                    20].text
                if commission:
                    transactionObject[self.csvHeader[2]
                                      ] = self.formatPrice(commission, '£')

                orderValue = transaction.find_elements_by_tag_name('td')[
                    14].text
                if orderValue:
                    transactionObject[self.csvHeader[11]
                                      ] = self.formatPrice(orderValue, '£')

                click_date = transaction.find_elements_by_tag_name('td')[
                    2].text
                if click_date:
                    # datetime.strptime(click_date,'%d/%m/%Y, %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                    formatedDate = click_date
                    transactionObject[self.csvHeader[4]] = formatedDate
                    transactionObject[self.csvHeader[3]
                                      ] = formatedDate  # cwhen
                    transactionObject[self.csvHeader[10]
                                      ] = formatedDate  # orddate

                status = transaction.find_elements_by_tag_name('td')[
                    7].text
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

        except Exception as err:
            # driver.quit()
            return err

