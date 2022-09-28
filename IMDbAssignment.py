# importing required modules
from requests import get
from bs4 import BeautifulSoup
import pandas as panda

#-----------------------13 Reasons Why---------------------#

# Fetching URL #
url = "https://www.imdb.com/title/tt1837492/episodes?season="
response = get(url)
print(response.text[:250])

# Parsing the content #
html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

# VARIABLES required #
# Ep Title
# Ep Number
# Airdate
# Rating
# Number of Votes
# Ep Desc

# Initalize List #
dd_episode = []

# Inserting the seasons range of 13 reasons why all seasons #
for sn in range(1, 5):
    # Requesting from the server
    response = get(
       "https://www.imdb.com/title/tt1837492/episodes?season="+ str(sn)) #url of all seasons

    # Parsing
    page_html = BeautifulSoup(response.text, 'html.parser')

    # Containers for episode
    episode_containers = page_html.find_all('div', class_='info')

    # Loop to compile the episode data
    for episodes in episode_containers:
        season = sn
        episode_number = episodes.meta['content']
        title = episodes.a['title']
        airdate = episodes.find('div', class_='airdate').text.strip()
        rating = episodes.find('span', class_='ipl-rating-star__rating').text
        total_votes = episodes.find(
            'span', class_='ipl-rating-star__total-votes').text
        desc = episodes.find('div', class_='item_description').text.strip()
        episode_data = [season, episode_number,
                        title, airdate, rating, total_votes, desc]

        # Appending the episode data into the data set
        dd_episode.append(episode_data)

# Dataframe - Using Pandas #
dd_episode = panda.DataFrame(dd_episode, columns=[
    'season', 'episode_number', 'title', 'airdate', 'rating', 'total_votes', 'description'])
dd_episode.head()


# Conversion - Total Votes, Rating, AirDate to Numeric #
def remove_str(votes):
    for r in ((',', ''), ('(', ''), (')', '')):
        votes = votes.replace(*r)
    return votes


dd_episode['total_votes'] = dd_episode.total_votes.apply(
    remove_str).astype(int) #converting the total episode into integer

dd_episode.head()
dd_episode['rating'] = dd_episode.rating.astype(float)
dd_episode['airdate'] = panda.to_datetime(dd_episode.airdate)
dd_episode.info()

# Convert To CSV #
dd_episode.to_csv('13ReasonsWhy_IMDb_Ratings.csv', index=False)
