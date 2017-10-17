# _*_ coding:utf-8 _*_
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("sql").config("spark_sql","value").getOrCreate()
df = spark.read.json("/input/age.json")
df.printSchema()
