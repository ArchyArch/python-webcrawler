import requests
from sys import argv
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
script, website_address = argv

def get_all(website_address):
    domain = urlparse(website_address)
    r = requests.get(website_address)
    soup = BeautifulSoup(r.text, 'html.parser')
    all_links = list()

    get_slash = soup.find_all("a", href=re.compile("^/"))
    for tag in get_slash:
        all_links.append(domain.scheme + "://" + domain.netloc + tag['href'])

    all_tags = soup.find_all("a", href = re.compile(website_address))
    for tag in all_tags:
        all_links.append(tag['href'])

    return(all_links)

def get_site_title(website_address):
    r = requests.get(website_address)
    soup = BeautifulSoup(r.text, 'html.parser')
    find_title = soup.find_all("title")
    return(find_title[0].string)

def site_map(website_address):
    visited_websites = set()
    websites_to_visit = [website_address]
    site_map = dict()

    while websites_to_visit:
        f = websites_to_visit.pop(0)
        if f in visited_websites:
            continue
        else:
            print("Visiting website: {}".format(f))
            links = get_all(f)
            websites_to_visit.extend(links)
            visited_websites.add(f)
            site_map[f] = {
              'title': get_site_title(f),
              'links': set(links)
            }
    return(site_map)

print(site_map(website_address))
