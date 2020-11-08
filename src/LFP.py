import urllib.request
import time
from bs4 import BeautifulSoup

class LFP_Scraper():

	# Inicializamos la classe
	def __init__(self):
		self.url = "https://es.fcstats.com"
		self.subdomain = "/partidos,primera-division-espana,19,1.php"

		self.dataMatches = []
		self.dataEvents = []
		self.dataLineups = []

	# Descargamos la página seleccionada
	def download_html(self, url):
		response = urllib.request.urlopen(url)
		html = response.read()
		return html

	# Obtenemos la lista de partidos
	def get_match_links(self, html):

		# Get link for all match
		bs = BeautifulSoup(html, 'html.parser')
		match_Links = bs.findAll("td", {"class": "matchResult"})

		return match_Links

	def get_match_cols(self, bs, url_Match):

		cols_general = ['ID', 'Local', 'Visitante', 'Liga', 'Temporada',
						'Fecha-hora', 'Árbitro', 'Estadio', 'Sistema_Local', 'Sistema_Visitante']
		cols_goles = ['Goles_Local', 'Goles_Visitante', 'Goles_1er_tiempo_Local',
					  'Goles_1er_tiempo_Visitante']

		# Podemos obtener los nombres de las columnas a partir del primer partido:
		matchStatistics = bs.find("div", {"id": "matchStatistics"})
		stats = matchStatistics.findAll("div")

		cols_stats = []
		for i in range(1, 64, 4):
			cols_stats.append(stats[i].findAll("div")[1].text.strip().replace(' ','_').replace('[%]','(por)'))

		# Nos interesa que cada estadística se guarde por separado LOCAL y VISITANTE:
		cols_lv = []
		for col in cols_stats:
			cols_lv.append(col + '_Local')
			cols_lv.append(col + '_Visitante')

		cols = cols_general + cols_goles + cols_lv

		# Store the data
		self.dataMatches.append(cols)

	def get_match_details(self, match_Id, bs, url_Match):
		#print("get_match_details")

		# Pintamos la cabecera la primera vez
		if len(self.dataMatches) == 0: self.get_match_cols(bs, url_Match)

		matchInfo = bs.find("div", {"id": "matchInfo"})
		matchStatistics = matchInfo.find("div", {"id": "matchStatistics"})

		if matchStatistics == None:
			principal_info = bs.find("div", {"id": "matchInfo"})
			a = principal_info.findAll("a")
			match_row = [match_Id, a[2].text.strip(), a[3].text.strip(),
						 "".join(a[0].text.strip().split()),
						 principal_info.findAll("div")[1].text.strip()[19:28],
						 a[1].text.strip().replace(',', ' -')]
			aplazado = ['Sin disputar'] * 4 + ['-1'] * 36
			self.dataMatches.append(match_row + aplazado)
			return match_row + aplazado
		else:
			matchSystems = bs.find("div", {"id": "matchLineups"})
			matchSystems = matchSystems.findAll("div", {"class": "matchLineupsValues"})[0]
			matchSystems = matchSystems.findAll("div")

			stats = matchStatistics.findAll("div")

			principal_info = bs.find("div", {"id": "matchInfo"})
			matchResult = bs.find("td", {"id": "matchResult"})
			[golesL, golesV] = matchResult.text.strip().split(':')
			a = principal_info.findAll("a")
			d = principal_info.findAll("div")
			[goles_1erT_L, goles_1erT_V] = d[6].text.strip()[-3:].split(':')

			match_row = [match_Id, a[2].text.strip(), a[3].text.strip(),
						 "".join(a[0].text.strip().split()), d[1].text.strip()[19:28],
						 a[1].text.strip().replace(',', ' -'), d[3].text.strip()[9:].replace(',', ' -'),
						 d[4].text.strip()[9:], matchSystems[0].text, matchSystems[1].text,
						 golesL, golesV, goles_1erT_L, goles_1erT_V]

			for i in range(1, 64, 4):
				match_row.append(stats[i].findAll("div")[0].text.strip())
				match_row.append(stats[i].findAll("div")[2].text.strip())

			self.dataMatches.append(match_row)

			return match_row[0:6]

	def get_event_home_away(self, event_minute_home):
		event_minute_home = event_minute_home.text.strip()
		if event_minute_home != "":
			event_home_away = 'Local'
		else:
			event_home_away = 'Visitante'

		return event_home_away

	def clear_event_type(self, event_Type):

		# Get de class
		event_Type = event_Type['class']
		# Get second component
		event_Type = event_Type[1]
		# Remove 'eventIcon_' String
		event_Type = event_Type[10:]

		list_Event_Type = {
			'1': 'Gol',
			'2': 'Autogol',
			'3': 'Gol Penalti',
			'4': 'Penalti Fallado',
			'5': 'Tarjeta Amarillla',
			'6': 'Tarjeta Roja',
			'7':  'Cambio'
		}

		# Find value in list. Default return value
		event_Type = list_Event_Type.get(event_Type, event_Type)

		return event_Type

	def clear_event_minute(self, event_home_away, event_minute_home, event_minute_away):

		if event_home_away == "Local":
			event_minute = event_minute_home.text.strip()
		else:
			event_minute = event_minute_away.text.strip()

		return event_minute.replace('\'', '')

	def clear_event_player(self, event_home_away, event_player_home, event_player_away):

		if event_home_away == "Local":
			event_player = event_player_home.text.strip()
		else:
			event_player = event_player_away.text.strip()

		start = event_player.find('(')
		stop = event_player.find(')')
		if len(event_player) > stop:
			event_player = event_player[0: start:] + event_player[stop + 1::]

		return event_player.strip()

	def clear_event_2_player(self, event_home_away, event_player_home, event_player_away, event_type):

		if event_home_away == "Local":
			event_2_player = event_player_home.text.strip()
		else:
			event_2_player = event_player_away.text.strip()

		# If is a event type in list, remove a web bug (second player)
		if event_type in ('Cambio'):
			start = event_2_player.find('(')
			stop = event_2_player.find(')')
			if len(event_2_player) > stop:
				event_2_player = event_2_player[start + 1:stop]
		else:
			event_2_player = ''

		return event_2_player.strip()

	def get_match_events(self, match_info, match_events):

		# print('***** matchEvents *****')
		# Pintamos la cabecer
		if len(self.dataEvents) == 0:
			current_event = []
			current_event.append('ID')
			current_event.append('Local')
			current_event.append('Visitante')
			current_event.append('Liga')
			current_event.append('Temporada')
			current_event.append('Minuto')
			current_event.append('Evento')
			current_event.append('Equipo')
			current_event.append('Jugador')
			current_event.append('Jugador_2')
			# Store the data
			self.dataEvents.append(current_event)

		match_event = match_events.findAll("div", {"class": "matchEvent"})
		for event in match_event:

			# Get all Divs
			divs = event.findAll('div')

			event_home_away = self.get_event_home_away(divs[1])
			event_team = ''
			if event_home_away == 'Local': event_team = match_info[1]
			if event_home_away == 'Visitante': event_team = match_info[2]

			event_minute = self.clear_event_minute(event_home_away, divs[1], divs[3])
			event_type = self.clear_event_type(divs[2])
			event_player = self.clear_event_player(event_home_away, divs[0], divs[4])
			event_2_player = self.clear_event_2_player(event_home_away, divs[0], divs[4], event_type)

			# Create Current Event
			current_event = []
			current_event.append(match_info[0])
			current_event.append(match_info[1])
			current_event.append(match_info[2])
			current_event.append(match_info[3])
			current_event.append(match_info[4])
			current_event.append(event_minute)
			current_event.append(event_type)
			current_event.append(event_team)
			current_event.append(event_player)
			current_event.append(event_2_player)

			# Store the data
			self.dataEvents.append(current_event)

		return True

	def get_match_lineups_players(self, match_info, matchLineups, titular):

		list_Position = {
			'G': 'Portero',
			'D': 'Defensa',
			'M': 'Mediocentro',
			'F': 'Delantero'
		}

		# print('***** get_match_lineups_players *****')
		divs_team = matchLineups.findAll("div", recursive=False)

		for team in [0, 1]:
			if team == 0: home_away = match_info[1]
			if team == 1: home_away = match_info[2]

			divs_player = divs_team[team].findAll("div")
			for div in divs_player:

				position = div.find("span", {"class": "lineupPosition"})
				if position is None: position = ""
				else:
					position = position.text.strip()
					position = list_Position.get(position, position)


				rating = div.find("span", {"class": "lineupRating"})
				if rating is None: rating = ""
				else: rating = rating.text.strip()

				captain = div.find("span", {"class": "lineupCaptain"})
				if captain is None: captain = ""
				else: captain = captain.text.strip()

				player = div.contents[2]
				if player is None: player = ""
				else: player = player.strip()

				# Curren Player
				current_lineups = []
				current_lineups.append(match_info[0])
				current_lineups.append(match_info[1])
				current_lineups.append(match_info[2])
				current_lineups.append(match_info[3])
				current_lineups.append(match_info[4])
				current_lineups.append(home_away)
				current_lineups.append(titular)
				current_lineups.append(position)
				current_lineups.append(player)
				current_lineups.append(rating)
				current_lineups.append(captain)
				# Store the data
				self.dataLineups.append(current_lineups)

		return True

	def get_match_lineups(self, match_info, matchLineups):

		#print('***** matchLineups *****')

		# Añadimos las cabeceras
		if len(self.dataLineups) == 0:
			current_lineups = []
			current_lineups.append('ID')
			current_lineups.append('Local')
			current_lineups.append('Visitante')
			current_lineups.append('Liga')
			current_lineups.append('Temporada')
			current_lineups.append('Equipo')
			current_lineups.append('Titular')
			current_lineups.append('Posicion')
			current_lineups.append('Jugador')
			current_lineups.append('Puntuacion')
			current_lineups.append('Capitan')

			# Store the data
			self.dataLineups.append(current_lineups)

		match_lineup = matchLineups.findAll("div", {"class": "matchLineupsValues"})
		self.get_match_lineups_players(match_info, match_lineup[1], 'Si')
		self.get_match_lineups_players(match_info, match_lineup[2], 'No')

		return True

	def get_match(self, url_Match):
		#print('***** get_match *****')
		match_Id = url_Match.split(sep=',')[3]
		match_Id = match_Id[0:-4]

		# Download HTML
		html = self.download_html(self.url + '/' + url_Match)
		bs = BeautifulSoup(html, 'html.parser')

		# Get the data of the data match in a row:
		# Obtenemos el id y los dos equipos
		match_info = self.get_match_details(match_Id, bs, url_Match)

		matchEvents = bs.find("div", {"id": "matchEvents"})
		if matchEvents is not None:
			self.get_match_events(match_info, matchEvents)

		matchLineups = bs.find("div", {"id": "matchLineups"})
		if matchLineups is not None:
			self.get_match_lineups(match_info, matchLineups)

		return match_info

	# Pasamos una estructura a CSV
	def data2csv(self, data, filename):
		# Overwrite to the specified file.
		# Create it if it does not exist.
		file = open("../csv/" + filename, "wb+")

		# Dump all the data with CSV format
		for i in range(len(data)):
			new_line = ""
			for j in range(len(data[i])):
				new_line += data[i][j] + ","
			new_line += "\n"
			file.write(new_line.encode('utf8'))
		file.close()

	# Pasamos todas las estructuras a csv
	def all_data_2_csv(self, fileMatchsName, fileEventsName, fileLineupsName):
		self.data2csv(self.dataMatches, fileMatchsName)
		self.data2csv(self.dataEvents, fileEventsName)
		self.data2csv(self.dataLineups, fileLineupsName)

	# Función principal, le pasamos los 3 nombres de los ficheros y opcional si queremos coger solo X partidos.
	def scrape(self, output_fileMatches, output_fileEvents, output_fileLineups, num_de_partidos=1000):
		print("Web Scraping de la LFP desde '" + self.url + self.subdomain + "'")
		print("Este proceso puede tardar alrededor de 5 minutos.\n")

		# Start timer
		start_time = time.time()

		# Download HTML
		html = self.download_html(self.url + self.subdomain)
		bs = BeautifulSoup(html, 'html.parser')

		# Get the links of each match
		match_links = self.get_match_links(html)

		# Cogemos los X primeros para pruebas, o todos si no pasamos parametro
		match_links = match_links[:num_de_partidos]

		# Bucle para todos los partidos seleccionados
		contador = 0
		num_partidos = len(match_links)
		for match in match_links:
			contador += 1
			print('Procesando partido número ' + str(contador) + ' de ' + str(num_partidos))

			match_link = match.find('a').get('href')
			self.get_match(match_link)

		# Pasamos los datos a CSV
		self.all_data_2_csv(output_fileMatches, output_fileEvents, output_fileLineups)

		# Show elapsed time
		end_time = time.time()
		print("\nelapsed time: " + str(round(((end_time - start_time) / 60), 2)) + " minutes")
