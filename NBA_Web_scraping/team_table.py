from bs4 import BeautifulSoup
import pandas as pd

# lists to store the resulting tables for each year's players stats
div_tables = []
exp_tables = []

# Range of years for which we want the data
years = list(range(1991, 2024))

# Iterate through the years to extract team stats tables from each year's player stats web page
for year in years:

    # Open the files in which we saved team stats web pages and read the data in the files in each iteration
    with open("team_stats/team_{}.html".format(year), encoding="utf-8") as f:
        data = f.read()
        f.close()

    # Use BeautifulSoup to parse the data
    soup = BeautifulSoup(data, 'html.parser')

    # Remove the unwanted rows or items from the table we are extracting
    soup.find('tr', class_="over_header").decompose()
    dec = soup.findAll('tr', class_ = 'thead')

    # Soup cannot delete multiple elements at once. Use for loop to delete elements iteratively
    for script in dec:
        script.decompose()

    # Find and extract the table we want
    sdive = soup.find('table', id = 'divs_standings_E')

    # Use pandas to read the html of the table and convert into a list containing a dataframe object
    tabldive = pd.read_html(str(sdive))

    # Find and extract the table we want
    sdivw = soup.find('table', id = 'divs_standings_W')

    # Use pandas to read the html of the table and convert into a list containing a dataframe object
    tabldivw = pd.read_html(str(sdivw))

    # To combine two dataframes into a single dataframe object
    tabldiv = tabldive[0]._append(tabldivw[0])

    # To create a common column to store Conference names for Eastern and Western Conferences
    tabldiv["Conference"] = tabldiv['Eastern Conference'].fillna(tabldiv['Western Conference'])

    # Add the year for which the player stats were recorded in a new column in the dataframe
    tabldiv["year"] = year

    # Append the dataframe to the list we declared above
    div_tables.append(tabldiv)

    # Find and extract the table we want
    s = soup.find('table', id = 'expanded_standings')

    # Use pandas to read the html of the table and convert into a list containing a dataframe object
    tabl = pd.read_html(str(s))

    # Add the year for which the player stats were recorded in a new column in the dataframe
    tabl[0]['year'] = year

    # Create a list of column names from the dataframe's columns
    cols = list(tabl[0])

    # To store the columns we want to drop in the datafrmae
    dropcols=[]

    # Iterate through each column in the dataframe and split the relevant columns' data
    # in each ell into two items and store each item in two new separate columns
    for col in cols:
        if col != "Team" and col != "Rk" and col != "year":
            tabl[0][["{}_wins".format(col), "{}_losses".format(col)]] = tabl[0][col].apply(lambda x: pd.Series(str(x).split("-")))

            # Append the column in the list to drop
            dropcols.append(col)

    # Drop the columns given in the 'dropcols' variable form the dataframe permanently
    tabl[0].drop(dropcols, axis=1, inplace=True)

    # Append the dataframe to the list we declared above
    exp_tables.append(tabl[0])

# Concatenate each dataframe we extracted and stored as separate list objects into a single dataframe
div_df = pd.concat(div_tables)

# Download the final Dataframe as a CSV file
div_df.to_csv("team_standings_division.csv")

# Concatenate each dataframe we extracted and stored as separate list objects into a single dataframe
exp_df = pd.concat(exp_tables)

# Download the final Dataframe as a CSV file
exp_df.to_csv("team_standings_expanded.csv")