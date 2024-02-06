import requests
import numpy as np
import pandas as pd
import os
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
WEBPAGE = requests.get('https://en.wikipedia.org/wiki/List_of_Canadian_provinces_and_territories_by_historical_population')


def get_data1(page):
    soup = BeautifulSoup(page.text, 'html.parser')
    tables = soup.find_all('table', class_='wikitable sortable')
    hyperlinks = []
    temp = {}
    dic = {}
    
    # Get Table Data:
    for table in tables:
        header_data = []
        row_data = []
        
        header_row = table.find('tr') # get the header row
        headers = header_row.find_all('th') # get the headers
        for header in headers:
            header_data.append(header.text.rstrip())
            
        rows = table.find_all('tr')[1:] # get the rows
        for row in rows:
            # Get HyperLinks:
            row_cells = row.find_all('td')
            for cell in row_cells:
                links = cell.find_all('a') # get all hyperlinks from tables
                for link in links:
                    href = link.get('href')
                    if (not href.startswith('#cite_note')): 
                        hyperlinks.append(href)

            row_values = [row_cell.text.rstrip() for row_cell in row_cells]
            row_data.append(row_values)
            
        for col_index, header in enumerate(header_data):
            column_values = [row[col_index] for row in row_data]
            temp[header] = column_values
        dic.update(temp)
            
            
    

    # Iterate through each list and insert None at the appropriate positions
    for key, value in dic.items():
        if len(value) < max_length:
            indices_to_insert_none = [i for i in range(max_length) if i >= len(value)]
            for index in indices_to_insert_none:
                value.insert(index, None)

    # Create the DataFrame using the dic dictionary
    combined_frame = pd.DataFrame(dic)

    combined_frame = combined_frame[combined_frame["Name"] != "Canada"] # remove the canada and total row
    combined_frame = combined_frame[combined_frame["Name"] != "Total"] # remove the canada and total row
    combined_frame.rename(columns={'Confederated[d]': 'Confederated'}, inplace=True) # rename the column to remove the references
    combined_frame.rename(columns={'1871[e]': '1871'}, inplace=True) # rename the column to remove the references
    return combined_frame, hyperlinks



def sanitize_text(text):
    # Remove unwanted characters and extra spaces
    return re.sub(r'\[\d+\]|\[[a-zA-Z]+\]|\n', '', text.strip())


def get_data(page):
    data_dict = {}
    soup = BeautifulSoup(page.text, 'html.parser')
    tables = soup.find_all('table', class_='wikitable sortable')

    for table in tables:
        rows = table.find_all('tr')
        header = [sanitize_text(header.get_text()) for header in rows[0].find_all('th')]
        for row in rows[1:]:
            columns = row.find_all(['td', 'th'])
            key = sanitize_text(columns[0].get_text())
            values = [sanitize_text(col.get_text()) for col in columns[1:]]
            data_dict[key] = dict(zip(header[1:], values))
            
    # Sanitize the data in the dictionary
    for key, value in data_dict.items():
        data_dict[key] = {sanitize_text(k): sanitize_text(v) for k, v in value.items()}

    
    
    
    df = pd.DataFrame(data_dict)

    # Transpose the DataFrame to have provinces/territories as rows and years as columns
    df = df.T

    print(df)

    # Find all h2 elements and display their text content
    h2_elements = soup.find_all('h2')
    h2_texts = [h2.get_text() for h2 in h2_elements]
    print(h2_texts)

    # Generate a list of all hyperlinks embedded within the tables
    tables = soup.find_all('table', class_='wikitable sortable')
    all_hyperlinks = []

    for table in tables:
        links = table.find_all('a')
        links_text = [link.get('href') for link in links if link.get('href')]
        all_hyperlinks.extend(links_text)

    print(all_hyperlinks)





def download_links(links: list):
    for link in links:
        url = f'https://en.wikipedia.org{link}'
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join("pages", link.split('/')[-1] + '.html')
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {url}")
        else:
            print(f"Failed to download: {url}")

    return

#data, hyperlinks = get_data(WEBPAGE)

get_data(WEBPAGE)
#download_links(hyperlinks)


