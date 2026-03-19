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
firm_names = []
firm_links = []
firm_descriptions = []
phone_numbers = []
addresses = []
websites = []
practice_areas = []

target_states = ['Alabama']

first_page_containers = driver.find_elements(by="xpath", value="//ul[@id='states-list']/li")
#second_page_containers = driver.find_elements(by="xpath", value="//div[@class='inner']")
#third_page_containers = driver.find_elements(by="xpath", value="//section[@class='firm-detail-content']")
#third_page_containers_broken = driver.find_elements(by="xpath", value="//div[@id='apus-main-content']")
                                
#2nd page xpaths
#//div[@class='inner']/div[@class='job-title-wrapper']/h2/a.get_attribute("href") details button xpath

#3rd page xpaths
#//section[@class='firm-detail-content']/div[@class='detail-phones']/p firm's phone number xpath "works on both good layouts but not the broken one"
#//section[@class='firm-detail-content']/div/p[@class='detail-description'] firm's description xpath "works on both good layouts but not the broken one"
#//section[@class='firm-detail-content']/div/div[@class='col-sm-8 col-sm-pull-4 address-block']/p[@class='address-text'] firm's address xpath "works on both good layouts but not the broken one"
#//section[@class='firm-detail-content']/div/div[@class='col-sm-8 col-sm-pull-4 address-block']/a firm's website xpath "works on first good layout but not the second good layout or the broken one"
#//div[@id='apus-main-content']/section[@class='wrapper-main-page container inner']/div[@class='row']/div[@id='main-content']/section[@class='practice-areas-block']/ul/li[@class='main-area'] firm's practice areas xpath "works on both good layouts but not the broken one"

#//div[@id='apus-main-content']/section[@class='wrapper-main-page container inner']/div[@class='row']/div[@class='detail-phones']/p firm's phone number xpath on the third page BROKENPAGE
#//div[@id='apus-main-content']/section[@class='wrapper-main-page container inner']/div[@class='row']/div/p[@class='detail-description'] firm's description xpath on the third page BROKENPAGE
#//div[@id='apus-main-content']/section[@class='wrapper-main-page container inner']/div[@class='row']/div[@id='main-content']/section[@class='firm-detail-block']/section[@class='firm-detail-content']/div[@class='col-sm-8 col-sm-pull-4 address-block']/p[@class='address-text'] firm's address xpath on the third page BROKENPAGE
#//div[@id='apus-main-content']/section[@class='practice-areas-block']/ul/li[@class='main-area'] firm's practice areas xpath on the third page BROKENPAGE

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
        firm_names.append(container1.find_element(by="xpath", value="./div[@class='job-title-wrapper']/h2/a").text)
        firm_links.append(container1.find_element(by="xpath", value="./div[@class='job-title-wrapper']/h2/a").get_attribute("href"))
        a_tag1.click()

        third_page_containers = driver.find_elements(by="xpath", value="//section[@class='firm-detail-content']")
        practice_areas_containers = driver.find_elements(by="xpath", value="//div[@id='apus-main-content']/section[@class='wrapper-main-page container inner']/div[@class='row']/div[@id='main-content']")

        for container3 in practice_areas_containers:
            try:
                a_tag2 = container3.find_element(by="xpath", value="./div/div[@class='col-sm-8 col-sm-pull-4 address-block']/a")
                items = container3.find_elements(by="xpath", value="./section[@class='practice-areas-block']/ul/li[@class='main-area']")
                if len(items) > 0:
                    items_text = [item.text.strip() for item in items]
                    practice_areas.append(", ".join(items_text))
            except NoSuchElementException:
                try:
                    items = container3.find_elements(by="xpath", value="./section[@class='practice-areas-block']/ul/li[@class='main-area']")
                    if len(items) > 0:
                        items_text = [item.text.strip() for item in items]
                        practice_areas.append(", ".join(items_text))
                except NoSuchElementException:
                    practice_areas.append('N/A')

        #for container2 in third_page_containers:
            #try:
                #a_tag2 = container2.find_element(by="xpath", value="./div/div[@class='col-sm-8 col-sm-pull-4 address-block']/a")
                #phone_numbers.append(container2.find_element(by="xpath", value="./div[@class='detail-phones']/p").text)
                #addresses.append(container2.find_element(by="xpath", value="./div/div[@class='col-sm-8 col-sm-pull-4 address-block']/p[@class='address-text']").text)
                #websites.append(container2.find_element(by="xpath", value="./div/div[@class='col-sm-8 col-sm-pull-4 address-block']/a").get_attribute("href"))
                #firm_descriptions.append(container2.find_element(by="xpath", value="./div/p[@class='detail-description']").text)
                #practice_areas.append(container2.find_element(by="xpath", value="./section[@class='wrapper-main-page container inner']/div[@class='row']/div[@id='main-content']/section[@class='practice-areas-block']/ul/li[@class='main-area']").text.strip())
            #except NoSuchElementException:
                #websites.append('N/A')
                #third_page_containers_broken = driver.find_elements(by="xpath", value="//div[@id='apus-main-content']")
                #try:
                    #phone_numbers.append(container2.find_element(by="xpath", value="./section[@class='wrapper-main-page container inner']/div[@class='row']/div[@class='detail-phones']/p").text)
                    #addresses.append(container2.find_element(by="xpath", value="./section[@class='wrapper-main-page container inner']/div[@class='row']/div[@id='main-content']/section[@class='firm-detail-block']/section[@class='firm-detail-content']/div[@class='col-sm-8 col-sm-pull-4 address-block']/p[@class='address-text']").text)
                    #firm_descriptions.append(container2.find_element(by="xpath", value="./section[@class='wrapper-main-page container inner']/div[@class='row']/div/p[@class='detail-description']").text)
                    #practice_areas.append(container2.find_element(by="xpath", value="./section[@class='wrapper-main-page container inner']/div[@class='row']/div[@id='main-content']/section[@class='practice-areas-block']/ul/li[@class='main-area']").text.strip())
                #except NoSuchElementException:
                    #phone_numbers.append('N/A')
                    #addresses.append('N/A')
                    #firm_descriptions.append('N/A')
                    #practice_areas.append('N/A')

        driver.back()
    driver.back()
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@id='states-list']/li")))

# Create a DataFrame with the extracted data
#df_main = pd.DataFrame({"Firm": firm_names, "Link": firm_links, "Description": firm_descriptions, "Phone": phone_numbers, "Address": addresses, "Website": websites})
df_practice_areas = pd.DataFrame({"Practice Area": practice_areas})

# Save the DataFrame to a CSV file
#df_main.to_csv("D:/Git/US_Firms_Project/data/firms_list_2.csv", index=False)
df_practice_areas.to_csv("D:/Git/US_Firms_Project/data/practice_areas_2.csv", index=False)

driver.quit()
