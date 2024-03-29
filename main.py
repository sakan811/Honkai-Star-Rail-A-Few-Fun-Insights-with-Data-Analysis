from loguru import logger

from hsrws.scrape_stats import HonkaiStarRailScrapeStats
from hsrws.scrape_paths_elements_rarities import HonkaiStarRailScrapePathAndElement

logger.add('main.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w')

if __name__ == '__main__':
    url = ['https://www.prydwen.gg/star-rail/characters/gallagher']

    # main = HonkaiStarRailScrape(urls=url)
    # main.hsr_scrape()

    # main = HonkaiStarRailScrapePathAndElement(urls=url)
    # main.hsr_scrape()
