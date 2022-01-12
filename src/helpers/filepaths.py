from pathlib import Path
import os

from src.config import urls_to_strip, html_folder

def is_html_already_saved(filepath: str):
	"""
	Checks if an html file has already been saved in the html folder.
	"""
	return Path(filepath).is_file()

def get_filepath_from_url(url: str):
	"""
	Turns a url into a filepath, by removing predefined substrings (from
	 config), keeping the '/' chars as directories, and making the last section
	 of the url a file.
	"""
	sections = url.strip('/')
	for to_strip in urls_to_strip:
		sections = sections.replace(to_strip, "")
	return (html_folder + sections).strip('/') + '.html'

def make_folders_for_file(filepath: str):
	"""
	Takes a filepath as a string and makes sure each directory in the path has
	 an existing folder - if not, makes them all.

	e.g. will check for/create all the directories (and not the txt file)
	 in "~/output/files/test.txt"
	"""
	# break up the filepath by / and make each part a folder
	sections = filepath.strip('/').split('/')[:-1]
	# but don't do anything if the path to the last folder already exists
	if os.path.exists('/'.join(sections)):
		return

	# create a folder for each section if one doesn't exist
	checked_sections = ""
	for sec in sections:
		checked_sections += '/' + sec
		checked_sections = checked_sections.strip('/')
		if not os.path.exists(checked_sections):
			os.mkdir(checked_sections)
