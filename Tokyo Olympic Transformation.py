# Databricks notebook source
from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType,DoubleType,BooleanType,DateType

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
"fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
"fs.azure.account.oauth2.client.id": "",
"fs.azure.account.oauth2.client.secret": '',
"fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/tenantid/oauth2/token"}



dbutils.fs.mount(
source = "abfss://tokyo-olympic-data@tokyoolympicdatavicky.dfs.core.windows.net", # contrainername@storageaccname
mount_point = "/mnt/tokyoolymic",
extra_configs = configs)

# COMMAND ----------

# MAGIC %fs
# MAGIC ls "/mnt/tokyoolymic"

# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------

athletes = spark.read.format("csv").option("header","true").option("InfersSchema","true").load("/mnt/tokyoolymic/raw-data/athletes.csv")
coaches = spark.read.format("csv").option("header","true").option("InfersSchema","true").load("/mnt/tokyoolymic/raw-data/coaches.csv")
entriesgender = spark.read.format("csv").option("header","true").option("InfersSchema","true").load("/mnt/tokyoolymic/raw-data/entriesgender.csv")
medals = spark.read.format("csv").option("header","true").option("InfersSchema","true").load("/mnt/tokyoolymic/raw-data/medals.csv")
teams = spark.read.format("csv").option("header","true").option("InfersSchema","true").load("/mnt/tokyoolymic/raw-data/teams.csv")


# COMMAND ----------

athletes.printSchema()
coaches.printSchema()
entriesgender.printSchema()
medals.printSchema()
teams.printSchema()

# COMMAND ----------

entriesgender = entriesgender.withColumn("female",col("female").cast(IntegerType()))\
    .withColumn("male",col("male").cast(IntegerType()))\
    .withColumn("Total",col("Total").cast(IntegerType()))    

# COMMAND ----------

athletes.printSchema()
coaches.printSchema()
entriesgender.printSchema()
medals.printSchema()
teams.printSchema()

# COMMAND ----------

# Find the top countries with the highest number of gold medals
top_gold_medal_countries = medals.orderBy("Gold", ascending=False).select("Team_Country","Gold").show()

# COMMAND ----------

# Calculate the average number of entries by gender for each discipline
average_entries_by_gender = entriesgender.withColumn(
    'Avg_Female', entriesgender['Female'] / entriesgender['Total']
).withColumn(
    'Avg_Male', entriesgender['Male'] / entriesgender['Total']
)
average_entries_by_gender.show()
     

# COMMAND ----------

athletes.write.mode("overwrite").option("header","true").csv("/mnt/tokyoolymic/transformed-data/athletes")

# COMMAND ----------

coaches.repartition(1).write.mode("overwrite").option("header","true").csv("/mnt/tokyoolymic/transformed-data/coaches")
entriesgender.repartition(1).write.mode("overwrite").option("header","true").csv("/mnt/tokyoolymic/transformed-data/entriesgender")
medals.repartition(1).write.mode("overwrite").option("header","true").csv("/mnt/tokyoolymic/transformed-data/medals")
teams.repartition(1).write.mode("overwrite").option("header","true").csv("/mnt/tokyoolymic/transformed-data/teams")

# COMMAND ----------


