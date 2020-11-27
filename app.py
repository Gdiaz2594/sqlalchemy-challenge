import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_
from flask import Flask, jsonify
#Data base setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite") 
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
#Flask setup
app = Flask(__name__)
#routes
@app.route("/")
def home():
    return f"""
        <p>Available routes:</p>
        <p>/api/v1.0/precipitation</p>
        <p>/api/v1.0/stations</p>
        <p>/api/v1.0/tobs</p>
        <p>/api/v1.0/2016-08-25</p>
        <p>/api/v1.0/<start>/<end></p>
    """
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp)
    session.close()
    dates_and_prcp = []
    for date, prcp in results:
        dates_and_prcp.append({
            "Date": date,
            "Precipitation": prcp
        })
    return jsonify(dates_and_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    results = list(np.ravel(results))
    session.close()
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281", Measurement.date >= '2016-08-23').all()
    session.close()
    temp_observed = []
    for date, tobs in results:
        temp_observed.append({
            "Date": date,
            "Temperature": tobs
        })
    return jsonify(temp_observed)

@app.route("/api/v1.0/2016-08-25")
def startDate():
    session = Session(engine)
    min = session.query(func.min(Measurement.tobs)).filter(Measurement.date > '2016-08-25').all()
    max = session.query(func.max(Measurement.tobs)).filter(Measurement.date > '2016-08-25').all()
    avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date > '2016-08-25').all()
    session.close()
    results = [{"Minimum temperature": min[0][0], "Maximum temperature": max[0][0],"Average temperature": avg[0][0]}]
    return jsonify(results)

@app.route("/api/v1.0/2014-08-25/2015-08-25")
def startEndDate():
    session = Session(engine)
    min = session.query(func.min(Measurement.tobs)).filter(and_(Measurement.date > '2014-08-25', Measurement.date < '2015-08-25')).all()
    max = session.query(func.max(Measurement.tobs)).filter(and_(Measurement.date > '2014-08-25', Measurement.date < '2015-08-25')).all()
    avg = session.query(func.avg(Measurement.tobs)).filter(and_(Measurement.date > '2014-08-25', Measurement.date < '2015-08-25')).all()
    session.close()
    results = [{"Minimum temperature": min[0][0], "Maximum temperature": max[0][0],"Average temperature": avg[0][0]}]
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)