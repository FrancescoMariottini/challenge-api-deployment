from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
from selenium.webdriver import FirefoxProfile
import time
import random
from random import randint
import re
import requests

def get_search_results(minresults=40):
    """Collect property urls and types by going through the search result pages of new houses and appartments,
    stopping when having reached the minimum number of results and returning a dictionary of {'url1':True/False, 'url2':True/False, ...}.
    True means house. False means apartment. Without argument only the first page is collected (~60 results)"""

    search_results = {}

    result_count = 0
    # set on which page to start the search
    page_number = 1

    options = FirefoxOptions()
    options.add_argument('-headless')
    options.set_preference("dom.webdriver.enabled", False)
    profile = FirefoxProfile('src/scraping/bolzyxyb.heroku')
    profile.set_preference('useAutomationExtension', False)

    driver = Firefox(firefox_binary='usr/lib/firefox/firefox',
                        options=options,
                        firefox_profile=profile)

    driver.implicitly_wait(15)
    
    # start the progress indicator and timeout logic
    start_time = time.monotonic()
    time_spent = 0

    while result_count < minresults and time_spent < 1800:
        # for each loop, scrape one results page of houses and one of appartments
        # the results are added if they are not there yet
        for houselink in get_page_urls(pagenr=page_number,kind="house",drv=driver):
            if houselink not in search_results:
                search_results[houselink] = True
        for apartmentlink in get_page_urls(pagenr=page_number,kind="apartment",drv=driver):
            if apartmentlink not in search_results:
                search_results[apartmentlink] = False
        result_count = len(search_results)
        page_number += 1
        # update progress indicator
        time_spent = time.monotonic() - start_time
        total_time_estimation = 1/(result_count/minresults) * time_spent
        if total_time_estimation > 1800:
            capped_time = 1800
        else:
            capped_time = total_time_estimation
        time_remaining = capped_time - time_spent
        print(f"Finishing in {time_remaining/60:.1f} minutes")
        
    driver.close()
    
    print("Finished")
    return search_results

def get_page_urls(pagenr,kind,drv):
    '''A subroutine scraping links from 1 specific search result page, links to projects are ignored'''
    # initialise the return
    links = []
    # I slow down the frequency of requests to avoid being identified and therefore ban from the site
    time.sleep(random.uniform(1.0, 2.0))
    url=f'https://www.immoweb.be/en/search/{kind}/for-sale?countries=BE&isALifeAnnuitySale=false&page={pagenr}&orderBy=newest'
    drv.get(url)
    html = drv.page_source
    soup = BeautifulSoup(html,'lxml')
    
    for elem in soup.find_all('a', attrs={"class":"card__title-link"}):
        hyperlink = elem.get('href')
        # include in the return if it is not a -project-
        if "-project-" not in hyperlink:
            # cut the searchID off
            hyperlink = re.match("(.+)\?searchId=.+", hyperlink).group(1)
            links.append(hyperlink)
            
    return links



def get_property_value(soup, name):    
    #Looks into every row of the tables
    for elem in soup.find_all('tr'):
        #If it finds an element with text equals to property name it will return it's equivalent value
         if elem.th and re.search(name, str(elem.th.string)):
            if name == "Price":              
                for descendant in elem.td.descendants:
                    if re.search("(\d{5,})\s€", str(descendant)):
                        return int(re.search("(\d{5,})\s€", str(descendant))[1])
            else:
                return elem.td.contents[0].strip()
    #If nothing was found, will return None 
    return None

def get_property_bool(soup, name):
    #Looks into every row of the tables
    for elem in soup.find_all('tr'):
        #If it finds an element with text equals to property name it will return true
        if elem.th and re.search(name, str(elem.th.string)):
            return True
    #If nothing was found, will return false
    return False

def scrap_list(dict_urls): 
    #listing all the property names
    properties = ["hyperlink" ,"locality", "postcode", "house_is", "property_subtype",  "price", "sale", "rooms_number", "area", "kitchen_has", "furnished",    "open_fire", "terrace", "terrace_area", "garden", "garden_area", "land_surface", "land_plot_surface", "facades_number", "swimming_pool_has"]

    #making a dict with all the property names as key and an empty list as value
    dict_dataframe = {}
    for property_name in properties:
        dict_dataframe[property_name] = []

    #scrap each url of the input and put the result into a variable
    url_number = 0
    for key in dict_urls:
        dict_result_scrapping = scrap(key, dict_urls[key])

        #for each property (key) of the scrapping out put, match it with dataframe property. If none exist, just use None
        for key1 in dict_dataframe:
            dict_dataframe[key1].append(dict_result_scrapping[key1])
        url_number += 1
        if url_number % 10 == 0:
            print(f"{time.asctime()}: {url_number} property searched. ")
    return dict_dataframe

def scrap(url, is_house): 
    dictionary = {}
    time.sleep(random.uniform(1.0, 2.0))
    r = requests.get(url) 
    soup = BeautifulSoup(r.content,'html.parser')     

    #for every property, call the right function to get the needed data

    dictionary["hyperlink"] = url
    dictionary["locality"] = url.split("/")[7]
    dictionary["postcode"] = url.split("/")[8]
    dictionary['house_is'] = is_house
    dictionary['property_subtype'] = url.split("/")[5]   
    dictionary['price'] = get_property_value(soup, "Price")     
    dictionary['sale'] = ''
    dictionary['rooms_number'] = get_property_value(soup, 'Bedrooms')
    dictionary['area'] = get_property_value(soup, 'Living area')
    dictionary['kitchen_has'] = get_property_bool(soup, 'Kitchen type')
    dictionary['furnished'] = get_property_bool(soup, 'Furnished')
    dictionary['open_fire'] = get_property_bool(soup, 'Fireplace')
    dictionary['terrace'] = get_property_bool(soup, 'Terrace')
    dictionary['terrace_area'] = get_property_value(soup, 'Terrace surface')
    dictionary['garden'] = get_property_bool(soup, 'Garden')
    dictionary['garden_area'] = get_property_value(soup, 'Garden surface')
    dictionary['land_surface'] = None
    dictionary['land_plot_surface'] = get_property_value(soup, 'Surface of the plot')
    dictionary['facades_number'] = get_property_value(soup, 'Facades')
    dictionary['swimming_pool_has'] = get_property_bool(soup, 'Swimming pool')
    
    return dictionary

