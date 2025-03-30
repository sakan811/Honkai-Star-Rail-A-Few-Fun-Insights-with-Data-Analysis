# Honkai Star Rail: A Few Fun Insights with Data Analysis

Some insights about **Honkai Star Rail**'s characters' data.

Data is based on <https://wiki.hoyolab.com/pc/hsr/aggregate/character>
and <https://honkai-star-rail.fandom.com/wiki/Character/List>

## Status

[![CodeQL](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis/actions/workflows/codeql.yml)

[![Test Scraper](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis/actions/workflows/test-scraper.yml/badge.svg)](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis/actions/workflows/test-scraper.yml)

## Visualizations

Click [here](./docs/VISUAL.md) to view the visualizations.

## To Run Web-Scraping Process

* Clone this repo: <https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis.git>

* Create **.env** file with the **USER_AGENT** variable.

  * ```text
    USER_AGENT=
    ```

* Find your **User Agent** with this website: <https://www.whatismybrowser.com/detect/what-is-my-user-agent/>

* Enter your **User Agent** into the **USER_AGENT** variable in the **.env** file
* Run:

  * ```bash
    # Run complete pipeline (scraping and visualization)
    python main.py

    # Run only data scraping
    python main.py --mode scrape

    # Run only visualization generation
    python main.py --mode visualize
    ```
