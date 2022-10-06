#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager



# In[2]:


# Set up Splinter
#executable_path = {'executable_path': ChromeDriverManager().install()}
#browser = Browser('chrome', **executable_path, headless=False)


# In[ ]:






# In[3]:


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    # Run all scraping functions and store results in dictionary

    # ## JPL Space Images Featured Image

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    # ## Mars Facts


    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        mars_df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    mars_df.columns=['Description', 'Mars', 'Earth']
    mars_df.set_index('Description', inplace=True)
        # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    #img_url_rel = img_soup.find('img', class_='wide-image').get('src')
    #img_url_rel
    slide_elem = img_soup.select_one('div')
# print (slide_elem)


    # title_rel = slide_elem.find('div', class_='title').get_text()
    titles= slide_elem.find_all('div', class_='description')
    #print(titles)

    # In[18]:


    #full_image_elem = browser.find_by_tag('a')[4]
    #4 - Cerberus Hemisphere
    #6 - schiaparelli
    #8- Syrtis Major
    #10 - Valles Marineris
    #full_image_elem.click()


    # In[20]:
    for i  in range(4):
        img_url_rel = img_soup.find_all('img', class_='thumb')[i].get('src')
        img_url = f'https://marshemispheres.com/{img_url_rel}'
        img_title = titles[i].h3.text
        img_dict = {'img_url': f'{img_url}', 'title': img_title}
        hemisphere_image_urls.append(img_dict)


    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": img_url,
        "facts": mars_df.to_html(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_image_urls
    }
    # Stop webdriver and return data
    browser.quit()
  #  print(data)
    return data


if __name__ == "__main__":
# If running as script, print scraped data
    print(scrape_all())






