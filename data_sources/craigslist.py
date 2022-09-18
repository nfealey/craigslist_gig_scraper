import time
import logging
import requests
from typing import Tuple
from bs4 import BeautifulSoup
from util import extract_one_day_of_earnings_from_text


def get_number_of_listings(url: str):
    """
    Gets the total number of listings/gigs for this type of search
    """
    listing_page = requests.get(url)
    soup = BeautifulSoup(listing_page.text, "html.parser")
    return int(soup.find(class_='totalcount').string)


def get_all_titles_and_links_from_specific_url(url: str, include_duplicates: bool):
    """
    Gets the title and links for a gigs page

    :param url - URL of target page
    :param include_duplicates - Flag on whether duplicate listings/gigs should be included
    :return data - Dictionary containing the title and href/link

    """
    listing_page = requests.get(url)
    soup = BeautifulSoup(listing_page.text, "html.parser")

    data = {}
    for count, i in enumerate(soup.findAll(class_='result-row')):
        a_tag = i.find(class_='result-title')
        title = a_tag.string
        href = a_tag['href']

        if include_duplicates:
            data[f'{title} {count}'] = href
        else:
            data[f'{title}'] = href
    return data


def gets_data_from_all_gigs(steps: list, include_duplicates: bool):
    """
    Gets all titles and links from all listings in Boston
    """
    listings_from_all_pages = {}
    for page in steps:
        titles_and_links_from_gigs_page = get_all_titles_and_links_from_specific_url(f'https://boston.craigslist.org/search/ggg?s={page}&is_paid=yes&sort=date', include_duplicates)
        listings_from_all_pages = listings_from_all_pages | titles_and_links_from_gigs_page

    return listings_from_all_pages


def find_potential_earnings_using_gig_titles(data_from_all_listings: Tuple, number_of_working_hours_in_a_day: int):
    """
    Finds the potential_earnings for completing all boston gigs in one day by extracting data from the
    titles of listings/gigs.

    :param data_from_all_listings - Title and links for all the listings/gigs
    :param number_of_working_hours_in_a_day - Number of working hours in a day
    """
    list_of_links_that_dont_have_price_in_title = []

    total_amount = 0
    for title, href in data_from_all_listings.items():
        logging.info(href)
        one_day_of_earnings = extract_one_day_of_earnings_from_text(title, number_of_working_hours_in_a_day)
        if isinstance(one_day_of_earnings, int):
            total_amount += one_day_of_earnings
        else:
            # This adds the links where titles did not have any matches with the regex checks. This is so we
            # Can do a second pass with a deeper inspection on the descriptions of the page at a later time.
            list_of_links_that_dont_have_price_in_title.append(href)

    return total_amount, list_of_links_that_dont_have_price_in_title


def find_potential_earnings_using_gig_descriptions(links: list, number_of_working_hours_in_a_day: int):
    """
    Finds the potential_earnings for completing all boston gigs in one day by extracting data from the
    descriptions of listings/gigs.

    :param links - List of gig links that are to be loaded for description extraction
    :param number_of_working_hours_in_a_day - Number of working hours in a day

    """
    total_amount = 0
    for link in links:
        logging.info(link)
        try:
            # Added a 1-second delay so the code doesn't hammer Craigslists website
            time.sleep(1)
            listing_page = requests.get(link)

            soup = BeautifulSoup(listing_page.text, "html.parser")
            description = soup.find(id='postingbody').text

            one_day_of_earnings = extract_one_day_of_earnings_from_text(description, number_of_working_hours_in_a_day)
            if isinstance(one_day_of_earnings, int):
                total_amount += one_day_of_earnings

        except:
            print(f'URL Failed to load: {link}')
            continue

    return total_amount
