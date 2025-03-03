# Climate App for Trip Planning in Honolulu, Hawaii

Aloha! This Flask API was designed to help plan a holiday vacation to Honolulu, Hawaii. It provides tools for analyzing climate data about the area to make informed decisions about my dream trip.

# Resources
`app.py` - Establishes Flask routes along with queries to view precipitation and temperature related data from across a year-long period.

`climate_starter.ipynb` - Contains the queries and summary statistics regarding temperature weather data 

## Overview

This Climate App offers a series of API endpoints to retrieve various climate-related data, including:

* Precipitation data for the last 12 months.
* A list of weather stations.
* Temperature observations for the most active station for the last 12 months.
* Minimum, average, and maximum temperatures for a specified date range.

## API Endpoints

* `/`: Homepage with a list of available routes.
* `/api/v1.0/precipitation`: Precipitation data for the last 12 months.
* `/api/v1.0/stations`: List of weather stations.
* `/api/v1.0/tobs`: Temperature observations for the most active station for the last 12 months.
* `/api/v1.0/<start>`: Minimum, average, and maximum temperatures for all dates greater than or equal to the start date.
* `/api/v1.0/<start>/<end>`: Minimum, average, and maximum temperatures for the dates between the start and end dates (inclusive).

## Data

The app uses a SQLite database (`hawaii.sqlite`) containing climate data for Hawaii. The database has two tables:
* `measurement`: Contains daily climate measurements (station ID, date, precipitation, temperature).
* `station`: Contains information about the weather stations (station ID, name, latitude, longitude, elevation).

## References
* Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical Climatology Network-Daily
* Database. Journal of Atmospheric and Oceanic Technology, 29, 897-910, https://journals.ametsoc.org/view/journals/atot/29/7/jtech-d-11-00103_1.xml
* Google for research and guide with debugging
