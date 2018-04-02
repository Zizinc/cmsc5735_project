from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession

class SparkEngine:
	
	def init_spark_component(self):
		self.sc = SparkContext()
		self.sqlContext = SQLContext(self.sc)
		self.spark = SparkSession.builder \
			.master("local") \
			.appName("SQL Query") \
			.config("spark.some.config.option", "some-value") \
			.getOrCreate()

	def load_csv_to_table(self):
		file_path = "data/yelp_business.csv"
		yelpBusinessDf = self.spark.read.csv(file_path, mode="DROPMALFORMED", header=True)
		yelpBusinessDf.registerTempTable("yelp_business")
		
		file_path = "data/yelp_review_small_1000.csv"
		yelpReviewDf = self.spark.read.csv(file_path, mode="DROPMALFORMED", header=True, multiLine=True)
		yelpReviewDf.registerTempTable("yelp_review")
		
		file_path = "data/yelp_user_small_1000.csv"
		yelpUserDf = self.spark.read.csv(file_path, mode="DROPMALFORMED", header=True, multiLine=True)
		yelpUserDf.registerTempTable("yelp_user")
		
		file_path = "data/yelp_checkin_small_1000.csv"
		yelpCheckinDf = self.spark.read.csv(file_path, mode="DROPMALFORMED", header=True)
		yelpCheckinDf.registerTempTable("yelp_checkin")
		
		# Test
		#distinctBusinessCityDf = self.spark.sql("SELECT distinct city FROM yelp_business ORDER BY city")
		#distinctBusinessCityDf.show(10)
	
	def get_sc(self):
		return self.sc
		
	def get_spark(self):
		return self.spark
	
	def __init__(self):
		self.init_spark_component()
		self.load_csv_to_table()
