# Craigslist Web Scraper
 
## Overview 
This application is designed to extract information from Craigslist listings/gigs.
In its current form it will extract the necessary information to calculate the total amount of 
potential earnings someone could make per day if they did all the gigs. In its current state it is 
also only targeting the BOSTON area.


## Pipeline Design
1. Get the total number of gigs/listings in Boston
2. Get the pagination numbers/indexes required to capture all the data (see code for more details)
3. Use Regex to find potential earnings from gigs by extracting potential earnings data from gig titles.
   If earnings information can NOT be found in the title, the URL for that gig is appended to a 
   list named _links_without_price_in_title_.
4. If CONFIG['do_description_scan']=True. A second regex scan will be performed on the descriptions of every 
   gig saved in the links_without_price_in_title variable. NOTE: This step will take some time as it has to load the 
   webpage for each gig in the list. 


## Config
There's a few important configurations that can be adjusted here. 

 **number_of_working_hours_in_a_day**: This setting will 
affect the final calculation in the calculation. 
 This sets the assumed number of working hours in a day. So if you only plan on
 making the daily calculation based off of an 8 hour workday.

**do_description_scan**: If set to true, this will do a scan of the gig/listing descriptions/ 
                         in the event earnings information could not be found in the listing title.

**include_duplicate_gigs**: If set to true, this will include duplicate gigs/listings. 
                            By duplicate listings I'm referring to 
                            listings that are typically identical, but have different 
                            locations listed throughout Boston.

**target_url** You can adjust the target URL to another city or update the existing one if it changes
 

```
CONFIG = {'number_of_working_hours_in_a_day': 24,
          'do_description_scan': False,
          'include_duplicate_gigs': True,
          'target_url': 'https://boston.craigslist.org/search/ggg?is_paid=yes&sort=date'}
```

## Support
* My program is failing on the get_number_of_listings method? 
  * Confirm that the target URL is properly configured in the CONFIG variable. Please test this URL yourself if you 
    continue to have problems
* My final result is significantly different from I expected?
  * If the result is significantly different from what you were expecting you can put the program into 
    debug mode to get a more detailed readout during the regex matches. This is useful incase some bad data is getting 
    included in the calculation. To put the program into debug mode please update the 
    ```logging.basicConfig(stream=sys.stderr, level=logging.INFO)``` to 
   ```logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)``` to 

## Future Improvements
1. Adjust the code so it can be put into debug mode by only needing to adjust the CONFIG variable. 