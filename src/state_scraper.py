from selenium import webdriver
from selenium.webdriver.edge.service import Service
import pandas as pd

website = "https://www.us-barassociation.org/content/state-list/"
path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedgedriver.exe"
service = Service(executable_path=path)
driver = webdriver.Edge(service=service)
driver.get(website)

state_list = []
state_list_links = []

containers = driver.find_elements(by="xpath", value="//ul[@id='states-list']/li")
print(len(containers))

for container in containers:
    state_list.append(container.find_element(by="xpath", value="./a").text)
    state_list_links.append(container.find_element(by="xpath", value="./a").get_attribute("href"))        

# Create a DataFrame with the extracted data
df = pd.DataFrame({"State": state_list, "Link": state_list_links})

# Save the DataFrame to a CSV file
df.to_csv("state_list.csv", index=False)

driver.quit()
