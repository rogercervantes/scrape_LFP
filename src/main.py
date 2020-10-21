from LFP import LFP_Scraper

output_fileEvents = "dataEvents.csv"

scraper = LFP_Scraper()
scraper.scrape()
scraper.data2csv(output_fileEvents)

