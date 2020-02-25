import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data including the date and precipitation amount"""
    # Query 
    pre_results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precip
    all_precip = []
    for date, pcrp in pre_results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = pcrp
        all_precip.append(precipitation_dict)

    return jsonify(all_precip)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    sta_results = session.query(Station.station).all()

    session.close()

    return jsonify(sta_results) 

@app.route("/api/v1.0/tobs")
def temperature(): 

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for last year of dates and temperatures
    temp_results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > '2016-08-28').filter(Measurement.date<'2017-08-23').all()

    session.close()

    return jsonify(temp_results) 

@app.route("/api/v1.0/<start>")
def start(start=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    

    star_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    session.close()

    # function usage example
    return jsonify(star_results)

@app.route("/api/v1.0/<start>/<end>")
def end(start = None, end = None): 
    # Create our session (link) from Python to the DB
    session = Session(engine)

    star_end_results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    # function usage example
    return jsonify(star_end_results)


if __name__ == '__main__':
    app.run(debug=True)