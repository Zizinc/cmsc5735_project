from flask import Blueprint
from flask import Flask, render_template, request

from ajax_data import AjaxDataHandler

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/dashboard')
def dashboard_page():
	#distinctBusinessCityDf = engine.get_spark().sql("SELECT distinct city FROM yelp_business ORDER BY city")
	#city = distinctBusinessCityDf.collect()[0]
	return render_template('dashboard.html')

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