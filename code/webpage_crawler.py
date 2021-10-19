import urllib.request as urlrequest
import urllib.parse
import requests
from googlesearch import search
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

def WebsiteCollection(keyword,result_num = None):
    query = str(keyword)
    my_results_list = []
    for i in search(query,  # The query you want to run
                    tld='com',  # The top level domain
                    lang='en',  # The language
                    # num = 10,     # Number of results per page
                    start=0,  # First result to retrieve
                    stop=result_num,  # Last result to retrieve
                    pause=2.0,  # Lapse between HTTP requests
                    ):
        my_results_list.append(i)

    # print out the results
    print('website:',my_results_list)

    # header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}
    # request = urllib.request.Request(my_results_list[0], headers = header)
    # response = urllib.request.urlopen(request).read
    # page = requests.get(my_results_list[0])
    # soup = BeautifulSoup(page.content, 'html.parser')
    # print('soup content:',soup.prettify())

keyword = 'decision tree'
WebsiteCollection(keyword)

