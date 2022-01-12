
class ProductItem:
	"""
	Represents a single Product and metadata found while crawling any site.
	"""

	def __init__(self, name, details, price, url):
		self.name = name
		"""The name of the product."""
		self.details = details
		"""Additional details about the product - may differ by site."""
		self.price = price
		"""The price of the product - units my differ by site."""
		self.url = url
		"""A direct url link to the product or its page, if one exists."""

	def get_tsv_header():
		"""Get an appropriate header for a tsv file which contains ProductItems."""
		return "name\tdetails\tprice\turl\n"

	def to_tsv(self):
		"""
		Get this ProductItem represented as a tsv line, according to the
		 get_tsv_header function
		"""
		return f"{self.name}\t{self.details}\t{self.price}\t{self.url}\n"

	# define eq and hash so matching products aren't put in product sets
	def __eq__(self, other):
		return self.name == other.name \
			and self.details == other.details \
			and self.price == other.price \
			and self.url == other.url

	def __hash__(self):
		return hash((self.name, self.details, self.price, self.url))