import requests
import fnmatch
from src.config import ROBOTS_DISALLOW, ROBOTS_ALL_AGENTS, ROBOTS_AGENTS

def read_robots(robots_url: str) -> set[str]:
	"""
	Parses the robots.txt file from a given url. Looks for the wildcard agent
	 and then finds every url it is disallowed from; then adds these sites to
	 a set, so they can be monitored.
	Returns the set of disallowed urls.
	"""
	robots_disallowed: set[str] = set()
	# get the robots text
	req = requests.get(robots_url)
	robots_text = req.text
	# tag to only include Disallow commands which are for our agent
	check_disallow = False
	for line in robots_text.splitlines():
		# start checking Disallow
		if line.startswith(ROBOTS_ALL_AGENTS):
			check_disallow = True
		if check_disallow and line.startswith(ROBOTS_DISALLOW):
			robots_disallowed.add(line.replace(ROBOTS_DISALLOW, ""))
		# if we reach an agent which is not the wildcard, stop checking Disallow
		if line.startswith(ROBOTS_AGENTS) and not line.startswith(ROBOTS_ALL_AGENTS):
			check_disallow = False

	return robots_disallowed

def is_robots_disallowed(url: str, robots_disallowed: set[str]):
	"""
	Returns a boolean indicating if a given url is in the robots_disallowed set.
	"""
	for r_url in robots_disallowed:
		return fnmatch.fnmatch(url, r_url)