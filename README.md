US Bar Association – Multi‑Layer Selenium Scraper

Automated Extraction of Law Firm Data by State

This project is a Python + Selenium automation workflow designed to scrape law firm information from the U.S. Bar Association website. It demonstrates multi‑page navigation, dynamic content handling, and data normalization across inconsistent page layouts — all wrapped into a clean, automated pipeline that exports structured data to CSV.

The scraper supports single or multiple states, handles three different detail‑page layouts, and merges all extracted fields into a unified dataset.

---

Features

Multi‑Layer Navigation
The scraper automatically navigates through:
1. State list page  
2. Firm list page for each selected state  
3. Firm detail page (three possible layouts)

Robust Element Handling
- Explicit waits for dynamic content  
- Graceful fallbacks for missing or inconsistent fields  
- Automatic return to previous pages after scraping details  

Layout‑Aware Extraction
The detail pages on the site use three different HTML structures.  
Your script detects and extracts data from all of them:
- Main layout (full details + website link)  
- Secondary layout (missing website link)  
- Broken layout (PHP error but still contains partial data)

Clean Data Output
All extracted fields are merged into a single, normalized DataFrame:
- Firm name  
- State  
- Description  
- Phone  
- Address  
- Website  
- Practice areas  
- Source link  

The final dataset is exported as a timestamped CSV.

---

How does it work?

1. Load the State List
The script loads the main directory page and extracts all available states.  
The user is prompted to select one or more states to scrape.

2. Navigate to Each Selected State
For each chosen state:
- Selenium clicks the state link  
- Waits for the firm list to load  
- Extracts firm names, locations, and detail‑page links  

3. Visit Each Firm’s Detail Page
For every firm:
- Selenium clicks the “Details” link  
- Detects which layout is being used  
- Extracts all available fields  
- Returns to the firm list page  

4. Normalize and Merge Data
Because different layouts expose different fields, the script:
- Merges all DataFrames  
- Fills missing values using fallback layouts  
- Ensures each firm has a complete record  

5. Export to CSV
A timestamped CSV is saved to the project’s /data directory.

---

Project Structure

`
USFirmsProject/
│── data/
│ └── Firms-List-<DATE>.csv
│
│── src/
│ └── scraper.py # (Your main script)
│
│── README.md
`

---

Technologies Used

- Python 3.x
- Selenium WebDriver
- webdriver‑manager
- Pandas
- MS Edge / Chrome WebDriver
- Explicit Waits (EC.presenceofallelementslocated)

---

Key Challenges Solved

1. Handling Multiple Page Layouts
The detail pages are inconsistent.  
Your script solves this by:
- Checking multiple XPath patterns  
- Using try/except blocks  
- Storing fallback values  
- Merging all layouts into a unified dataset  

2. Maintaining Navigation State
Because Selenium opens detail pages in the same tab:
- The script uses driver.back() to return  
- Explicit waits ensure the previous page is fully reloaded  

3. User‑Driven State Selection
The script validates user input against the live state list, ensuring:
- No invalid states  
- No typos  
- Clean multi‑state selection  

---

How to Run

1. Install dependencies:
   `
   pip install -r requirements.txt
   `

2. Run the scraper:
   `
   python scraper.py
   `

3. Enter one or more states when prompted:
   `
   Alabama, California
   `

4. The script will:
   - Navigate the site  
   - Scrape all firm details  
   - Export a CSV to /data  

---

Output Example

Each row in the CSV contains:

| Firm | Firm link from US BAR Association website | Phone | Address | Firm's Website Link | State | Practice Area | Description |
|------|-------------------------------------------|-------|---------|---------------------|-------|--------------|--------------|


Future Improvements

- Add multiprocessing for faster scraping  
- Add retry logic for slow-loading pages  
- Add SQLite or PostgreSQL export  
- Add CLI flags (e.g., --all-states)  
- Add logging instead of print statements  

---

Final Notes

This project is a strong demonstration of:
- Multi‑step Selenium automation  
- Real‑world web scraping challenges  
- Data cleaning and normalization  
- Modular, production‑ready Python scripting  