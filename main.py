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

from loguru import logger

import hsrws

logger.add('main.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {thread} | {name} | {module} | {function} | {line} | {message}",
           mode='w')

if __name__ == '__main__':
    url = ['https://www.prydwen.gg/star-rail/characters/boothill']
    #
    main = hsrws.HonkaiStarRailScrapeStats(urls=url)
    #
    # main = hsrws.HonkaiStarRailScrapeStats(auto=True)
    #
    main.hsr_scrape()
    #
    # main = hsrws.HonkaiStarRailScrapePathAndElement(auto=True)
    # main.hsr_scrape()

    pass
