from bs4 import BeautifulSoup
import pandas as pd

# A list to store the resulting tables for each year's MVP votes
tables = []

# Range of years for which we want the data
years = list(range(1991, 2024))

# Iterate through the years to extract MVP votes table from each year's MVP votes web page
for year in years:

    # Open the files in which we saved MVP votes web pages and read the data in the files in each iteration
    with open("mvp/{}.html".format(year), encoding="utf-8") as f:
        data = f.read()
        f.close()

    # Use BeautifulSoup to parse the data
    soup = BeautifulSoup(data, 'html.parser')

    # Remove the unwanted rows or items from the table we are extracting
    soup.find('tr', class_ = "over_header").decompose()

    # Find and extract the table we want
    s = soup.find('table', id = 'mvp')

    # Use pandas to read the html of the table and convert into a list containing a dataframe object
    tabl = pd.read_html(str(s))

    # Add the year for which the MVP votes were recorded in a new column in the dataframe
    tabl[0]['year'] = year

    # Append the dataframe to the list we declared above
    tables.append(tabl[0])

# Concatenate each dataframe we extracted and stored as separate list objects into a single dataframe
df = pd.concat(tables)

# Download the final Dataframe as a CSV file
df.to_csv("mvp_all_seasons.csv")