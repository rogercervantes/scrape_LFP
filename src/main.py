from LFP import LFP_Scraper

output_fileMatches = "Partidos.csv"
output_fileEvents = "Eventos.csv"
output_fileLineups = "Alineaciones.csv"

scraper = LFP_Scraper()
scraper.scrape(output_fileMatches, output_fileEvents, output_fileLineups, 20)

