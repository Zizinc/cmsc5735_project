from flask import Blueprint
from flask import Flask, render_template, request
from engine import SparkEngine

from ajax_data import AjaxDataHandler

app = Flask(__name__)
spark_engine = SparkEngine()
ajax_data_handler = AjaxDataHandler(spark_engine)


@app.route('/')
@app.route('/dashboard')
def dashboard_page():
    # distinctBusinessCityDf = engine.get_spark().sql("SELECT distinct city
    # FROM yelp_business ORDER BY city")
    # city = distinctBusinessCityDf.collect()
    return render_template('dashboard.html')


@app.route('/user_query')
def user_query_page():
    return render_template('user_query.html')


@app.route('/featured_user_analysis')
def featured_user_analysis_page():

    return render_template('featured_user_analysis.html')


@app.route('/featured_city_analysis')
def featured_city_analysis_page():
    return render_template('featured_city_analysis.html')


@app.route('/ajax_data', methods=['GET', 'POST'])
def handle_ajax_data():
    if request.method == 'GET':
        return ajax_data_handler.handle_ajax_data(request.args.get("dataName"))
    else:
        return ajax_data_handler. \
          handle_post_ajax_data(request.args.get("dataName"), request)


@app.route('/test')
def test():
    return "Test: Ok"


if __name__ == '__main__':
    app.run(debug=True)
