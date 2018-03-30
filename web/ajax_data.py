from flask import request
import json


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
		yelp_user_info = [
			{"user_id": "JJ-aSuM4pCFPdkfoZ34q0Q", "name": "Chris", "review_count": 12
			, "num_of_friends": 123, "avg_stars": 2.3
			, "useful_sum": 22, "funny_sum": 1, "cool_sum": 3}
		]
		return json.dumps(yelp_user_info)
	
	def ajax_yelp_reviews_by_user_id(self, user_id):
		yelp_review_info = [
			{"business_id": "AEx2SYEUJmTxVVB18LlCwA", "stars": 5, "date": "2016-05-28"
			, "reviews": "Super simple place but amazing nonetheless. It's been around since the 30's and they still serve the same thing they started with: a bologna and salami sandwich with mustard. Staff was very helpful and friendly."
			, "useful": 0 , "funny": 0, "cool": 0}
		]
		return json.dumps(yelp_review_info)
		
	def __init__(self, spark_engine):
		self.spark_engine = spark_engine