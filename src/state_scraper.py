# Import all the needed libraries:
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import os
import sys
import psycopg2
import pandas as pd

# Set the driver path, website path and headless mode using msedge. Disabling GPU mode for Windows. Adding path for executable file and timeframe.
website = "https://www.us-barassociation.org/content/state-list/"
path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedgedriver.exe"
service = Service(executable_path=path)
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(website)
app_path = os.path.dirname(sys.executable)
now = datetime.now()
strf = now.strftime("%m%d%Y")

# Variables for the first and second pages (States list and firm names with their US Bar Association website link)
state_list = []
states_names = []
firm_names = []
firm_links = []

# Variables for the third page (Firm's details webpage and all 3 different layouts)
# First layout
firm_descriptions = []
phone_numbers = []
addresses = []
websites = []
practice_areas = []

# Second layout
firm_descriptions_1 = []
phone_numbers_1 = []
addresses_1 = []

# Third layout
firm_descriptions_broken = []
phone_numbers_broken = []
addresses_broken = []
practice_areas_broken = []

# Ask user what states to scrape firms from
first_page_containers = driver.find_elements(by="xpath", value="//ul[@id='states-list']/li")
for contain in first_page_containers:
    state_list.append(contain.find_element(by="xpath", value="./a").text.strip())

while True:
    user_input = input("What state(s) do you want the firm list from? " + "\nIf choosing multiple states, separate each other using a comma. (e.g: Alabama, California): ")
    
    # Split the input by comma and strip whitespace from each state.
    input_states = [state.strip() for state in user_input.split(",")]
    
    # Check if all input states are valid.
    all_valid = True
    for input in input_states:
        if input not in state_list:
            print(f"Invalid state: '{input}'. Please try again.")
            all_valid = False
            break
    
    if all_valid:
        target_states = input_states
        print(f"Selected states: {target_states}")
        print("Retrieving the information and exporting to CSV file... This may take a few minutes...")
        break
    else:
        print("Please enter valid state name(s) separated by commas.")
        
# Defining the first page xpath and looping through it to get all the states list. Also, make sure to click on the state link to access the firm list from said state.
for container in range(len(first_page_containers)):
    first_page_containers = driver.find_elements(by="xpath", value="//ul[@id='states-list']/li")
    containers = first_page_containers[container]
    a_tag = containers.find_element(by="xpath", value="./a")
    
    # Looping through the state we want to scrape the firm lists from. Stripping the name for accuracy purposes.
    state_list = a_tag.text.strip()
    if state_list not in target_states:
        continue
    a_tag.click()

    # Defining the second page xpath and looping through it to get all the firm names with their US Bar Association website link.
    second_page_containers = driver.find_elements(by="xpath", value="//div[@class='inner']")
    
    for container1 in second_page_containers:
        a_tag1 = container1.find_element(by="xpath", value="./div[@class='job-title-wrapper']/h2/a")
        firm_names.append(container1.find_element(by="xpath", value="./div[@class='job-title-wrapper']/h2/a").text)
        firm_links.append(container1.find_element(by="xpath", value="./div[@class='job-title-wrapper']/h2/a").get_attribute("href"))
        states_names.append(container1.find_element(by="xpath", value="./div[@class='job-metas']/div[@class='job-location']").text.strip().split(","))
        a_tag1.click()

        # Defining the third page xpaths for all of the 3 different layouts found.
        third_page_main_layout = driver.find_elements(by="xpath", value="//section[@class='firm-detail-content']")
        third_page_broken_layout = driver.find_elements(by="xpath", value="//div[@id='apus-main-content']/section[@class='wrapper-main-page container inner']/div[@class='row']")
        practice_areas_containers = driver.find_elements(by="xpath", value="//div[@id='apus-main-content']")  

        # Looping through the practice areas blocks and the title block using the xpaths for the 2 different layouts and appending the information found to the respective lists.
        for container2 in practice_areas_containers:
            try:
                items = container2.find_elements(by="xpath", value="./section[@class='wrapper-main-page container inner']/div[@class='row']/div[@id='main-content']/section[@class='practice-areas-block']/ul/li[@class='main-area']")
                if len(items) > 0:
                    items_text = [item.text.strip() for item in items]
                    practice_areas.append(", ".join(items_text))
                else:
                    practice_areas.append('N/A')
            except NoSuchElementException:
                practice_areas.append('N/A')
        
        for container3 in practice_areas_containers:
            try:
                items_broken = container3.find_elements(by="xpath", value="./section[@class='practice-areas-block']/ul/li[@class='main-area']")
                if len(items_broken) > 0:
                    items_text = [item.text.strip() for item in items_broken]
                    practice_areas_broken.append(", ".join(items_text))
                else:
                    practice_areas_broken.append('N/A')
            except NoSuchElementException:
                practice_areas_broken.append('N/A')

        # Looping through the first layout and appending the information found to the respective lists. (Website button included)
        for container2 in third_page_main_layout:
            try:
                a_tag2 = container2.find_element(by="xpath", value="./div/div[@class='col-sm-8 col-sm-pull-4 address-block']/a")
                phone_numbers.append(container2.find_element(by="xpath", value="./div[@class='detail-phones']/p").text)
                addresses.append(container2.find_element(by="xpath", value="./div/div[@class='col-sm-8 col-sm-pull-4 address-block']/p[@class='address-text']").text)
                firm_descriptions.append(container2.find_element(by="xpath", value="./div/p[@class='detail-description']").text)
                websites.append(container2.find_element(by="xpath", value="./div/div[@class='col-sm-8 col-sm-pull-4 address-block']/a").get_attribute("href"))
            except NoSuchElementException:
                phone_numbers.append('N/A')
                addresses.append('N/A')
                firm_descriptions.append('N/A')
                websites.append('N/A')

        # Looping through the second layout and appending the information found to the respective lists. (Website button missing) 
        for container3 in third_page_main_layout:
            try:
                phone_numbers_1.append(container3.find_element(by="xpath", value="./div[@class='detail-phones']/p").text)
                addresses_1.append(container3.find_element(by="xpath", value="./div/div[@class='col-sm-8 col-sm-pull-4 address-block']/p[@class='address-text']").text)
                firm_descriptions_1.append(container3.find_element(by="xpath", value="./div/p[@class='detail-description']").text)
            except NoSuchElementException:
                phone_numbers_1.append('N/A')
                addresses_1.append('N/A')
                firm_descriptions_1.append('N/A')

        # Looping through the last layout and appending the information found to the respective lists. (Broken layout showing a 'PHP not found' error message)
        for container3 in third_page_broken_layout:
            try:
                phone_numbers_broken.append(container3.find_element(by="xpath", value="./div[@class='detail-phones']/p").text)
                addresses_broken.append(container3.find_element(by="xpath", value="./div[@id='main-content']/section[@class='firm-detail-block']/section[@class='firm-detail-content']/div[@class='col-sm-8 col-sm-pull-4 address-block']/p[@class='address-text']").text)
                firm_descriptions_broken.append(container3.find_element(by="xpath", value="./div/p[@class='detail-description']").text)
            except NoSuchElementException:
                phone_numbers_broken.append('N/A')
                addresses_broken.append('N/A')
                firm_descriptions_broken.append('N/A')

        # Coming back to second page to access the next firm details page
        driver.back()

    # Coming back to the first page to access the next state (if required in the 'target_states' variable)    
    driver.back()

    #Telling the driver to wait 10 second until the condition is met which is wait for all the states in the list of the first page to show up.
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@id='states-list']/li")))

