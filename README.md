# Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis

Some insights about Honkai Star Rail's characters' data.

Data is based on https://wiki.hoyolab.com/pc/hsr/aggregate/character and https://honkai-star-rail.fandom.com/wiki/Character/List


## Status
Project Latest update: June 21, 2024  



## Visualizations
Visualizations Latest update: June 21, 2024  
[Power BI](https://app.powerbi.com/view?r=eyJrIjoiNThhMWE5ODEtN2NkMy00NjEyLTgyMTItYWNmZTUwNTQ0YTZmIiwidCI6ImZlMzViMTA3LTdjMmYtNGNjMy1hZDYzLTA2NTY0MzcyMDg3OCIsImMiOjEwfQ%3D%3D)    
[Instagram](https://www.instagram.com/p/C8d_dyJugPW/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)  
[Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid033ShCbrt5Emrb6LGy5DjVs8qCw2UwXAMx45hQUcB26HiRxW21PULCR7s8R1dRfboBl&id=61553626169836)

## To Run Web-Scraping Process

If you want to **manually** enter the **URL** of the character page from https://www.prydwen.gg/star-rail/ to scrape its
data.
- Run ```main.py```

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

To load data to SQLite database using ```sqlite_pipeline.py```:

- Go to ```sqlite_pipeline.py``` script
- Set the SQLite database name
  ```
  # Set database name as needed
  database = 'hsr.db'
  ```
- Run the script to load the data to a SQLite database

## Other Scripts
```stats_of_desired_lvl.py```:

- Run through all Excels in the specific directory.
- Process each Excel.
  - Extract ATK, DEF, HP, SPD of the given Level.
- Combined processed Excels into one.      


