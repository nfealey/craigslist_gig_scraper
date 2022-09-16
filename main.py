import csv
import requests
from IPython import embed
from bs4 import BeautifulSoup
import re

def get_number_of_listings(url: str):
    """
    Gets the total number of listings/gigs for this type of search
    """
    listing_page = requests.get(url)
    soup = BeautifulSoup(listing_page.text, "html.parser")
    return int(soup.find(class_='totalcount').string)


def get_all_titles_and_links_from_specific_url(url: str):
    """
    Gets the title and links for a gigs page page

    :param url - URL of target page
    :return data - Dictionary containing the title and href/link

    """
    listing_page = requests.get(url)
    soup = BeautifulSoup(listing_page.text, "html.parser")

    data = {}
    for count, i in enumerate(soup.findAll(class_='result-row')):
        a_tag = i.find(class_='result-title')
        # print(a_tag)

        #data_id=a_tag['data-id']
        title=a_tag.string
        href=a_tag['href']

        data[f'{title}{count}'] = href

    return data


def get_url_steps_for_pagination(number_of_listings: int):
    """
    Returns the steps/index numbers required to capture all of the data
    This is the number that is passed into the URL to properly handle pagination
    """
    steps = []
    for i in range(0,number_of_listings,120):
        steps.append(i)
    return steps


def get_all_listings(steps: list):
    listings_from_all_pages = {}
    for page in steps:
        titles_and_links_from_gigs_page = get_all_titles_and_links_from_specific_url(f'https://boston.craigslist.org/search/ggg?s={page}&is_paid=yes&sort=date')
        listings_from_all_pages = listings_from_all_pages | titles_and_links_from_gigs_page

    return listings_from_all_pages

def main():
    """
    """
    number_of_listings = get_number_of_listings('https://boston.craigslist.org/search/ggg?is_paid=yes&sort=date')
    steps = get_url_steps_for_pagination(number_of_listings) 

    data_from_all_listings = get_all_listings(steps)
    print(data_from_all_listings)
    embed()

    for title, value in data_from_all_listings.items():
        # print(titles) 
        # print(value)

        # Looks for $Number/Week
        per_week = re.search("[$]\d+/week+|[$]\d+/Week+", title)
        if per_week:
            print(title)
            print(per_week)

        #if per_week = re.search("[$]\d+/Day+", title)






    # titles_and_links = get_all_titles_and_links_from_specific_url('https://boston.craigslist.org/search/ggg?is_paid=yes&sort=date')
    
    #for keys, value in titles_and_links.items():
    #    print(keys)
    # print(titles_and_links.keys)
    # write_dict_to_csv(titles_and_links)


main()