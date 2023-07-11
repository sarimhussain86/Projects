from selenium import webdriver
import time

# To create a new folder on the same directory as the current py file
'''import os
os.mkdir("player_stats")'''

# The URL for player stats per year. Note we added "{}" before ".html" at the end of the string.
# This is a placeholder and a value can be inserted inside it. In our case, the value is year
url = 'https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'

# Range of years for which we want the data
years = list(range(1991, 2024))

for year in years:

    # Through Selenium test we will invoke the executable file which will then #invoke actual browser
    driver = webdriver.Chrome()

    # to maximize the browser window
    driver.maximize_window()

    # get method to launch the URL
    driver.get(url.format(year))

    # to close the browser
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)

    # Download the HTML of the entire web page
    html = driver.page_source
    time.sleep(2)

    # Store the HTML of each web page in separate HTML files through iteration
    with open("player_stats/{}_stats.html".format(year), "w+", encoding="utf-8") as f:
        f.write(html)
        f.close()