# Create a DataFrame with the extracted data
df_main = pd.DataFrame({"Firm": firm_names, "Link": firm_links, "Description": firm_descriptions, "Phone": phone_numbers, "Address": addresses, "Website": websites})
df_main_no_website = pd.DataFrame({"Firm": firm_names, "Link": firm_links, "Description": firm_descriptions_1, "Phone": phone_numbers_1, "Address": addresses_1})
df_broken = pd.DataFrame({"Firm": firm_names, "Link": firm_links, "Description": firm_descriptions_broken, "Phone": phone_numbers_broken, "Address": addresses_broken})
df_practice_areas = pd.DataFrame({"Firm": firm_names, "Link": firm_links, "Practice Area": practice_areas})
df_practice_areas_broken = pd.DataFrame({"Firm": firm_names, "Link": firm_links, "Practice Area": practice_areas_broken})
df_states = pd.DataFrame({"State": states_names})

# Merge all dataframes into one single dataframe with all the columns available
df_main_no_website['State'] = df_states['State'].str.get(1)
df_main_no_website['Website'] = df_main['Website'].values
df_main_no_website['Practice Area'] = df_practice_areas['Practice Area'].values
df_broken['Website'] = 'N/A'
df_broken['Practice Area'] = df_practice_areas_broken['Practice Area'].values
df_main_no_website['Description'] = df_main_no_website['Description'].mask(df_main_no_website['Description'] == 'N/A', df_broken['Description'])
df_main_no_website['Phone'] = df_main_no_website['Phone'].mask(df_main_no_website['Phone'] == 'N/A', df_broken['Phone'])
df_main_no_website['Address'] = df_main_no_website['Address'].mask(df_main_no_website['Address'] == 'N/A', df_broken['Address'])
df_main_no_website['Practice Area'] = df_main_no_website['Practice Area'].mask(df_main_no_website['Practice Area'] == 'N/A', df_broken['Practice Area'])

tuples = list(df_main_no_website.itertuples(index=False, name=None))
              
# Save the DataFrame to a CSV file
file_name = f"D:/Git/US_Firms_Project/data/Firms-List-{strf}.csv"
final_path = os.path.join(app_path, file_name)

df_main_no_website.to_csv(final_path, index=False)

print(f"!CSV generated successfully! You can find it on the following path: {final_path}.")

# Connecting to the database using postgresql and inserting the information extracted from usbar_association website
print("Inserting information into the database...")

conn = psycopg2.connect(
    database = "postgres",
    user = "postgres",
    password = "admin",
    host = "localhost",
    port = "5432"
)

cursor = conn.cursor()
cursor.executemany("INSERT INTO firms (firm, firm_link, description, phone_number, address, state_name, website, practice_area) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", tuples)

conn.commit()
print("Information inserted successfully into the database!")
conn.close()
# Quitting the program
driver.quit()