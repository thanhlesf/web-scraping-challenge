# Dependencies
import time
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
from splinter import Browser

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    #
    ### NASA Mars News 
    #

    # Visit url for NASA Mars News -- Latest News
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    time.sleep(2)

    # Parse HTML with Beautiful Soup  
    html = browser.html
    soup = bs(html, "html.parser")
    
    # Get article title and paragraph text
    # article = soup.find("div", class_='list_text')
    # title = article.find("div", class_="content_title").text
    # para = article.find("div", class_ ="article_teaser_body").text

    #  Get article title and paragraph text as title = soup.find('a', target_='_self').text
    title= soup.find('div', class_='list_text').find('div', class_='content_title').text
    para = soup.find('div', class_='list_text').find("div", class_ ="article_teaser_body").text

    #
    ### JPL Mars Space Images
    #

    # Visit url for JPL Featured Space Image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

   #Click on the the button to get to the full image
    image_full=browser.find_by_id('full_image')
    image_full.click()
    time.sleep(1)
    browser.click_link_by_partial_text('more info')

   #find the image url to the full size
    html_image = browser.html
    #Parse with 'html.parser
    soup = bs(html_image, 'html.parser')

   
    # Get featured image url from style tag/scrape url
    img_url=soup.find('img', class_ = 'main_image')['src']
    featured_img_url = "https://www.jpl.nasa.gov" + img_url
    featured_img_url    

    #
    ### Mars Weather
    #

    # Visit Twitter url for latest Mars Weather
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    # Request from weather_url
    twitter_response = req.get(weather_url)

    # Parse HTML with Beautiful Soup
    soup = bs(twitter_response.text, 'html.parser')

    # Find all elements that contain tweets
    latest_tweet = soup.find_all('div', class_='js-tweet-text-container')

    #last tweet is the first elelment of the soup list
    mars_weather = latest_tweet[0].text

    print(mars_weather)

    #
    ### Mars Facts
    #

    # Visit Mars Facts webpage for interesting facts about Mars
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    time.sleep(3)
    html = browser.html

    # Use Pandas to scrape the table containing facts about Mars
    mars_facts =pd.read_html('https://space-facts.com/mars/')[0]

    # Rename columns
    mars_facts.columns = ['Description','Value']

    # Reset Index to be description
    mars_facts.set_index('Description', inplace=True)

    # Use Pandas to convert the data to a HTML table string
    mars_facts = mars_facts.to_html(classes="table.html")
    
    #
    ### Mars Hemispheres
    #

    # Visit USGS webpage for Mars hemispehere images
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    time.sleep(3)
   
    # Parse HTML with Beautiful Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Create dictionary to store titles & links to images
    hemisphere_image_urls = []

    # Retrieve all elements that contain image information
    results = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")

    # Iterate through each image
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    #
    ### Store Data
    #

    # Store data in a dictionary
    mars_data = {
        "title": title,
        "para": para,
        "featured_img_url": featured_img_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
