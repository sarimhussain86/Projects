import requests
import time

# To create a new folder on the same directory as the current py file
'''import os
os.mkdir("mvp")'''

# The URL for MVP stats. Note we added "{}" before ".html" at the end of the string. This
# is a placeholder and a value can be inserted inside it. In our case, the value is year
url = 'https://www.basketball-reference.com/awards/awards_{}.html'

# Range of years for which we want the data
years = list(range(1991, 2024))

for year in years:
    print(year)

    # We insert the value of year inside the url string's placeholder
    urld = url.format(year)

    # Use Requests library to download web page for each year's MVP votes
    data = requests.get(urld)

    # Open separate HTML files for saving each year's web page with MVP votes
    with open("mvp/{}.html".format(year), "w+", encoding="utf-8") as f:
        f.write(data.text)
        f.close()

    # The URL will block the user for some time if the number of requests made to it exceeds 30 under
    # 1 minute. To prevent that, use time.sleep to suspend execution for specified seconds
    time.sleep(5)