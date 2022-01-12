if __name__ == "__main__":
	print("Please run this program as a module: from its parent folder, with command\npython3 supermarket_crawler")
	exit()

from src.config import controller, output_file
from src.helpers.robots import *
from src.helpers.Crawler import Crawler
from src.model.ProductItem import ProductItem

def main():
	# crawl the website, find every product, and store it
	crawler = Crawler(controller)
	crawler.start_crawl()

	# print them all to a file
	with open(output_file, 'w') as f:
		f.write(ProductItem.get_tsv_header())
		for item in crawler.found_products:
			f.write(item.to_tsv())
