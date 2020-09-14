from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--dns-prefetch-disable')
options.add_argument('--no-referrers')
options.add_argument('--disable-gpu')
options.add_argument('--disable-audio')
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')

driver = webdriver.Chrome(executable_path='/Users/lfd/Downloads/chromedriver', chrome_options=options)
driver.get('https://blog.csdn.net/kingzhsh/article/details/100175342')
width = driver.execute_script(
    "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);")
height = driver.execute_script(
    "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
print(width)
print(height)
driver.set_window_size(width + 100, height + 100)
driver.save_screenshot('/Users/lfd/Downloads/shot.png')
driver.close()
