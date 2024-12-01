# type: ignore


from pyspark.sql import SparkSession 
from pyspark.sql.functions import col, to_date

# Initialisation de la session Spark
spark = SparkSession.builder \
    .appName("MeteoDataProcessing") \
    .getOrCreate()

# Chargement des fichiers CSV depuis HDFS
df = spark.read.csv("hdfs://data/*.csv", header=True, inferSchema=True)

# Suppression des lignes avec valeurs manquantes
df_cleaned = df.dropna()

# Formatage des dates
df_cleaned = df_cleaned.withColumn("DATE", to_date(col("DATE"), "yyyy-MM-dd"))

# Suppression des doublons
df_cleaned = df_cleaned.dropDuplicates()

# Conversion de la température de Fahrenheit en Celsius
df_cleaned = df_cleaned.withColumn("TEMP_C", (col("TEMP") - 32) * 5 / 9)

# Enregistrement des résultats dans Hive
df_aggregated.write.mode("overwrite").saveAsTable("meteo_aggregated_data")

# Arrêt la session Spark pour libérer les ressources
spark.stop()
