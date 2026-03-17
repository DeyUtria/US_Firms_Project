from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import pandas as pd

website = "https://www.us-barassociation.org/content/state-list/"
path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedgedriver.exe"
service = Service(executable_path=path)
driver = webdriver.Edge(service=service)
driver.get(website)

state_list = []
state_list_links = []
firm_name = []
firm_link = []
firm_description = []
phone_number = []
address = []
website = []
practice_area = []

target_states = ['Wyoming']

first_page_containers = driver.find_elements(by="xpath", value="//ul[@id='states-list']/li")
#second_page_containers = driver.find_elements(by="xpath", value="//div[@class='inner']")
#third_page_containers = driver.find_elements(by="xpath", value="//section[@class='firm-detail-content']")
#third_page_containers_broken = driver.find_elements(by="xpath", value="//div[@class='row']")
                                
#//section[@class='firm-detail-content']/div/p[@class='detail-description'] firm's description xpath
#//div[@class='inner']/div[@class='job-title-wrapper']/h2/a.get_attribute("href") details button xpath
#/div[@class='detail-phones']/p firm's phone number xpath
#/div/div[@class='col-sm-8 col-sm-pull-4 address-block']/p[@class='address-text'] firm's address xpath
#/div/div[@class='col-sm-8 col-sm-pull-4 address-block']/a firm's website xpath
#//div[@class='row']/div/p[@class='detail-description'] firm's description xpath on the third page BROKENPAGE
#//section[@class='practice-areas-block']/ul/li firm's practice areas xpath on the third page BROKENPAGE
#//div[@class='row']/div[@class='detail-phones']/p/ firm's phone number xpath on the third page BROKENPAGE

for container in range(len(first_page_containers)):
    first_page_containers = driver.find_elements(by="xpath", value="//ul[@id='states-list']/li")
    containers = first_page_containers[container]
    a_tag = containers.find_element(by="xpath", value="./a")
    states_names = a_tag.text.strip()
    if states_names not in target_states:
        continue
    a_tag.click()

    second_page_containers = driver.find_elements(by="xpath", value="//div[@class='inner']")
    for container1 in second_page_containers:
        a_tag1 = container1.find_element(by="xpath", value="./div[@class='job-title-wrapper']/h2/a")
        firm_name.append(container1.find_element(by="xpath", value="./div[@class='job-title-wrapper']/h2/a").text)
        firm_link.append(container1.find_element(by="xpath", value="./div[@class='job-title-wrapper']/h2/a").get_attribute("href"))
        a_tag1.click()

        third_page_containers = driver.find_elements(by="xpath", value="//section[@class='firm-detail-content']")
        third_page_containers_broken = driver.find_elements(by="xpath", value="//div[@class='row']")
        for container2 in third_page_containers:
            try:
                a_tag2 = container2.find_element(by="xpath", value="./div/div[@class='col-sm-8 col-sm-pull-4 address-block']/a")
                phone_number.append(container2.find_element(by="xpath", value="./div[@class='detail-phones']/p").text)
                address.append(container2.find_element(by="xpath", value="./div/div[@class='col-sm-8 col-sm-pull-4 address-block']/p[@class='address-text']").text)
                website.append(container2.find_element(by="xpath", value="./div/div[@class='col-sm-8 col-sm-pull-4 address-block']/a").get_attribute("href"))
                firm_description.append(container2.find_element(by="xpath", value="./div/p[@class='detail-description']").text)
                practice_area.append(container2.find_element(by="xpath", value="./section[@class='practice-areas-block']/ul/li").text)
            except NoSuchElementException:
                a_tag2 = 'N/A'
                phone_number.append('N/A')
                address.append('N/A')
                website.append('N/A')
                firm_description.append('N/A')
                practice_area.append('N/A')

        #for container3 in third_page_containers_broken:
            #try:
                #phone_numbers.append(container3.find_element(by="xpath", value="./div[@class='detail-phones']/p").text)
                #addresses.append(container3.find_element(by="xpath", value="./div/div[@class='col-sm-8 col-sm-pull-4 address-block']/p[@class='address-text']").text)
                #websites.append(container3.find_element(by="xpath", value="./div/div[@class='col-sm-8 col-sm-pull-4 address-block']/a").get_attribute("href"))
            #except NoSuchElementException:
                #phone_numbers.append('N/A')
                #addresses.append('N/A')
                #websites.append('N/A')
        driver.back()
    driver.back()
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@id='states-list']/li")))

# Create a DataFrame with the extracted data
df = pd.DataFrame({"Firm": firm_name, "Link": firm_link, "Description": firm_description, "Phone": phone_number, "Address": address, "Website": website})

# Save the DataFrame to a CSV file
df.to_csv("D:/Git/US_Firms_Project/data/firms_list_1.csv", index=False)

driver.quit()
