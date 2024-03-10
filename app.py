# Import the dependencies.

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################


# Home Route

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )


# Precipitation Route

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    one_year_before = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_before).all()
    
    session.close()

    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)


# Stations Route

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all stations
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


# TOBS Route

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return Query of dates and temperature observations of the most-active station for the previous year of data"""
    
    # Find the most active station
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()

    # Save the Most Active Station as a variable
    most_active_station = active_stations[0][0]

    # Calculate the date one year from the last date in the data set.
    one_year_before = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Find temperature observations from the most active station
    temperature_stats = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == most_active_station).\
    filter(Measurement.date >= one_year_before).all()

    session.close()

    # Create JSON List
    temperature_json = [{"date": date, "tobs": tobs} for date, tobs in temperature_stats]

    # Return the JSON list
    return jsonify(temperature_json)


# Start Route

@app.route("/api/v1.0/<start>")
def temperature_stats_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return TMIN, TAVG, and TMAX for all dates greater than or equal to the start date."""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    # Convert the query results to a JSON response
    temperature_stats = {
        "Start Date": start,
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }
    return jsonify(temperature_stats)

@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate TMIN, TAVG, and TMAX for dates between start and end (inclusive)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    # Convert the query results to a JSON list
    temperature_stats = {
        "Start Date": start,
        "End Date": end,
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return jsonify(temperature_stats)


if __name__ == '__main__':
    app.run(debug=True)

