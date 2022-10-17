

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


# Set executable path 
def scrape_all():
# Initiate headless driver for deployment
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=True)
        news_title, news_paragraph = mars_news(browser)

# Run all scraping functions and store results in a dictionary
        data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres":  mars_hemispheres(browser)
    }
# Stop webdriver and return data
        browser.quit()
        return data

def mars_news(browser):
# Assign the url and instruct the browser to visit it.
# Visit the mars nasa news site
        url = 'https://redplanetscience.com'
        browser.visit(url)
# Optional delay for loading the page
        browser.is_element_present_by_css('div.list_text', wait_time=1)
# Searching for elements with a specific combination of tag (div) and attribute (list_text).
# Telling our browser to wait one second before searching for components. 

# Set up the HTML parser
        html = browser.html
        news_soup = soup(html, 'html.parser')
# Add try/except for error handling
        try:
                slide_elem = news_soup.select_one('div.list_text')

# Assign the title and summary text to variables we'll reference later

# slide_elem.find('div', class_='content_title') # Variable holds a ton of information, so look inside of that information to find this specific data.
# The specific data is in a <div /> with a class of 'content_title'.

# Output is HTML containing the content title and anything else nested inside of that <div />.

# Use the parent element to find the first `a` tag and save it as `news_title`
                news_title = slide_elem.find('div', class_='content_title').get_text()
# news_title

# Once executed, the result is the most recent title published on the website. 
# When the website is updated and a new article is posted, when our code is run again, it will return that article instead.

# Use the parent element to find the paragraph text
                news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
# news_p
# output is the summary of the article.
        except AttributeError:
                return None, None

        return news_title, news_p


# ### Featured Images


# Visit URL
def featured_image(browser):
# Visit URL
        url = 'https://spaceimages-mars.com'
        browser.visit(url)

# Find and click the full image button
        full_image_elem = browser.find_by_tag('button')[1]
        full_image_elem.click()

# Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')
# Add try/except for erroe handling
        try:

# Find the relative image url
                img_url_rel = img_soup.find('img', class_='fancybox-image').get('src') #.get('src') pulls the link to the image.
        except AttributeError:
                return None
#img_url_rel
# Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."

# Use the base URL to create an absolute URL
        img_url = f'https://spaceimages-mars.com/{img_url_rel}' #This variable holds our f-string.
        #This is an f-string, a type of string formatting used for print statements in Python.
#img_url #The curly brackets hold a variable that will be inserted into the f-string when it's executed.
        return img_url


def mars_facts():
# Add try/except for error handling
        try:
# Use 'read_html' to scrape the facts table into a dataframe
                df = pd.read_html('https://galaxyfacts-mars.com')[0]
        except BaseException:
                return None
 # Assign columns and set index of dataframe
        df.columns=['description', 'Mars', 'Earth'] #assign columns to the new DataFrame for additional clarity.
        df.set_index('description', inplace=True) #By using the .set_index() function, we're turning the Description column 
# into the DataFrame's index. inplace=True means that the updated index will remain in place, without having to reassign 
# the DataFrame to a new variable.
#df

# Convert our DataFrame back into HTML, add bootstrap
        return df.to_html(classes="table table-striped")



def mars_hemispheres(browser):
    # Visit URL to moon-hemispheres website
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    hemispheres_soup = soup(html, 'html.parser')
    #finding the tag item common to the  4 images
    items = hemispheres_soup.find_all('div', class_='item')  
    #loop through the 4 items
    for i in range(len(items)):
        hemispheres = {}
        # get link to each full-image resolution
        full_image_link = items[i].find_all('a',class_='itemLink product-item')[0].get('href')
        # visit the new page, where there is the info of each image 
        browser.visit(url+full_image_link)
        html = browser.html
        newpage = soup(html, 'html.parser')
        # get relative url link of image
        image_link = newpage.find_all('div', class_='downloads')[0].find_all('a')[0].get('href')
        # full url image 
        hemispheres['img_url'] = url+image_link
        # get name of the image and saving it in the dictionary
        image_title = newpage.find_all('div', class_='cover')[0].find_all('h2', class_='title')[0].get_text()
        hemispheres['title'] = image_title
        # adding the image info to the list of dictionaries w/all information about the 4 images
        hemisphere_image_urls.append(hemispheres)
        browser.back()
        
    return hemisphere_image_urls
if __name__ == "__main__":

    # If running as script, print scraped data
        print(scrape_all())
# End the automated browsing sessionpyt
#browser.quit()
        




