
from flask import request
from pyspark.sql.functions import udf
from pyspark.sql.functions import split
from pyspark.sql.types import IntegerType

import json
class AjaxDataHandler:
	def handle_post_ajax_data(self, data_name, request):
		self.request = request
		return self.handle_ajax_data(data_name)

	def handle_ajax_data(self, data_name):
		if data_name == "yelpTableInformation":
			return self.ajax_yelp_table_information()
		elif data_name == "CitySummary":
			return self.ajax_citySummary()
		elif data_name == "UserSummary":
			return self.ajax_UserSummary()
		elif data_name == "oneCity":
			user_id = request.form["userId"]
			return self.ajax_oneCity(user_id)
		else:
			msg = {"error_message": "data name is undefined"}
			return json.dumps(msg)

	def ajax_citySummary(self):
		ajax_citySummary = self.spark_engine.get_spark().sql("SELECT city,sum(review_count) FROM yelp_business WHERE review_count > 450 GROUP BY city ORDER BY sum(review_count) desc ")
		star_rating_distribution_list = []
		for row in ajax_citySummary.collect():
			star_rating_distribution_list.append({
				"x": row[0],
				"y": row[1]
			})
		return json.dumps(star_rating_distribution_list)
		#return json.dumps(yelp_table_list)
	def ajax_UserSummary(self):
		ajax_UserSummary = self.spark_engine.get_spark().sql("SELECT review_count,average_stars FROM yelp_user WHERE review_count > 450 ORDER BY average_stars desc ")
		star_rating_distribution_list = []
		for row in ajax_UserSummary.collect():
			star_rating_distribution_list.append({
				"x": row[1],
				"y": row[0]
			})
		return json.dumps(star_rating_distribution_list)
		
	def ajax_oneCity(self,user_id):
		import pandas as pd
		import warnings
		import seaborn as sns
		pd.options.mode.chained_assignment = None  # default='warn'
		business=pd.read_csv("/Users/tuxinzhang/Desktop/yelp-dataset/yelp_business.csv")
		Citybusiness = business[business['city'] == str(user_id)]
		business_cats=' '.join(Citybusiness['categories'])
		cats=pd.DataFrame(business_cats.split(';'),columns=['category'])
		x=cats.category.value_counts()
		#prep for chart
		x=x.sort_values(ascending=False)
		x=x.iloc[0:20]
		tmp = []
		for i in range(len(x.values)):
			tmp.append({
			"x":x.index[i],
			"y":x.values[i]
			})
		return json.dumps(tmp)


	def ajax_yelp_table_information(self):
		yelp_table_list = [
			{"table_name": "yelp_business", "num_of_record": "54,600", "num_of_col": "12"}
			, {"table_name": "yelp_business_attributes", "num_of_record": "12,000", "num_of_col": "50"}
			, {"table_name": "yelp_review", "num_of_record": "3,485,147", "num_of_col": "9"}

		]
		return json.dumps(yelp_table_list)

	def __init__(self, spark_engine):
		self.spark_engine = spark_engine
