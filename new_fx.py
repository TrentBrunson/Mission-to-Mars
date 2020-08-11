# --- testing f(x) --- 

# Import Splinter, Pandas and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def mars_hemi(browser):
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # visit the site with the hemisphere photos
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    hemi_html = browser.html
    hemi_soup = soup(hemi_html, "html.parser")


    h3_tag = hemi_soup.find_all('h3')
    h3_tags = []
    for text in h3_tag:
        h3_tags.append(text.get_text())

    # Initialize list of dictionaries
    img_list = []

    # Create for loop to parse data
    # h3 tags refere to each image title
    for item in h3_tags:
        # click on the link
        browser.visit(hemi_url)
        full_img_elem = browser.find_by_text(item, wait_time=1)
        full_img_elem.click()

        html = browser.html
        img_soup = soup(html, 'html.parser')
        # Find the more info button and click that
        try:
            browser.is_text_present('Open', wait_time=1)
            open_elem = browser.links.find_by_partial_text('Open')
            open_elem.click()

        except:
            pass
        
        img_rel_url = img_soup.select_one('img.wide-image').get('src') # do this right 'img.wide-image'???
        # img says look for class img, .wide-image says get
        img_url = f'https://astrogeology.usgs.gov{img_rel_url}'
        img_title = img_soup.find('h2', class_='title').get_text()
        img_dict = {'img_url':img_url, 'title':img_title}
        img_list.append(img_dict)

    return img_list