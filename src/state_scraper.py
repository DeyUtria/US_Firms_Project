from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

first_page_containers = driver.find_elements(by="xpath", value="//ul[@id='states-list']/li")
second_page_containers = driver.find_elements(by="xpath", value="//div[@class='inner']")

#//div[@class='inner']/div[@class='job-date-author'] firm's description
#//div[@class='inner']/div[@class='job-title-wrapper']/h2/a.get_attribute("href") details button

for container in first_page_containers:
    state_list.append(container.find_element(by="xpath", value="./a").text)
    state_list_links.append(container.find_element(by="xpath", value="./a").get_attribute("href"))
    link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.xpath, "./a".get_attribute("href"))))
    link.click()
    for container1 in second_page_containers:
        firms_by_state_list.append(container1.find_element(by="xpath", value="./div[@class='job-title-wrapper']/h2/a").text)
        firms_by_state_list_links.append(container1.find_element(by="xpath", value="./div[@class='job-title-wrapper']/h2/a").get_attribute("href"))
        firms_descriptions.append(container1.find_element(by="xpath", value="./div[@class='job-date-author']").text)
        link1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.xpath, "./a".get_attribute("href"))))
        link1.click()
# Create a DataFrame with the extracted data
df = pd.DataFrame({"State": state_list, "Link": state_list_links})

# Save the DataFrame to a CSV file
df.to_csv("D:/Git/US_Firms_Project/data/state_list.csv", index=False)

driver.quit()
