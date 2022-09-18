import re
import requests
from IPython import embed
from bs4 import BeautifulSoup
from util import get_url_steps_for_pagination, extract_one_day_of_earnings_from_text
import time

# Pull this value in from whatever scheduling tool that is typically used
CONFIG = {'number_of_working_hours_in_a_day': 24,
          'target_url': 'https://boston.craigslist.org/search/ggg?is_paid=yes&sort=date',
          'include_duplicate_gigs': False}


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
        title=a_tag.string
        href=a_tag['href']

        if include_duplicates: 
            data[f'{title} {count}'] = href
        else:
            data[f'{title} {count}'] = href
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





def find_potential_earnings_using_gig_titles(data_from_all_listings, number_of_working_hours_in_a_day: int):
    """
    Examples).
    "Earn $26 to $52 per hour" (Selecting the upper range value of 52 per hour)
    " $30+ Per Hour "  --> $30 per hour

    """
    list_of_links_that_dont_have_price_in_title = []

    total_amount = 0
    for title, href in data_from_all_listings.items():
        one_day_of_earnings = extract_one_day_of_earnings_from_text(title, number_of_working_hours_in_a_day)
        if isinstance(one_day_of_earnings, int):
            total_amount += one_day_of_earnings
        else:
            # This adds the links where titles did not have any matches with the regex checks. This is so we
            # Can do a second pass with a deeper inspection on the descriptions of the page at a later time.
            list_of_links_that_dont_have_price_in_title.append(href)

    return total_amount, list_of_links_that_dont_have_price_in_title


def find_potential_earnings_using_gig_descriptions(links: list, number_of_working_hours_in_a_day: int):
    total_amount = 0
    for link in links:
        try:
            time.sleep(1)
            listing_page = requests.get(link)

            soup = BeautifulSoup(listing_page.text, "html.parser")

            # section_tag = soup.find(id='postingbody').text
            description = soup.find(id='postingbody').text

            one_day_of_earnings = extract_one_day_of_earnings_from_text(description, number_of_working_hours_in_a_day)
            if isinstance(one_day_of_earnings, int):
                total_amount += one_day_of_earnings

        except:
            print(f'URL Failed to load: {link}')
            continue

    return total_amount


def main():
    """
    TODO Add flag for duplicates
    """
    # Gets the total number of listings or gigs
    number_of_listings = get_number_of_listings(CONFIG['target_url'])

    # Breaks up the total number of listings/gigs into pieces to make pagination easier
    pagination_steps = get_url_steps_for_pagination(number_of_listings)

    titles_and_links = gets_data_from_all_gigs(pagination_steps, CONFIG['include_duplicate_gigs'])

    total_amount_from_titles, list_of_links_that_dont_have_price_in_title = find_potential_earnings_using_gig_titles(titles_and_links, CONFIG['number_of_working_hours_in_a_day'])
    print(f'Total Amount Earned from titles: {total_amount_from_titles}')

    total_amount_from_descriptions = find_potential_earnings_using_gig_descriptions(list_of_links_that_dont_have_price_in_title, CONFIG['number_of_working_hours_in_a_day'])
    total = total_amount_from_descriptions + total_amount_from_titles

    print(f'Total Amount Earned from titles: {total_amount_from_titles}')
    print(f'Total potential earnings for all gigs in Boston in one day: {total}')





main()


# Features to add
# Try Catches to ensure no numbers exist
#

# TODO
# Add remove non numbers from every imported value





