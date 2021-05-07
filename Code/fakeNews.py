
from openwpm import CommandSequence
from openwpm import TaskManager
from openwpm.utilities import db_utils
from openwpm.SocketInterface import clientsocket
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import random

import csv

# The list of sites that we wish to crawl
NUM_BROWSERS = 2

with open('fakelist.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
sites = [x.strip() for x in content] 

# Loads the default manager params
# and NUM_BROWSERS copies of the default browser params
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

def jiggle_mouse(number_jiggles, **kwargs):
    driver = kwargs['driver']
    for i in xrange(0, number_jiggles):
        x = random.randrange(0, 50)
        y = random.randrange(0, 50)
        action = ActionChains(driver)
        action.move_by_offset(x, y)
        action.perform()

def collect_links_level1(table_name, scheme, **kwargs):
    """ Collect links with `scheme` and save in table `table_name` """
    driver = kwargs['driver']
    manager_params = kwargs['manager_params']
    #visit_id = kwargs['visit_id']
    link_urls = []
    for element in driver.find_elements_by_tag_name('a'):
        try:
            if element.get_attribute("href").startswith(scheme + '://'):
                link_urls.append((element.get_attribute("href"),element.get_attribute("innerHTML")))
        except Exception as e:
            pass
    current_url = driver.current_url

    sock = clientsocket()
    sock.connect(*manager_params['aggregator_address'])

    query = ("CREATE TABLE IF NOT EXISTS %s ("
             "top_url TEXT, link TEXT);" % table_name)
    sock.send(("create_table", query))

    for link,text in link_urls:
        query = (table_name, {
            "top_url": current_url,
            "link": link
            #"linkText": text,
        })
        sock.send(query)
    sock.close()

def collect_links(table_name, scheme, **kwargs):
    """ Collect links with `scheme` and save in table `table_name` """
    driver = kwargs['driver']
    manager_params = kwargs['manager_params']
    crawl_id = kwargs['crawl_id']
    visit_id = kwargs['command'].visit_id
    link_urls = []
    for element in driver.find_elements_by_tag_name('a'):
        try:
            if element.get_attribute("href").startswith(scheme + '://'):
                #link_urls.append((element.get_attribute("href"),element.get_attribute("innerHTML")))
                link_urls.append(element.get_attribute("href"))
        except Exception as e:
            pass
    current_url = driver.current_url

    sock = clientsocket()
    sock.connect(*manager_params['aggregator_address'])

    query = ("CREATE TABLE IF NOT EXISTS %s ("
             "top_url TEXT, link TEXT,"
             "visit_id INTEGER, crawl_id INTEGER);" % table_name)
    sock.send(("create_table", query))

    for link in link_urls:
        query = (table_name, {
            "top_url": current_url,
            "link": link,
            #"linkText": text,
            "visit_id": visit_id,
            "crawl_id": crawl_id
        })
        sock.send(query)
    sock.close()
    
def find_all_iframes(driver, ads_urls):
    print("In here")
    iframes = driver.find_elements_by_xpath("//iframe")
    print(len(iframes))
    for index, iframe in enumerate(iframes):
        try:
            #ads_urls.append((driver.current_url,iframe.get_attribute("src")))
            print(iframe.get_attribute("src"))
            driver.switch_to.frame(index)
            for element in driver.find_elements_by_tag_name('a'):
                print(element.get_attribute("href"))
                #ads_urls.append((driver.current_url,element.get_attribute("href")))
                find_all_iframes(driver,ads_urls)
                driver.switch_to.parent_frame()
        except Exception as e:
            print(e)
            pass

def isAttribtuePresent(element,attribute):
    result = False
    try:
        value = element.get_attribute(attribute);
        if (value != None):
            result = True
    except Exception as e:
        pass

    return result
            
def frame_search(driver, path , indexVal):
    framedict = {}
    for child_frame in driver.find_elements_by_tag_name('iframe'):
        print(child_frame)
        try:
            print(isAttribtuePresent(child_frame,'id'))
            print(isAttribtuePresent(child_frame,'name'))
            print(isAttribtuePresent(child_frame,'title'))
            print(isAttribtuePresent(child_frame,'src'))
            #child_frame_name = child_frame.get_attribute('id')
            framedict[indexVal] = {'framepath' : path, 'children' : {}}
            #xpath = '//iframe[@id="{}"]'.format(child_frame_name)
            xpath = '//iframe['+str(indexVal)+']'
            indexVal = indexVal + 1
            driver.switch_to.frame(driver.find_element_by_xpath(xpath))
            framedict[indexVal]['children'] = frame_search(driver, framedict[indexVal]['framepath']+[indexVal], 0)
            for element in driver.find_elements_by_tag_name('a'):
                print((element.get_attribute("href")))
            driver.switch_to.default_content()
            if len(framedict[indexVal]['framepath'])>0:
                for parent in framedict[indexVal]['framepath']:
                    parent_xpath = '//iframe[@id="{}"]'.format(parent)
                    driver.switch_to.frame(driver.find_element_by_xpath(parent_xpath))
        except Exception as e:
            print(e)
            pass 
    return framedict

def collect_ads(table_name, scheme, **kwargs):
    """ Collect ads with `scheme` and save in table `table_name` """
    driver = kwargs['driver']
    manager_params = kwargs['manager_params']
    crawl_id = kwargs['command'].crawl_id
    visit_id = kwargs['command'].visit_id
    driver.execute_script("document.body.style.transform='scale(0.5)';")
    try:
        for i in range(0, 10):
            x = random.randrange(0, 20)
            y = random.randrange(0, 20)
            action = ActionChains(driver)
            action.move_by_offset(x, y)
            action.perform()
    except Exception as e:
        pass
    try:
        #seq = driver.find_elements_by_tag_name('iframe')
        ads_urls = []
        #find_all_iframes(driver,ads_urls)
        frametree = frame_search(driver, [], 0)
        print(frametree)
    except Exception as e:
        pass


    
# Update browser configuration (use this for per-browser settings)
for i in range(NUM_BROWSERS):
    # Record HTTP Requests and Responses
    browser_params[i]['http_instrument'] = False
    # Record cookie changes
    browser_params[i]['cookie_instrument'] = False
    # Record Navigations
    browser_params[i]['navigation_instrument'] = False
    # Record JS Web API calls
    browser_params[i]['js_instrument'] = False
    # Record the callstack of all WebRequests made
    browser_params[i]['callstack_instrument'] = False
    # Launch only browser 0 headless
    browser_params[i]['display_mode'] = 'headless'

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/Desktop/03272021/'
manager_params['log_directory'] = '~/Desktop/03272021/'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites
for site in sites:

    # Parallelize sites over all number of browsers set above.
    command_sequence = CommandSequence.CommandSequence(
        site, reset=True,
        callback=lambda success, val=site:
        print("CommandSequence {} done".format(val)))

    # Start by visiting the page
    command_sequence.get(sleep=3, timeout=120)
    #command_sequence.run_custom_function(collect_links_level1, ('page_links', 'http'))
    command_sequence.run_custom_function(collect_links_level1, ('fake_level1_1', 'https'), timeout=300)
    manager.execute_command_sequence(command_sequence)
    
# Shuts down the browsers and waits for the data to finish logging
manager.close()


