if __name__ == "__main__":
	print("Please run this program as a module: from its parent folder, with command\npython3 supermarket_crawler")
	exit()

from pathlib import Path
import os
import requests
from bs4 import BeautifulSoup
from src.config import *
from src.model.ProductItem import ProductItem

found_products: 'set[ProductItem]' = set()
read_pages: 'set[str]' = set()

def crawl(url: str):
	print(f"crawling {url}")
	filepath = get_filepath_from_url(url)
	print(f"saving url html to {filepath}")
	html = get_page_html(url, filepath)
	soup = BeautifulSoup(html, 'html.parser')
	return read_and_crawl(soup, filepath)

def get_page_html(url: str, filepath: str) -> str:
	html = ""
	if USE_LOCAL_HTML and is_html_already_saved(filepath):
		print("reading html from local file")
		with open(filepath) as f:
			html = f.read()
	else:
		r = requests.get(url)
		html = r.text

		# write this to a file so we can use less requests next time
		make_folders_for_file(filepath)
		print(f'writing to {filepath}')
		with open(filepath, 'w') as f:
			f.write(html)

	return html

def read_and_crawl(soup, filepath: str):
	# guard so we aren't bothering with products on certain non-product pages
	#  this reduces double-checking of products
	if not controller.is_product_page(soup):
		return
	# add all products on the page to found_products
	new_items = controller.get_all_product_items_in_page(soup)
	for item in new_items:
		found_products.add(item)
	# add the page to the set of read pages
	read_pages.add(filepath)

	# find next page to scrape
	next_page_url = find_unchecked_page(soup)
	if next_page_url != None:
		crawl(next_page_url)
	return


def find_unchecked_page(pages: list):
	# TODO
	return None


def is_html_already_saved(filepath: str):
	return Path(filepath).is_file()


def get_filepath_from_url(url: str):
	sections = url.strip('/')
	for to_strip in URLS_TO_STRIP:
		sections = sections.replace(to_strip, "")
	return (HTML_FOLDER + sections).strip('/') + '.html'

def make_folders_for_file(filepath: str):
	sections = filepath.strip('/').split('/')[:-1]
	print(sections)
	print(f"Checking if filepath: {'/'.join(sections)} exists")
	if os.path.exists('/'.join(sections)):
		print("It exists")
		return

	checked_sections = ""
	for sec in sections:
		checked_sections += '/' + sec
		checked_sections = checked_sections.strip('/')
		if not os.path.exists(checked_sections):
			print(f"Making folder {checked_sections}")
			os.mkdir(checked_sections)

def main():

	# TODO: check robots.txt

	# find every product and store it
	crawl(BASE_URL + STARTING_SECTION)

	# print it to a file
	with open(OUTPUT_FILE, 'w') as f:
		f.write("name\tdetails\tprice\turl\n")
		for item in found_products:
			f.write(f"{item.name}\t{item.details}\t{item.price}\t{item.url}\n")

	# navigate through every page


	# hop into a category (left nav bar)
	# get the categories list


	# hop into a subcategory (top nav bar)

	# hop into a subsubcategory (top nav bar)

	# read all the products

	# continue
