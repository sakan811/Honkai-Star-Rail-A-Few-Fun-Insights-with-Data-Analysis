# Honkai Star Rail: A Few Fun Insights with Data Analysis

This project collects, analyzes, and visualizes character data from Honkai Star Rail.

The application scrapes character information, then transforms this data into insightful visualizations.

Data is based on <https://wiki.hoyolab.com/pc/hsr/aggregate/character>
and <https://honkai-star-rail.fandom.com/wiki/Character/List>

## Status

[![CodeQL](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis/actions/workflows/codeql.yml)

[![Test Scraper](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis/actions/workflows/test-scraper.yml/badge.svg)](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis/actions/workflows/test-scraper.yml)

## Visualizations

Click [here](./docs/VISUAL.md) to view the visualizations.

## Setup and Installation

### Prerequisites

- Install Docker Desktop: <https://www.docker.com/products/docker-desktop/>

### Deploying the Application

- Download [Docker Compose](./docker-compose.yml) file from this repository.

- Place the **docker-compose.yml** file in a directory of your choice.

- Find your **User Agent** with this website: <https://www.whatismybrowser.com/detect/what-is-my-user-agent/>

- Enter your **User Agent** into the **USER_AGENT** variable in the **docker-compose.yml** file

## Running the Application

- Run:

  ```bash
  docker-compose up -d
  ```

- Scrape data:
  
  ```bash
  curl http://localhost:1234/scrape
  ```

- Make visualizations:

  ```bash
  curl http://localhost:1234/visualize
  ```

  - This will create visualizations in the **visual_img** folder in the same directory.
