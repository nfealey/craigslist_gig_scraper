import sys
import logging
from util import get_url_steps_for_pagination
from data_sources.craigslist import get_number_of_listings, gets_data_from_all_gigs, \
                                    find_potential_earnings_using_gig_titles, \
                                    find_potential_earnings_using_gig_descriptions


# Pull this value in from whatever scheduling tool that is typically used
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
CONFIG = {'number_of_working_hours_in_a_day': 24,
          'do_description_scan': True,
          'include_duplicate_gigs': True,
          'target_url': 'https://boston.craigslist.org/search/ggg?is_paid=yes&sort=date'}


def main():
    # Gets the total number of listings or gigs
    number_of_listings = get_number_of_listings(CONFIG['target_url'])

    # Breaks up the total number of listings/gigs into pieces to make pagination easier
    pagination_steps = get_url_steps_for_pagination(number_of_listings)
    titles_and_links = gets_data_from_all_gigs(pagination_steps, CONFIG['include_duplicate_gigs'])

    total_amount_from_titles, links_without_price_in_title = find_potential_earnings_using_gig_titles(titles_and_links, CONFIG['number_of_working_hours_in_a_day'])
    total = total_amount_from_titles

    # If do_description_scan is False, the pipeline will only look for potential earnings in title
    if CONFIG['do_description_scan']:
        total_amount_from_descriptions = find_potential_earnings_using_gig_descriptions(links_without_price_in_title, CONFIG['number_of_working_hours_in_a_day'])
        total = total_amount_from_descriptions + total_amount_from_titles

    print(f'You can make ${total}/day\n')


main()




