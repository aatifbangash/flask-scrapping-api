obj = {
    "name": "atif",
    "age": 30
}
keys = obj.keys()
values = obj.values()

print({key: value for key, value in obj.items() if key == 'age'})
# from datetime import datetime

# print(datetime.strptime("31/01/2020, 17:07:37",
#                         '%d/%m/%Y, %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'))
###### working example #####
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# # from selenium.webdriver.common.keys import Keys
# import time
# import json
# from pprint import pprint
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')

# driver = webdriver.Chrome(executable_path='./chromedriver',options=options)

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')

# driver = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options)
# driver.get('http://datawork.hasoffers.com')

# privacyCheck = driver.find_element_by_id('privacyCheckbox').click()

# cookieCheck = driver.find_element_by_id('cookieCheckbox').click()

# continueBtn = driver.find_element_by_id('euContinueButton').click()

# driver.refresh()

# driver.find_element_by_id('UserEmail').send_keys('affiliate-pt@orangebuddies.com')
# password = driver.find_element_by_id('UserPassword').send_keys('OrangeDatawork')

# driver.find_element_by_id('loginButton').click()
# time.sleep(2)

# reportLink = driver.find_element_by_xpath('//*[@id="sidebar"]/div/nav/div[3]/a').click()
# time.sleep(1)
# conversionReportLink = driver.find_element_by_xpath('//*[@id="sidebar"]/div/nav/div[3]/ul/li[2]/a').click()

# transactionsArr = []
# element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-jqgrid-view table tr')))
# time.sleep(1)
# transactionsList = driver.find_elements_by_css_selector('.ui-jqgrid-view table tr')
# for (i, l) in enumerate(transactionsList):
#     obj = {}
#     if(i == 0):
#         continue

#     for (j, e) in enumerate(l.find_elements_by_css_selector('td')):
#         if(e.text):
#             obj[j] = e.text

#     if(len(obj) > 0):
#         transactionsArr.append(obj)

# # print(json.dumps(transactionsArr, indent=1))
# pprint(transactionsArr)

# driver.quit()
#### onlineustaad example ###
# driver.set_page_load_timeout(30)
# driver.get('https://onlineustaad.com/blog/')
# articles = driver.find_elements_by_css_selector('.content-inner')
# resultArr = []
# for article in articles:
#     obj = {}
#     obj['title'] = article.find_elements_by_css_selector(
#         '.entry-content .entry-header')[0].text
#     obj['src'] = article.find_elements_by_css_selector(
#         'img')[0].get_attribute('data-lazy-src')
#     obj['link'] = article.find_elements_by_css_selector(
#         'a.post-image')[0].get_attribute('href')
#     obj['desc'] = article.find_elements_by_css_selector(
#         '.entry-content .entry-summary p')[0].text

#     resultArr.append(obj)

# driver.quit()


###### EXAMPLE 1 #####
# from selenium import webdriver

# # options = webdriver.ChromeOptions()
# # options.add_argument('--ignore-certificate-errors')
# # options.add_argument('--incognito')
# # options.add_argument('--headless')

# # driver = webdriver.Chrome(executable_path='./chromedriver',options=options)

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options)
# driver.get('https://www.google.com/')

# print(driver.title)
# driver.quit()
