from src.Site import Site
from src.controllers.SiteController import SiteController

## Config for general use ##

# Base Config #
# Change this per use as you like
SITE = Site.ODA_MAIN
USE_LOCAL_HTML = True



# Derived Config #
# Avoid touching this if you aren't developing
# urls
BASE_URL = ""
STARTING_SECTION = ""

# filepaths
HTML_FOLDER = "supermarket_crawler/"
URLS_TO_STRIP = ""
OUTPUT_FILE = "supermarket_crawler/output_text/"

# site controller
controller: SiteController = None

# set the above based on the current site
if SITE == Site.ODA_MAIN:
	import src.site_config.oda_config as oc
	from src.controllers.OdaController import OdaController
	BASE_URL = oc.BASE_URL
	STARTING_SECTION = oc.STARTING_SECTION
	HTML_FOLDER += oc.HTML_FOLDER
	URLS_TO_STRIP = oc.URLS_TO_STRIP
	OUTPUT_FILE += oc.OUTPUT_FILE

	controller = OdaController