import requests
from bs4 import BeautifulSoup

from src.config import USE_LOCAL_HTML
from src.helpers.filepaths import *
from src.helpers.robots import *
from src.controllers.SiteController import SiteController
from src.model.ProductItem import ProductItem

class Crawler:
	"""
	The main crawler. Contains general crawling behaviour, and uses its
	 stored SiteController for behaviour specific to the sites it is crawling.
	Works with two main functions, which call each other recursively. One
	 gathers the html and data for a url, the other searches that html for links
	 and products, and calls the first one on each link.
	"""

	def __init__(self, controller: SiteController):
		self.controller = controller
		self.found_urls: set[str] = set()
		"""Stores urls we have already found and will visit, so sites aren't double-checked."""

		self.found_products: set[ProductItem] = set()
		"""Store the products found while crawling"""

		self.robots_disallowed: set[str] = read_robots(controller.robots_url)
		"""Stores disallowed urls found in robots.txt"""

	def start_crawl(self):
		"""
		Starts crawling through the website.
		"""
		self._crawl(self.controller.base_url + self.controller.starting_section)

	def _crawl(self, url: str):
		"""
		Gathers the filepath and page html for a given url, and starts
		 the read and crawl process for that html.
		"""
		filepath = get_filepath_from_url(url)
		html = Crawler._get_page_html(url, filepath)
		soup = BeautifulSoup(html, 'html.parser')
		return self._read_and_crawl(url, soup)

	def _get_page_html(url: str, filepath: str) -> str:
		"""
		Gets the html for a given page. If local html is on in the config,
		 will also check for a locally stored version of the file, and use
		 that if it exists instead of downloading the html directly. If not,
		 downloads the html and saves it so it can be used next time.
		"""
		print(f"reading html for {url}, at {filepath}")
		html = ""
		if USE_LOCAL_HTML and is_html_already_saved(filepath):
			print("reading html from local file")
			with open(filepath) as f:
				html = f.read()
		else:
			print("requesting html from url")
			r = requests.get(url)
			html = r.text

			# write this to a file so we can use less requests next time
			make_folders_for_file(filepath)
			with open(filepath, 'w') as f:
				f.write(html)

		return html

	def _read_and_crawl(self, url: str, soup):
		"""
		Searches a given html page for navigable links which have not already
		 been marked for searching; and reads it for products if it is a valid
		 product page; then starts the crawl process on each link.
		"""
		# find all the navigable links on this page
		to_crawl_stack: list[str] = self.controller.find_next_navigable_links(soup, url, self.found_urls)
		# Add all pages which are noted for crawling to found urls so we don't double check them
		[self.found_urls.add(url) for url in to_crawl_stack]

		# if this is a lowest-level product page, add all products to found_products
		if self.controller.is_product_page(soup):
			new_items = self.controller.get_all_product_items_in_page(soup)
			for item in new_items:
				self.found_products.add(item)

		# crawl through the stack
		while len(to_crawl_stack) > 0:
			next_url = to_crawl_stack.pop(0)
			if (not is_robots_disallowed(next_url, self.robots_disallowed)):
				self._crawl(next_url)

