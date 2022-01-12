## Config for general use ##
from src.Site import Site

# Base Config #
# Change this per use as you like
SITE = Site.ODA_MAIN
"""Which website to run the crawler on."""
USE_LOCAL_HTML = True
"""Whether to use locally stored html or make each call fresh."""

ROBOTS_DISALLOW = "Disallow: "
ROBOTS_ALL_AGENTS = "User-agent: *"
ROBOTS_AGENTS = "User-agent: "
# ----------- #


# Derived Config #
# Avoid touching this if you aren't developing

# filepaths
html_folder = "supermarket_crawler/"
urls_to_strip: 'list[str]' = []
output_file = "supermarket_crawler/output_text/"

# site controller
controller = None

# set the above based on the current site
if SITE == Site.ODA_MAIN:
	import src.site_config.oda_config as oc
	from src.controllers.OdaController import OdaController
	html_folder += oc.oda_html_folder
	urls_to_strip += oc.oda_urls_to_strip
	output_file += oc.oda_output_file

	controller = OdaController()
# -------------- #