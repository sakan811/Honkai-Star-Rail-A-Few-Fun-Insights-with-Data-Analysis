# Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis
The project gives insights that delve into the Honkai Star Rail's character's stats of all available characters as of the given date.

Data is based on https://www.prydwen.gg/star-rail/ and https://honkai-star-rail.fandom.com/wiki/Character/List

Latest update: Mar 29th, 2024

This repo is only to show the codes and raw data.

To see the visualizations, check out posts below:  
[Instagram](https://www.instagram.com/p/C5Ga0VUrvw6/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)  
[Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid021XN18hLpJm7qcaPduZRF55TrkdnCSpvx329UpKyXhAtQ7yiheLPaRVxFwqDXQnrkl&id=61553626169836)

## To Run Web-Scraping Process

- Go to ```main.py```
- To scrape characters' stats
  - import **hsrws** package
    - ```from hsrws.scrape_stats import HonkaiStarRailScrapeStats```
    - To let script automatically get URLs, set 'auto' parameter as follows:
      - ```
        main = HonkaiStarRailScrape(auto=True)
        main.hsr_scrape()
        ```
    - To manually get URLs, set 'urls' parameter as follows:
      - ```
        urls = ['character/page/url']
        main = HonkaiStarRailScrape(urls=urls)
        main.hsr_scrape()
        ```
- To scrape characters' element, path, and rarity data
  - import **hsrws** package
    - ```from hsrws.scrape_paths_elements_rarities import HonkaiStarRailScrapePathAndElement```
    - To let script automatically get URLs, set 'auto' parameter as follows:
      - ```
        main = HonkaiStarRailScrapePathAndElement(auto=True)
        main.hsr_scrape()
        ```
    - To manually get URLs, set 'urls' parameter as follows:
      - ```
        urls = ['character/page/url']
        main = HonkaiStarRailScrapePathAndElement(urls=url)
        main.hsr_scrape()
        ```

## Scripts in ```hsrws``` package
```web_scrap.py```:

- Contain methods related to web-scraping the desired data from the website.
- Use a function from ```calculate_hsr.py``` to process each file.
  - Save them to the specified directory.

```get_urls_auto.py```:

- Automatically gather all URLs to each character page from the website.

```calculate_hsr.py```:

- Process an Excel.
  - Add growth rate and growth rate % for all stats as columns.
- Save the processed Excel at the given directory.

```create_excel.py```:

- Create an Excel file and add data from the stats list into the file.

```scrape_stats.py```:

- To scrape characters' stats data from the website.
- Use a method from ```web_scrap.py``` to perform web scraping.

```scrape_paths_elements_rarities.py```:

- Scrape Paths, Elements, Rarities of all character from the website.
- Combined and save these data into an Excel file.

## Other Scripts
```stats_of_desired_lvl.py```:

- Run through all Excels in the specific directory.
- Process each Excel.
  - Extract ATK, DEF, HP, SPD of the given Level.
- Combined processed Excels into one.      


