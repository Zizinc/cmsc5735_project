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
		#file_path = "/home/ubuntu/Downloads/spark-2.1.0-bin-hadoop2.7/cmsc5735_project/data/yelp_business_small_1000.csv"
		file_path = "/data/yelp_business_small_1000.csv"
		yelpBusinessDf = self.spark.read.csv(file_path, header=True, mode="DROPMALFORMED")
		#self.spark.sql("DROP TABLE IF EXISTS yelp_business")
		yelpBusinessDf.registerTempTable("yelp_business")
		#yelpBusinessDf.write.saveAsTable("yelp_business")
		
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
