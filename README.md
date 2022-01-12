# Supermarket Crawler

A web crawler which walks through product websites and gathers basic metadata about every product.

## Use
Set Config files as you prefer (which site to crawl, and whether to use locally stored html if the program has been run on it before)
Run `python3 supermarket_crawler` from a parent folder.

Product details are found in a tsv file in output_text/<WEBSITE>.tsc

## Currently Implemented Supermarket sites
* Oda (Main)


### How to add more sites
To add new functionality for a new site, you need to add a small set of defined functions and variables defining how to access the new site, and how to recognise its products and next pages. These will be automatically read in by the program once you add them to config.py.

The steps are:

* Add a unique implementation of the SiteController for the new site under controllers (look at OdaController for inspiration), and implement every function
* Add a value for the site to the Site enum
* Add a config file in the site_config folder
* Add a check and your new variables/class to the derived section of config.py (look at how oda_config is imported and used)
