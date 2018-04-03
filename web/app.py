from flask import Flask, render_template, request
from ajax_data import AjaxDataHandler
from engine import SparkEngine
from redis_engine import RedisEngine
import matplotlib


matplotlib.use('Agg')
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
    import pandas as pd
    import io
    import urllib
    import base64
    import warnings
    import seaborn as sns
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    import matplotlib.gridspec as gridspec

    pd.options.mode.chained_assignment = None  # default='warn'
    #business=pd.read_csv("data/yelp_business_small_1000.csv")
    business = spark_engine.get_spark().sql("SELECT * FROM yelp_business")
    business = business.toPandas()
    business_cats=' '.join(business['categories'])
    cats=pd.DataFrame(business_cats.split(';'),columns=['category'])
    x=cats.category.value_counts()

    #prep for chart

    x=x.sort_values(ascending=False)
    x=x.iloc[0:20]

    #chart
    plt.figure(figsize=(16,8))
    ax = sns.barplot(x.index, x.values, alpha=0.8)#,color=color[5])
    plt.title("What are the top categories?",fontsize=25)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=80)
    plt.ylabel('# businesses', fontsize=12)
    plt.xlabel('Category', fontsize=12)

    #adding the text labels
    rects = ax.patches
    labels = x.values
    for rect, label in zip(rects, labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2, height + 10, label, ha='center', va='bottom')

    img = io.BytesIO()  # create the buffer
    plt.savefig(img, format='png')
    img.seek(0)  # rewind your buffer
    plot_data = urllib.quote(base64.b64encode(img.read()).decode())
    #distinctBusinessCityDf = engine.get_spark().sql("SELECT distinct city FROM yelp_business ORDER BY city")
    distinctBusinessCityDf =spark_engine.get_spark().sql("SELECT distinct name,city,review_count,address FROM yelp_business WHERE review_count > 1000 ORDER BY review_count desc ")
    #Select those cities with review_count > 200
    city = distinctBusinessCityDf.collect()
    return render_template('featured_city_analysis.html', city=city,plot_url = plot_data)


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
