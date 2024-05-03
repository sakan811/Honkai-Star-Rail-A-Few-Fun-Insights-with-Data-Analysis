# Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis
The project gives insights that delve into the Honkai Star Rail's character's stats of all available characters as of the given date.

Data is based on https://www.prydwen.gg/star-rail/ and https://honkai-star-rail.fandom.com/wiki/Character/List

Latest update: Apr 30th, 2024

To see the visualizations, check out posts below:  
[Instagram](https://www.instagram.com/p/C6Ww0r0BJF5/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)  
[Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid0A5XHXHEEkAeTiPd2LpfzKqYYpFQ9aSqukoZbFZP6cRqpev117f6658QhMrPi8dtml&id=61553626169836)

## To Run Web-Scraping Process

- Go to ```main.py```
- Import the following packages
  - ```
        from loguru import logger # optional

        import hsrws
      
        # optional
        logger.add('main.log',
                   format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
                   mode='w')
    ```
- **To scrape characters' stats**
  - To let a script automatically get URLs, follow the code snippets below:
    - ```
      if __name__ == '__main__':
          main = hsrws.HonkaiStarRailScrape(auto=True)
          main.hsr_scrape()
      ```
  - To manually get URLs, follow the code snippets below:
    - ```
      if __name__ == '__main__':
          urls = ['character/page/url']
          main = hsrws.HonkaiStarRailScrape(urls=urls)
          main.hsr_scrape()
      ```
- **To scrape characters' element, path, and rarity data**
  - To let a script automatically get URLs, follow the code snippets below:
    - ```
      if __name__ == '__main__':
          main = hsrws.HonkaiStarRailScrapePathAndElement(auto=True)
          main.hsr_scrape()
      ```
  - To manually get URLs, follow the code snippets below:
    - ```
      if __name__ == '__main__':
         urls = ['character/page/url']
         main = hsrws.HonkaiStarRailScrapePathAndElement(urls=url)
         main.hsr_scrape()
      ```

## ```hsrws``` package
```web_scrap.py```:

- Contain methods related to web-scraping the desired data from the website.
- Use a function from ```calculate_hsr.py``` to process each file.
  - Save them to the specified directory.

```get_urls_auto.py```:

- Contain method to automatically gather all URLs to each character page from the website.

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
- Combine and save these data into an Excel file.

## SQLite Pipeline

```sqlite_pipeline.py```:

- Migrate Excel data to SQLite database
- Create Views

To use ```sqlite_pipeline.py```:

- Go to ```sqlite_pipeline.py``` script
- Run the script
- The created SQLite database is named 'hsr'

## Other Scripts
```stats_of_desired_lvl.py```:

- Run through all Excels in the specific directory.
- Process each Excel.
  - Extract ATK, DEF, HP, SPD of the given Level.
- Combined processed Excels into one.      


