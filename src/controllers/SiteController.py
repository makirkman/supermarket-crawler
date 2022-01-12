from typing import List
from src.model.ProductItem import ProductItem

class SiteController:
	"""
	An abstract parent class for controllers which manage site-specific
	 behaviour for the crawler. Most functions are unimplemented, and the
	 behaviour is defined by a child class unique to that site.
	If you want to add a new site to the crawler, you must add an
	 implementation of this Controller for it.
	"""

	base_url = ""
	"""The base url for the chosen site"""
	starting_section = ""
	"""Any string to add to the base_url to make the initial crawl url"""
	robots_url = ""
	"""The url of the site's robots.txt file"""

	def is_product_page(self, soup) -> bool:
		"""
		Checks a page for the assumed characteristics of 'product pages' for
		 a particular site.
		"""
		pass

	def find_next_navigable_links(self, soup, cur_url, urls_to_ignore: set[str]) -> list[str]:
		"""
		Finds all links on the page which will take the crawler further towards
		 an unread product page.
		Should add any links which are not marked to ignore based on the urls
		 to ignore param, to a list.
		Returns the list of unignored links.
		"""
		pass

	def get_all_product_items_in_page(self, soup) -> List[ProductItem]:
		"""
		Finds all product items on a page, and adds their details to discrete
		ProductItem objects, according to the implementation of
		 _create_product_item_from_soup.
		Returns the list of ProductItems.
		"""
		pass

	def _create_product_item_from_soup(self, soup) -> ProductItem:
		"""
		Takes a BeautifulSoup html object holding the information for one
		 product, and extracts the relevant details according to the particular
		 site, to create a ProductItem object for that product.
		Returns the ProductItem.
		"""
		pass

	def _find_unvisited_urls(self, link_list: list[str], urls_to_ignore: set[str]) -> list[str]:
		"""
		Takes a list of links (site internal uris), converts them to urls,
		 and finds any which are not present in the urls_to_ignore set.
		Returns the list of unignored urls (not links).
		"""
		unvisited_urls: list[str] = []
		for link in link_list:
			url = self.base_url.strip('/') + link
			if url not in urls_to_ignore:
				unvisited_urls.append(url)

		return unvisited_urls