def remove_non_numbers(str1: str):
    """
    Removes non-numbers from strings
    """
    import re
    return re.sub('[^0-9]','', str1)


def get_url_steps_for_pagination(number_of_listings: int):
    """
    Returns the steps/index numbers required to capture all of the data
    This is the number that is passed into the URL to properly handle pagination
    """
    steps = []
    for i in range(0,number_of_listings,120):
        steps.append(i)
    return steps