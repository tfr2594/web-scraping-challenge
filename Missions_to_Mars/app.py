# import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Import pymongp to connect to flask app and mongodb
import pymongo

#create instance of Flask app
app = Flask(__name__)

# PyMongo and Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")


#create route 
@app.route("/")

def home():

	#Find one record of data from the mongo database
	mars_info = mongo.db.mars.find_one()

	#Return template and data
	return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scraper():

	mars = mongo.db.mars
	data = scrape_mars.scrape_all()
	mars.update({}, data, upsert=True)
	return redirect("/", code=302)
  
# to run from command line(dont' forget)
if __name__ == "__main__":
	app.run(debug=True)