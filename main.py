# Importing Modules

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

# Creating the empty list to append data in it

movie_name = []
year = []
run_time = []
imdb_rating = []
grossInDoll = []
genres = []
directors = []
stars = []
votes = []

'''
np.arrange(1,1001,50) is a function in the NumPy Python library, 
and it takes four arguments — but we’re only using the first three
 which are: start, stop, and step. 
 step is the number that defines the spacing between each. So: Start at 1, stop at 1001, and step by 50.
'''
pages = np.arange(1, 1001, 100)

for page in pages:

    url = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=' + str(page)
    source = requests.get(url)

    # To show any error in the link

    # source.raise_for_status()

    # GETTING the html text
    soup = BeautifulSoup(source.text, 'html.parser')

    # Grabbing the list of movies

    movies = soup.find('div', class_='lister-list').find_all(class_='lister-item mode-advanced')
    # print(len(movies))

    # Want to grab all movies name from the 'lister-item mode-detail' class

    for movie in movies:
        name = movie.find('h3', class_='lister-item-header').a.text
        movie_name.append(name)

        year1 = movie.find('span', class_='lister-item-year text-muted unbold').text.strip('()')
        year.append(year1)

        genre = movie.find('span', class_='genre').get_text(strip=True)
        genres.append(genre)

        time = movie.find('span', class_='runtime').text
        run_time.append(time)

        rating = movie.find('div', class_='inline-block ratings-imdb-rating').strong.text
        imdb_rating.append(rating)

        cast = movie.find_all('p', class_='')
        cast_ = cast[0].get_text(strip=True).split('|')

        director = cast_[0].replace('Director:', "")
        director_ = director.replace('Directors:', "")
        directors.append(director)

        star = cast_[1].replace('Stars:', "")
        stars.append(star)

        value = movie.find_all('p', class_='sort-num_votes-visible')[0]
        value_ = value.get_text(strip=True).split('|')

        vote = value_[0].replace('Votes:', "")
        votes.append(vote)

        if len(value_) > 1:
            gross = value_[1].replace('Gross:', "")
        else:
            gross = "NA"
        grossInDoll.append(gross)

# Creating a dataframe using a dictionary

movies_DF = pd.DataFrame({'Name of movie': movie_name, 'Year': year, 'Rating': imdb_rating, 'Run Time': run_time,
                          'Genre': genres, 'Directors': directors, 'Stars': stars, 'Votes': votes,
                          'Gross': grossInDoll})

# Saving the dataframe into csv format

movie = movies_DF.to_csv("C:\\Users\\asus\PycharmProjects\\WebScraping-1000s-Movies-data\\IMDB-1000s-movies.csv")

print(movies_DF)
