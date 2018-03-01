
# coding: utf-8

# # Mission to Mars Web Scraping

# In[11]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
import time
import tweepy
import json


# ### NASA Mars News


def scrape():
    url = 'https://mars.nasa.gov/news/?page=0&per_page=15&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    
    response = requests.get(url)
    
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    results = soup.find_all('div',class_='slide')

    title_lst = []
    teaser_lst = []
    for result in results:
        try:
            title = result.find('div',class_='content_title').text
            title = title.strip('\t\r\n')
            teaser = result.find('a').text
            teaser = teaser.strip('\t\r\n')
    
            if(title and teaser):
                title_lst.append(title)
                
                teaser_lst.append(teaser)
        except Exception as e:
                print(e)

    
    
    # ### JPL Mars Space Image
   
    executable_path = {'executable_path': "chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)
    
    browser.find_by_id('full_image').first.click()
    
    time.sleep(5)
    
    soup = BeautifulSoup(browser.html,'html.parser')
    image = soup.find('img',class_='fancybox-image')['src']
    JPL_image = "https://www.jpl.nasa.gov"+image
       
    # ### Mars Weather
  
    consumer_key = "TzLrhwUVMPqB0AeQoDc3lpVOk"
    consumer_secret = "4ZkmmV4ASo4gJzPtMJLlUAiKBU5vWZekAzFXainTHIbJpn03Go"
    access_token = "942094742950518785-7b7scF6iKbikgCaBnMGlH60NIzbwOr1"
    access_token_secret = "KorsLpCIGzsoeCKI52SMkBglukDq6C855sf1BuxiG9LOh"
    

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    
    target = "@MarsWxReport"
    
    weather_tweets = api.user_timeline(target)[0]["text"]

    # ### Mars Facts
    
    url_facts = 'http://space-facts.com/mars/'
    fact_pd = pd.read_html(url_facts, attrs = {'id': 'tablepress-mars'})[0]
    fact_pd = fact_pd.set_index(0).rename(columns={1:"value"})
    del fact_pd.index.name
    mars_facts = fact_pd.to_html()

    # ### Mars Hemisperes

    url_hem = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    exec_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **exec_path, headless=True)
    
    browser.visit(url_hem)
    
    first = browser.find_by_tag('h3')[0].text
    second = browser.find_by_tag('h3')[1].text
    third = browser.find_by_tag('h3')[2].text
    fourth = browser.find_by_tag('h3')[3].text
    
    browser.find_by_css('.thumb')[0].click()
    first_img = browser.find_by_text('Sample')['href']
    browser.back()
    
    browser.find_by_css('.thumb')[1].click()
    second_img = browser.find_by_text('Sample')['href']
    browser.back()
    
    browser.find_by_css('.thumb')[2].click()
    third_img = browser.find_by_text('Sample')['href']
    browser.back()
    
    browser.find_by_css('.thumb')[3].click()
    fourth_img = browser.find_by_text('Sample')['href']
    
    hemisphere_image_urls = [
        {'title': first, 'img_url': first_img},
        {'title': second, 'img_url': second_img},
        {'title': third, 'img_url': third_img},
        {'title': fourth, 'img_url': fourth_img}
    ]
    

    data = {"News_Header":title_lst,"News_Article":teaser_lst,"JPL_Image":JPL_image,"Weather":weather_tweets,"Facts":mars_facts,"Hemispheres":hemisphere_image_urls}

    return data