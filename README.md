# Honkai Star Rail: A Few Fun Insights with Data Analysis

Some insights about Honkai Star Rail's characters' data.

Data is based on https://wiki.hoyolab.com/pc/hsr/aggregate/character and https://honkai-star-rail.fandom.com/wiki/Character/List


## Status
Project Latest update: 17 July 2024

[![CodeQL](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis/actions/workflows/codeql.yml)

[![Test Scraper](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis/actions/workflows/test-scraper.yml/badge.svg)](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis/actions/workflows/test-scraper.yml)

## Visualizations
Visualizations Latest update: 17 July 2024

[Power BI](https://app.powerbi.com/view?r=eyJrIjoiNThhMWE5ODEtN2NkMy00NjEyLTgyMTItYWNmZTUwNTQ0YTZmIiwidCI6ImZlMzViMTA3LTdjMmYtNGNjMy1hZDYzLTA2NTY0MzcyMDg3OCIsImMiOjEwfQ%3D%3D)    

[Instagram](https://www.instagram.com/p/C9OrzJXvk8U/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)  

[Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid02yJ7cAGC62UzKtQR9jh4N3fnwM5L5jvsin7LZxeAmBqYtytEs2FLpTzBDWmAvyPjKl&id=61553626169836)

## To Run Web-Scraping Process
- Run ```main.py```

## ```hsrws``` package
[data_transformer.py](hsrws%2Fdata_transformer.py)
- Contain functions for data transformation

[hsr_scraper.py](hsrws%2Fhsr_scraper.py)
- Contain the web-scraper as a function

[sqlite_pipeline.py](hsrws%2Fsqlite_pipeline.py)
- Contain functions for loading data to SQLite

[utils.py](hsrws%2Futils.py)
- Contain utility functions

