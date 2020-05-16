
import requests
import json
import pandas as pd
from urllib.parse import urljoin

from bs4 import BeautifulSoup

def movie():
    baseRotten = 'https://www.rottentomatoes.com/'
    searchUrl = 'https://www.rottentomatoes.com/napi/search/?query='

    rawSearchQuery = input('Enter the name of movie: ')

    searchQuery = rawSearchQuery.replace(' ','%20')

    searchResults = requests.get(searchUrl+searchQuery)

    searchResults

    searchJson = json.loads(searchResults.text)

    searchJson

    moviesList = searchJson['movies']

    count=1
    for ele in range(len(moviesList)):
        print('\n\n=========================== MOVIE NUMBER ',count,'================================')
        eleData = moviesList[ele]
        print('Movie Name : ',eleData['name'])
        print('Movie Year : ',eleData['year'])
        print('\nCAST :')
        print(pd.DataFrame(eleData['castItems']))
        count = count +1

    searchNum = int(input('Enter the movie Number to get more details : '))

    searchNum = searchNum - 1
    movie = moviesList[searchNum]
    movieUrl = movie['url']

    movieUrl = urljoin(baseRotten,movieUrl)

    print('URL of Rotten Tomatoes - ',movieUrl)