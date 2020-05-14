import requests
from bs4 import BeautifulSoup

# ======================

def gotDirectResult(result,tempUrl):
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
    parsed = BeautifulSoup(html,'html.parser')
    return parsed    
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
    destUrl = gotSearchRes(res)
elif(res is None):
    searchRes = search.find('h1')
    print(searchRes)
    #print(search)
    if(searchRes is not None):
        destUrl = gotDirectResult(searchRes,searchLink)

#searching done        

destPage = reqThenParse(destUrl)

bioTable = destPage.find('table',{'class':'infobox biography vcard'})

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

generalTable = dict(zip(keys,values))

print('TABLE = ')
print(generalTable)
