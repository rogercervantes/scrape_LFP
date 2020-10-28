from LFP import LFP_Scraper

output_fileMatches = "dataMatches.csv"
output_fileEvents = "dataEvents.csv"
output_fileLineups = "dataLineups.csv"

scraper = LFP_Scraper()
scraper.scrape(output_fileMatches, output_fileEvents, output_fileLineups, 3)


