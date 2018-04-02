from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession


class SparkEngine:
    def init_spark_component(self):
        self.sc = SparkContext()
        self.sqlContext = SQLContext(self.sc)
        self.spark = SparkSession.builder \
            .config("spark.driver.allowMultipleContexts","true") \
            .master("local") \
            .appName("SQL Query") \
            .getOrCreate()
#            .config("spark.driver.allowMultipleContexts","true") \
    def load_csv_to_table(self):
        file_path = "/Users/tuxinzhang/Desktop/yelp-dataset/yelp_business.csv"
        yelpBusinessDf = self.spark.read \
            .csv(file_path, mode="DROPMALFORMED", header=True)
        yelpBusinessDf.registerTempTable("yelp_business")

        file_path = "/Users/tuxinzhang/Desktop/yelp-dataset/yelp_review_small.csv"
        yelpReviewDf = self.spark.read \
            .csv(file_path, mode="DROPMALFORMED", header=True, multiLine=True)
        yelpReviewDf.registerTempTable("yelp_review")

        file_path = "/Users/tuxinzhang/Desktop/yelp-dataset/yelp_user_small.csv"
        yelpUserDf = self.spark.read.csv(file_path, mode="DROPMALFORMED", header=True, multiLine=True)
        yelpUserDf.registerTempTable("yelp_user")
        #yelpBusinessDf.write.saveAsTable("yelp_user")

        file_path = "/Users/tuxinzhang/Desktop/yelp-dataset/yelp_checkin_small.csv"
        yelpCheckinDf = self.spark.read.csv(file_path, mode="DROPMALFORMED", header=True)
        yelpCheckinDf.registerTempTable("yelp_checkin")

    def get_sc(self):
        return self.sc

    def get_spark(self):
        return self.spark

    def __init__(self):
        self.init_spark_component()
        self.load_csv_to_table()
