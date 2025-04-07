# Honkai Star Rail: A Few Fun Insights with Data Analysis

Some insights about **Honkai Star Rail**'s characters' data.

Data is based on <https://wiki.hoyolab.com/pc/hsr/aggregate/character>
and <https://honkai-star-rail.fandom.com/wiki/Character/List>

## Status

[![CodeQL](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis/actions/workflows/codeql.yml)

[![Test Scraper](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis/actions/workflows/test-scraper.yml/badge.svg)](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis/actions/workflows/test-scraper.yml)

## Visualizations

Click [here](./docs/VISUAL.md) to view the visualizations.

## Setup and Installation

### Clone the Repository

* Clone this repo: <https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis.git>

### Configure Environment

* Create **.env** file (Git Bash)

  * ```bash
    touch ./.env
    ```

* Add an **USER_AGENT** variable.

  * ```text
    USER_AGENT=
    ```

* Find your **User Agent** with this website: <https://www.whatismybrowser.com/detect/what-is-my-user-agent/>

* Enter your **User Agent** into the **USER_AGENT** variable in the **.env** file

### Install Dependencies with UV Python

1. Install UV (if not already installed): <https://docs.astral.sh/uv/getting-started/installation/>

2. Create a virtual environment and install project dependencies using UV:

   ```bash
   uv venv
   uv sync
   ```

## Running the Application

Run the application using one of the following commands:

```bash
# Run complete pipeline (scraping and visualization)
python main.py

# Run only data scraping
python main.py --mode scrape

# Run only visualization generation
python main.py --mode visualize
```
