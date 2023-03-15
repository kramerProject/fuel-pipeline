"""
Processing JOB
"""

import sys
import pyspark.sql.functions as f
sys.path.insert(0, './helpers')
from helpers.spark import get_spark_session
sys.path.insert(0, './config')
from config.aws import LANDING_BUCKET, PROCESSING_BUCKET
from pyspark.sql import (
    SparkSession, 
    DataFrame
)
import re

def normalize_column(column_name: str):
  column_normalized = re.sub("[-_]", " ", column_name.strip()) 
  column_normalized = column_normalized.lower()
  return re.sub(" +", "_", column_normalized) 


def read_csv(spark: SparkSession, bucket: str) -> DataFrame:
    """Read CSV files from S3 bucket"""
    df = (
        spark
        .read
        .format("csv")
        .options(header='true', inferSchema='true', delimiter=';')
        .load(f"s3a://{bucket}/combustiveis/*.csv")
        .withColumn("file_name", f.input_file_name())
    )
    return df

def transform(df: DataFrame) -> DataFrame:
    for column in df.columns:
        df = df.withColumnRenamed(column, normalize_column(column))
    df = (
      df
      .withColumn(
        "valor_de_venda", 
        f.regexp_replace("valor_de_venda", ',', '.')
        .cast('double'))
      .withColumn(
        "valor_de_compra", 
        f.regexp_replace("valor_de_compra", ',', '.')
        .cast('double'))
    )
    return df

def write_parquet(bucket: str, df: DataFrame) -> DataFrame:
    """Write PARQUET files to S3 bucket"""
    df_path = f"s3a://{bucket}/combustiveis"
    print(f"Path: {df_path}")
    (
        df
        .write
        .format("parquet")
        .mode("overwrite")
        .save(df_path)
    )
    return True

if __name__ == "__main__":
    """Main ETL script definition."""
    spark = get_spark_session()

    print("Processing data from landing to processing")
    print("Reading Dataframe!")
    df = read_csv(spark, LANDING_BUCKET)
    print("Done!")
    print(f"Total lines:{df.count()}")
    print(f"Dataframe original schema: {df.printSchema()}")
    df = transform(df)
    print(f"Schema after processing: {df.printSchema()}")
    print("Writing Dataframe!")
    write_parquet(PROCESSING_BUCKET, df)
    print("Done!")
    spark.stop()
    
    