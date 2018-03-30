import json

class AjaxDataHandler:

	def handle_ajax_data(self, data_name):
		if data_name == "yelpTableInformation":
			return self.ajax_yelp_table_information()
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

	def __init__(self, spark_engine):
		self.spark_engine = spark_engine