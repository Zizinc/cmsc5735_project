from flask import Blueprint
from flask import Flask, render_template, request

from ajax_data import AjaxDataHandler

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/dashboard')
def dashboard_page():
	#distinctBusinessCityDf = engine.get_spark().sql("SELECT distinct city FROM yelp_business ORDER BY city")
	distinctBusinessCityDf = engine.get_spark().sql("SELECT distinct name,city,review_count,address FROM yelp_business WHERE review_count > 1000 ORDER BY review_count desc ")
	#Select those cities with review_count > 200
	city = distinctBusinessCityDf.collect()

	UserInfo = engine.get_spark().sql("SELECT name,review_count,yelping_since,useful,average_stars FROM yelp_user WHERE review_count > 1000 ORDER BY review_count desc ")
	#Select those users with high review count

	user = UserInfo.collect()

	return render_template('dashboard.html', city=city,user=user)

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
