'''Mars Scraping'''



import pandas as pd

import requests



from selenium import webdriver

from splinter import Browser

from bs4 import BeautifulSoup



  

def scrape():

    """Contains all the scraping of various sites

    for Mars info

    """



    #make a dict to store everything

    mars_dict = {}



    '''NASA Mars News'''



    #Mars News url

    news_url = 'https://mars.nasa.gov/news'



    #browser setup

    executable_path = {'executable_path': 'chromedriver.exe'}

    browser = Browser('chrome')

    browser.visit(news_url)



    #create BeautifulSoup object and parse

    soup = BeautifulSoup(browser.html, 'html.parser')



    #find the latest news title and remove newline characters

    news_title = soup.find(class_='content_title').get_text(strip=True)



    #find the latest news paragraph text and remove newline characters

    news_p = soup.find(class_='rollover_description_inner').get_text(strip=True)



    #add to dict

    mars_dict['news_title'] = news_title

    mars_dict['news_p'] = news_p





    '''JPL Mars Space Images - Featured Image'''



    #JPL Mars images url

    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    img_base_url = 'https://www.jpl.nasa.gov'



    #retrieve

    result = requests.get(img_url)



    #make it text

    html = result.text



    #create BeautifulSoup object and parse

    soup = BeautifulSoup(html, 'html.parser')

    

    #select the part that contains the image urls

    fancy_box = soup.select('li.slide a.fancybox')



    #make a list of just the data-fancybox-hrefs

    img_list = [i.get('data-fancybox-href') for i in fancy_box]



    #combine the base url with the first img url

    featured_image_url = img_base_url + img_list[0]   



    #add to dict

    mars_dict['featured_image_url'] = featured_image_url



    '''Mars Weather'''

    

    #scrape the latest Mars weather tweet from the Mars Weather twitter account

    twit_url = 'https://twitter.com/marswxreport?lang=en'

    result = requests.get(twit_url)

    

    #make it text

    html = result.text



    #create BeautifulSoup object and parse

    soup = BeautifulSoup(html, 'html.parser')



    #get the weather from the newest tweet

    mars_weather = soup.find(class_='tweet-text').get_text()

    

    #add to dict

    mars_dict['mars_weather'] = mars_weather



    '''Mars Facts'''



    #Mars space facts url

    facts_url = 'https://space-facts.com/mars/'



    #use Pandas to scrape the planet profile

    profile = pd.read_html(facts_url)

    

    #make a df

    profile_df = profile[0]



    #set index to the 0 column

    profile_df.set_index(0, inplace=True)



    #delete the index name

    profile_df.index.names = [None]



    #delete the column name

    profile_df.columns = ['']



    #convert the data to a HTML table string

    html_table = profile_df.to_html()



    #clean it up

    html_table = html_table.replace('\n', '')



    #add to dictt

    mars_dict['html_table'] = html_table



    '''Mars Hemispheres'''



    #USGS url

    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'



    #visit

    browser.visit(usgs_url)



    #create BeautifulSoup object and parse

    soup = BeautifulSoup(browser.html, 'html.parser')



    #get the 4 hemispheres (class of 'item')

    hemispheres = soup.select('div.item')



    #Loop through each hemisphere



    hemisphere_image_urls = []



    for h in hemispheres:

        title = (h.find('h3').text).replace(' Enhanced', '')

          

        #click the hemisphere

        browser.click_link_by_partial_text(title)



        #make new soup of that page

        soup = BeautifulSoup(browser.html, 'html.parser')



        #find the full image

        full = soup.find('a', text='Sample')



        #get the img url

        img_url = full['href']



        #make a dict and append to the list

        hemisphere_image_urls.append({'title': title, 'img_url': img_url})



        #go back 

        browser.back()



    #close browser

    browser.quit()    



    #add to dict

    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls



    return mars_dict