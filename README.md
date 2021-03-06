Stock-Data-Price-Prediction

Project : Stock Price Prediction using real time data

    1. Use Spark to fetch the stocks data in real time.
    2. Move data to a centralised data store in the cloud for further analysis in the data pipeline.
    3. Preprocess the data (Python + Spark).
    4. Store the cleaned data on HDFS
    5. Carry out the prediction using Mllib
    6. Visualization using flask

Use Spark to fetch the stocks data

VERSIONS: Hadoop 3.3.1, Spark 3.1.2, Python 3.9.5

Step1 : Create a spark session and import the required libraries

Step2 : Fetch the stock data using API key and store it into variable called CSV_URL

Step3 : The API data is stored into a csv file and store it to hadoop server (HDFS)

Step4 : Now stock data is on hdfs we have to fetch the data and create a spark dataframe from it to clean and process the data


Clean , Preprocess and build ML model

Step5 : Preprocessing the data to clean it 1.Create a python notebook and load create a spark session 
from pyspark.sql import SparkSession 
spark= SparkSession.builder.appName('Stock Data Prediction').getOrCreate()

Step6 : Load the data we fetched in spark dataframe 
df=spark.read.csv("hdfs://localhost:9000/Spark/StockDataPrediction/StockData.csv",inferSchema=True,header=True)

Step7 : Clean the data Removing the quotes
new_df=df.withColumnRenamed('["time"','time')
.withColumnRenamed(' "open"','open')
.withColumnRenamed(' "high"','high')
.withColumnRenamed(' "low"','low')
.withColumnRenamed(' "close"','close')
.withColumnRenamed(' "volume"]','volume')
Also, removing the unnecessary quotes and brackets 
df2 = new_df.withColumn('open', regexp_replace('open', '"', ''))
.withColumn('time', regexp_replace('time', '[', ''))
.withColumn('time', regexp_replace('time', '"', ''))
.withColumn('high', regexp_replace('high', '"', ''))
.withColumn('low', regexp_replace('low', '"', ''))
.withColumn('close', regexp_replace('close', '"', ''))
.withColumn('volume', regexp_replace('volume', ']', ''))
.withColumn('volume', regexp_replace('volume', '"', ''))

Step8: Show the cleaned data

Step9: Create vectors from features using vector assembler.
featureassembler=VectorAssembler(inputCols=["open","high","low"],outputCol="Features")

Step10: Transform the data and sort in ascending order
output=featureassembler.transform(df2) 
finalized_data=output.select("time","Features","close").sort("time",ascending=True)

Step11: Splitting the data into train and test data.
final_data=finalized_data.withColumn("rank",percent_rank().over(Window.partitionBy().orderBy("time"))) 
train_df=final_data.where("rank<=.8").drop("rank") 
test_df=final_data.where("rank>.8").drop("rank")

Step12: Write test data to parquet file for further use 
test_df.write.parquet('testdata')

Step13: Create model with linear regression algorithm regressor=LinearRegression(featuresCol='Features', labelCol='close') lr_model=regressor.fit(train_df) 
print(???Coefficients:??? +str(lr_model.coefficients)) 
print(???Coefficients:??? +str(lr_model.intercept))

Step14: Making predictions by transforming data into model 
predDF= lr_model.transform(test_df) predDF.select("Features","close","prediction").show(5)

Step5: Evaluating the model RMSE: It is the square root of the mean of the square of all the errors ie. it is the standard deviation of the residuals(predicted errors). 
from pyspark.ml.evaluation import RegressionEvaluator 
regressionEvaluator = RegressionEvaluator( predictionCol="prediction", labelCol="close", metricName="rmse") 
rmse = regressionEvaluator.evaluate(predDF) 
print(f"Root Mean Square Error (RMSE) is {rmse:.1f}")

Step15: Save model 
lr_model.save(???stock_data_model???)
