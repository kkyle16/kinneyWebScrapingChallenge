import pandas as pd 
import requests
from bs4 import BeautifulSoup as bs
import os
from splinter import Browser
import time
import re

def init_browser():
    executable_path = {"executable_path": "Firefox\geckodriver.exe"}
    return Browser("firefox", **executable_path, headless=False)

def mars_news():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    results = soup.find_all("div", class_="list_text")
    titles = []
    paragraphs = []
    for result in results:
        title = result.find('div', class_="content_title").text
        paragraph = result.find('div', class_="article_teaser_body").text
        titles.append(title)
        paragraphs.append(paragraph)
    
    news_title = titles[0]
    news_p = paragraphs[0]
    browser.quit()
    return (news_title, news_p)

def mars_feat_img():
    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    results = soup.find_all("article", class_="carousel_item")
    new_result = results[0].find("a")
    img = new_result["data-fancybox-href"]
    featured_img_url = "https://www.jpl.nasa.gov" + img
    browser.quit()
    return featured_img_url

def mars_weather():
    browser = init_browser()
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = bs(html, "html.parser")

    results = soup.find_all("article")
    new_results = results[0].find_all("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    mars_weather = new_results[4].text
    browser.quit()
    return mars_weather

def mars_facts():
    browser = init_browser()
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ["Topic", "Fact"]
    fact_table = df.to_html()
    browser.quit()
    return fact_table

def mars_hemi_imgs():
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    results = soup.find_all("div", class_="item")
    hrefs = []
    for result in results:
        href = result.find("a")
        hrefs.append(href["href"])
    
    re.split("/search/map/Mars/Viking/|_enhanced", hrefs[2])
    url = "https://astrogeology.usgs.gov"
    hemisphere_images_urls = []
    for href in hrefs:
        browser = init_browser()
        browser.visit(url + href)
        time.sleep(1)
        html = browser.html
        soup = bs(html, "html.parser")

        res = re.split("/search/map/Mars/Viking/|_enhanced", href)
        title = res[1]

        results = soup.find("img", class_="wide-image")
        img = results["src"]
        img_url = url + img

        hemisphere_images_urls.append({"title" : title, "img_url" : img_url})
        browser.quit()
    return hemisphere_images_urls

def scrape():
    news = mars_news()[0]
    paragraph = mars_news()[1]
    feat_img = mars_feat_img()
    weather = mars_weather()
    facts_table = mars_facts()
    hemi_imgs = mars_hemi_imgs()

    mars_dict = {"news" : news,
                "paragraph" : paragraph,
                "feat_img": feat_img,
                "weather" : weather,
                "facts_table" : facts_table,
                "hemi_imgs" : hemi_imgs
    }
    # browser.quit()
    return mars_dict