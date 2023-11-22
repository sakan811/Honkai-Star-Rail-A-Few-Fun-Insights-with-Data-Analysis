# Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis
The project gives insights that delve into the Honkai Star Rail's character's stats of all available characters as of the given date.

I used web scraping scripts written with Python to gather data from https://www.prydwen.gg/star-rail/

Latest update: 19 Nov 23

This repo is only to show the codes and data.

To see the details about the insights from his project, check out this link below to my Facebook page's post:
https://www.facebook.com/permalink.php?story_fbid=pfbid02F7Ex6e9sZsZwMMazqo9WWpN16DY9phiTVW47uXFuGeKu6MacMyhNQJPhTiVGJrCYl&id=61553626169836

# Codes
```web_scrap.py```: 
- Scrape ATK, DEF, HP, SPD, of each Level of the given character from the website.
- Save the data in an Excel at the specified directory.

```stats_of_desired_lvl.py```:
- Run through all Excels in the specific directory.
- Process each Excel.
  - Extract ATK, DEF, HP, SPD of the given Level.
- Combined processed Excel into one.       
   
```scrape_paths_elements_rarities.py```:
- Scrape Paths, Elements, Rarities of all character from the website.
- Save the data into an Excel.

```get_urls_auto.py```:
- Automatically gather all URLs to each character page from the website.

```calculate_hsr.py```:
- Process an Excel.
  - Add growth rate and growth rate % for all stats as columns.
- Save the processed Excel at the given directory.