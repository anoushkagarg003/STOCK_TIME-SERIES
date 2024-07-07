from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
geckodriver_path = r"C:\Users\anous\Downloads\geckodriver-v0.33.0-win64\geckodriver.exe"

firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Firefox()
driver.get('https://finance.yahoo.com/quote/NFLX/history/?period1=1022160600&period2=1719939586')
table_container = driver.find_element(By.CSS_SELECTOR, 'div.table-container.svelte-ewueuo')

# Locate the tbody within the div
tbody = table_container.find_element(By.TAG_NAME, 'tbody')

# Do something with the tbody, e.g., print its HTML content
inner_html=tbody.get_attribute('innerHTML')
soup = BeautifulSoup(inner_html, 'html.parser')

# Extract the data from the rows
rows = []
for tr in soup.find_all('tr', class_='svelte-ewueuo'):
    cols = [td.text.strip() for td in tr.find_all('td', class_='svelte-ewueuo')]
    rows.append(cols)


df = pd.DataFrame(rows, columns=["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"])
df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')
df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
df['High'] = pd.to_numeric(df['High'], errors='coerce')
df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
df['Adj Close'] = pd.to_numeric(df['Adj Close'], errors='coerce')
df['Volume'] = pd.to_numeric(df['Volume'].str.replace(',', ''), errors='coerce')
df.to_csv('stock_data.csv', index=False)
print(df)
driver.quit()