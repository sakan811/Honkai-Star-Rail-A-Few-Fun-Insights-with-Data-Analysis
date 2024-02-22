# Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis
The project gives insights that delve into the Honkai Star Rail's character's stats of all available characters as of the given date.

I used web scraping scripts written with Python to gather data from https://www.prydwen.gg/star-rail/

Latest update: 29 Jan 2024

This repo is only to show the codes and data.

To see the details about the insights from this project, check out this link below to my Facebook page's post:
https://www.facebook.com/permalink.php?story_fbid=pfbid0C3Vva972MnyiSt1Zi1Q1QFyDb3aCyvQPg3NbMV52J5atYJwB2AGimRPXendp17q9l&id=61553626169836

# Codes

```main.py```:

- Ask user to press 1 or 2:
  - 1: Automatically gather all URLs to each character's page.
  - 2: Manually enter URLs of each character's page.

```web_scrap.py```:
- Scrape ATK, DEF, HP, SPD, of each Level of the given character from the website.
- Save the data of each character in an Excel at the specified directory.
- Call a function from ```calculate_hsr.py``` to add additional columns to each file.
- Save them to the specified directory.

```stats_of_desired_lvl.py```:
- Run through all Excels in the specific directory.
- Process each Excel.
  - Extract ATK, DEF, HP, SPD of the given Level.
- Combined processed Excels into one.       
   
```scrape_paths_elements_rarities.py```:
- Ask user to press 1 or 2:
  - 1: Automatically gather all URLs to each character's page.
  - 2: Manually enter URLs of each character's page.
- Scrape Paths, Elements, Rarities of all character from the website.
- Combined and save these data into an Excel file.

```get_urls_auto.py```:
- Automatically gather all URLs to each character page from the website.

```calculate_hsr.py```:
- Process an Excel.
  - Add growth rate and growth rate % for all stats as columns.
- Save the processed Excel at the given directory.