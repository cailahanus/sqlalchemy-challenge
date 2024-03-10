# sqlalchemy-challenge

This repository involves a climate analysis of Honolulu, Hawaii, using Python, SQLAlchemy, and Flask. Here's a summary of the tasks and objectives:

## Part 1: Analyze and Explore the Climate Data found in climate_starterCAH.ipynb

Database Setup:
- Use create_engine() to connect to the SQLite database.
- Use automap_base() to reflect tables into classes (station and measurement).
- Create a SQLAlchemy session to link Python to the database.

Precipitation Analysis:
- Find the most recent date in the dataset.
- Query the previous 12 months of precipitation data.
- Load query results into a Pandas DataFrame.
- Sort the DataFrame by date.
- Plot the results using Matplotlib.
- Print summary statistics for precipitation data.

Station Analysis:
- Design queries to calculate the total number of stations and find the most-active stations.
- Query lowest, highest, and average temperatures for the most-active station.
- Query the previous 12 months of temperature observation (TOBS) data for the most-active station.
- Plot TOBS data as a histogram.


## Part 2: Design Your Climate App found in app.py
Flask API Design found in app.py

Create Flask routes for the following endpoints:
- / (Homepage with available routes).
- /api/v1.0/precipitation (Returns last 12 months of precipitation data as a JSON dictionary).
- /api/v1.0/stations (Returns a JSON list of stations).
- /api/v1.0/tobs (Returns temperature observations for the most-active station for the previous year).
- /api/v1.0/<start> (Returns temperature statistics from the specified start date to the end of the dataset).
- /api/v1.0/<start>/<end> (Returns temperature statistics for the specified start-end date range).

## Overall:
The repository guides you through exploratory data analysis, visualization, and the creation of a Flask API to provide climate-related information. It covers both basic analysis and more advanced Flask API development based on the analysis conducted earlier.
