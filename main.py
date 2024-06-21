#    Copyright 2024 Sakan Nirattisaykul
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import argparse

from loguru import logger

import hsrws

logger.add('main.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w')

parser = argparse.ArgumentParser(description='Argument Parser for main.py')
parser.add_argument('--stats', action='store_true', help='Scrape Characters\' Stats')
parser.add_argument('--p_e_r', action='store_true', help='Scrape Characters\' Path, Element, and Rarity')
parser.add_argument('--auto', action='store_true', help='Automatically get URLs')
args = parser.parse_args()


def main(urls: list[str]):
    """
    Main function to start the web-scraping process.
    :param urls: List of URLs.
    :return: None.
    """
    if args.stats and args.p_e_r:
        raise ValueError("Only one of --stats and --p_e_r can be parsed at a time.")
    elif args.stats:
        logger.info("Scraping Characters' Stats...")
        if args.auto:
            logger.info("Automatically get URLs...")
            main = hsrws.HonkaiStarRailScrapeStats(auto=True)
            main.hsr_scrape()
        else:
            logger.info("URLs were manually entered.")
            main = hsrws.HonkaiStarRailScrapeStats(urls=urls)
            main.hsr_scrape()
    elif args.p_e_r:
        logger.info("Scraping Characters' Path, Element, and Rarity...")
        if args.auto:
            logger.info("Automatically get URLs...")
            main = hsrws.HonkaiStarRailScrapePathElementRarity(auto=True)
            main.hsr_scrape()
        else:
            logger.info("URLs were manually entered.")
            main = hsrws.HonkaiStarRailScrapePathElementRarity(urls=urls)
            main.hsr_scrape()


if __name__ == '__main__':
    url = ['https://www.prydwen.gg/star-rail/characters/firefly']
    main(url)
