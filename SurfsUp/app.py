# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
Base.prepare(autoload_with=engine)

# Use the Base class to reflect the database tables
# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Welcome to the Climate Analysis<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# /api/v1.0/precipitation Route:
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last 12 months."""
    most_recent_date = session.query(Measurement.date).order_by(desc(Measurement.date)).first()[0]
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    return jsonify(precipitation_dict)

# /api/v1.0/stations Route:
@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    stations_data = session.query(Station.station).all()
    stations_list = [station[0] for station in stations_data]
    return jsonify(stations_list)

# /api/v1.0/tobs Route:
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the previous year."""
    most_recent_date = session.query(Measurement.date).order_by(desc(Measurement.date)).first()[0]
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(desc(func.count(Measurement.station))).first()[0]

    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()

    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in tobs_data]
    return jsonify(tobs_list)

# /api/v1.0/<start> and /api/v1.0/<start>/<end> Routes:
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end=None):
    """Return TMIN, TAVG, TMAX for a specified start or start-end range."""
    if end:
        temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()

    if temperature_stats:
        tmin, tavg, tmax = temperature_stats[0]
        return jsonify({"TMIN": tmin, "TAVG": tavg, "TMAX": tmax})
    else:
        return jsonify({"error": "Date range not found."}), 404
    