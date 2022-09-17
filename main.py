import re
import requests
from IPython import embed
from bs4 import BeautifulSoup
from util import remove_non_numbers, get_url_steps_for_pagination

# Pull this value in from whatever scheduling tool that is typically used
CONFIG = {'number_of_working_hours_in_a_day': 24,
          'target_url': 'https://boston.craigslist.org/search/ggg?is_paid=yes&sort=date'}


def get_number_of_listings(url: str):
    """
    Gets the total number of listings/gigs for this type of search
    """
    listing_page = requests.get(url)
    soup = BeautifulSoup(listing_page.text, "html.parser")
    return int(soup.find(class_='totalcount').string)


def get_all_titles_and_links_from_specific_url(url: str, include_duplicates: bool):
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
        #data_id=a_tag['data-id']
        title=a_tag.string
        href=a_tag['href']

        if include_duplicates: 
            data[f'{title} {count}'] = href
        else:
            data[f'{title} {count}'] = href
    return data


def get_all_listings(steps: list, include_duplicates: bool):
    listings_from_all_pages = {}
    for page in steps:
        titles_and_links_from_gigs_page = get_all_titles_and_links_from_specific_url(f'https://boston.craigslist.org/search/ggg?s={page}&is_paid=yes&sort=date', include_duplicates)
        listings_from_all_pages = listings_from_all_pages | titles_and_links_from_gigs_page

    return listings_from_all_pages


def find_potential_earnings_in_a_day(data_from_all_listings, number_of_working_hours_in_a_day: int):
    """
    Examples).
    "Earn $26 to $52 per hour" (Selecting the upper range value of 52 per hour)
    " $30+ Per Hour "  --> $30 per hour

    """

    total_amount = 0
    for title, href in data_from_all_listings.items():
        # Looks for $Number/Week
        per_week = re.search("[$]\d+/week+|[$]\d+/Week+", title)
        per_week_1 = re.search("[$]\d+[ ]Per[ ]Week+|[$]\d+[ ]PER[ ]WEEK+", title)
        per_day_1 = re.search("[$]\d+/day+|[$]\d+/Day+", title)
        per_day_2 = re.search("[$]\d+[ ]Daily", title)
        hourly = re.search("[$]\d+/hour+|[$]\d+/Hour+|[$]\d+/hr+|[$]\d+/HR+|[$]\d+[+]/hr+|[$]\d+[.]\d+/HR+|[$]\d+[ ]/HR+", title)
        per_hour = re.search("[$]\d+[ ]per[ ]hour+|[$]\d+[+][ ]Per[ ]Hour+|[$]\d+[ ]an[ ]hour+|[$]\d+[ ]per[ ]hr+|[$]\d+[ ]hour[ ]", title)
        other = re.search("[$]\d+[ ]", title) # Are values with no /per hour or day.
        if per_week:
            amount_earned_in_one_week = int(per_week.group().split('/')[0][1:])
            one_day_of_earnings = amount_earned_in_one_week/7
            total_amount += one_day_of_earnings
            print(f'title: {title}\n'
                  f'amount_earned_in_one_week: {amount_earned_in_one_week}\n'
                  f'amount_earned_in_one_day: {one_day_of_earnings}\n')
        if per_week_1:
            amount_earned_in_one_week =  int(remove_non_numbers(per_week_1.group().split(' ')[0]))
            one_day_of_earnings = amount_earned_in_one_week/7
            total_amount += one_day_of_earnings
            print(f'title: {title}\n'
                  f'amount_earned_in_one_week: {amount_earned_in_one_week}\n'
                  f'amount_earned_in_one_day: {one_day_of_earnings}\n')
        elif per_day_1:
            one_day_of_earnings = int(per_day_1.group().split('/')[0][1:])
            total_amount += one_day_of_earnings
            print(f'title: {title}\n'
                  f'amount_earned_in_one_day: {one_day_of_earnings}\n')
        elif per_day_2:
            one_day_of_earnings = int(remove_non_numbers(per_day_2.group().split(' ')[0]))
            total_amount += one_day_of_earnings
            print(f'title: {title}\n'
                  f'amount_earned_in_one_day: {one_day_of_earnings}\n')
        elif hourly:
            hourly = int(remove_non_numbers(hourly.group().split('/')[0]))
            one_day_of_earnings = hourly * number_of_working_hours_in_a_day
            total_amount += one_day_of_earnings
            print(f'title: {title}\n'
                  f'amount_earned_in_one_hour: {hourly}\n'
                  f'amount_earned_in_one_day: {one_day_of_earnings}\n')
        elif per_hour:
            hourly = int(remove_non_numbers(per_hour.group().split(' ')[0]))
            one_day_of_earnings = hourly * number_of_working_hours_in_a_day
            total_amount += one_day_of_earnings
            print(f'title: {title}\n'
                  f'amount_earned_in_one_hour: {hourly}\n'
                  f'amount_earned_in_one_day: {one_day_of_earnings}\n')
        elif other:
            # Other captures more of the edge cases (most inaccuracies will be in this section)
            # These are the values that do NOT have the rate like per day or per Hour. They
            # are mostly made of up fixed priced gigs. The code is assuming these can be completed within one day

            # The following ensures we exclude application fees from our calculation
            # Example).    " SURROGATES NEEDED - $500 application BONUS - Earn $50k- $70k+ "
            #              This will be excluded from the calculation
            is_value_an_application_fee = re.search("[$]\d+ application[ ]", title)
            if not is_value_an_application_fee:
                amount = int(remove_non_numbers(other.group()))
                total_amount += amount
                print(f'Other: {title}\n'
                      f'amount: {amount}\n')
    embed()
    return total_amount


def main():
    """
    TODO Add flag for duplicates
    """

    number_of_listings = get_number_of_listings(CONFIG['target_url'])
    pagination_steps = get_url_steps_for_pagination(number_of_listings)

    data_from_all_listings = get_all_listings(pagination_steps, True)

    total_amount = find_potential_earnings_in_a_day(data_from_all_listings, CONFIG['number_of_working_hours_in_a_day'])
    print(f'Total Amount: {total_amount}')


main()