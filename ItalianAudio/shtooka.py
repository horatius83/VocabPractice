from selenium import webdriver
from selenium.webdriver.common.by import By
import re

shtooka_net = r'http://shtooka.net/overview.php?lang=ita'

browser = webdriver.Chrome()
browser.get(shtooka_net)

links = [x for x in browser.find_elements(By.XPATH, '//a') if x.get_attribute('href').startswith('http://shtooka.net/listen/ita')]

for(link in links[1:]):
    browser.get(link)
    js_codes = [x.get_attribute('onClick') for x in browser.find_elements(By.XPATH, '//img[@olass="player_mini"]')]
    links = [re.search(r"'(http://[a-zA-z/\.\-0-9]*.ogg)'", x).group(1) for x in js_codes]
    
