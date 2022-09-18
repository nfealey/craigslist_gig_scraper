import re
def remove_non_numeric_values(str1: str):
    """
    Removes non-numeric values from strings

    :param str1 - String to remove non-numeric values from.
    """
    return re.sub('[^0-9]','', str1)


def get_url_steps_for_pagination(number_of_listings: int):
    """
    This gets the index's/steps that are to be passed into the URL in order to paginate capturing all the
    listings

    :param number_of_listings: Total number of listings/gigs
    :return list of all the "steps"/index. These steps will be passed into the URL on each interation
           to capture every page with all the gigs/listings

    """
    steps = []
    for i in range(0, number_of_listings, 120):
        steps.append(i)
    return steps


def extract_one_day_of_earnings_from_text(text: str, number_of_working_hours_in_a_day: int):
    """
    Takes in a string and determines what the potential earning for one day of work is for the specified gig.
    Uses regex to determine what the rate for potential earnings are.

    For example). If the earnings are written as $1500/Week
                  The potential earnings per day will be 1500/7 = 214

    :param text- String to look for potential earning values. This will be either a gig's title or description text
    :param number_of_working_hours_in_a_day - Number of working hours in a day.
                                              Example). Do you only want to work an 8 hour work day or 24hr?
    :return int/string: Integer of potential earnings for specific gig (one day of work).
                        Will return 'x' if text does not make any matches

    """
    per_week = re.search('[$]\d+/week+|[$]\d+/Week+', text)
    per_week_1 = re.search('[$]\d+[ ]Per[ ]Week+|[$]\d+[ ]PER[ ]WEEK+', text)
    per_day_1 = re.search('[$]\d+/day+|[$]\d+/Day+', text)
    per_day_2 = re.search('[$]\d+[ ]Daily', text)
    hourly = re.search(
        '[$]\d+/hour+|[$]\d+/Hour+|[$]\d+/hr+|[$]\d+/HR+|[$]\d+[+]/hr+|[$]\d+[.]\d+/HR+|[$]\d+[ ]/HR+|[$]\d+[+]/HR+', text)
    per_hour = re.search(
        '[$]\d+[ ]per[ ]hour+|[$]\d+[+][ ]Per[ ]Hour+|[$]\d+[ ]an[ ]hour+|[$]\d+[ ]per[ ]hr+|[$]\d+[ ]hour[ ]', text)
    other = re.search('[$]\d+[,]\d+|[$]\d+', text)  # Are values with no /per hour or day.
    if per_week:
        amount_earned_in_one_week = int(per_week.group().split('/')[0][1:])
        one_day_of_earnings = amount_earned_in_one_week / 7

        print(f'title: {text}\n'
              f'amount_earned_in_one_week: {amount_earned_in_one_week}\n'
              f'amount_earned_in_one_day: {one_day_of_earnings}\n')
        return one_day_of_earnings
    if per_week_1:
        amount_earned_in_one_week = int(remove_non_numeric_values(per_week_1.group().split(' ')[0]))
        one_day_of_earnings = amount_earned_in_one_week / 7
        print(f'title: {text}\n'
              f'amount_earned_in_one_week: {amount_earned_in_one_week}\n'
              f'amount_earned_in_one_day: {one_day_of_earnings}\n')
    elif per_day_1:
        one_day_of_earnings = int(remove_non_numeric_values(per_day_1.group().split('/')[0]))
        print(f'title: {text}\n'
              f'amount_earned_in_one_day: {one_day_of_earnings}\n')
        return one_day_of_earnings
    elif per_day_2:
        one_day_of_earnings = int(remove_non_numeric_values(per_day_2.group().split(' ')[0]))
        print(f'title: {text}\n'
              f'amount_earned_in_one_day: {one_day_of_earnings}\n')
        return one_day_of_earnings
    elif hourly:
        hourly = int(remove_non_numeric_values(hourly.group().split('/')[0]))
        one_day_of_earnings = hourly * number_of_working_hours_in_a_day
        print(f'title: {text}\n'
              f'amount_earned_in_one_hour: {hourly}\n'
              f'amount_earned_in_one_day: {one_day_of_earnings}\n')
        return one_day_of_earnings
    elif per_hour:
        hourly = int(remove_non_numeric_values(per_hour.group().split(' ')[0]))
        one_day_of_earnings = hourly * number_of_working_hours_in_a_day
        print(f'title: {text}\n'
              f'amount_earned_in_one_hour: {hourly}\n'
              f'amount_earned_in_one_day: {one_day_of_earnings}\n')
        return one_day_of_earnings
    elif other:
        # Other captures more of the edge cases (most inaccuracies will be in this section)
        # These are the values that do NOT have the rate like per day or per Hour. They
        # are mostly made of up fixed priced gigs. The code is assuming these can be completed within one day

        # The following ensures we exclude application fees from our calculation
        # Example).    " SURROGATES NEEDED - $500 application BONUS - Earn $50k- $70k+ "
        #              This will be excluded from the calculation
        is_value_an_application_fee = re.search('[$]\d+ application[ ]', text)
        if not is_value_an_application_fee:
            amount = int(remove_non_numeric_values(other.group()))
            print(f'Other: {text}\n'
                  f'amount: {amount}\n')
            return amount
    else:
        # Returns X when the item is a leftover or if no match occurs. This is important for the first pass through
        # As all the necessary information might not be included in the title.
        # In the first pass (title check) the 'x' being returned indicates that this gig/listing will
        # require a description scan
        return 'x'