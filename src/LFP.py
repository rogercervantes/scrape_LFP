#import urllib2
import urllib.request
#import urllib.error
#import re
import time
from bs4 import BeautifulSoup
#from dateutil import parser
from geopy.geocoders import Yandex
#from reason_classifier import ReasonClassifier

class LFP_Scraper():

	# Inicializamos la classe
	def __init__(self):
		self.url = "https://es.fcstats.com"
		self.subdomain = "/partidos,primera-division-espana,19,1.php"

		self.dataEvents = []

	# Descargamos la página seleccionada
	def download_html(self, url):
		response = urllib.request.urlopen(url)
		html = response.read()
		return html

	def get_match_links(self, html):

		# Get link for all match
		bs = BeautifulSoup(html, 'html.parser')
		match_Links = bs.findAll("td", {"class": "matchResult"})

		return match_Links

	def get_match_Details(self, matchHome, matchResult, matchAway):

		print('***** matchHome *****')
		print(matchHome.text.strip())
		print('***** matchResult *****')
		print(matchResult.text.strip())
		print('***** matchAway *****')
		print(matchAway.text.strip())

		return matchHome.text.strip() + '-' + matchAway.text.strip()

	def get_match_Events(self, match_Id, matchEvents):

		print('***** matchEvents *****')

		matchEvent = matchEvents.findAll("div", {"class": "matchEvent"})
		for event in matchEvent:

			# Add match Info
			currentEvent = []
			currentEvent.append(match_Id)

			divs = event.findAll('div')
			for div in divs:
				currentEvent.append(div.text.strip())

			print('**')
			print(currentEvent)
			# Store the data
			self.dataEvents.append(currentEvent)

		return True

	def get_match_Lineups(self, matchLineups):

		print('***** matchLineups *****')
		#print(matchLineups)

		return True

	def get_match_Statistics(self, matchStatistics):

		print('***** matchStatistics *****')
		#print(matchStatistics)

		return True

	def get_match(self, url_Match):
		# Download HTML
		html = self.download_html(self.url + '/' + url_Match)
		bs = BeautifulSoup(html, 'html.parser')

		matchHome = bs.find("td", {"id": "matchHome"})
		matchResult = bs.find("td", {"id": "matchResult"})
		matchAway = bs.find("td", {"id": "matchAway"})

		matchEvents = bs.find("div", {"id": "matchEvents"})
		matchLineups = bs.find("div", {"id": "matchLineups"})
		matchStatistics = bs.find("div", {"id": "matchStatistics"})

		match_Id = self.get_match_Details(matchHome, matchResult, matchAway)
		self.get_match_Events(match_Id, matchEvents)
		self.get_match_Lineups(matchLineups)
		self.get_match_Statistics(matchStatistics)

		return True

	def scrape(self):
		print("Web Scraping of LFP from '" + self.url + self.subdomain + "'")
		print("This process could take roughly XXX minutes.\n")

		# Start timer
		start_time = time.time()

		# Download HTML
		html = self.download_html(self.url + self.subdomain)
		bs = BeautifulSoup(html, 'html.parser')

		# Get the links of each match
		match_links = self.get_match_links(html)

		# Prueba para el primer partido, después lo hacemos para todos
		match = match_links[1]
		# Bucle para todos los partidos
		# for match in match_links:

		match_link = match.find('a').get('href')
		self.get_match(match_link)

		# Show elapsed time
		end_time = time.time()
		print("\nelapsed time: " +
			str(round(((end_time - start_time) / 60), 2)) + " minutes")


	def dataEvents2csv(self, filename):
		# Overwrite to the specified file.
		# Create it if it does not exist.
		file = open("../csv/" + filename, "w+")

		# Dump all the data with CSV format
		for i in range(len(self.dataEvents)):
			for j in range(len(self.dataEvents[i])):
				file.write(self.dataEvents[i][j] + ";");
			file.write("\n");


	def data2csv(self, fileEventsName):
		self.dataEvents2csv(fileEventsName)
