from selenium import webdriver
from bs4 import BeautifulSoup
from twilio.rest import Client
import json
import time

numbers_to_alert = [
    '+14438243228',
    '+14434180371'
]

url = 'https://www.nbatopshot.com/packs'
pack_url_specific = 'https://www.nbatopshot.com/listings/pack/a412fa28-1f13-446b-91ca-8f371dc846b1'
test_url = 'https://www.fantasy.tools/'
driver = webdriver.Chrome('./chromedriver')

def get_pack_availability_sleep(sleep_time):
    driver.get(pack_url_specific)
    time.sleep(sleep_time)
    html = driver.page_source
    containsPackNotAvailable = "Pack not available" in html
    return containsPackNotAvailable

def get_topshot_html_sleep(sleep_time):
    driver.get(url)
    time.sleep(sleep_time)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    packs_div = soup.find('div', {'class': 'ThumbnailLayouts__ThumbnailGrid-sc-18xwycr-0 iCffwQ'})
    return hash(str(packs_div))

def get_test_site_html_sleep(sleep_time):
    driver.get(test_url)
    time.sleep(sleep_time)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    packs_div = soup.find('div', {'id': 'stats-projected-table-div'})
    return hash(str(packs_div))

def send_alert():
    with open('credentials.json') as credentials_file:
        credentials = json.load(credentials_file)
        account_sid = credentials['sid']
        auth_token = credentials['auth_token']

        client = Client(account_sid, auth_token)

        for number in numbers_to_alert:
            message = client.messages \
                .create(
                body="Base 2 release 10 might be here! Check now at https://www.nbatopshot.com/listings/pack/a412fa28-1f13-446b-91ca-8f371dc846b1",
                from_='+12027594647',
                to=number
            )

# previous_html_hash = get_test_site_html_sleep(3)
# while(True):
#     new_html_hash = get_test_site_html_sleep(3)
#     if(previous_html_hash == new_html_hash):
#         print("Same website")
#     else:
#         send_alert()
#         print("Different!!!!")

old_status = get_pack_availability_sleep(3)
while(True):
    new_status = get_pack_availability_sleep(3)
    if(old_status == new_status):
        print("Same website")
    else:
        send_alert()
        break # pls dont keep texting me
        print("Different!!!!")
