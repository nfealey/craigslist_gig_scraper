from lib2to3.refactor import get_all_fix_names
import requests
from bs4 import BeautifulSoup
import csv

# def write_dict_to_csv(dict_to_write: dict):
#     field_names= ['Title', 'href']
#     with open('export.csv', 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=field_names)
#         writer.writeheader()
#         writer.writerows(dict_to_write)


def get_number_of_listings(url: str):
    """
    Gets the maxium number of listings for this type of search
    """
    listing_page = requests.get(url)
    soup = BeautifulSoup(listing_page.text, "html.parser")
    return int(soup.find(class_='totalcount').string)


def get_all_titles_and_links(url: str):
    listing_page = requests.get(url)
    soup = BeautifulSoup(listing_page.text, "html.parser")

    data = {}
    for i in soup.findAll(class_='result-row'):
        a_tag = i.find(class_='result-title')
        # print(a_tag)

        #data_id=a_tag['data-id']
        title=a_tag.string
        href=a_tag['href']

        data[title] = href

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

def main():
    """
    """
    number_of_listings = get_number_of_listings('https://boston.craigslist.org/search/ggg?is_paid=yes&sort=date')
    print(get_url_steps_for_pagination(number_of_listings))



    # titles_and_links = get_all_titles_and_links('https://boston.craigslist.org/search/ggg?is_paid=yes&sort=date')
    
    #for keys, value in titles_and_links.items():
    #    print(keys)
    # print(titles_and_links.keys)
    # write_dict_to_csv(titles_and_links)


main()