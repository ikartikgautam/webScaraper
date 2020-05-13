import requests
from bs4 import BeautifulSoup

# ======================

def gotDirectResult(result,destUrl):
    heading = result.get_text()
    print(heading)
    print('Your page is at : '+destUrl)

def gotSearchRes(firstResult):
    print(firstResult)
    firstResulta = firstResult.find('a')
    print(firstResulta)
    coUrl = firstResulta.get('href')
    final = wikiUrl+coUrl
    print(final)
    
# ======================

urlSearch = 'https://en.wikipedia.org/w/index.php?cirrusUserTesting=control&search='
wikiUrl = 'https://en.wikipedia.org'

name = input('Enter the First Name :')
srName = input('Enter the Last Name :')

searchLink = urlSearch+name+'+'+srName

print('Search Link = ',searchLink)

searchRes = requests.get(searchLink)

print('Search Request Code = ',searchRes)

html = searchRes.content
type(html)
search = BeautifulSoup(html, 'html.parser')

res = search.find('div', {'class': 'mw-search-result-heading'})

# print('Search div result = ',res)

if(res is not None):
    gotSearchRes(res)
elif(res is None):
    searchRes = search.find('h1')
    print(searchRes)
    #print(search)
    if(searchRes is not None):
        gotDirectResult(searchRes,searchLink)