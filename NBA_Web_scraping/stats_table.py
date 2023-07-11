from bs4 import BeautifulSoup
import pandas as pd

# A list to store the resulting tables for each year's players stats
tables = []

# Range of years for which we want the data
years = list(range(1991, 2024))

# Iterate through the years to extract player stats table from each year's player stats web page
for year in years:

    # Open the files in which we saved player stats web pages and read the data in the files in each iteration
    with open("player_stats/{}_stats.html".format(year), encoding="utf-8") as f:
        data = f.read()
        f.close()

    # Use BeautifulSoup to parse the data
    soup = BeautifulSoup(data, 'html.parser')

    # Remove the unwanted rows or items from the table we are extracting
    dec = soup.findAll('tr', class_ = 'thead')

    # Soup cannot delete multiple elements at once. Use for loop to delete elements iteratively
    for script in dec:
        script.decompose()

    # Find and extract the table we want
    s = soup.find('table', id='per_game_stats')

    # Use pandas to read the html of the table and convert into a list containing a dataframe object
    tabl = pd.read_html(str(s))

    # Add the year for which the player stats were recorded in a new column in the dataframe
    tabl[0]['year'] = year

    # Append the dataframe to the list we declared above
    tables.append(tabl[0])

# Concatenate each dataframe we extracted and stored as separate list objects into a single dataframe
df = pd.concat(tables)

# Download the final Dataframe as a CSV file
df.to_csv("player_stats_per_game_all_seasons.csv")