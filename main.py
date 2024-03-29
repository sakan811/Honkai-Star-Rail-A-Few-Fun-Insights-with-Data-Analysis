from loguru import logger

from codes.honkai_star_rail_scrape import HonkaiStarRailScrape

logger.add('main.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w')


if __name__ == '__main__':
    url = ['https://www.prydwen.gg/star-rail/characters/gallagher']
    main = HonkaiStarRailScrape(urls=url)
    main.hsr_scrape()
