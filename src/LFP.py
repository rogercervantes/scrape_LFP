import urllib.request
import time
from bs4 import BeautifulSoup

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

	def get_match_details(self, matchHome, matchResult, matchAway):

		'''
		print('***** matchHome *****')
		print(matchHome.text.strip())
		print('***** matchResult *****')
		print(matchResult.text.strip())
		print('***** matchAway *****')
		print(matchAway.text.strip())
		'''
		return matchHome.text.strip() + '-' + matchAway.text.strip()

	def get_event_home_away(self, event_minute_home):
		event_minute_home = event_minute_home.text.strip()
		if event_minute_home != "":
			event_home_away = 'Home'
		else:
			event_home_away = 'Away'

		return event_home_away

	def clear_event_type(self, event_Type):

		# Get de class
		event_Type = event_Type['class']
		# Get second component
		event_Type = event_Type[1]
		# Remove 'eventIcon_' String
		event_Type = event_Type[10:]

		list_Event_Type = {
			'1': 'Goal',
			'2': 'Own Goal',
			'3': 'Penalty Goal',
			'4': 'Missed Penalty',
			'5': 'Yellow Card',
			'6': 'Red Card',
			'7':  'Change'
		}

		# Find value in list. Default return value
		event_Type = list_Event_Type.get(event_Type, event_Type)

		return event_Type

	def clear_event_minute(self, event_home_away, event_minute_home, event_minute_away):

		if event_home_away == "Home":
			event_minute = event_minute_home.text.strip()
		else:
			event_minute = event_minute_away.text.strip()

		return event_minute.replace('\'', '')

	def clear_event_player(self, event_home_away, event_player_home, event_player_away):

		if event_home_away == "Home":
			event_player = event_player_home.text.strip()
		else:
			event_player = event_player_away.text.strip()

		start = event_player.find('(')
		stop = event_player.find(')')
		if len(event_player) > stop:
			event_player = event_player[0: start:] + event_player[stop + 1::]

		return event_player.strip()

	def clear_event_2_player(self, event_home_away, event_player_home, event_player_away, event_type):

		if event_home_away == "Home":
			event_2_player = event_player_home.text.strip()
		else:
			event_2_player = event_player_away.text.strip()

		# If is a event type in list, remove a web bug (second player)
		if event_type in ('Change'):
			start = event_2_player.find('(')
			stop = event_2_player.find(')')
			if len(event_2_player) > stop:
				event_2_player = event_2_player[start + 1:stop]
		else:
			event_2_player = ''

		return event_2_player.strip()

	def get_match_events(self, match_id, match_events):

		# print('***** matchEvents *****')
		# Read features' names?
		if len(self.dataEvents) == 0:
			current_event = []
			current_event.append('match_id')
			current_event.append('minute')
			current_event.append('type')
			current_event.append('home_away')
			current_event.append('player')
			current_event.append('player_2')
			# Store the data
			self.dataEvents.append(current_event)

		match_event = match_events.findAll("div", {"class": "matchEvent"})
		for event in match_event:

			# Get all Divs
			divs = event.findAll('div')

			event_home_away = self.get_event_home_away(divs[1])
			event_minute = self.clear_event_minute(event_home_away, divs[1], divs[3])
			event_type = self.clear_event_type(divs[2])
			event_player = self.clear_event_player(event_home_away, divs[0], divs[4])
			event_2_player = self.clear_event_2_player(event_home_away, divs[0], divs[4], event_type)

			# Create Current Event
			current_event = []
			current_event.append(match_id)
			current_event.append(event_minute)
			current_event.append(event_type)
			current_event.append(event_home_away)
			current_event.append(event_player)
			current_event.append(event_2_player)

			# Store the data
			self.dataEvents.append(current_event)

		return True

	def get_match_lineups(self, matchLineups):

		# print('***** matchLineups *****')

		return True

	def get_match_statistics(self, matchStatistics):

		# print('***** matchStatistics *****')
		#print(matchStatistics)

		return True

	def get_match(self, url_Match):
		#print('***** get_match *****')
		match_Id = url_Match.split(sep=',')[3]
		match_Id = match_Id[0:-4]
		#print('match_Id: ' + match_Id)

		# Download HTML
		html = self.download_html(self.url + '/' + url_Match)
		bs = BeautifulSoup(html, 'html.parser')

		matchHome = bs.find("td", {"id": "matchHome"})
		matchResult = bs.find("td", {"id": "matchResult"})
		matchAway = bs.find("td", {"id": "matchAway"})

		matchEvents = bs.find("div", {"id": "matchEvents"})
		matchLineups = bs.find("div", {"id": "matchLineups"})
		matchStatistics = bs.find("div", {"id": "matchStatistics"})

		self.get_match_details(matchHome, matchResult, matchAway)
		if matchEvents is not None:
			self.get_match_events(match_Id, matchEvents)
		if matchLineups is not None:
			self.get_match_lineups(matchLineups)
		if matchStatistics is not None:
			self.get_match_statistics(matchStatistics)

		return match_Id

	def scrape(self):
		print("Web Scraping of LFP from '" + self.url + self.subdomain + "'")
		print("This process could take roughly 5 minutes.\n")

		# Start timer
		start_time = time.time()

		# Download HTML
		html = self.download_html(self.url + self.subdomain)
		bs = BeautifulSoup(html, 'html.parser')

		# Get the links of each match
		match_links = self.get_match_links(html)

		# Cogemos los X primeros para pruebas
		match_links = match_links[:60]

		# Bucle para todos los partidos
		contador = 0
		num_partidos = len(match_links)
		for match in match_links:
			contador += 1
			print('Processing match number ' + repr(contador) + ' of ' + repr(num_partidos))

			match_link = match.find('a').get('href')
			self.get_match(match_link)

		# Show elapsed time
		end_time = time.time()
		print("\nelapsed time: " +
			str(round(((end_time - start_time) / 60), 2)) + " minutes")


	def dataEvents2csv(self, filename):
		# Overwrite to the specified file.
		# Create it if it does not exist.
		file = open("../csv/" + filename, "wb+")

		# Dump all the data with CSV format
		for i in range(len(self.dataEvents)):
			a = ""
			for j in range(len(self.dataEvents[i])):
				a += self.dataEvents[i][j] + ";"
			file.write(a.encode('utf8'))
			file.write("\n".encode('utf8'))
		file.close()

	def data2csv(self, fileEventsName):
		self.dataEvents2csv(fileEventsName)
