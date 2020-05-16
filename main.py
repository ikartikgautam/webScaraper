import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import json


# ======================

def gotDirectResult(result, tempUrl):
    heading = result.get_text()
    print(heading)
    print('Your page is at : '+tempUrl)
    return tempUrl


def gotSearchRes(firstResult):
    print(firstResult)
    firstResulta = firstResult.find('a')
    print(firstResulta)
    coUrl = firstResulta.get('href')
    final = wikiUrl+coUrl
    print(final)
    return final


def reqThenParse(page):
    prs = requests.get(page)
    html = prs.content
    parsed = BeautifulSoup(html, 'html.parser')
    return parsed


def findHead(page):
    hTag = page.find('h1', {'id': 'firstHeading'})
    if(hTag is not None):
        return hTag.get_text()

# rotten Tomato Listing
def movie():
    baseRotten = 'https://www.rottentomatoes.com/'
    searchUrl = 'https://www.rottentomatoes.com/napi/search/?query='

    rawSearchQuery = input('Enter the name of movie: ')

    searchQuery = rawSearchQuery.replace(' ', '%20')

    searchResults = requests.get(searchUrl+searchQuery)

    searchResults

    searchJson = json.loads(searchResults.text)

    searchJson

    moviesList = searchJson['movies']

    count = 1
    for ele in range(len(moviesList)):
        print('\n\n=========================== MOVIE NUMBER ',
              count, '================================')
        eleData = moviesList[ele]
        print('Movie Name : ', eleData['name'])
        print('Movie Year : ', eleData['year'])
        print('\nCAST :')
        print(pd.DataFrame(eleData['castItems']))
        count = count + 1

    searchNum = int(input('Enter the movie Number to get more details : '))

    searchNum = searchNum - 1
    movie = moviesList[searchNum]
    movieUrl = movie['url']

    movieUrl = urljoin(baseRotten, movieUrl)

    print('URL of Rotten Tomatoes - ', movieUrl)

## function to get Wiki Data of Person

def wiki():
    urlSearch = 'https://en.wikipedia.org/w/index.php?cirrusUserTesting=control&search='
    wikiUrl = 'https://en.wikipedia.org'

    name = input('Enter the First Name :')
    srName = input('Enter the Last Name :')

    searchLink = urlSearch+name+'+'+srName

    print('Search Link = ', searchLink)

    searchRes = requests.get(searchLink)

    print('Search Request Code = ', searchRes)

    html = searchRes.content
    type(html)
    search = BeautifulSoup(html, 'html.parser')

    res = search.find('div', {'class': 'mw-search-result-heading'})

    # print('Search div result = ',res)

    if(res is not None):
        destUrl = gotSearchRes(res)
    elif(res is None):
        searchRes = search.find('h1')
        print(searchRes)
        # print(search)
        if(searchRes is not None):
            destUrl = gotDirectResult(searchRes, searchLink)

    # searching done

    destPage = reqThenParse(destUrl)

    bioTable = destPage.find('table', {'class': 'infobox biography vcard'})

    tr = bioTable.find_all('tr')

    left = []
    right = []
    for i in tr:
        if(i.find('th') is not None):
            if(i.find('td') is not None):
                left.append(i.find_all('th'))
                right.append(i.find_all('td'))

    keys = []
    for eleL in left:
        for ele in eleL:
            keys.append(ele.get_text())

    values = []
    for eleR in right:
        for ele in eleR:
            values.append(ele.get_text())

    generalTable = dict(zip(keys, values))

    print('TABLE = ')
    print(generalTable)

    # Headings in the page
    headings = destPage.find_all('span', {'class': 'mw-headline'})

    print('HEADINGS IN PAGE')
    for ele in headings:
        print(ele.get_text())

    print('\n\n ALL INFORMATION IN PAGE :')
    dfPerson = pd.DataFrame(generalTable.items())
    print(dfPerson)
    ch = input('Export to CSV ? (y/n)')

    if ch=='y':    
        dfPerson.to_csv('personal info.csv')

## IMDB Rating,Cast,details Listing
def imdb():
    baseImdb = 'https://www.imdb.com/'
    searchBase = 'https://www.imdb.com/find?q='

    movieName = input('Enter the movie to search :')

    movieName.replace(' ','+')
    searchQuery = searchBase + movieName

    req = requests.get(searchQuery)
    html = req.content
    soup = BeautifulSoup(html,'html.parser')

    searchTd = soup.find_all('td',{'class':'result_text'})
    searchTd

    aLink = []
    count = 1

    for i in searchTd:
        a=i.find('a')
        print(count,'. ',i.get_text())
        aLink.append(a.get('href'))
        count = count +1

    select = int(input('Enter the number to search details for : '))

    directory = aLink[select-1]

    pageImdb = urljoin(baseImdb,directory)

    print('Page Link = ',pageImdb)

    req = requests.get(pageImdb)
    html = req.content
    movieSoup = BeautifulSoup(html,'html.parser')

    head = movieSoup.find('h1')


    Title = head.get_text().replace('\xa0',' ')

    ratingRaw = movieSoup.find('span',{'itemprop':'ratingValue'})
    ratingCountRaw = movieSoup.find('span',{'itemprop':'ratingCount'})

    rating = ratingRaw.get_text()
    ratingCount = ratingCountRaw.get_text()

    ratingCount

    """# Table Cast"""

    table = movieSoup.find('table',{'class':'cast_list'})

    castRaw = table.find_all('img')

    cast = []
    for i in castRaw:
        cast.append(i.get('title'))

    cast

    """# Other info"""

    storyLineRaw = movieSoup.find('div',attrs={'class':'article','id':'titleStoryLine'})

    storyLine = storyLineRaw.find('div',{'class':'inline'}).find('span').get_text()

    didYouKnow = movieSoup.find('div',{'id':'titleDidYouKnow'}).get_text()

    print('\n\nDETAILS:\n')

    print('Title : ',Title)
    print('Rating = ',rating)
    print('Total Rating Count = ',ratingCount)
    print('\nCast of Movie \n')
    for i in cast:
        print('==> ',i)
    print('\nSTORY LINE\n',storyLine)
    # print('\nDID YOU KNOW ?\n',didYouKnow.replace('See more',''))



# ======================


print('What Do you Want to Search for ?')
print('1 = Movies\n2 = Persons Information')

choice = int(input(''))

if choice==1:
    source = int(input('Which Source ? (1 = Rotten Tomatoes/2 = IMDB)'))
    if source==1:
        movie()
    elif source==2:
        imdb()
    else:
        print('ERROR !')        
elif choice==2:
    wiki()
else:
    print('ERROR !')                
