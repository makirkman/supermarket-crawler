import requests
from src.site_config.oda_config import BASE_URL, HTML_FOLDER
# from bs4 import BeautifulSoup

from src.model.ProductItem import ProductItem
from src.controllers.SiteController import SiteController


class OdaController(SiteController):
	# r = requests.get(BASE_URL + STARTING_SECTION)
	# _oda_base_html = r.text
	## TEMP:
	# _oda_base_html = ""
	# with open('test.html') as f:
	# 	_oda_base_html = f.read()



	# def save_all_category_pages(main_page_soup):
	# 	categories = main_page_soup.find_all('li', {'class': 'product-category parent-category'})
	# 	# open up each category to get the link to that category
	# 	for category in categories:
	# 		# get the name of the category
	# 		category_name = category.find('span').string.strip()

	# 		# get the url for the category, and get the html from it
	# 		category_r = requests.get(BASE_URL + category.find('a').get('href'))
	# 		category_html = category_r.text

	# 		# write this to a file so we can dev with less requests
	# 		f = open('./html/categories/' + category_name + '.html', 'w')
	# 		f.write(category_html)
	# 		f.close()

	# def save_all_subcategory_pages(category_page_soup):
	# 	print()

	def is_product_page(soup):
		# TODO
		return True

	def get_all_product_items_in_page(soup):
		items = soup.findAll('div', {'class': 'product-list-item'})

		oda_items = []
		for item in items:
			oda_items.append(OdaController._create_product_item_from_soup(item))

		return oda_items

	def _create_product_item_from_soup(soup):
		name = soup.find('div', {'class': 'name-main wrap-two-lines'})
		# TBD: do we want price for item or by amount?
		price = soup.find('p', {'class': 'price label label-price'})
		# discounted prices have a different class
		# TBD: should we store discounted price or normal?
		alt_price = soup.find('p', {'class': 'price label label-price-discounted'})
		details = soup.find('div', {'class': 'name-extra wrap-one-line'})
		url = soup.find('a', {'class': 'modal-link'})

		# check that each piece of metadata was found before continuing
		#  a missing name is an error, but the rest can be None
		assert name.string, "Found a product which does not have a name - this is not supported behaviour. Please investigate."
		name = name.string.strip()
		if price and price.string:
			price = price.string.strip()
		elif alt_price:
			alt_price.find('span').decompose()
			price = next(alt_price.stripped_strings)
		if details and details.string:
			details = details.string.strip()
		if url:
			url = url.get('href')

		return ProductItem(name, price, details, url)