## Code Documentation

### Procedure
* Install Requirements
* Run scraping script (for level 1, level 2, ..)
* Export the tables from the previous step to csv files for the pre-processing script.
* Execute the pre-processing notebook to generate the files for network analysis


#### Requirements:
This script depends on OpenWPM (https://github.com/mozilla/OpenWPM), please follow the installation process here (https://github.com/mozilla/OpenWPM#installation) and simply execute the fakeNews.py script. Change the list of 'sites' in the script to scrape different levels/websites.

Additional Python libraries:
* tldextract (https://pypi.org/project/tldextract/)
* Pandas (https://pypi.org/project/pandas/)


### Scraping Websites for Hyperlinks using OpenWPM
Please make sure that you have OpenWPM installed (explained below) before running the script. This is a generic hyperlink scraping script which accesses the input file ```fakelist.txt``` that has all the domains that have to be scraped. The script stores all the hyperlinks in a table name ```(fake_level1_1)``` specified in the line (https://github.com/sehgalvibhor/misinformation-networks/blob/3e61e321ea00337bb2fe2d0c320cc1c4ac440a68/Code/fakeNews.py#L1290) of the script. Don't forget to change the table name in case you are doing multi-level analysis.

Run ```python fakeNews.py```
