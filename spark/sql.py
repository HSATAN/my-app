# _*_ coding:utf-8 _*_
from pyspark.sql import SparkSession

# spark = SparkSession.builder.appName("sql").config("spark_sql","value").getOrCreate()
# df = spark.read.json("/input/age.json")
# df.printSchema()
from pyspark.sql import Row
sc = spark.sparkContext
line = sc.textFile("/input/person.txt")
parts = line.map(lambda l:l.split(","))
people = parts.map(lambda p:Row(name=p[0],age=p[1]))
datapeople = spark.createDataFrame(people)
datapeople.createOrReplaceTempView("people")
teenagers = spark.sql("select * from people")
teen_name = teenagers.rdd.map(lambda p: "name : "+p.name).collect()
for name in teen_name:
    print(name)

