import os
PYPPETEER_CHROMIUM_REVISION = '1263111'

os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION
import time
import datetime
from requests_html import HTMLSession
from mysql.connector import Error
from data_connection import create_data_connection
from insert_news import (execute_query,
                        insert_reporter,
                        get_reporter_id, 
                        insert_category,
                        get_category_id, 
                        insert_news,
                        get_news_id,
                        insert_publisher,
                        get_publisher_id,
                        insert_image)


def process_and_insert_news_data(connection, publisher_website, publisher, title, reporter, news_datetime, category, news_body, images, url):
    
    try:
        # Insert category if not exists
        category_id = insert_category(connection, category, f"{category} সম্পর্কিত") 
        c_id = get_category_id(connection, category)
        
        # Insert reporter if not exists
        reporter_id = insert_reporter(connection, reporter, f"{reporter}@gmail.com")
        r_id = get_reporter_id(connection, reporter)
        
        # Insert publisher as a placeholder (assuming publisher is not provided)
        publisher_id = insert_publisher(connection, publisher, f"{publisher_website}")
        p_id = get_publisher_id(connection, publisher)
        
        # Insert news article
        news_id = insert_news(connection, c_id, r_id, p_id, news_datetime, title, news_body, url)
        n_id = get_news_id(connection, title)
        
        # Insert images
        for image_url in images:
            image_id = insert_image(connection, n_id, image_url)
    
    except Error as e:
        print(f"Error while processing news data - {e}")


def single_news_scraper(url):
    session = HTMLSession()
    try:
        response = session.get(url)
        response.html.render()  # This will download Chromium if not found
        time.sleep(3)

        
        publisher_website = url.split('/')[2]       
        publisher = publisher_website.split('.')[-2]  

        title = response.html.find('h1', first=True).text
        reporter = response.html.find('.contributor-name', first=True).text
        
        datetime_element = response.html.find('time', first=True)
        news_datetime = datetime_element.attrs['datetime']
        category = response.html.find('.print-entity-section-wrapper', first=True).text

        news_body = '\n'.join([p.text for p in response.html.find('p')])

        img_tags = response.html.find('img')
        images = [img.attrs['src'] for img in img_tags if 'src' in img.attrs]
        
        #print(publisher_website, publisher, title, reporter, news_datetime, category, images)
        # process_and_insert_news_data(conn, publisher_website, publisher, title, reporter, reporter_location, datetime, category, images)
        return publisher_website, publisher, title, reporter, news_datetime, category, news_body, images
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()



if __name__ == "__main__":
    conn = create_data_connection()
    if conn is not None:
        
       news_urls = [
            "https://www.prothomalo.com/entertainment/drama/vsfm28d2sj",
            "https://www.prothomalo.com/chakri/chakri-suggestion/txzjp2tm2l",
            "https://www.prothomalo.com/lifestyle/health/qlkk7dbt65"
        ]
        
    for url in news_urls:
            result = single_news_scraper(url)
            if result is not None:
                publisher_website, publisher, title, reporter, news_datetime, category, news_body, images = result
                process_and_insert_news_data(conn, publisher_website, publisher, title, reporter, news_datetime, category, news_body, images, url)
            else:
                print(f"Failed to scrape the news article from URL: {url}")