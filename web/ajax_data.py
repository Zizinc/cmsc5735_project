from flask import request
from pyspark.sql.functions import udf
from pyspark.sql.functions import split
from pyspark.sql.types import IntegerType

import json

def count_num_of_friends(friend_string):
   return len(friend_string.split(','))

class AjaxDataHandler:

	def handle_post_ajax_data(self, data_name, request):
		self.request = request
		return self.handle_ajax_data(data_name)

	def handle_ajax_data(self, data_name):
		if data_name == "yelpTableInformation":
			return self.ajax_yelp_table_information()
		elif data_name == "userBasicInformationByUserId":
			user_id = request.form["userId"]
			return self.ajax_yelp_user_basic_information_by_user_id(user_id)
		elif data_name == "reviewsByUserId":
			user_id = request.form["userId"]
			return self.ajax_yelp_reviews_by_user_id(user_id)
		elif data_name == "starRatingDistribution":
			return self.ajax_yelp_star_rating_distribution()
		elif data_name == "analysisOnTopUsers":
			return self.ajax_yelp_analysis_on_top_users()
		elif data_name == "reviewNumbersDistribution":
			return self.ajax_yelp_review_numbers_distribuion()
		elif data_name == "userCheckin":
			return self.ajax_yelp_user_checkin()
		elif data_name == "businessHeatMap":
			city = request.form["city"]
			return self.ajax_yelp_business_heat_map(city)
		else:
			msg = {"error_message": "data name is undefined"}
			return json.dumps(msg)

	def ajax_yelp_table_information(self):
		yelp_table_list = [
			{"table_name": "yelp_business", "num_of_record": "54,600", "num_of_col": "12"}
			, {"table_name": "yelp_business_attributes", "num_of_record": "12,000", "num_of_col": "50"}
			, {"table_name": "yelp_review", "num_of_record": "3,485,147", "num_of_col": "9"}
			
		]
		return json.dumps(yelp_table_list)

	def ajax_yelp_user_basic_information_by_user_id(self, user_id):
		'''
		# Sample data
		yelp_user_info = [
			{"user_id": "JJ-aSuM4pCFPdkfoZ34q0Q", "name": "Chris", "review_count": 12
			, "num_of_friends": 123, "avg_stars": 2.3
			, "useful_sum": 22, "funny_sum": 1, "cool_sum": 3}
		]
		'''
		sql = '''
		select
			user_id,
			name,
			review_count,
			friends,
			useful,
			funny,
			cool,
			fans,
			average_stars
		from
			yelp_user
		'''
		udf_count_num_of_friends = udf(count_num_of_friends, IntegerType())
		yelpUserInfoDf = self.spark_engine.get_spark().sql(sql)
		yelpUserInfoDf = yelpUserInfoDf.filter(yelpUserInfoDf["user_id"] == user_id) \
			.withColumn("num_of_friends", udf_count_num_of_friends("friends")) 
		
		yelp_user_info = []
		for row in yelpUserInfoDf.collect():
			yelp_user_info.append({
				"user_id": row[0],
				"name": row[1],
				"review_count": row[2],
				"friends": row[3],
				"useful_sum": row[4],
				"funny_sum": row[5],
				"cool_sum": row[6],
				"num_of_fans": row[7],
				"average_stars": row[8],
				"num_of_friends": row[9]
			})
		
		return json.dumps(yelp_user_info)
	
	def ajax_yelp_reviews_by_user_id(self, user_id):
		'''
		# Sample data
		yelp_review_info = [
			{"business_id": "AEx2SYEUJmTxVVB18LlCwA", "stars": 5, "date": "2016-05-28"
			, "reviews": "Super simple place but amazing nonetheless. It's been around since the 30's and they still serve the same thing they started with: a bologna and salami sandwich with mustard. Staff was very helpful and friendly."
			, "useful": 0 , "funny": 0, "cool": 0}
		]
		'''
		
		sql = '''
		select
			business_id,
			stars,
			date,
			text,
			useful,
			funny,
			cool
		from
			yelp_review
		where
			user_id = '%s'
		''' % (user_id)
		yelpReviewInfoDf = self.spark_engine.get_spark().sql(sql)
		yelp_review_info = []
		for row in yelpReviewInfoDf.collect():
			yelp_review_info.append({
				"business_id": row[0],
				"stars": row[1],
				"date": row[2],
				"reviews": row[3],
				"useful": row[4],
				"funny": row[5],
				"cool": row[6]
			})
		return json.dumps(yelp_review_info)
	
	def ajax_yelp_star_rating_distribution(self):
		starRatingDistributionDf = self.spark_engine.get_spark().sql("SELECT stars, count(business_id) FROM yelp_business GROUP BY stars ORDER BY stars")
		star_rating_distribution_list = []
		for row in starRatingDistributionDf.collect():
			star_rating_distribution_list.append({
				"x": row[0],
				"y": row[1]
			})
		return json.dumps(star_rating_distribution_list)
	
	def ajax_yelp_analysis_on_top_users(self):
		topUsersDf = self.spark_engine.get_spark().sql("SELECT review_count, friends, useful, fans FROM yelp_user")
		topUsersDf = topUsersDf.withColumn("useful", topUsersDf["useful"].cast("int"))
		topUsersDf = topUsersDf.orderBy(topUsersDf.useful.desc()).limit(100)
		
		udf_count_num_of_friends = udf(count_num_of_friends, IntegerType())
		topUsersDf = topUsersDf.withColumn("num_of_friends", udf_count_num_of_friends("friends"))
		
		topUsersDf = topUsersDf.withColumn("review_count", topUsersDf["review_count"].cast("int")) \
			.withColumn("fans", topUsersDf["fans"].cast("int")) 
		
		top_user_list = []
		for row in topUsersDf.collect():
			top_user_list.append({
				"review_count": row[0],
				"useful": row[2],
				"fans": row[3],
				"num_of_friends": row[4]
			})
		return json.dumps(top_user_list)
	
	def ajax_yelp_review_numbers_distribuion(self):
		# Only focus on the first 50 review counts
		max_review_count = 50
		reviewDf = self.spark_engine.get_spark().sql("SELECT review_count, count(review_count) count FROM yelp_user GROUP BY review_count")
		reviewDf = reviewDf.withColumn("review_count", reviewDf["review_count"].cast("int"))
		reviewDf = reviewDf.filter(reviewDf["review_count"] <= max_review_count).orderBy(reviewDf["review_count"].asc())
		
		review_list = []
		count_sum = 0
		for row in reviewDf.collect():
			count_sum += row[1]
			review_list.append({
				"review_count": row[0],
				"count": row[1],
				"pdf": 0,
				"cdf": 0
			})
		
		cdf_sum = 0
		for review in review_list:
			pdf = float(review["count"]) / count_sum
			review["pdf"] = round(pdf, 4)
			
			cdf_sum += pdf
			review["cdf"] = round(cdf_sum, 4)
		return json.dumps(review_list)
	
	def ajax_yelp_user_checkin(self):
		checkinDf = self.spark_engine.get_spark().sql("SELECT weekday, hour, checkins FROM yelp_checkin")
		checkinDf = checkinDf.withColumn("checkins", checkinDf["checkins"].cast("int")) \
			.withColumn("hour", split(checkinDf["hour"], ":")[0].cast("int"))
		checkinDf = checkinDf.groupBy("weekday", "hour").agg({'checkins': 'sum'}).orderBy("weekday", "hour")
		
		checkin_data = {}
		for row in checkinDf.collect():
			weekday = row[0]
			hour = row[1]
			checkins = row[2]
			if weekday in checkin_data:
				checkin_data[weekday].append({
					"hour": hour,
					"checkins": checkins
				})
			else:
				checkin_data[weekday] = [{
					"hour": hour,
					"checkins": checkins
				}]
		return json.dumps(checkin_data)
		
	def ajax_yelp_business_heat_map(self, city):
		businessDf = self.spark_engine.get_spark().sql("SELECT city, latitude, longitude, stars, review_count FROM yelp_business")
		businessDf = businessDf.filter(businessDf["city"] == city)
		businessDf = businessDf.withColumn("latitude", businessDf["latitude"].cast("double")) \
			.withColumn("longitude", businessDf["longitude"].cast("double")) \
			.withColumn("stars", businessDf["stars"].cast("int")) \
			.withColumn("review_count", businessDf["review_count"].cast("int"))
		
		businessDf = businessDf.withColumn("popularity", businessDf["stars"] * businessDf["review_count"] * 100)
		sumBusinessDf = businessDf.groupBy("city").agg({'latitude': 'sum', 'longitude': 'sum', '*': 'count'}) \
			.withColumnRenamed("SUM(latitude)", "latitude") \
			.withColumnRenamed("SUM(longitude)", "longitude") \
			.withColumnRenamed("COUNT(1)", "count")
		
		map_center = [0, 0]
		for row in sumBusinessDf.collect():
			map_center[0] = float(row["latitude"]) / row["count"]
			map_center[1] = float(row["longitude"]) / row["count"]
		
		business_list = []
		for row in businessDf.collect():
			business_list.append([
				row["latitude"],
				row["longitude"],
				str(row["popularity"])
			])
		data = {
			"map_center": map_center,
			"business_list": business_list
			#"business_list": []
			}
		return json.dumps(data)
		
	def __init__(self, spark_engine):
		self.spark_engine = spark_engine