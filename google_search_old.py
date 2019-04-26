from bs4 import BeautifulSoup
import urllib, urllib2
import socket
import random
import types
import sys
import time

# SOCKS5_PROXY_HOST = '127.0.0.1' 
# SOCKS5_PROXY_PORT = 1090
# default_socket = socket.socket
# socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY_HOST, SOCKS5_PROXY_PORT) 
# socket.socket = socks.socksocket

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
 (KHTML, like Gecko) Element Browser 5.0', \
 'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
 Version/6.0 Mobile/10A5355d Safari/8536.25', \
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
 Chrome/28.0.1468.0 Safari/537.36', \
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']

def randomSleep():
    sleeptime =  random.randint(1, 3)
    time.sleep(sleeptime)


def search(queryStr):
    try:
        queryStr = urllib2.quote(queryStr)
    except:
        queryStr = urllib2.quote(queryStr.encode('utf-8', 'ignore'))
    url = 'https://www.google.com/search?q=%s' % queryStr
    print queryStr
    request = urllib2.Request(url, None)
    index = random.randint(0, 9)
    user_agent = user_agents[index]
    request.add_header('User-agent', user_agent)
    try:
        response = urllib2.urlopen(request,timeout=10)
        html = response.read()
    except:
        print "connection error"
        return ""
    return html

def extractSearchResults(html):
    soup = BeautifulSoup(html)
    results=[]
    div = soup.find('div', id  = 'search')
    if (type(div) != types.NoneType):
        lis = div.findAll('div', {'class': 'g'})
        if(len(lis) > 0):
            for li in lis:
                out={}
                h3 = li.find('h3', {'class': 'r'})
                if h3==None:
                    continue
                out["name"]=h3.getText()
                if(type(h3) == types.NoneType):
                    continue

                link = h3.find('a')
                if (type(link) == types.NoneType):
                  continue 
                out["url"]=link['href']

                span = li.find('span', {'class': 'st'})
                if (type(span) != types.NoneType):
                    content = span.getText()
                    out["snippet"]=content
                    # print content
                results.append(out)
    return results


def google_web_search(t_keywords):
    html=search(t_keywords)
    res=extractSearchResults(html)
    if res==[]:
        sys.stderr.write("..... search again ...") 
        randomSleep()
        html=search(t_keywords)
        res=extractSearchResults(html)
        return res
    return res

if __name__ == '__main__':
    for i in ["F668","F660","RT-N66U","ZXR10"]:
        print google_web_search(i)
