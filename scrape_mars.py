#Import
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# Scrape
def scrape_all():
    #Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #grab news
    currTitle, newsP = scrape_news(browser)
    marsNews = {
        "currrentNews": currTitle,
        "currentParagraph": newsP,
        "image": scrape_image(browser),
        "facts": scrape_facts(browser),
        "hemispheres": hemi_scrape(browser),
        

    }



    browser.quit()
    return marsNews


# Mars scrape
def scrape_news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    #delay
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #converts to soup
    html=browser.html
    newsSoup = soup(html, 'html.parser')
    slideElem = newsSoup.select_one('div.list_text')
    #title
    currTitle = slideElem.find('div', class_='content_title').get_text()
    #paragraph
    newsP = slideElem.find('div', class_='article_teaser_body').get_text()

    return currTitle, newsP

# Image scrape
def scrape_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    fullimage = browser.find_by_tag('button')[1]
    fullimage.click()
    html = browser.html
    imageSoup = soup(html, 'html.parser')
    imageURL = imageSoup.find('img', class_= 'fancybox-image').get('src')
    imageURL = f'https://spaceimages-mars.com/{imageURL}'
    return imageURL
# Facts scrape
def scrape_facts(browser):
    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)
    html = browser.html
    factsSoup = soup(html, 'html.parser')
    factsLoc = factsSoup.find('div', class_ = "diagram mt-4")
    factsTable = factsLoc.find('table')

    facts = ""
    facts+=str(factsTable)

    return(facts)
    

# Hemispheres scrape
def hemi_scrape(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    hemiURLS = []
    for i in range(4):
        hemiInfo = {}
        #grab elements in the loop
        browser.find_by_css('a.product-item img')[i].click()
        #grab image hrefs
        sample = browser.links.find_by_text('Sample').first
        hemiInfo["img_url"] = sample['href']
        #grab hemi titles
        hemiInfo['title'] = browser.find_by_css('h2.title').text
    
        hemiURLS.append(hemiInfo)
        browser.back()
    
    return hemiURLS


# flask 
if __name__ == "__main__":
    print(scrape_all())