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
firms_by_state_list = []
firms_by_state_list_links = []
firms_descriptions = []
phone_numbers = []
addresses = []
websites = []


first_page_containers = driver.find_elements(by="xpath", value="//ul[@id='states-list']/li")
#second_page_containers = driver.find_elements(by="xpath", value="//div[@class='inner']")
#third_page_containers = driver.find_elements(by="xpath", value="//section[@class='firm-detail-content']")
                                             
#//div[@class='inner']/div[@class='job-date-author'] firm's description
#//div[@class='inner']/div[@class='job-title-wrapper']/h2/a.get_attribute("href") details button
#/div[@class='detail-phones']/p firm's phone number
#/div/div[@class='col-sm-8 col-sm-pull-4 address-block']/p[@class='address-text'] firm's address
#/div/div[@class='col-sm-8 col-sm-pull-4 address-block']/a firm's website

for container in range(len(first_page_containers)):
    first_page_containers = driver.find_elements(by="xpath", value="//ul[@id='states-list']/li")
    containers = first_page_containers[container]
    a_tag = first_page_containers[container].find_element(by="xpath", value="./a")
    state_list.append(first_page_containers[container].find_element(by="xpath", value="./a").text)
    state_list_links.append(first_page_containers[container].find_element(by="xpath", value="./a").get_attribute("href"))
    a_tag.click()

    second_page_containers = driver.find_elements(by="xpath", value="//div[@class='inner']")
    for container1 in second_page_containers:
        a_tag1 = container1.find_element(by="xpath", value="./div[@class='job-title-wrapper']/h2/a")
        firms_by_state_list.append(container1.find_element(by="xpath", value="./div[@class='job-title-wrapper']/h2/a").text)
        firms_by_state_list_links.append(container1.find_element(by="xpath", value="./div[@class='job-title-wrapper']/h2/a").get_attribute("href"))
        firms_descriptions.append(container1.find_element(by="xpath", value="./div[@class='job-date-author']").text)
        a_tag1.click()

        third_page_containers = driver.find_elements(by="xpath", value="//section[@class='firm-detail-content']")
        for container2 in third_page_containers:
            try:
                a_tag2 = container2.find_element(by="xpath", value="./div/div[@class='col-sm-8 col-sm-pull-4 address-block']/a")
                phone_numbers.append(container2.find_element(by="xpath", value="./div[@class='detail-phones']/p").text)
                addresses.append(container2.find_element(by="xpath", value="./div/div[@class='col-sm-8 col-sm-pull-4 address-block']/p[@class='address-text']").text)
                websites.append(container2.find_element(by="xpath", value="./div/div[@class='col-sm-8 col-sm-pull-4 address-block']/a").get_attribute("href"))
            except NoSuchElementException:
                a_tag2 = None
                phone_numbers.append(None)
                addresses.append(None)
                websites.append(None)
        driver.back()
    driver.back()
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@id='states-list']/li")))

# Create a DataFrame with the extracted data
df = pd.DataFrame({"State": state_list, "Link": state_list_links, "Firm": firms_by_state_list, "Firm_Link": firms_by_state_list_links, "Description": firms_descriptions, "Phone": phone_numbers, "Address": addresses, "Website": websites})

# Save the DataFrame to a CSV file
df.to_csv("D:/Git/US_Firms_Project/data/state_list.csv", index=False)

driver.quit()
