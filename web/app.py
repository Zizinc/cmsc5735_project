#from flask import Blueprint
from flask import Flask, render_template, request
from ajax_data import AjaxDataHandler
from engine import SparkEngine
from redis_engine import RedisEngine


app = Flask(__name__)
spark_engine = SparkEngine()
r_engine = RedisEngine()
ajax_data_handler = AjaxDataHandler(spark_engine, r_engine)

@app.route('/')
@app.route('/index.html')
def index_page():
    return render_template('index.html')


@app.route('/user_query')
def user_query_page():
    return render_template('user_query.html')


@app.route('/featured_user_analysis')
def featured_user_analysis_page():
    return render_template('featured_user_analysis.html')


@app.route('/city_query')
def city_query_page():
    return render_template('city_query.html')


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
