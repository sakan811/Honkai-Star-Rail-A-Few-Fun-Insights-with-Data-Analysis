# Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis
The project gives insights that delve into the Honkai Star Rail's character's stats of all available characters as of the given date.

Data is based on https://www.prydwen.gg/star-rail/ and https://honkai-star-rail.fandom.com/wiki/Character/List

Latest update: Mar 21st, 2024

This repo is only to show the codes and raw data.

To see the visualizations, check out posts below:  
[Instagram](https://www.instagram.com/p/C4xvn6GLHs-/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)  
[Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid0kSNFkF9jcaGRfF81juiWHaQ4DtUjyPQQEywUdjH63nqbuGQku6zPkkcctUYShCHVl&id=61553626169836)

# Main Scripts

```main.py```:

- To let script automatically get URLs, set 'auto' parameter as follows:
  - ```
    main = Main(auto=True)
    main.main()
    ```
- To manually get URLs, set 'urls' parameter as follows:
  - ```
    urls = ['website/url']
    main = Main(urls=urls)
    main.main()
    ```
- Use a function from ```web_scrap.py``` to perform web scraping.

# Scripts in ```codes``` package
```web_scrap.py```:
- Scrape ATK, DEF, HP, SPD, of each Level of the given character from the website.
- Save the data of each character in an Excel at the specified directory.
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

# Other Scripts
```scrape_paths_elements_rarities.py```:
- Ask user to press 1 or 2:
  - 1: Automatically gather all URLs to each character's page.
  - 2: Manually enter URLs of each character's page.
- Scrape Paths, Elements, Rarities of all character from the website.
- Combined and save these data into an Excel file.

```stats_of_desired_lvl.py```:

- Run through all Excels in the specific directory.
- Process each Excel.
  - Extract ATK, DEF, HP, SPD of the given Level.
- Combined processed Excels into one.      


