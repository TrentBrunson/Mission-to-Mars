# Import Splinter, Pandas and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemi(browser),
        "last_modified": dt.datetime.now()
}
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser): # scrape Mars news
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # slide_elem.find("div", class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find more info button and clcik
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try: 
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
    try: 
        # Mars facts: use pandas 'read_html' f(x) to scrape facts into DF
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    # assigning columns and setting index
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    return df.to_html(classes="table table-striped table-dark")

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

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())