# ROOM.nl recent data scraper

This is a simple Python script that scrapes the most recent data from the ROOM.nl website (https://www.room.nl/en/recently-rented) and saves it to a Supabase DB. 

## Prerequisites

- Install the required packages by running ```pip install -r requirements.txt```
- Create ```.env``` file from ```example.env``` and fill in the required fields

## Usage

- To scrape and save data run ```python main.py``` (preferably every 24 hours)
- To backup the data from Supabase run ```python backup.py```
