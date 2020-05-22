from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re


#####################################################################################################################
# CODE TAKEN FROM - Ufuk, U., 2018. Fast Reddit Scraping. [online] Utku's Blog. Available at: <https://utkuufuk.com/2018/07/29/reddit-scraping/> 

reddit_link = 'https://old.reddit.com/'
REQUEST_AGENT = 'Chrome/47.0.2526.106'

def createSoup(url):
    return BeautifulSoup(requests.get(url, headers={'User-Agent':REQUEST_AGENT}).text, 'lxml')#lxml’s HTML parser

def getScraperResults(scrapUrl): #Using the built Url we can retrieve the search results in form of a bs4.element.Tag array
    posts = []
    
    if len(posts)<=25: #limit posts to 25 
        resultPage = createSoup(scrapUrl) #retrieve posts using beautifulSoup
        posts += resultPage.findAll('div', {'class':'search-result-link'}) # Append posts to an array


        
    return posts

def parsePosts(posts, searchedCur, keyword):
    
    for post in posts: #From posts we extract the required information

        title = post.find('a', {'class':'search-title'}).text #finds relevant tags 
        time = post.find('time')['datetime'] #retrieve title, date and time
        date = datetime.strptime(time[:19], '%Y-%m-%dT%H:%M:%S')

        

        comments = post.find('a', {'class':'search-comments'})
        url = comments['href'] #retrieve comments to get link of article
        

        
        score = post.find('span', {'class':'search-score'}).text #retrieve score for further implementaion
        score = int(re.match(r'[+-]?\d+', score).group(0))
        
        searchedCur.append({'title':title, 'url':url, 'date':str(date), 'score':score}) #Append all values to searchedCur

    return searchedCur



def start(pKeyword):
#pKeyword is the user parameter (Name of cryptocurrency to be scraped for in Reddit )

    keyword = str(pKeyword)
    date1 = 'week'
    subreddit = 'cryptocurrency'

    scrapUrl = reddit_link + 'r/' + subreddit + '/search?q="' + keyword + '"&restrict_sr=on'
    scrapUrl += '&t=' + date1 #builds the URL to be searched for 
    posts = getScraperResults(scrapUrl) #scrapes through a maximum of 25 posts 

        
    searched = [] #array created for searched currency
    
    searched = parsePosts(posts, searched, keyword)
   
#####################################################################################################################   

    
######  ADDITIONAL IMPLEMENTAITON #######


    n = len(searched)


    for a in range(n): #bubble sort algorithm  to sort retrieved posts according to reddit score
        for j in range(0,n-a-1):
            if searched[j]['score']> searched[j+1]['score']:
                searched[j] , searched[j+1] = searched[j+1],searched[j]


    rank = searched[-5:] #xyz contains last 5 indexes of res 
    ret_list = []
    
    
    for x in range(5):
        one = dict()
        one['title'] = rank[x]['title']
        one['url'] = rank[x]['url']
        one['date'] = rank[x]['date']
        one['score'] = rank[x]['score']
        ret_list.append(one)
    
    
    return ret_list





