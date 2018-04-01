from flask import Blueprint
from flask import Flask, render_template, request

from ajax_data import AjaxDataHandler

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/dashboard')
def dashboard_page():
	#distinctBusinessCityDf = engine.get_spark().sql("SELECT distinct city FROM yelp_business ORDER BY city")
	#distinctBusinessCityDf = engine.get_spark().sql("SELECT distinct name,city,review_count,address FROM yelp_business WHERE review_count > 1000 ORDER BY review_count desc ")
	#Select those cities with review_count > 200
	#city = distinctBusinessCityDf.collect()

	#UserInfo = engine.get_spark().sql("SELECT name,review_count,yelping_since,useful,average_stars FROM yelp_user WHERE review_count > 1000 ORDER BY review_count desc ")
	#Select those users with high review count

	#user = UserInfo.collect()

	#return render_template('dashboard.html',user=user)
	return render_template('dashboard.html')

@main.route('/city')
def City_Summary_Page():
	#distinctBusinessCityDf = engine.get_spark().sql("SELECT distinct city FROM yelp_business ORDER BY city")
	distinctBusinessCityDf = engine.get_spark().sql("SELECT distinct name,city,review_count,address FROM yelp_business WHERE review_count > 1000 ORDER BY review_count desc ")
	#Select those cities with review_count > 200
	city = distinctBusinessCityDf.collect()

	return render_template('CitySummary.html', city=city)
@main.route('/usersummary')
def User_Summary_Page():
	UserInfo = engine.get_spark().sql("SELECT name,review_count,yelping_since,useful,average_stars FROM yelp_user WHERE review_count > 1000 ORDER BY review_count desc ")
	#Select those users with high review count
	userSummary = UserInfo.collect()

	return render_template('usersummary.html', user=userSummary)
@main.route('/cityplot')
def City_Plot_Page():
	import pandas as pd
	import io
	import urllib
	import base64
	import warnings
	import matplotlib.pyplot as plt
	import seaborn as sns
	import matplotlib.gridspec as gridspec
	import matplotlib.gridspec as gridspec
	pd.options.mode.chained_assignment = None  # default='warn'
	business=pd.read_csv("/Users/tuxinzhang/Desktop/yelp-dataset/yelp_business.csv")

	f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,7))
	rating_data=business[['latitude','longitude','stars','review_count']]
	# Creating a custom column popularity using stars*no_of_reviews
	rating_data['popularity']=rating_data['stars']*rating_data['review_count']

	#a random point inside vegas
	lat = 36.207430
	lon = -115.268460
	#some adjustments to get the right pic
	lon_min, lon_max = lon-0.3,lon+0.5
	lat_min, lat_max = lat-0.4,lat+0.5
	#subset for vegas
	ratings_data_vegas=rating_data[(rating_data["longitude"]>lon_min) &\
	                    (rating_data["longitude"]<lon_max) &\
	                    (rating_data["latitude"]>lat_min) &\
	                    (rating_data["latitude"]<lat_max)]

	#Facet scatter plot
	ratings_data_vegas.plot(kind='scatter', x='longitude', y='latitude',
	                color='yellow',
	                s=.02, alpha=.6, subplots=True, ax=ax1)
	ax1.set_title("Las Vegas")
	ax1.set_facecolor('black')

	#a random point inside pheonix
	lat = 33.435463
	lon = -112.006989
	#some adjustments to get the right pic
	lon_min, lon_max = lon-0.3,lon+0.5
	lat_min, lat_max = lat-0.4,lat+0.5
	#subset for pheonix
	ratings_data_pheonix=rating_data[(rating_data["longitude"]>lon_min) &\
	                    (rating_data["longitude"]<lon_max) &\
	                    (rating_data["latitude"]>lat_min) &\
	                    (rating_data["latitude"]<lat_max)]
	#plot pheonix
	ratings_data_pheonix.plot(kind='scatter', x='longitude', y='latitude',
	                color='yellow',
	                s=.02, alpha=.6, subplots=True, ax=ax2)
	ax2.set_title("Pheonix")
	ax2.set_facecolor('black')
	#plt.show()
	img = io.BytesIO()  # create the buffer
	plt.savefig(img, format='png')
	img.seek(0)  # rewind your buffer
	plot_data = urllib.quote(base64.b64encode(img.read()).decode())
	return render_template('CityPlot.html',plot_url = plot_data)

@main.route('/ajax_data', methods=['GET'])
def handle_ajax_data():
	return ajax_data_handler.handle_ajax_data(request.args.get("dataName"))

def create_app(spark_engine):
	global engine
	global ajax_data_handler

	engine	= spark_engine
	ajax_data_handler = AjaxDataHandler(spark_engine)

	app = Flask(__name__)
	app.register_blueprint(main)
	return app

if __name__ == '__main__':
	# run without spark engine
	# for test and debug use
	spark_engine = None
	create_app(spark_engine).run(debug=True, host='0.0.0.0')
