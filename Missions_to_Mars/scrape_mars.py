from bs4 import BeautifulSoup
import pandas as pd
#import requests
#import pymongo
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

scraped_data = {}

def scrape():       


     
# NASA MARS   -------------------------------------------------------------------------------------------
    # Setup the Splinter Path with the NASA URL
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Scrape NASA Mars News Site using BS, browser, and HTML
    url_nasa = 'https://redplanetscience.com/'
    browser.visit(url_nasa)
    
    html = browser.html
    soup_nasa = BeautifulSoup(html, 'html.parser')
    
    
    # Use "findall" to Pull the News Title and Paragraph Text (assign to variables)
    nasa_news_title = soup_nasa.find('div', attrs={'class':'content_title'}).get_text()
    print(nasa_news_title)
    
    nasa_news_para = soup_nasa.find('div', attrs={'class':'article_teaser_body'}).get_text()
    print(nasa_news_para)

    scraped_data["nasa_news_title"] = nasa_news_title
    scraped_data["nasa_news_para"] = nasa_news_para

# JPL MARS SPACE IMAGES  ----------------------------------------------------------------------------------
    # Setup the Splinter Path with URL, use BS with Parser
    url_jpl = 'https://spaceimages-mars.com/'
    browser.visit(url_jpl)
    
    html = browser.html
    soup_jpl = BeautifulSoup(html, 'html.parser')
    
    # Pull Featured Image and Make the Link (Base URL + Image URL) (**ASSIGN TO STRING using SRC**)
    jpl_img_path = soup_jpl.find("img", attrs={"headerimage fade-in"})["src"]
    
    featured_image_url = url_jpl+jpl_img_path
    print(featured_image_url)
    
    scraped_data["jpl_img_path"] = jpl_img_path
    
# MARS FACTS  ---------------------------------------------------------------------------------------------
    # Pull URL, Use pd.read to Make Table
    url_facts = 'https://galaxyfacts-mars.com/'
    browser.visit(url_facts)
    
    from tabulate import tabulate
    
    facts_table = pd.read_html(url_facts)
    print(tabulate(facts_table))
    
    facts_df = facts_table[0]
    facts_df.columns = ['Mars-Earth Comparison', 'Mars', 'Earth']
    facts_df
    
    scraped_data[facts_table] = facts_df
    
# MARS HEMISPHERES  ----------------------------------------------------------------------------------------
    # Pull URL, use BS and parser
    url_base_hemi = 'https://marshemispheres.com/'
    browser.visit(url_base_hemi)
    html = browser.html
    
    soup_hemi = BeautifulSoup(html, 'html.parser')
    
    # Use Find_All to retrieve Each Image using For Loop
    hemi_images = soup_hemi.find_all('img', attrs={'class':'thumb'})
    
    #Store Images
    hemisphere_image_urls = []

    # Use ATTRS in loop to return src alt and title, append dictionary
    for finalimages in hemi_images:
        url = finalimages.attrs['src']
        title = finalimages.attrs['alt']
        hemisphere_image_urls.append({'title':title,'img_url':url})

    # Print All Image URLS and Descriptions
    hemisphere_image_urls
    
    scraped_data["hemisphere_image_urls"] = hemisphere_image_urls

    return scraped_data